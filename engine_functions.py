import datetime
import decimal


def date_range(fromdate, todate):
    if type(fromdate) is not datetime.date:
        fromdate = datetime.date.fromisoformat(fromdate)
    delta = datetime.timedelta(1)
    if todate is None:
        while True:
            yield fromdate
            fromdate += delta
    if type(todate) is not datetime.date:
        todate = datetime.date.fromisoformat(todate)
    while fromdate < todate:
        yield fromdate
        fromdate += delta


def arg_range(variant_arg, delta_type, end_value, function, *args):
    if not (0 <= variant_arg < len(args)):
        raise ValueError("variant_arg must be in range [0, {})".format(len(args)))
    elif delta_type not in ("int", "date"):
        raise ValueError("Accepted deltas are: [int, date]")
    nargs = list(args)
    dynrange = {"int": range, "date": date_range}
    retvals = []
    for i in dynrange[delta_type](args[variant_arg], end_value):
        nargs[variant_arg] = i
        retvals.append((i, function(*nargs)))
    return retvals


def make_income(book, in_type, desc, value, f, t):
    if type(value) is not decimal.Decimal:
        value = decimal.Decimal(value)
    if value < 0:
        raise ValueError("Incomes must have positive value")
    if type(f) is not datetime.date:
        f = datetime.date.fromisoformat(f)
    if type(t) is not datetime.date:
        t = datetime.date.fromisoformat(t)
    return book.add_income(in_type, desc, value, f, t)


def make_outcome(book, out_type, desc, value, f, t):
    if type(value) is not decimal.Decimal:
        value = decimal.Decimal(value)
    if value > 0:
        raise ValueError("Outcomes must have negative value")
    if type(f) is not datetime.date:
        f = datetime.date.fromisoformat(f)
    if type(t) is not datetime.date:
        t = datetime.date.fromisoformat(t)
    return book.add_outcome(out_type, desc, value, f, t)


def calc_income(book, on_date):
    if type(on_date) is not datetime.date:
        on_date = datetime.date.fromisoformat(on_date)
    return sum(map(lambda x: x.value, book.incomes_for_day(on_date)))


def calc_outcome(book, on_date):
    if type(on_date) is not datetime.date:
        on_date = datetime.date.fromisoformat(on_date)
    return sum(map(lambda x: x.value, book.outcomes_for_day(on_date)))


def calc_balance(book, on_date):
    return calc_income(book, on_date) + calc_outcome(book, on_date)
