import pandas as pd


def merge_files(file1, file2, output_file):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    combined_df = pd.concat([df1, df2], ignore_index=True)

    unique_df = combined_df.drop_duplicates(subset=['line', 'city'])

    num_duplicates = len(combined_df) - len(unique_df)
    num_unique_records = len(unique_df)

    unique_df.to_csv(output_file, index=False)

    print(f'Merged {file1} and {file2} into {output_file} with no duplicates.')
    print(f'Number of duplicates: {num_duplicates}')
    print(f'Number of unique records: {num_unique_records}')


if __name__ == '__main__':
    file1 = 'TX_addresses.csv'
    file2 = 'TX_addresses_2.csv'
    output_file = 'all_states/TX_addresses.csv'
    merge_files(file1, file2, output_file)
