from re import sub

import numpy as np
import pandas as pd

path_to_save = 'domains/'

# ================================= READING CSV FILE ======================================
path_to_read = '/Users/samoylovartem/Documents/Data migration/catchall_Registration_info - lddomains.csv'
df = pd.read_csv(path_to_read, sep=',', keep_default_na=False)

# =============================== DELETING SOME COLUMNS ====================================
# df.drop(df[df['ID'] == ''].index, inplace=True)
# df.drop(columns=['ID', 'AirFrance'], axis=1, inplace=True)


# ======================== RENAMING ALL COLUMN AS A SNAKE_CASE ===============================
def camel_to_snake(item):
    item = sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
    item = sub('[\s*]', '', item)
    item = sub('[()]', '', item)
    return sub('([a-z0-9])([A-Z])', r'\1_\2', item).lower()


df.columns = map(camel_to_snake, df.columns)
df.rename(
    columns={
        'auto-renew': 'auto_renew',
        'privacy': 'is_private',
        'lock': 'is_locked',
        'defaultroute': 'is_default_route',
        'secdomain': 'is_second_domain',
    },
    inplace=True,
)

# ================================= ADDING NEW COLUMNS ======================================
df['type'] = 'CATCHALLS'
df['created_by'] = 5

df = df[
    [
        'domain_name',
        'type',
        'status',
        'expiration_date',
        'auto_renew',
        'is_private',
        'is_locked',
        'is_default_route',
        'is_second_domain',
        'created_by',
    ]
]

print(df.columns)

# ============================== CONVERT DTYPES (if needed) =================================
# # df['errors_failed'] = df['errors_failed'].convert_dtypes()


# ============================= STRIPPING WHITESPACES IN CELLS ===============================
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# =================================== REPLACING VALUES =======================================
# df['disabled'].replace(
#     to_replace=['disable', 'Disable', 'Disabled', 'Disabed', 'y'],
#     value=1,
#     regex=True,
#     inplace=True,
# )
# df['password_matching'].replace(
#     to_replace=['Incorrect', 'Correct'], value=[0, 1], regex=True, inplace=True
# )
df['is_private'].replace(to_replace=['Private', 'Public'], value=[1, 0], inplace=True)
df['auto_renew'].replace(to_replace=['On'], value=[1], inplace=True)
df['is_locked'].replace(to_replace=['Locked', 'Unlocked'], value=[1, 0], inplace=True)
df['is_default_route'].replace(to_replace=['done'], value=[1], inplace=True)
df['is_second_domain'].replace(to_replace=['done'], value=[1], inplace=True)
df['status'].replace(
    to_replace=['Active', 'Pending Transfer Away'],
    value=['active', 'pending'],
    inplace=True,
)
# df.replace(to_replace='MATEEN', value=6, inplace=True)

# =========================== REPLACING EMPTY CELLS WITH NaN =================================
# df['errors_failed'].replace(r'^\s*$', np.nan, regex=True, inplace=True)

# =========================== FILLING ALL NaN FIELDS WITH NA =================================
df.fillna('NA', inplace=True)
#
print(df)

# =========================== SPLITTING DF TO SAVE IN A FEW CSV ===============================
df.to_csv('catchalls_domains.csv', index=False)
