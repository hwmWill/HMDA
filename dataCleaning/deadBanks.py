import pandas as pd

deadBanks = pd.read_csv('../queryResults/firstRepbulic_siliconValley.csv', 
                       dtype={'jumbo':'bool'})
deadBanks['county_st_code'] = [f'{x:0>5}' for x in deadBanks.county_st_code]
deadBanks['census_tract'] = ['{x:0>11}' for x in deadBanks.census_tract]

svb = deadBanks.loc[deadBanks.respondent_name=='Silicon Valley Bank']\
    .groupby(['respondent_name', 'jumbo', 'year']).agg(
        {'loan_amount':'sum', 'income':'median', 'property_value':'median', 
         'interest_rate':'median', 'rate_spread':'median', 'county_st_code':pd.Series.mode})\
    .reset_index()

svb = svb.merge(
    deadBanks.loc[deadBanks.respondent_name=='Silicon Valley Bank', ['respondent_name', 'jumbo', 'year', 'loan_amount']]\
        .groupby(['respondent_name', 'jumbo', 'year']).count().reset_index().rename(columns={'loan_amount':'loan_count'}),
    on=['respondent_name', 'jumbo', 'year'])

svb_jumbo = svb.loc[svb.jumbo==1].drop(columns='jumbo').rename(columns=
    {'loan_amount':'Jumbo_Total', 
     'loan_count':'Jumbo_Count',
     'income':'jumbo_Median_Income',
     'property_value':'Jumbo_Median_Property_Value',
     'interest_rate':'jumbo_Median_Interest_Rate',
     'rate_spread':'Jumbo_Median_Rate_Spread',
     'county_st_code':'Jumbo_Mode_County'})
svb_nonjumbo = svb.loc[svb.jumbo==0].drop(columns='jumbo').rename(columns=
    {'loan_amount':'Conforming_Total', 
     'loan_count':'Conforming_Count',
     'income':'Conforming_Median_Income',
     'property_value':'Conforming_Median_Property_Value',
     'interest_rate':'Conforming_Median_Interest_Rate',
     'rate_spread':'Conforming_Median_Rate_Spread',
     'county_st_code':'Conforming_Mode_County'})

svb = svb_jumbo.merge(svb_nonjumbo, on=['respondent_name', 'year'])

fr = deadBanks.loc[deadBanks.respondent_name!='Silicon Valley Bank']\
    .groupby(['respondent_name', 'jumbo', 'year']).agg(
        {'loan_amount':'sum', 'income':'median', 'property_value':'median', 
         'interest_rate':'median', 'rate_spread':'median', 'county_st_code':pd.Series.mode})\
    .reset_index()

fr = fr.merge(
    deadBanks.loc[deadBanks.respondent_name!='Silicon Valley Bank', ['respondent_name', 'jumbo', 'year', 'loan_amount']]\
        .groupby(['respondent_name', 'jumbo', 'year']).count().reset_index().rename(columns={'loan_amount':'loan_count'}),
    on=['respondent_name', 'jumbo', 'year'])

fr_jumbo = fr.loc[fr.jumbo==1].drop(columns='jumbo').rename(columns=
    {'loan_amount':'Jumbo_Total', 
     'loan_count':'Jumbo_Count',
     'income':'Jumbo_Median_Income',
     'property_value':'Jumbo_Median_Property_Value',
     'interest_rate':'Jumbo_Median_Interest_Rate',
     'rate_spread':'Jumbo_Median_Rate_Spread',
     'county_st_code':'Jumbo_Mode_County'})
fr_nonjumbo = fr.loc[fr.jumbo==0].drop(columns='jumbo').rename(columns=
    {'loan_amount':'Conforming_Total', 
     'loan_count':'Conforming_Count',
     'income':'Conforming_Median_Income',
     'property_value':'Conforming_Median_Property_Value',
     'interest_rate':'Conforming_Median_Interest_Rate',
     'rate_spread':'Conforming_Median_Rate_Spread',
     'county_st_code':'Conforming_Mode_County'})

fr = fr_jumbo.merge(fr_nonjumbo, on=['respondent_name', 'year'])

final = pd.concat([svb, fr], ignore_index=True)
final['respondent_name'] = final.respondent_name.str.title()
final['Total_Loans'] = final.Jumbo_Count + final.Conforming_Count
final['Total_Loaned'] = final.Jumbo_Total + final.Conforming_Total
final['Perc_Loans_Jumbo'] = final.Jumbo_Count / final.Total_Loans
final['Perc_Loan_Sum_Jumbo'] = final.Jumbo_Total / final.Total_Loaned
final.rename(columns={'respondent_name':'Lender', 'year':'Year'}, inplace=True)

final[['Lender', 'Year', 'Jumbo_Count', 'Total_Loans', 'Perc_Loans_Jumbo', 'Jumbo_Total', 'Total_Loaned', 'Perc_Loan_Sum_Jumbo',
       'Jumbo_Median_Income', 'Conforming_Median_Income', 'Jumbo_Median_Property_Value', 'Conforming_Median_Property_Value', 
       'Jumbo_Median_Interest_Rate', 'Conforming_Median_Interest_Rate', 'Jumbo_Median_Interest_Rate', 'Conforming_Median_Interest_Rate']]\
       .to_excel('../cleanedData/DeadBanks.xlsx', index=False)