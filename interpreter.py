import decimal
import itertools
import sqlite3

from engine_functions import *

sqlite3.register_adapter(decimal.Decimal, str)
sqlite3.register_converter("decimal", decimal.Decimal)


def tokenize(cmd_in: str):
    if "#" in cmd_in:
        cmd, args = cmd_in.split('#')
        args = [i.strip() for i in args.split(",")]
        return [cmd, args]
    elif "," not in cmd_in:
        return [cmd_in, []]
    else:
        return [None, []]


def save_book(book, file="book.db"):
    db = sqlite3.connect(file)
    c = db.cursor()
    c.execute("create table if not exists income(type text, description text, value decimal, start date, end date);")
    c.execute("create table if not exists outcome(type text, description text, value decimal, start date, end date);")
    c.execute("create table if not exists aliases(link text, target text);")
    c.execute("delete from income;")
    c.execute("delete from outcome;")
    c.execute("delete from aliases;")
    incomes = [(i.type, i.desc, i.value, i.start, i.end) for i in book.incomes]
    c.executemany("insert into income values(?,?,?,?,?)", incomes)
    outcomes = [(i.type, i.desc, i.value, i.start, i.end) for i in book.outcomes]
    c.executemany("insert into outcome values(?,?,?,?,?)", outcomes)
    aliases = [(k, book.alias[k]) for k in book.alias.keys()]
    c.executemany("insert into aliases values(?,?)", aliases)
    db.commit()
    db.close()


def load_book(book, file="book.db"):
    db = sqlite3.connect(file)
    c = db.cursor()
    book.incomes = []
    book.outcomes = []
    ic = c.execute("select * from income;")
    for i in ic:
        make_income(book, *i)
    oc = c.execute("select * from outcome;")
    for o in oc:
        make_outcome(book, *o)
    aq = c.execute("select * from aliases;")
    for a in aq:
        book.alias[a[0]] = a[1]
    c.close()


def query_request(book):
    line = str(input(">> "))
    offns = {"sum_range": lambda x: sum(x[1]), "print_range": lambda x: [str(i) for i in list(zip(*x))],
             "print_tuple": lambda x: [tuple(str(v) for v in i) for i in x],
             "avg_range": lambda x: (float(sum(x[1])) / float(len(x[1])))}
    tabs = {"income": lambda: book.incomes, "outcome": lambda: book.outcomes}
    if "~" in line:
        link, target = line.split("~")
        book.alias[link] = target
        print(f"{link} now points to {target}")
    elif line == "aliaslist":
        print(book.alias)
    elif "→/" in line:
        srctabs, jc = line.split("→/")
        srctabs = srctabs.split(",")
        if "|" in jc:
            jc, of = jc.split("|")
            of = offns[of]
        else:
            of = offns["print_tuple"]
        jc = eval(jc, {}, {})
        srctabs = [tabs[i]() for i in srctabs]
        srcqs = list(itertools.product(*srctabs))
        qs = list(filter(jc, srcqs))
        print(of(qs))
    elif "·" in line:
        query, tendency = line.split("·")
        if "|" in tendency:
            tendency, of = tendency.split("|")
            of = offns[of]
        else:
            of = offns["sum_range"]
        arg, tendency = tendency.split("→")
        tendency, argtype = tendency[1:], tendency[0]
        argtype = {"i": "int", "d": "date"}[argtype]
        query = tokenize(query)
        if query[0] in book.alias.keys():
            query = (book.alias[query[0]], query[1])
        query = (funcs[query[0]], query[1])
        try:
            print(of(list(zip(*arg_range(int(arg) + 1, argtype, tendency, query[0], book, *query[1])))))
        except ValueError as e:
            print(e)
            if "isoformat" in str(e):
                print("Dates must be in isoformat (YYYY-MM-DD)")
        except KeyError as e:
            print("No alias or function for {}".format(query[0]))
    else:
        query = tokenize(line)
        if query[0] in book.alias.keys():
            query = ((book.alias[query[0]], query[0]), query[1])
        else:
            query = ((query[0], query[0]), query[1])
        query = ((funcs[query[0][0]], query[0][1]), query[1])
        call_function(book, query)


def call_function(book, query):
    try:
        result = query[0][0](book, *query[1])
        call_string = "{}#{}".format(query[0][1], ','.join(query[1]))
        print("{}: {} ({})".format(call_string, result, str(type(result))))
    except ValueError as e:
        print(e)
        if "isoformat" in str(e):
            print("Dates must be in isoformat (YYYY-MM-DD)")
    except KeyError as e:
        print("No alias or function for {}".format(query[0]))


funcs = {'add_income': make_income, 'add_outcome': make_outcome, 'calculate_income': calc_income,
         'calculate_outcome': calc_outcome, 'calculate_balance': calc_balance, 'save': save_book,
         'restore': load_book}
