import gspread
import pandas as pd

gservice_file = r"Gservice.json"
gp = gspread.service_account(filename=gservice_file)

google_sheet = gp.open_by_url('https://docs.google.com/spreadsheets/d/1eKdNvXwWvGMADmglb2tyR9XOGbcE13Q-Ttf_aX270hU/')

trade_shift_dict = google_sheet.worksheet('Amex Tradeshift').get_all_records()
citi_virtual_dict = google_sheet.worksheet('Citi Virtual').get_all_records()
global_rewards_dict = google_sheet.worksheet('Global Rewards').get_all_records()
divvy_visa_dict = google_sheet.worksheet('Divvy Visa').get_all_records()

data_frame_trade_shift = pd.DataFrame(trade_shift_dict)
data_frame_citi_virtual = pd.DataFrame(citi_virtual_dict)
data_frame_global_rewards = pd.DataFrame(global_rewards_dict)
data_frame_divvy_visa = pd.DataFrame(divvy_visa_dict)


def get_data_frame():
    final_data_frame = pd.concat([
        data_frame_trade_shift,
        data_frame_citi_virtual,
        data_frame_global_rewards,
        data_frame_divvy_visa
    ], ignore_index=True)
    return final_data_frame.to_html()


if __name__ == '__main__':
    print(get_data_frame())
    # get_data_frame()
# print(final_data_frame.to_html())
