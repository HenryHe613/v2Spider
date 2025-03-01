from datetime import datetime

def parse_date(date_str:str) -> int:
    try:
        return int(datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z').timestamp())
    except ValueError:
        return int(datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').timestamp())
