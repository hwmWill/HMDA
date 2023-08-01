SELECT census_tract, state, jumbo, SUM(loan_amount) AS amount_loaned, COUNT(*) AS loans
FROM 
(
SELECT census_tract, state, loan_amount, 
-- 		when there is no census_tract
		CASE WHEN one_unit_limit IS NULL THEN
				CASE WHEN total_units = 1 THEN loan_amount > 647200
					 WHEN total_units = 2 THEN loan_amount > 828700
					 WHEN total_units = 3 THEN loan_amount > 1001650
					 ELSE loan_amount > 1244850
				 END 
-- 		when census_tract not null	 
			 ELSE 
				 CASE WHEN total_units = 1 THEN loan_amount > one_unit_limit
					  WHEN total_units = 2 THEN loan_amount > two_unit_limit
					  WHEN total_units = 3 THEN loan_amount > three_unit_limit
					  ELSE loan_amount > four_unit_limit 
				  END 
			 END AS jumbo

-- single-family, noncommercial, conventional, non-open-line-of-credit, non-reverse-mortgage, first-lien home purchase and refinance mortgages originated 2018-2022
FROM (SELECT SUBSTR(PRINTF('%011d', census_tract),1,5) AS county_st_code, PRINTF('%011d', census_tract) AS census_tract, total_units, loan_amount, state_code, loan_amount
	  FROM LAR
      WHERE action_taken = 1 AND 
			derived_dwelling_category IN ('Single Family (1-4 Units):Site-Built', 'Single Family (1-4 Units):Manufactured') AND
			derived_loan_product_type IS 'Conventional:First Lien' AND 
			reverse_mortgage != 1 AND 
			open_end_line_of_credit != 1 AND 
			business_or_commercial_purpose != 1 AND 
			loan_purpose IN (1, 31, 32) AND
-- 			year is 2022 
			activity_year = 2022
			) AS fromLAR
			
-- loan limits by county, unit count, and year
LEFT JOIN (SELECT PRINTF('%02d', state_code)||PRINTF('%03d', county_code) AS county_st_code, state, year, one_unit_limit, two_unit_limit, three_unit_limit, four_unit_limit
	FROM LoanLimits
	WHERE year = 2022) AS fromLL
	ON fromLAR.county_st_code = fromLL.county_st_code

)

GROUP BY census_tract, jumbo
