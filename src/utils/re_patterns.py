from dataclasses import dataclass


@dataclass
class Patterns:
    auction_id = r'obj=(.*)'
    auction_date = r'Дата — (\d{1,2} [А-Яа-я]+ \d{4})'
    auction_time = r'в (\d{2}:\d{2})'
    auction_timezone = r'\((по .*?)\)'
    auction_deadline = r'\d{1,2} (?:[A-Яа-я]+) \d{4}\b|\b\d{2}.\d{2}.\d{4}'
