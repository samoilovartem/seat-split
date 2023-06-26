import pandas as pd


def calculate_tokens(text):
    # Calculate tokens (assuming each token is about 4 characters)
    token_count = len(text) / 4

    return token_count


# Load the data
df = pd.read_csv("data_full.csv", encoding='ISO-8859-1', delimiter=';')

# Create a new column with the count of tokens in each row of 'Column5'
df['token_count'] = df['Column5'].apply(calculate_tokens)

# Print the total amount of tokens in 'Column5'
print(f"Total tokens in 'Column5': {df['token_count'].sum()}")
