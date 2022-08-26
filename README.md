# Aggregate Covid cases and deaths by state in US with poppulation.
### Data Engineering Capstone Project

#### Project Summary
--describe your project at a high level--

In this project, I collected 2 datasets. The Covid date shows the covid cases and deaths by state code. The second data shows the population of each state in US.
So, i would like aggregate the covid case group by state include poppulation data.
The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

### Step 1: Scope the Project and Gather Data

#### Scope 

* I would like to see if the airport is ennough for the US city's population. The stakeholder can decide to invest more budget if that airport is not enough.
* Use redshift to store structered data from raw source. Then, we can analysis.

#### Describe and Gather Data 
* In this project, I will use 2 dataset: us-cities-demograpics & airport-codes. 2 files were upload on S3 bucket.
* Dataset come from Udacity provided.


### Step 2: Explore and Assess the Data

#### Explore the Data 
##### US Cities demographic
* City: string (nullable = true)
* State: string (nullable = true)
* Median Age: string (nullable = true)
* Male Population: string (nullable = true)
* Female Population: string (nullable = true)
* Total Population: string (nullable = true)
* Number of Veterans: string (nullable = true)
* Foreign-born: string (nullable = true)
* Average Household Size: string (nullable = true)
* State Code: string (nullable = true)
* Race: string (nullable = true)
* Count: string (nullable = true)

##### Airport codes
* ident: string (nullable = true)
* type: string (nullable = true)
* name: string (nullable = true)
* elevation_ft: string (nullable = true)
* continent: string (nullable = true)
* iso_country: string (nullable = true)
* iso_region: string (nullable = true)
* municipality: string (nullable = true)
* gps_code: string (nullable = true)
* iata_code: string (nullable = true)
* local_code: string (nullable = true)
* coordinates: string (nullable = true)

#### Cleaning Steps
* Use SELECT DISTINCT to remove duplicate row values.
* Use WHERE column IS NOT NULL to skip null values

### Step 3: Define the Data Model
#### 3.1 Conceptual Data Model
I choose 2 datasets. 
* The airport codes show the air code name, air code type in many place (include US)
* The us cities demographic show the population in each state (state code)
I would like to see how many are code type in each US state.

#### 3.2 Mapping Out Data Pipelines
* Connect to S3 bucket
* Create staging US demographic table
* Create staging aircode table
* Create fact cities airport table
* Create dimension tables (races, cities, airports)
* COPY from s3 to redshift cluster to insert staging table.
* INSERT to each fact and dimension tables

### Step 4: Run Pipelines to Model the Data 
#### 4.1 Create the data model
Build the data pipelines to create the data model.

#### 4.2 Data Quality Checks
Explain the data quality checks you'll perform to ensure the pipeline ran as expected. These could include:
 * Integrity constraints on the relational database (e.g., unique key, data type, etc.)
 * Unit tests for the scripts to ensure they are doing the right thing
 * Source/Count checks to ensure completeness
 
Run Quality Checks

#### 4.3 Data dictionary 
Create a data dictionary for your data model. For each field, provide a brief description of what the data is and where it came from. You can include the data dictionary in the notebook or in a separate file.
##### staging_demographic. Load from us-cities-demographic.csv on S3 bucket
* city: varchar nullable
* state: varchar nullable
* median_age: numeric nullable
* male_population: int4 nullable
* female_population: int8 nullable
* total_population: int8 nullable
* number_veterans: int8 nullable
* foreign_born: int8 nullable
* household_size: numeric nullable
* state_code: varchar nullable
* race: varchar nullable
* count: int8 nullable

##### staging_aircodes. Load from airport-codes_csv.csv on S3 bucket
* ident	varchar	nullable
* type	varchar	nullable
* name	varchar	nullable
* elevation_ft	int4	nullable
* continent	varchar	nullable
* iso_country	varchar	nullable
* iso_region	varchar	nullable
* municipality	varchar	nullable
* gps_code	varchar	nullable
* iata_code	varchar	nullable
* local_code	varchar	nullable
* coordinates	varchar	nullable

##### cities_airport. Join staging_demographic with staging_aircodes
* cities_air_id	int4	not null
* state_code	varchar	nullable
* city	varchar	nullable
* state	varchar	nullable
* median_age	numeric	nullable
* male_population	int4	nullable
* female_population	int4	nullable
* total_population	int4	nullable
* number_veterans	int4	nullable
* foreign_born	int4	nullable
* household_size	numeric	nullable
* race	varchar	nullable
* count	int4	nullable
* ident	varchar	nullable
* type	varchar	nullable
* name	varchar	nullable

##### airports. Select from staging_demographic
* airports_id	int4	not null
* type	varchar	nullable
* name	varchar	nullable
* iso_region	varchar	nullable
* municipality	varchar	nullable
* gps_code	varchar	nullable

##### cities. Select from staging_demographic
* cities_id	int4	not null
* state_code	varchar	nullable
* state	varchar	nullable
* city	varchar	nullable

##### races. Select from staging_demographic
* race_id	int4	not null
* race	varchar	nullable
* count	int4	nullable

#### Step 5: Complete Project Write Up
##### Clearly state the rationale for the choice of tools and technologies for the project.
* Use redshift to store face and dimension tables. Source datasets were uploaded on S3 bucket.
##### Propose how often the data should be updated and why.
* This data type is not frequency updated. Because of the cost to collect data. So I suppose the data was updated yearly
##### Write a description of how you would approach the problem differently under the following scenarios:
 * The data was increased by 100x. => Not problem if using redshift. Or I can use spark to write to S3 parquet. 
 * The data populates a dashboard that must be updated on a daily basis by 7am every day. => Use automation Airflow then set the schedule to run task every
 * The database needed to be accessed by 100+ people.





# Project introduction
Use AWS redshift to build an ETL pipeline for a database.
Load data from S3 to staging tables on Redshift 
and execute SQL statements that create the analytics tables from these staging tables.

## How to run
- Create connection to Redshift. Run redshift.py
** Please do not run redshift.py file because we have initial redshift already.
- Add IAM Role by run create_iam_role.py
- Create database connection by run create_tables.py
** Please do not run create_tables.py because we have all databases
- Read etl to run load CSV file from S3, then insert to own database (staging, fact and dimension)

** Run delete_cluster.py will delete all redshift. Please carefully.