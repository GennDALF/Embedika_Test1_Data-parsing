
import datetime as dt
import locale as lc
import json
import csv

lc.setlocale(lc.LC_ALL, 'ru_RU.UTF-8')

table = {}
# text and number matching of months
months = {
    "янв": 1,
    "фев": 2,
    "мар": 3,
    "апр": 4,
    "май": 5,
    "июн": 6,
    "июл": 7,
    "авг": 8,
    "сен": 9,
    "окт": 10,
    "ноя": 11,
    "дек": 12
}
months_reverse = {v: k for k, v in months.items()}
# reading file with data
with open("data-20200316T1222.csv", newline='', encoding="windows-1251") as file:
    reader = csv.reader(file)
    for row in reader:
        # skipping header (and other possible comment or text rows)
        if row[0][0] not in "1234567890":
            continue
        # conversion to <date> object that refer to monitoring range beginning
        # it is also will be the key of our dictionary
        date = dt.date(int("20" + row[0].split('.')[2]),
                       months[row[0].split('.')[1]],
                       int(row[0].split('.')[0]))
        if date not in table.keys():
            # only unique monitoring ranges are allowed
            table[date] = float(row[2].replace(',', '.'))


# auxiliary function adjusting input date to monitoring ranges
def set_date(date, end=False, first_day=15):
    # we need to catch random date into one of our monitoring ranges
    if not end:
        # and here we adjust it to the standard date of monitoring range beginning
        if date.day >= first_day:
            date = dt.date(date.year, date.month, first_day)
        else:
            date -= dt.timedelta(days=28)
            date = dt.date(date.year, date.month, first_day)
        return date
    else:
        # or we could use to find the date of monitoring range ending
        if date.day >= first_day:
            date = dt.date(date.year, date.month + 1, first_day - 1)
        else:
            date = dt.date(date.year, date.month, first_day - 1)
        return date


# auxiliary function searching all adjusted dates within input range
def set_date_range(date_range_string):
    date1 = dt.date(int(date_range_string.split()[2]),
                    int(date_range_string.split()[1]),
                    int(date_range_string.split()[0]))
    date2 = dt.date(int(date_range_string.split()[6]),
                    int(date_range_string.split()[5]),
                    int(date_range_string.split()[4]))

    if date1 < date2 < dt.date.today():
        # in case if one of the dates is out of our database's range
        # we'll start or end count with first or last known value
        if date1 < dt.date(2013, 3, 15):
            # next version should take left and right borders of database
            # from database - and put it here
            date1 = dt.date(2013, 3, 15)
        elif date1 > dt.date(2020, 3, 14):
            # out of our database
            raise IndexError
        else:
            # caught you!
            date1 = set_date(date1)
        if date2 > dt.date(2020, 3, 15):
            date2 = dt.date(2020, 3, 15)
        elif date2 < dt.date(2013, 3, 15):
            # out of our database
            raise IndexError
        else:
            # caught you!
            date2 = set_date(date2)
    else:
        # this is not forecasting, check your dates
        # special thanks if you entered first date that is later than second
        raise ValueError

    # adjusted to monitoring ranges left border
    dates = [date1]
    for i in range(1, (date2 - date1).days // 30):
        # adjusted to monitoring ranges inner dates
        dates.append(set_date(date1 + dt.timedelta(days=31 * i)))
    # adjusted to monitoring ranges right border
    dates.append(date2)
    return dates


# first method
def get_price(date_string):
    # we assume that string format is "DD MM YYYY"
    global table
    try:
        # converting input to <date> object
        search_date = dt.date(int(date_string.split()[2]),
                              int(date_string.split()[1]),
                              int(date_string.split()[0]))
        if dt.date(2013, 3, 15) <= search_date <= dt.date(2020, 3, 14):
            return table[set_date(search_date)]
        else:
            # we really haven't this data, call get_stats() to clarify dates
            return "...some warning about missing data for input date..."
    except Exception as e:
        # just in case
        return "...RTFM...\nError: <{}>".format(e.args[0])


# second method
def get_average_price(date_range_string):
    # we assume that string format is "DD MM YYYY - DD MM YYYY"
    global table
    try:
        prices = [table[i] for i in set_date_range(date_range_string)]
        average = (sum(prices) / len(prices))
        return round(average, 1)
    except IndexError:
        # we really haven't this data, call get_stats() to clarify dates
        return "...some warning about missing data for input date..."
    except ValueError:
        # try harder
        return "...some warning about wrong input..."
    except Exception as e:
        # just in case
        return "...RTFM...\nError: <{}>".format(e.args[0])


# third method
def get_min_max_prices(date_range_string):
    # we assume that string format is "DD MM YYYY - DD MM YYYY"
    global table
    try:
        prices = [table[i] for i in set_date_range(date_range_string)]
        min_max = [{"min": min(prices), "max": max(prices)}]
        return json.dumps(min_max, indent=2)
    except Exception as e:
        # just in case
        return "...RTFM...\nError: <{}>".format(e.args[0])


# fourth method
def get_stats():
    global table
    try:
        stats = [{
            "all entries": len(table),
            "start of monitoring": min(table.keys()).strftime("%d %B %Y"),
            "end of monitoring": set_date(max(table.keys()), end=True).strftime("%d %B %Y"),
            "global min price": [min(table.values()),
                                 "{0:%d %B %Y} – {1:%d %B %Y}".format(min(table, key=table.get),
                                                                      set_date(min(table, key=table.get), end=True))
                                 ],
            "global max price": [max(table.values()),
                                 "{0:%d %B %Y} – {1:%d %B %Y}".format(max(table, key=table.get),
                                                                      set_date(max(table, key=table.get), end=True))
                                 ]
            # why would I even did all that formatting?
        }]
        return json.dumps(stats, indent=2, ensure_ascii=False)
    except Exception as e:
        # just in case
        return "...RTFM...\nError: <{}>".format(e.args[0])
