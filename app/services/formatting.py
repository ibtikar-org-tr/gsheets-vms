from datetime import datetime

# Date & Time
def strptime2(date_string):
    return strptime_format(date_string, ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%d/%m/%Y", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S.%f"])

def strptime_format(date_string, formats):
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    raise ValueError(f"time data '{date_string}' does not match any format in {formats}")
