from collections import defaultdict
from json import load

with open('seatscouts_tickets_response_example.json') as f:
    data = load(f)

seats_by_section_and_row = defaultdict(lambda: defaultdict(list))

for ticket in data['tickets']:
    section = ticket['section']
    row = ticket['row']
    seat = ticket['seat']
    seats_by_section_and_row[section][row].append(seat)


def display_available_seats(seats_by_section_and_row: dict):
    for section, rows in seats_by_section_and_row.items():
        for row, seats in rows.items():
            sorted_seats = sorted(seats)
            first_seat = sorted_seats[0]
            last_seat = sorted_seats[-1]

            if first_seat == last_seat:
                seat_range = f'{first_seat}'
            else:
                seat_range = f'{first_seat}-{last_seat}'
            print(f'Section {section}, Row {row}, Seats: {seat_range}')


if __name__ == '__main__':
    display_available_seats(seats_by_section_and_row)
