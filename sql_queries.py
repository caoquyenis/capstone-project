# DROP TABLES
stg_demographic_table_drop = "DROP TABLE IF EXISTS stg_demographic"
stg_covid_us_table_drop = "DROP TABLE IF EXISTS stg_covid_us"
agg_covid_state_table_drop = "DROP TABLE IF EXISTS agg_covid_state"
dim_states_table_drop = "DROP TABLE IF EXISTS dim_states"


# CREATE TABLES
stg_demographic_table_create = ("""
    CREATE TABLE IF NOT EXISTS stg_demographic (
        city varchar(256) NULL,
        state varchar(256) NULL,
        median_age decimal NULL,
        male_population int8 NULL,
        female_population int8 NULL,
        total_population int8 NULL,
        num_veterans int8 NULL,
        foreign_born int8 NULL,
        avg_household_size decimal NULL,
        state_code varchar(256) NULL,
        races varchar(256) NULL,
        "count" int8 NULL
    );
""")

stg_covid_us_create = ("""
    CREATE TABLE IF NOT EXISTS stg_covid_us (
        fips varchar NULL,
        county varchar(256) NULL,
        state varchar(256) NULL,
        lat decimal NULL,
        long decimal NULL,
        "date" varchar(16) NULL,
        cases int8 NULL,
        state_code varchar(256) NULL,
        deaths int8 NULL
    );
""")
# Create fact table
agg_covid_state_table_create = ("""
    CREATE TABLE IF NOT EXISTS agg_covid_state (
        id int identity(0,1) PRIMARY KEY NOT NULL,
        state_code varchar(256) NOT NULL,
        state varchar(256) NULL,
        total_male_population int8,
        total_female_population int8,
        state_population int8,
        total_veterans int8 NULL,
        total_cases int8,
        total_deaths int8
    );
""")
# Create dimension tables
dim_states_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_states (
        state_id int identity(0,1) PRIMARY KEY NOT NULL,
        state_code varchar(32) NOT NULL,
        state varchar(255) NULL
    );
""")

# COPY from local csv to redshift
stg_demographic_copy = ("""
    COPY stg_demographic FROM 's3://gencapstone/us-cities-demographics.csv'
    iam_role 'arn:aws:iam::854296470795:role/redshiftRole'
    CSV
    delimiter ';'
    IGNOREHEADER 1
    compupdate off region 'us-east-1';
""")
 
stg_covid_us_copy = ("""
    COPY stg_covid_us FROM 's3://gencapstone/covid_us_county.csv'
    iam_role 'arn:aws:iam::854296470795:role/redshiftRole'
    CSV
    IGNOREHEADER 1
    compupdate off region 'us-east-1';
""")

# Insert Fact table(s)
agg_covid_state_table_insert = ("""
    INSERT INTO agg_covid_state (
        state_code,                      
        state,                            
        total_male_population,           
        total_female_population,          
        state_population,            
        total_veterans,
        total_cases,
        total_deaths         
    )
    SELECT distinct 
        sd.state_code, 
        sd.state, 
        AVG (sd.male_population) as total_male_poppulation, 
        AVG (sd.female_population) as total_female_population, 
        AVG (sd.total_population) as state_poppulation,
        AVG (sd.num_veterans) as total_veterans,
        AVG (sc.cases) as total_cases,
        AVG (sc.deaths) as total_deaths  
    FROM stg_demographic as sd
    INNER JOIN stg_covid_us as sc
    ON sd.state_code = sc.state_code
    GROUP BY sd.state_code, sd.state;
""")


dim_states_table_insert = ("""
    INSERT INTO dim_states (        
        state_code,          
        state                    
    )
    SELECT distinct state_code, state
    FROM stg_demographic
    WHERE state_code IS NOT NULL;
""")


# QUERY LISTS

create_table_queries = [stg_demographic_table_create, stg_covid_us_create,
                        agg_covid_state_table_create, dim_states_table_create]
drop_table_queries = [stg_demographic_table_drop, stg_covid_us_table_drop, agg_covid_state_table_drop, dim_states_table_drop]

# COPY QUERIES = [staging_events_copy]
copy_table_queries = [stg_demographic_copy, stg_covid_us_copy]
insert_table_queries = [agg_covid_state_table_insert, dim_states_table_insert]
