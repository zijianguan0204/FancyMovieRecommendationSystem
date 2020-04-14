import pandas as pd

data = pd.read_csv("movies_metadata.csv", dtype=object)

data["adult"] = data["adult"].replace(r'False', "0")
data["adult"] = data["adult"].replace(r'True', "1")

data["video"] = data["video"].replace(r'False', "0")
data["video"] = data["video"].replace(r'True', "1")
data["video"] = data["video"].fillna(-1)

data["revenue"] = data["revenue"].fillna(-1)

data["popularity"] = data["popularity"].fillna(-1.0)

data["release_date"] = data["release_date"].fillna('9999-12-31')


data["runtime"] = data["runtime"].fillna(-1.0)

data["vote_average"] = data["vote_average"].fillna(-1.0)

data["vote_count"] = data["vote_count"].fillna(-1)

data.to_csv (r'movies_metadata_new.csv', index = False, header=True)