<h1>HMDA</h1>
Exploration of jumbo lending trends and top lenders, prompted by proposed changes to Basel rules.

<ul id="top">
    <li><a href="#queries">Data queries</a></li>
    <li><a href="#cleaning">Data cleaning</a></li>
</ul>

<h2 id="queries">Data queries</h2>

Queries were run to assess changes in the volume and amount of jumbo loans from 2018-2022, the most active jumbo markets geographically in 2022, the most active jumbo lenders in 2022 and the jumbo lending profiles of First Republic Bank and Silicon Valley Bank.

In each of these queries, whether a loan was labeled "jumbo" was determined based on the mortgaged property's county and number of units and on the year the loan was made. If the loan exceeded its respective limit, it was labeled "jumbo." In a minority of cases, loans were missing census tract data, which are used to find their loan limits. In those instances, the mode by unit-count for the loan's year was substituted.

<h4>Jumbo loans over time</h4>

<a href="./queries/totalsByYear.sql" target="_blank">This query</a> retrieves the total amount of money loaned, the number of loans made and the number of loan providers each year for jumbo and conforming loans. The query sums loan_amount, counts lei and counts the distinct lei, grouped by year and jumbo/conforming.

<h4>Jumbo loans by location 2022</h4>

<a href="./queries/totalsByCensusTract.sql" target="_blank">This query</a> retrieves the state abbreviation, total amount of money loaned, number of loans made and number of loan providers in 2022 for jumbo and conforming loans, grouped by census tract and jumbo/conforming.

<h4>Jumbo loans by lender 2022</h4>

<a href="./queries/totalsByLEI.sql" target="_blank">This query</a> retrieves the respondent name, total amount of money loaned and number of loans made in 2022 for jumbo and conforming loans, grouped by legal entity identifier and jumbo/conforming.

<h4>Jumbo loans by First Republic and Silicon Valley banks</h4>

<a href="./queries/fr_sv_banks.sql" target="_blank">This query</a> retrieves the respondent name, uyear, loan amount, income, property value, combined loan-to-value ratio, interest rate, rate spread, county-state code, census tract, state and jumbo status for jumbo and conforming loans originated by First Repbulic Bank and Silicon Valley Bank from 2018 to 2022.

<a href="#top">Return to top</a>

<h2 id="cleaning">Data cleaning</h2>

This step cleaned up query results and created the final spreadsheets used in the visualizations.

<ul>
    <li><a href="./dataCleaning/byYear.py" target="_blank">Jumbo by Year</a></li>
    <li><a href="./dataCleaning/byCensusTract.py" target="_blank">Jumbo by State</a></li>
    <li><a href="./dataCleaning/byLender.py" target="_blank">Jumbo by Lender</a></li>
    <li><a href="./dataCleaning/deadBanks.py" target="_blank">First Republic and Silicon Valley</a></li>
</ul>

<a href="#top">Return to top</a>