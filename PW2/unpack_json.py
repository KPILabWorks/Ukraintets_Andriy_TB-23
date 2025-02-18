# Практична робота 2
# Векторизоване зчитування JSON. Зчитайте великий JSON-файл у Pandas через pd.read_json() та розпакуйте вкладені структури.

import pandas
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Unpack nested JSON files")
    parser.add_argument("--path", type=str, default='data.json', help="Input JSON file path")
    args = parser.parse_args()

    dataframe = pandas.read_json(args.path)

    print(dataframe)

    if 'details' in dataframe.columns:
        nested_dataframe = pandas.json_normalize(dataframe['details'])
        dataframe = dataframe.drop(columns=['details']).join(nested_dataframe)

    print(dataframe)
