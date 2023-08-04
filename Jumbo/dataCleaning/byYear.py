import pandas as pd

byYear = pd.read_csv('../queryResults/byYear.csv', 
                       dtype={'jumbo':'bool'})

grouped = byYear.groupby(['year', 'jumbo']).sum()

year_pc_jumbo = pd.DataFrame()
for year in byYear.year.unique():
    year_pc_jumbo = \
        pd.concat(
            [year_pc_jumbo,
                pd.DataFrame(dict(zip(
                ['year', 'Perc_Loans_Jumbo'],
                [year,
                grouped.loc[(year, True), ['loans', 'amount_loaned', 'lenders']].div(
                (grouped.loc[(year, False), ['loans', 'amount_loaned', 'lenders']] + grouped.loc[(year, True), ['loans', 'amount_loaned', 'lenders']]))]
                ))
            )])


year_pc_jumbo = year_pc_jumbo.reset_index()\
                             .rename(columns={'index':'Category'})\
                             .pivot(index='year', columns='Category', values='Perc_Loans_Jumbo')\
                             .reset_index()\
                             .rename(columns={'loans':'perc_loans_jumbo', 
                                              'amount_loaned':'perc_loan_sum_jumbo',
                                              'lenders':'perc_lenders_jumbo'})

byYear.query('jumbo == True').merge(year_pc_jumbo, on='year').drop(columns='jumbo')\
    .to_excel('../cleanedData/JumboByYear.xlsx', index=False)                                              