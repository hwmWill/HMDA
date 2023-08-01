import pandas as pd

byLender = pd.read_csv('../queryResults/byLEI_2022.csv', 
                       dtype={'jumbo':'bool'})

grouped = byLender[['lei', 'jumbo', 'loans', 'amount_loaned']].groupby(['lei', 'jumbo']).sum()
lenders = byLender.lei.unique()
lender_pc_jumbo = pd.DataFrame()
for lender in lenders:
    try:
        lender_pc_jumbo = \
            pd.concat(
                [lender_pc_jumbo,
                 pd.DataFrame(dict(zip(
                             ['lei', 'Perc_Loans_Jumbo'],
                             [lender,
                              grouped.loc[(lender, True), ['loans', 'amount_loaned']].div(
                                (grouped.loc[(lender, False), ['loans', 'amount_loaned']] + grouped.loc[(lender, True), ['loans', 'amount_loaned']]))]
                            ))
                     )])
    except KeyError:
        pass

lender_pc_jumbo = lender_pc_jumbo.reset_index()\
                             .rename(columns={'index':'Category'})\
                             .pivot(index='lei', columns='Category', values='Perc_Loans_Jumbo')\
                             .reset_index()\
                             .rename(columns={'loans':'perc_loans_jumbo', 
                                              'amount_loaned':'perc_loan_sum_jumbo'})

byLender[['lei','respondent_name','jumbo','loans','amount_loaned']].query('jumbo == True').merge(lender_pc_jumbo, on='lei').drop(columns='jumbo')\
    .to_excel('../cleanedData/JumboByLender2022.xlsx', index=False)                                              