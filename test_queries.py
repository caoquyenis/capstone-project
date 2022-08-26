# Fact table test case
stg_demographic_table_test = ("""
    SELECT COUNT(*)
    FROM {s};
""")
# stg_covid_us_table_test = ("""
#     SELECT COUNT(*)
#     FROM stg_covid_us;
# """)
# agg_covid_state_table_test = ("""
#     SELECT COUNT(*)
#     FROM agg_covid_state;
# """)
# dim_states_table_test = ("""
#     SELECT COUNT(*)
#     FROM dim_states;
# """)


check_state_code_len = ("""
    SELECT state_code FROM agg_covid_state
    WHERE length(state_code) > 2
""")
# QUERY TEST CASE

#check_greater_than_zero_queries = [stg_demographic_table_test, stg_covid_us_table_test, agg_covid_state_table_test, dim_states_table_test]
check_field_len_queries = [check_state_code_len]


