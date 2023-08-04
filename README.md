<h1>HMDA</h1>
Repository for working with Home Mortgage Disclosure Act data.

<ul id="top">
    <li><a href="#sources">Data sources</a></li>
    <li><a href="#acquisition">Data acquisition</a></li>
    <li><a href="#joins">Data joining</a></li>
    <li><a href="#projects">HMDA reporting</a></li>
</ul>

<h2 id="sources">Data sources</h2>

<img src="./img/Datasets.png" />

This analysis relies on Home Mortgage Disclosure Act data disclosures maintained by the Consumer Financial Protection Bureau. Both the loan application records and transmittal sheet records can be found <a href="https://ffiec.cfpb.gov/data-publication/dynamic-national-loan-level-dataset/2022" target="_blank">here</a>.

LAR data provides dozens of details about every loan application. This analysis narrowed the pool of LAR records to originated, conventional, first-lien, non-reverse-mortgage, non-open-line-of-credit, noncommercial mortgages used to purchase or refinance single-family dwellings.

Transmittal sheet data provides lenders' names, addresses and legal entity identifiers. 

This analysis also relies on the conforming loan limits set each year by the Federal Housing Finance Agency. Annual limits by unit count and county can be found <a href="https://www.fhfa.gov/DataTools/Downloads/Pages/Conforming-Loan-Limit.aspx" target="_blank">here</a>.

<a href="#top">Return to top</a>

<h2 id="acquisition">Data acquisition</h2>

Data was imported into a SQLite database using Python. The notebook used in this step is available <a href="./createSQL.py" target="_blank">here</a>.

When importing LAR data, 'Exempt' was used as a null value when reading numeric columns in the source data, state_code and applicant_age/co_applicant_age (which are given as age ranges) were imported as strings, and pipes were used as delimiters.

When importing TS data, pipes were used as delimiters and a column was added concatenating respondent_name and respondent_state to serve as a unique identifier for entities that had common names.

Loan limit dataframes were concatenated in their entirety, with a column added for year and columns renamed for easier querying.

<a href="#top">Return to top</a>

<h2 id="joins">Data joining</h2>

<img src="./img/Joins.png" />

Starting with the filtered LAR data, conforming loan limit data and transmittal sheet data were each left-joined. Left joins were chosen to prevent the loss of any loans in the filtered LAR data in the event that loans are missing the attributes used to join with the other datasets.

Loan limits were joined based on the first five digits of zero-padded LAR census tracts being equal to loan limits' concatenated zero-padded state and county codes <strong>AND</strong> LAR's activity year being equal to loan limits' year. LAR census tracts were chosen instead of LAR county and state codes because census tracts had far fewer missing or errant data.

Transmittal sheet data was joined based on legal identiy identifier and activity year.

<a href="#top">Return to top</a>

<h2 id="projects">HMDA reporting</h2>

Projects using this dataset include:

<ul>
    <li><a href="./Jumbo/README.md">Jumbo loans 2018-2022</a></li>
    <li><a href="./HSBC/README.md">HSBC redlining</a></li>
</ul>

<a href="#top">Return to top</a>
