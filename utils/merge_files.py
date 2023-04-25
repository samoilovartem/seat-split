import pandas as pd


def merge_files(files: list[str], output_file: str):
    dataframes = []

    for file in files:
        df = pd.read_csv(file)
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    unique_df = combined_df.drop_duplicates(subset=['line', 'city'])

    num_duplicates = len(combined_df) - len(unique_df)
    num_unique_records = len(unique_df)

    unique_df.to_csv(output_file, index=False)

    print(f'Merged {len(files)} files into {output_file} with no duplicates.')
    print(f'Number of duplicates: {num_duplicates}')
    print(f'Number of unique records: {num_unique_records}')


if __name__ == '__main__':
    files = [
        'WY_addresses.csv',
        'WY_addresses_2.csv',
    ]
    output_file = 'all_states/WY_addresses.csv'
    merge_files(files, output_file)
