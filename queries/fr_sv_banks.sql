SELECT respondent_name, fromLAR.activity_year AS year, loan_amount, income, property_value, combined_loan_to_value_ratio, interest_rate, rate_spread, fromLAR.county_st_code, fromLAR.census_tract, state, 
-- 		when there is no census_tract
		CASE WHEN one_unit_limit IS NULL THEN 
-- 				2018 mode by unit
				CASE WHEN fromLAR.activity_year = 2018 THEN 
					 CASE WHEN total_units = 1 THEN loan_amount > 453100
						  WHEN total_units = 2 THEN loan_amount > 580150
						  WHEN total_units = 3 THEN loan_amount > 701250
					      ELSE loan_amount > 871450 
					  END
-- 				2019 mode by unit
					WHEN fromLAR.activity_year = 2019 THEN 
					CASE WHEN total_units = 1 THEN loan_amount > 484350
						 WHEN total_units = 2 THEN loan_amount > 620200
						 WHEN total_units = 3 THEN loan_amount > 749650
						 ELSE loan_amount > 931600
					  END
-- 				2020 mode by unit
					WHEN fromLAR.activity_year = 2020 THEN 
					CASE WHEN total_units = 1 THEN loan_amount > 510400
						 WHEN total_units = 2 THEN loan_amount > 653550
						 WHEN total_units = 3 THEN loan_amount > 789950
						 ELSE loan_amount > 981700
					 END 
-- 				2021 mode by unit
					WHEN fromLAR.activity_year = 2021 THEN 
					CASE WHEN total_units = 1 THEN loan_amount > 548250
						 WHEN total_units = 2 THEN loan_amount > 702000
						 WHEN total_units = 3 THEN loan_amount > 848500
						 ELSE loan_amount > 1054500
					 END 
-- 				2022 mode by unit
				ELSE  
					CASE WHEN total_units = 1 THEN loan_amount > 647200
						 WHEN total_units = 2 THEN loan_amount > 828700
						 WHEN total_units = 3 THEN loan_amount > 1001650
						 ELSE loan_amount > 1244850
					 END 
				END 	
-- 			 when census_tract not null	 
			 ELSE 
				 CASE WHEN total_units = 1 THEN loan_amount > one_unit_limit
					  WHEN total_units = 2 THEN loan_amount > two_unit_limit
					  WHEN total_units = 3 THEN loan_amount > three_unit_limit
					  ELSE loan_amount > four_unit_limit 
				  END 
			 END AS jumbo

FROM 
(SELECT SUBSTR(PRINTF('%011d', census_tract),1,5) AS county_st_code, PRINTF('%011d', census_tract) AS census_tract, total_units, loan_amount, lei,
	income, property_value, combined_loan_to_value_ratio, interest_rate, rate_spread, activity_year
FROM LAR
WHERE action_taken = 1 AND 
	derived_dwelling_category IN ('Single Family (1-4 Units):Site-Built', 'Single Family (1-4 Units):Manufactured') AND
	derived_loan_product_type IS 'Conventional:First Lien' AND 
	reverse_mortgage != 1 AND 
	open_end_line_of_credit != 1 AND 
	business_or_commercial_purpose != 1 AND 
	loan_purpose IN (1, 31, 32) AND
-- 	Silicon Valley Bank, First Republic Bank
	lei IN ('0K2D5AK28E3O5CC06E35', 'YWC0TIKBQM2JV8L4IV08')) AS fromLAR
	
-- loan limits by county, unit count, and year
LEFT JOIN (SELECT PRINTF('%02d', state_code)||PRINTF('%03d', county_code) AS county_st_code, state, year, one_unit_limit, two_unit_limit, three_unit_limit, four_unit_limit
	FROM LoanLimits
	WHERE year = 2022) AS fromLL
	ON fromLAR.county_st_code = fromLL.county_st_code
	
-- entity names by lei and year
LEFT JOIN (SELECT lei, respondent_name, activity_year 
	FROM Entities) AS fromEntities
	ON fromLAR.lei = fromEntities.lei AND fromLAR.activity_year = fromEntities.activity_year
