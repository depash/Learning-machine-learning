import pandas as pd

df = pd.read_csv("hf://datasets/hugginglearners/netflix-shows/netflix_titles.csv")

output = df.describe()

print(output)