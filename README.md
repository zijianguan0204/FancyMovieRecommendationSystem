# FancyMovieRecommendationSystem - Data Preprocessing

- Data Import

  - File movies_metadata.csv -> Table [movies_metadata]
    1. Run script data_prep.py on the original csv file movies_metadata.csv, to get movies_metadata_new.csv;
    2. Delete rows of broken data manually (3 broken data found).
        In the new csv file, Ctrl + G(Mac) to go to lines listed below to remove them.
        1. 19764
        2. 29572
        3. 35670
    3. Save and import (using correspinding part in movierecommender.sql)
