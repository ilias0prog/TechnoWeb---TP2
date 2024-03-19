from app.schemas.books import Book
from app.database import bookstore


def get_all_books() -> list[Book]:
    """
    Retrieves all books from the bookstore.

    Returns:
        list[Book]: A list of book objects.
    """
    books_data = bookstore["books"]
    books = [Book.model_validate(data) for data in books_data]
    return books

def check_input_validity(*args):
    """
    Checks the validity of input fields.

    Args:
        *args: Variable number of input fields to check.

    Raises:
        ValueError: If any of the input fields is empty or contains only spaces.

    Returns:
        None
    """
    for input in args:
        # Check if empty string :
        if len(input) < 1:
            raise ValueError("All the fields must be filled")
        # Check if only spacebars :
        i = input.strip()
        if len(i) < 1:
            raise ValueError("Please provide real title, author and editor")
    return
    
def get_book_by_id(book_id: str) -> Book | None:
    """
    Retrieves a book from the bookstore by its ID.

    Args:
        book_id (str): The ID of the book to retrieve.

    Returns:
        Book | None: The book object if found, None otherwise.
    """
    selected_book = [
        book for book in bookstore["books"]
        if book["id"] == book_id
    ]
    if len(selected_book) < 1:
        return None
    selected_book = Book.model_validate(selected_book[0])
    return selected_book

def save_book(new_book: Book) -> Book:
    """
    Saves a new book to the bookstore.

    Args:
        new_book (Book): The book object to save.

    Returns:
        Book: The saved book object.
    """
    book = {
        "id" : new_book.id,
        "name" : new_book.name,
        "author" : new_book.author,
        "editor" :  new_book.editor,
    }
    bookstore["books"].append(book)
    return new_book


def delete_book_data(book_id):
    """
    Deletes a book from the bookstore based on its ID.

    Args:
        book_id (str): The ID of the book to delete.

    Returns:
        None
    """
    for book in range(0,len(bookstore["books"])):
        if bookstore["books"][book]["id"]==book_id:
            bookstore["books"].pop(book)
            return True
    return None

def update_book_data(updated_fields: Book) -> Book | None:
    """
    Updates the fields of a book in the bookstore.

    Args:
        book_id (str): The ID of the book to update.
        updated_fields (dict): A dictionary containing the updated fields and their values.

    Returns:
        Book | None: The updated book object if found and updated successfully, None otherwise.
    """
    
    for i, book in enumerate(bookstore["books"]):
        if book["id"] == updated_fields.id :
            book["name"] = updated_fields.name 
            book["author"] = updated_fields.author
            book["editor"] = updated_fields.editor
            bookstore["books"][i] = book
            return book