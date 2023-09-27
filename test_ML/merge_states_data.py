import os
import pandas as pd 
from pandas import DataFrame


def replace_comma_with_semicolon(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace(",", ";")

    with open(file_path, 'w') as file:
        file.write(content)


def read_csvs_in_folder(folder_path) -> DataFrame:
    files = os.listdir(folder_path)
    
    csv_files = [f for f in files if f.endswith('.csv')]
    
    main_df = pd.DataFrame()
    
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        
        df = pd.read_csv(file_path, delimiter=";")
        df['state'] = csv_file[:-4]
        
        main_df = pd.concat([main_df, df], ignore_index=True)
        
    return main_df


states_data = read_csvs_in_folder(r"/Users/vinggio/pr/workers/MachineLearning/states_data")
print(states_data.columns)


states_data.rename(columns={
    'total_robos': "thefts",
    'total_lesiones': "injuries",
    'total_homicidios': "homicides",
    'delitos_patrimoniales': "property_crimes",
    'secuestro': "kidnappings",
    'violacion': "rapes",
    'otros_delitos': "other",
}, inplace=True)
states_data.to_csv("/test_ML/Files/crimes_by_state.csv", index=False)
print(states_data.head())