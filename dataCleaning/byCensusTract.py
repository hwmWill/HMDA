import pandas as pd

byCensus = pd.read_csv('../queryResults/byCensusTract_2022.csv', 
                       dtype={'jumbo':'bool'})
byCensus['census_tract'] = [f'{x:0>11}' for x in byCensus.census_tract]

grouped = byCensus[['state', 'jumbo', 'loans', 'amount_loaned']].groupby(['state', 'jumbo']).sum()
states = byCensus.state.unique()
state_pc_jumbo = pd.DataFrame()
for state in states:
    try:
        state_pc_jumbo = \
            pd.concat(
                [state_pc_jumbo,
                 pd.DataFrame(dict(zip(
                    ['state', 'Perc_Loans_Jumbo'],
                    [state,
                    grouped.loc[(state, True), ['loans', 'amount_loaned']].div(
                    (grouped.loc[(state, False), ['loans', 'amount_loaned']] + grouped.loc[(state, True), ['loans', 'amount_loaned']]))]
                    ))
                )])
    except KeyError:
        pass

state_pc_jumbo = state_pc_jumbo.reset_index()\
                             .rename(columns={'index':'Category'})\
                             .pivot(index='state', columns='Category', values='Perc_Loans_Jumbo')\
                             .reset_index()\
                             .rename(columns={'loans':'perc_loans_jumbo', 
                                              'amount_loaned':'perc_loan_sum_jumbo'})

byCensus[['state', 'jumbo', 'loans', 'amount_loaned']].query('jumbo == True').merge(state_pc_jumbo, on='state').drop(columns='jumbo')\
    .to_excel('../cleanedData/JumboByState2022.xlsx', index=False) 