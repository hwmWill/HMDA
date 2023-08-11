import sqlite3 as sql
import pandas as pd

class hmdaLender:
    def __init__(self, lei, years, dbPath):
        self.lei            = lei
        self.years          = years
        self.dbPath         = dbPath
        self.baseConditions = '''
-- 		Single-family
		AND derived_dwelling_category IN ("Single Family (1-4 Units):Site-Built", "Single Family (1-4 Units):Manufactured")
-- 		Not purchased loans
		AND action_taken != 6
-- 		Not reverse mortgage
		AND reverse_mortgage != 1 
'''
    
    def getMsaAppCount(self, year, msa):
        return f'''
SELECT 	COUNT(*) AS applications
FROM 	LAR 
WHERE 	activity_year = {year}
		AND derived_msa_md = "{msa}"
		AND lei = "{self.lei}" {self.baseConditions}
'''
    
    def getHalfDouble(self, year, msa):
        return f'''
SELECT  applications, applications * 0.5 AS half, applications * 2 AS double 
FROM 
({self.getMsaAppCount(year, msa)})
'''
    
    def runAppCount(self, year, msa):
        with sql.connect(self.dbPath) as conn:
            appCount = pd.read_sql_query(self.getHalfDouble(year, msa), conn)
        return appCount
    
    def getPeers(self, year, msa, appCount):
        half = appCount.half.item()
        double = appCount.double.item()
        return f'''
SELECT  DISTINCT(lei) AS lei
FROM 
(
SELECT 	lei, COUNT(*) AS applications
FROM 	LAR 
WHERE 	activity_year = {year}
		AND derived_msa_md = "{msa}"
-- 		Not self.lei
		AND lei != "{self.lei}" {self.baseConditions}
GROUP BY lei 
)
WHERE   applications BETWEEN {half} AND {double}
'''
    
    def runPeers(self, year, msa, appCount):
        with sql.connect(self.dbPath) as conn:
            peers = pd.read_sql_query(self.getPeers(year, msa, appCount), conn)
        return peers
    
    def getLeiAndPeers(self, year, msa, peers):
        peerList = peers.lei.to_list()
        peerList.append(self.lei)
        peerList = [f'"{x}"' for x in peerList]
        return f'''
SELECT  activity_year, lei,
--      location info
        derived_msa_md, PRINTF('%011d', census_tract) AS census_tract,
-- 		loan info
		derived_loan_product_type, conforming_loan_limit, action_taken, loan_purpose,
		open_end_line_of_credit, business_or_commercial_purpose,
		loan_amount, interest_rate, combined_loan_to_value_ratio, rate_spread, hoepa_status, 
        total_loan_costs, origination_charges, discount_points, lender_credits, loan_term,
		intro_rate_period, negative_amortization, interest_only_payment, balloon_payment,
		other_nonamortizing_features, initially_payable_to_institution,
-- 		site info
		property_value, construction_method, occupancy_type,
		manufactured_home_land_property_interest, manufactured_home_secured_property_type,
		total_units, 
-- 		applicant info
		derived_ethnicity, derived_race, derived_sex, applicant_age, income, debt_to_income_ratio,
		applicant_age_above_62,
		applicant_race_1, applicant_race_2, applicant_race_3, applicant_race_4, applicant_race_5,
		co_applicant_race_1, co_applicant_race_2, co_applicant_race_3, co_applicant_race_4, co_applicant_race_5,
		applicant_ethnicity_1, applicant_ethnicity_2, applicant_ethnicity_3, applicant_ethnicity_4, applicant_ethnicity_5,
		co_applicant_ethnicity_1, co_applicant_ethnicity_2, co_applicant_ethnicity_3, co_applicant_ethnicity_4, co_applicant_ethnicity_5,
-- 		denial info
		denial_reason_1, denial_reason_2, denial_reason_3, denial_reason_4,
-- 		tract info
		tract_population, tract_minority_population_percent, ffiec_msa_md_median_family_income,
		tract_to_msa_income_percentage, tract_owner_occupied_units, tract_one_to_four_family_homes,
		tract_median_age_of_housing_units
FROM    LAR
WHERE   activity_year = {year}
        AND derived_msa_md = "{msa}"
--      lei and peers
		AND lei IN ({",".join(peerList)}) {self.baseConditions}
'''
    
    def runLeiAndPeers(self, year, msa, peers):
        with sql.connect(self.dbPath) as conn:
            larByYear = pd.read_sql_query(self.getLeiAndPeers(year, msa, peers), conn)
        return larByYear

    def runAllYears(self, msa):
        dfs = []
        for year in self.years:
            print(f'Getting app count for {year}...')
            appCount = self.runAppCount(year, msa)
            print('apps:', appCount.applications.item())
            print(f'Getting peers for {year}...')
            peers = self.runPeers(year, msa, appCount)
            print(f'peers:', len(peers))
            print(f'Getting LAR data for {year}...')
            larByYear = self.runLeiAndPeers(year, msa, peers)
            dfs.append(larByYear)
        if len(dfs) > 1:
            final = dfs[0]
            for df in dfs[1:]:
                final = pd.concat([final, df], ignore_index=True)
            return final
        else:
            return dfs[0]
        
hsbc = hmdaLender(lei    = '1IE8VN30JCEQV1H4R804', 
                  years  = [2018, 2019, 2020, 2021], 
                  dbPath = '../HMDA_full/HMDA.sqlite')
df = hsbc.runAllYears('11244')

df.to_csv('./byAssessmentArea/OrangeCounty.csv', index=False)