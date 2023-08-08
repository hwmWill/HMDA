SELECT activity_year, COUNT(DISTINCT(lei)) AS lenders
FROM LAR
WHERE action_taken = 1 AND 
	derived_dwelling_category IN ('Single Family (1-4 Units):Site-Built', 'Single Family (1-4 Units):Manufactured') AND
	derived_loan_product_type IS 'Conventional:First Lien' AND 
	reverse_mortgage != 1 AND 
	open_end_line_of_credit != 1 AND 
	business_or_commercial_purpose != 1 AND 
	loan_purpose IN (1, 31, 32)
GROUP BY activity_year;