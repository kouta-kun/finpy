import datetime
import decimal


class Book:
    def __init__(self):
        self.incomes = []
        self.outcomes = []
        self.alias = {"CB": "calculate_balance", "AI": "add_income", "AO": "add_outcome", "CI": "calculate_income",
                      "CO": "calculate_outcome"}

    def add_income(self, _type, desc, value, start, end):
        ic = Income(_type, desc, value, start, end)
        self.incomes.append(ic)
        return ic

    def add_outcome(self, _type, desc, value, start, end):
        oc = Outcome(_type, desc, value, start, end)
        self.outcomes.append(oc)
        return oc

    def incomes_for_day(self, day: datetime.date):
        return list(filter(lambda x: (x.start <= day < x.end) and (x.type == "DAY" or day.day == 1), self.incomes))

    def outcomes_for_day(self, day: datetime.date):
        return list(filter(lambda x: (x.start <= day < x.end) and (x.type == "DAY" or day.day == 1), self.outcomes))


class Income:
    def __init__(self, _type: str, desc: str, value: decimal.Decimal, start: datetime.date, end: datetime.date):
        self.type = _type
        self.desc = desc
        self.value = value
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.desc}: {self.value}/{self.type} {self.start} to {self.end}"


class Outcome:
    def __init__(self, _type: str, desc: str, value: decimal.Decimal, start: datetime.date, end: datetime.date):
        self.type = _type
        self.desc = desc
        self.value = value
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.desc}: {self.value}/{self.type} {self.start} to {self.end}"
