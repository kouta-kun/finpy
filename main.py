import datetime
import itertools

from interpreter import query_request
from models import Book

book = Book()

while True:
    query_request(book)
