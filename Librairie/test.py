from app.database import bookstore


for book in bookstore:
    for elmt in book:
        print(type(elmt))
        for key in elmt:
            print(      type(key))