import pandas as pd
import sqlite3 as sql

def cleanLAR(year, dataFolder='./rawData/LAR'):
    """Funnels txt file into Pandas DataFrame.

    Imports HMDA pipe-delimited LAR data. Uses 'Exempt' as null value for float coloumns. 
    Sets datatype of age and state code columns to string.

    Txt file name must be in "2022.txt" format based on year.

    Args:
        year:       Year of data as int.
        dataFolder: Filepath to folder with txt files as string.

    Returns:
        Pandas DataFrame
    """
    fp = f'{dataFolder}/{year}.txt'

    # Create dictionary of columns where 'Exempt' is a null value
    exempts = [
        'combined_loan_to_value_ratio', 'interest_rate', 'rate_spread', 
        'total_loan_costs', 'total_points_and_fees', 'origination_charges',
        'discount_points', 'lender_credits', 'loan_term',
        'prepayment_penalty_term', 'intro_rate_period', 'property_value',
        'total_units', 'multifamily_affordable_units', 'debt_to_income_ratio'
        ]
    exemptNulls = dict(zip(exempts, ['Exempt']*len(exempts)))

    return pd.read_csv(fp, delimiter='|',  
                 na_values = exemptNulls,
                 dtype={
                    'state_code':'str', 
                    'applicant_age':'str', 
                    'co_applicant_age':'str'
                }
        )

def cleanLEI(year, df, dataFolder='./rawData/TS'):
    """Funnels txt file into Pandas DataFrame and concatenates with existing DataFrame.

    Imports HMDA pipe-delimited TS data. Creates column concatenating respondent_name and 
    respondent_state. 

    Txt file name must be in "2022.txt" format based on year.

    Args:
        year:       Year of data as int.
        df:         DataFrame for concatenation as Pandas DataFrame.
        dataFolder: Filepath to folder with txt files as string.

    Returns:
        Pandas DataFrame
    """
    fp = f'{dataFolder}/{year}.txt'

    temp = pd.read_csv(fp, delimiter='|')
    temp['name_state'] = [f'{x} ({y})' for x, y in 
                          zip(temp.respondent_name, temp.respondent_state)]
    
    return pd.concat(
            [df, temp],
            ignore_index=True
        )

def cleanLL(year, df, dataFolder='./rawData/LL'):
    """Funnels Excel file into Pandas DataFrame and concatenates with existing DataFrame.

    Imports FHFA loan limit data from Excel spreadsheets into Pandas DataFrame, renames 
    columns, and concatenates to existing DataFrame.

    Excel file name must be in "2022.xlsx" format based on year.

    Args:
        year:       Year of data as int.
        df:         DataFrame for concatenation as Pandas DataFrame.
        dataFolder: Filepath to folder with txt files as string.

    Returns:
        Pandas DataFrame
    """
    fp = f'{dataFolder}/{year}.xlsx'
    
    cols = ['state_code', 'county_code', 'county_name', 'state', 'cbsa', 'one_unit_limit',
        'two_unit_limit', 'three_unit_limit', 'four_unit_limit']

    temp = pd.read_excel(fp, skiprows=1, sheet_name='GSE Limits', names=cols)
    temp['year'] = year

    return pd.concat(
            [df, temp], 
            ignore_index=True
        )

### Create LAR SQLite table
# LAR needs to be one year at a time due to file size

lar = cleanLAR(2018)
with sql.connect('./HMDA_Full/HMDA.sqlite') as conn:
    lar.to_sql('LAR', conn, index=False)
    print('LAR - 2018\n')
    del lar 

for year in list(range(2019, 2023)):
    print('LAR -', year, '\n')
    del lar
    lar = cleanLAR(year)
    with sql.connect('./HMDA_Full/HMDA.sqlite') as conn:
        lar.to_sql('LAR', conn, index=False, if_exists='append')

del lar 

print('------   FINISHED LAR   ------\n')

### Create Entities & LoanLimits SQLite tables

for year in list(range(2018, 2023)):
    lei = cleanLEI(year, lei)
    ll = cleanLL(year, ll)
    print('Finished importing TS and LL files.\n')

with sql.connect('./HMDA_Full/HMDA.sqlite') as conn:
    lei.to_sql('Entities', conn, index=False)
    print('------   FINISHED Entities   ------\n')
    ll.to_sql('LoanLimits', conn, index=False)
    print('------   FINISHED LoanLimits   ------\n')
