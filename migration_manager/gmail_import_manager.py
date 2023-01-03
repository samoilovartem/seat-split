import numpy as np
import pandas as pd
from re import sub

path_to_save = 'accounts/gmail/'


# ================================= READING CSV FILE ======================================
path_to_read = '/Users/samoylovartem/Documents/Data migration/Accounts/Mateen Gmail (full original version).csv'
df = pd.read_csv(path_to_read, sep=',', keep_default_na=False)

# =============================== DELETING SOME COLUMNS ====================================
df.drop(df[df['ID'] == ''].index, inplace=True)
df.drop(columns=['Secondary Password', 'SeatScoutsPassword', 'PasswordMatching',
                 'TicketID', 'ID'], axis=1, inplace=True)


# ======================== RENAMING ALL COLUMN AS A SNAKE_CASE ===============================
def camel_to_snake(item):
    item = sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
    item = sub('[\s*]', '', item)
    item = sub('[()]', '', item)
    return sub('([a-z0-9])([A-Z])', r'\1_\2', item).lower()


df.columns = map(camel_to_snake, df.columns)
df.rename(columns={
    'air_france': 'airfrance',
    'recovery_or_disabled': 'disabled',
    'forward_email_pass': 'forward_email_password',
    'date_created': 'created_at'}, inplace=True)

print(df.columns)

# ================================= ADDING NEW COLUMNS ======================================
df['type'] = 'gmail'

# ============================== CONVERT DTYPES (if needed) =================================
# # df['errors_failed'] = df['errors_failed'].convert_dtypes()


# ============================= STRIPPING WHITESPACES IN CELLS ===============================
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# =================================== REPLACING VALUES =======================================
df['disabled'].replace(to_replace=['disable', 'Disable', 'Disabled', 'Disabed', 'y'],
                       value=1, regex=True, inplace=True)
df['last_opened'].replace(to_replace=['2022-11-1', '2022-11-2', '2022-11-3', '2022-11-4',
                                      '2022-11-5'],
                          value=['2022-11-01', '2022-11-02', '2022-11-03', '2022-11-04',
                                 '2022-11-05'], inplace=True)
df.replace(to_replace=['N', 'Y'], value=[0, 1], inplace=True)
df.replace(to_replace='MATEEN', value=6, inplace=True)

# =========================== REPLACING EMPTY CELLS WITH NaN =================================
df['errors_failed'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
df['comments'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
df['team'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
df['axs_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
df['tm_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
df['sg_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
df['specific_team'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
df['forward_email_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
df['ld_computer_used'].replace(r'^\s*$', np.nan, regex=True, inplace=True)

# =========================== FILLING ALL NaN FIELDS WITH NA =================================
df.fillna('NA', inplace=True)

print(df)

# =========================== SPLITTING DF TO SAVE IN A FEW CSV ===============================
df1 = df.iloc[:3000].to_excel(path_to_save + 'Gmail accounts part 1.xlsx', index=False)
df2 = df.iloc[3000:6000].to_excel(path_to_save + 'Gmail accounts part 2.xlsx', index=False)
df3 = df.iloc[6000:].to_excel(path_to_save + 'Gmail accounts part 3.xlsx', index=False)

# df2 = df.iloc[1500:3000].to_excel('Mateen Gmail (prepared version) part 2.xlsx', index=False)
# df3 = df.iloc[3000:4500].to_excel('Mateen Gmail (prepared version) part 3.xlsx', index=False)
# df4 = df.iloc[4500:6000].to_excel('Mateen Gmail (prepared version) part 4.xlsx', index=False)
# df5 = df.iloc[6000:7500].to_excel('Mateen Gmail (prepared version) part 5.xlsx', index=False)
# df6 = df.iloc[7500:].to_excel('Mateen Gmail (prepared version) part 6.xlsx', index=False)
# df.to_csv('Mateen Gmail (prepared version).csv', index=False)
