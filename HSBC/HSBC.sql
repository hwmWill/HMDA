SELECT 	activity_year, 
-- 		location
		derived_msa_md, PRINTF('%011d', census_tract) AS census_tract,
-- 		loan info
		derived_loan_product_type, conforming_loan_limit, action_taken, preapproval, loan_purpose,
		lien_status, reverse_mortgage, open_end_line_of_credit, business_or_commercial_purpose,
		loan_amount, interest_rate, rate_spread, hoepa_status, total_loan_costs, total_points_and_fees,
		origination_charges, discount_points, lender_credits, loan_term, prepayment_penalty_term,
		intro_rate_period, negative_amortization, interest_only_payment, balloon_payment,
		other_nonamortizing_features, initially_payable_to_institution,
-- 		site info
		derived_dwelling_category, property_value, construction_method, occupancy_type,
		manufactured_home_land_property_interest, manufactured_home_secured_property_type,
		total_units, multifamily_affordable_units,
-- 		applicant info
		derived_ethnicity, derived_race, derived_sex, applicant_age, income, debt_to_income_ratio,
		applicant_age_above_62,
-- 		denial info
		denial_reason_1, denial_reason_2, denial_reason_3, denial_reason_4,
-- 		tract info
		tract_population, tract_minority_population_percent, ffiec_msa_md_median_family_income,
		tract_to_msa_income_percentage, tract_owner_occupied_units, tract_one_to_four_family_homes,
		tract_median_age_of_housing_units
FROM LAR 
WHERE	lei = '1IE8VN30JCEQV1H4R804'
		AND activity_year IN (2018, 2019, 2020, 2021)