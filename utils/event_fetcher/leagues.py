from collections import namedtuple

League = namedtuple('League', ['name', 'start_date', 'end_date'])
NBA = League('NBA', '2023-10-24', '2024-04-14')
MLS = League('MLS', '2023-09-01', '2024-07-17')
NHL = League('NHL', '2023-10-10', '2024-06-01')
MLB = League('MLB', '2023-03-30', '2023-10-01')
NFL = League('NFL', '2023-09-07', '2024-01-07')


def get_leagues():
    return {'NBA': NBA, 'MLS': MLS, 'NHL': NHL, 'MLB': MLB, 'NFL': NFL}
