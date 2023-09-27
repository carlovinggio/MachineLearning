# include new column with the state name
locations_data = pd.DataFrame()

# Sample DataFrame
locations_data = pd.DataFrame({
    'place_with_parent_names': ['|country|state|', '|country|state|municipality|', '|country|state|municipality|city|', '|country|state|municipality|city|neighborhood|']
})

# Splitting the 'vars' column into multiple columns
locations_data[['country', 'state', 'municipality', 'city', 'neighborhood']] = (
    prop_sell_df['place_with_parent_names']
    .str.strip('|')  # remove leading and trailing '|'
    .str.split('|', expand=True)  # split the string and expand to multiple columns
)

# Drop the original 'vars' column
locations_data = locations_data.drop(columns=['place_with_parent_names'])

# locations_data[['_','country', 'state', 'municipality', 'city', 'neighborhood','__']] = prop_sell_df["place_with_parent_names"].str.split("|", expand=True)
# locations_data.drop(columns=['_','__'], inplace=True)
print(len(prop_sell_df))
print(len(locations_data))

