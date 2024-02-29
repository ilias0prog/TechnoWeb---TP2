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
    bookstore["books"].append(new_book)
    return new_book


def delete_book_data(book_id):
    """
    Deletes a book from the bookstore based on its ID.

    Args:
        book_id (str): The ID of the book to delete.

    Returns:
        None
    """
    bookstore["books"] = [
        book for book in bookstore["books"]
        if not (book["id"] == book_id)
    ]


def update_book_data(book_id, updated_fields: dict) -> Book | None:
    """
    Updates the fields of a book in the bookstore.

    Args:
        book_id (str): The ID of the book to update.
        updated_fields (dict): A dictionary containing the updated fields and their values.

    Returns:
        Book | None: The updated book object if found and updated successfully, None otherwise.
    """
    target_book = get_book_by_id(book_id)
    
    if target_book is not None:
        for key in updated_fields.keys():
            target_book[key] = updated_fields[key]
        
        book_index = bookstore["books"].index(target_book)
        bookstore["books"][book_index] = target_book
        
        return Book.model_validate(target_book)
    else:
        return None