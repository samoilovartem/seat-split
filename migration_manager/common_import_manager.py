from re import sub

import numpy as np
import pandas as pd

path_to_save = 'accounts/'

# ================================= READING CSV FILE ======================================
path_to_read = (
    '/Users/samoylovartem/Documents/Data migration/Accounts/Summary of Accounts.csv'
)
df = pd.read_csv(path_to_read, sep=',', keep_default_na=False)

# =============================== DELETING SOME COLUMNS ====================================
# df.drop(df[df['ID'] == ''].index, inplace=True)
df.drop(columns=['ID', 'AirFrance'], axis=1, inplace=True)


# ======================== RENAMING ALL COLUMN AS A SNAKE_CASE ===============================
def camel_to_snake(item):
    item = sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
    item = sub('[\s*]', '', item)
    item = sub('[()]', '', item)
    return sub('([a-z0-9])([A-Z])', r'\1_\2', item).lower()


df.columns = map(camel_to_snake, df.columns)
df.rename(
    columns={
        'air_france': 'airfrance',
        'recovery_or_disabled': 'disabled',
        'forward_email_pass': 'forward_email_password',
        'date_created': 'created_at',
    },
    inplace=True,
)

print(df.columns)

# ================================= ADDING NEW COLUMNS ======================================
# df['type'] = 'gmail'

# ============================== CONVERT DTYPES (if needed) =================================
# # df['errors_failed'] = df['errors_failed'].convert_dtypes()


# ============================= STRIPPING WHITESPACES IN CELLS ===============================
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# =================================== REPLACING VALUES =======================================
# df['disabled'].replace(to_replace=['disable', 'Disable', 'Disabled', 'Disabed', 'y'],
#                        value=1, regex=True, inplace=True)
# df['password_matching'].replace(to_replace=['Incorrect', 'Correct'],
#                                 value=[0, 1], regex=True, inplace=True)
# df.replace(to_replace=['N', 'Y'], value=[0, 1], inplace=True)
# df.replace(to_replace='MATEEN', value=6, inplace=True)

# =========================== REPLACING EMPTY CELLS WITH NaN =================================
# df['errors_failed'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['comments'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['team'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['axs_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['tm_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['sg_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['specific_team'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['forward_email_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['ld_computer_used'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['phone'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['tickets_com_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['migrated_from'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['migrated_to'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['email'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['recovery_email'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['secondary_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['first_name'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['last_name'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['forward_to'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['password_matching'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# df['seat_scouts_password'].replace(r'^\s*$', np.nan, regex=True, inplace=True)

# =========================== FILLING ALL NaN FIELDS WITH NA =================================
# df.fillna('NA', inplace=True)
#
# print(df)

# =========================== SPLITTING DF TO SAVE IN A FEW CSV ===============================
# df.to_excel('Accounts (prepared version).xlsx', index=False)

# df1 = df.iloc[:3000].to_excel(path_to_save + 'Accounts (prepared version) part 1.xlsx', index=False)
# df2 = df.iloc[3000:6000].to_excel(path_to_save + 'Accounts (prepared version) part 2.xlsx', index=False)
# df3 = df.iloc[6000:9000].to_excel(path_to_save + 'Accounts (prepared version) part 3.xlsx', index=False)
# df4 = df.iloc[9000:12000].to_excel(path_to_save + 'Accounts (prepared version) part 4.xlsx', index=False)
# df5 = df.iloc[12000:15000].to_excel(path_to_save + 'Accounts (prepared version) part 5.xlsx', index=False)
# df6 = df.iloc[15000:18000].to_excel(path_to_save + 'Accounts (prepared version) part 6.xlsx', index=False)
# df7 = df.iloc[18000:21000].to_excel(path_to_save + 'Accounts (prepared version) part 7.xlsx', index=False)
# df8 = df.iloc[21000:24000].to_excel(path_to_save + 'Accounts (prepared version) part 8.xlsx', index=False)
# df9 = df.iloc[24000:27000].to_excel(path_to_save + 'Accounts (prepared version) part 9.xlsx', index=False)
# df10 = df.iloc[27000:30000].to_excel(path_to_save + 'Accounts (prepared version) part 10.xlsx', index=False)
# df11 = df.iloc[30000:].to_excel(path_to_save + 'Accounts (prepared version) part 11.xlsx', index=False)
