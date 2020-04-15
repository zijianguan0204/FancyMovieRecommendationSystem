import pandas as pd

# Read data from csv file
data = pd.read_csv("movies_metadata.csv", dtype=object)

# Remove duplicates on column id
data.drop_duplicates(subset ="id",inplace = True) 

# Covert False/True to Mysql Boolean(TINYINT) value 0/1
data["adult"] = data["adult"].replace(r'False', "0")
data["adult"] = data["adult"].replace(r'True', "1")

# Remove broken data 
data1 = data.loc[data['adult'] == '0']
data2 = data.loc[data['adult'] == '1']
data =  data1.append(data2)

# Covert False/True to Mysql Boolean(TINYINT) value 0/1
data["video"] = data["video"].replace(r'False', "0")
data["video"] = data["video"].replace(r'True', "1")
data["video"] = data["video"].fillna(-1) # Set NaN value to -1

data["revenue"] = data["revenue"].fillna(-1) # Set NaN value to -1

data["popularity"] = data["popularity"].fillna(-1.0) # Set NaN value to -1.0

data["release_date"] = data["release_date"].fillna('9999-12-31') # Set NaN value to 9999-12-31


data["runtime"] = data["runtime"].fillna(-1.0) # Set NaN value to -1.0

data["vote_average"] = data["vote_average"].fillna(-1.0) # Set NaN value to -1.0

data["vote_count"] = data["vote_count"].fillna(-1) # Set NaN value to -1

# Write updated data to new csv file
data.to_csv (r'movies_metadata_new.csv', index = False, header=True)