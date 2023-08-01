SELECT lei, jumbo, respondent_name, SUM(loan_amount) AS amount_loaned, COUNT(*) AS loans
FROM 
-- joined
(
SELECT fromLAR.lei, respondent_name, loan_amount, 
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
FROM
-- LAR query
(SELECT SUBSTR(PRINTF('%011d', census_tract),1,5) AS county_st_code, total_units, loan_amount, lei
FROM LAR
WHERE action_taken = 1 AND 
	derived_dwelling_category IN ('Single Family (1-4 Units):Site-Built', 'Single Family (1-4 Units):Manufactured') AND
	derived_loan_product_type IS 'Conventional:First Lien' AND 
	reverse_mortgage != 1 AND 
	open_end_line_of_credit != 1 AND 
	business_or_commercial_purpose != 1 AND 
	loan_purpose IN (1, 31, 32) AND
-- 	just 2022
	activity_year = 2022
	) AS fromLAR

-- loan limits by county, unit count, and year
LEFT JOIN (SELECT PRINTF('%02d', state_code)||PRINTF('%03d', county_code) AS county_st_code, year, one_unit_limit, two_unit_limit, three_unit_limit, four_unit_limit
	FROM LoanLimits
	WHERE year = 2022) AS fromLL
	ON fromLAR.county_st_code = fromLL.county_st_code
	
-- entity names by lei and year
LEFT JOIN (SELECT lei, respondent_name, name_state AS resp_name_st 
	FROM Entities
	WHERE activity_year = 2022) AS fromEntities
	ON fromLAR.lei = fromEntities.lei
)
GROUP BY lei, jumbo