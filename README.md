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
* Use redshift to store structered data from ast import JoinedStr
from raw source. Then, we can analysis.

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

##### stagging demographic table

|Field name            |Datatype    |Field Length   |Constraint   |Description                             |
|----------------------|------------|---------------|-------------|----------------------------------------|
|city                  |varchar     |256            |NULLABLE     |City in stage                           |
|state                 |varchar     |256            |NULLABLE     |State in US                             |
|median_age            |decimal     |               |NULLABLE     |Median Age                              |
|male_population       |int8        |               |NULLABLE     |Male population                         |
|female_population     |int8        |               |NULLABLE     |Female population                       |
|total_population      |int8        |               |NULLABLE     |Total population                        |
|num_veterans          |int8        |               |NULLABLE     |Number of veterans                      |
|foreign_born          |int8        |               |NULLABLE     |Foreign born                            |
|avg_household_size    |int8        |               |NULLABLE     |Average of household size               |
|state_code            |varchar     |256            |NULLABLE     |State code, FK to dim_states table      |
|races                 |varchar     |256            |NULLABLE     |Races                                   |
|count                 |int8        |               |NULLABLE     |Count                                   |


##### stgging covid_us table

|Field name            |Datatype    |Field Length   |Constraint   |Description                               |
|----------------------|------------|---------------|-------------|------------------------------------------|
|fips                  |varchar     |256            |NULLABLE     |Fips                                      |
|county                |varchar     |256            |NULLABLE     |County                                    |
|state                 |varchar     |256            |NULLABLE     |State                                     |
|lat                   |decimal     |               |NULLABLE     |Latitude. Not important                   |
|long                  |decimal     |               |NULLABLE     |Longitude. Not important                  |
|date                  |varchar     |16             |NULLABLE     |Date.                                     |
|cases                 |int8        |               |NULLABLE     |Covid cases. FK to agg_covid_state table  |
|state_code            |varchar     |256            |NULLABLE     |State code. FK to agg_covid_state table   |
|deaths                |int8        |               |NULLABLE     |Deaths. FK to agg_covid_state table       |


##### Aggregate Covid by state table

|Field name              |Datatype    |Field Length   |Constraint   |Description                               |
|------------------------|------------|---------------|-------------|------------------------------------------|
|id                      |identity    |               |PRIMARY KEY  |Id                                        |
|state_code              |varchar     |256            |NOT NULL     |State code                                |
|state                   |varchar     |256            |NULLABLE     |State                                     |
|total_male_population   |int8        |               |NOT NULL     |Total male population                     |
|total_female_population |int8        |               |NOT NULL     |Total female population                   |
|state_population        |int8        |               |NOT NULL     |State population                          |
|total_veterans          |int8        |               |NULLABLE     |Total veterans                            |
|total_cases             |int8        |               |NOT NULL     |Total covid cases                         |
|total_deaths            |int8        |               |NOT NULL     |Total deaths                              |


##### States dimension table

|Field name              |Datatype    |Field Length   |Constraint   |Description                               |
|------------------------|------------|---------------|-------------|------------------------------------------|
|state_id                |identity    |               |PRIMARY KEY  |State Id                                  |
|state_code              |varchar     |32             |NOT NULL     |State code                                |
|state                   |varchar     |256            |NULLABLE     |State                                     |


#### Step 5: Complete Project Write Up

##### Clearly state the rationale for the choice of tools and technologies for the project.

* In this project, I use **Star Scheme** to aggregate data and present dimension data. Because of:
1. It is simple to understand in this project type
2. No many Joins

* Use redshift to store face and dimension tables. Source datasets were uploaded on S3 bucket.
* Use S3 to store source csv due to S3 supports COPY command to Redshift cluster very fast. In case scale up, I can write to S3 to store parquet file.
* Redshift is a popular data warehouse database that can handle data on an exabytes scale. Redshift is able to execute on a large volume of data at lightning speed.

##### Propose how often the data should be updated and why.

This data type is not frequency updated. Because of the cost to collect data. So I suppose the data was updated yearly.

##### Write a description of how you would approach the problem differently under the following scenarios:

The data was increased by 100x.
* Not problem if using redshift. Or I can use spark to write to S3 parquet. 

The data populates a dashboard that must be updated on a daily basis by 7am every day.
* Use automation Airflow then set the schedule to run task every. Another option is combination of Airflow + Apache + Livy and EMR.

The database needed to be accessed by 100+ people.
* I consider to choose **NO SQL** database run by AWS.
* Elastic Load Balancing
* Try to Amazon ElastiCache

# Sample test result

[('MD', 18197, 312), ('PA', 17940, 342), ('AK', 2991, 15), ('AR', 4905, 71), ('CT', 34186, 698)]


# Project introduction
Use AWS redshift to build an ETL pipeline for a database.
Load data from S3 to staging tables on Redshift 
and execute SQL statements that create the analytics tables from these staging tables.

## How to run
run etl.py