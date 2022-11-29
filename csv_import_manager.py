import pandas as pd

columns = {
    'FirstName': 'first_name',
    'LastName': 'last_name',
    'Email': 'email',
    'Password': 'password',
    'RecoveryEmail': 'recovery_email',
    'Email Forwarding': 'email_forwarding',
    'AutoPOSeatScouts': 'auto_po_seats_scouts',
    'ErrorsFailed': 'errors_failed',
    'TMCreated': 'tm_created',
    'TMPassword': 'tm_password',
    'AXSCreated': 'axs_created',
    'AXSPassword': 'axs_password',
    'SGCreated': 'sg_created',
    'SGPassword': 'sg_password',
    'TicketsComCreated': 'tickets_com_created',
    'Eventbrite': 'eventbrite',
    'Etix': 'etix',
    'TicketWeb': 'ticket_web',
    'BigTickets': 'big_tickets',
    'Amazon': 'amazon',
    'SecondaryPassword': 'secondary_password',
    'SeatScoutsAdded': 'seat_scouts_added',
    'SeatScoutsStatus': 'seat_scouts_status',
    'AirFrance': 'airfrance',
    'Team': 'team',
    'SpecificTeam': 'specific_team',
    'ForwardTo': 'forward_to',
    'ForwardEmailPass': 'forward_email_password',
    'RecoveryOrDisabled': 'disabled',
    'Created (BY)': 'created_by',
    'EditedBy': 'edited_by',
    'LDComputerUsed': 'ld_computer_used',
    'DateCreated': 'created_at',
    'LastOpened': 'last_opened',
    'Comments': 'comments',
}

path = '/Users/samoylovartem/Documents/Accounts Data/Mateen Gmail (full original version).csv'
df = pd.read_csv(path, sep=',', keep_default_na=False)
df.drop(df[df['ID'] == ''].index, inplace=True)  # removing all rows where are no ID
df.drop(columns=['Secondary Password', 'SeatScoutsPassword', 'PasswordMatching',
                 'TicketID'], axis=1, inplace=True)
df.rename(columns=columns, inplace=True)
df['type'] = 'gmail'
print(df.dtypes)
# df['edited_by'] = df['edited_by'].convert_dtypes()
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  # striping whitespaces
df['disabled'].replace(to_replace=['disable', 'Disable', 'Disabled', 'Disabed', 'y'],
                       value=1, regex=True, inplace=True)
df['last_opened'].replace(to_replace=['2022-11-1', '2022-11-2', '2022-11-3', '2022-11-4',
                                      '2022-11-5'],
                          value=['2022-11-01', '2022-11-02', '2022-11-03', '2022-11-04',
                                 '2022-11-05'], inplace=True)
df.replace(to_replace=['N', 'Y'], value=[0, 1], inplace=True)  # replacing N and Y to 0 and 1
df.fillna('NA', inplace=True)
df1 = df.iloc[:3000]
df2 = df.iloc[3000:6000]
df3 = df.iloc[6000:]
df1.to_excel('Mateen Gmail (prepared version) part 1.xlsx', index=False)
df2.to_excel('Mateen Gmail (prepared version) part 2.xlsx', index=False)
df3.to_excel('Mateen Gmail (prepared version) part 3.xlsx', index=False)
# df.to_csv('Mateen Gmail (prepared version).csv', index=False)
