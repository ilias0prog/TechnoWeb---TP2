# Import necessary modules and classes
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from Librairie.app.schemas import books
import Librairie.app.services.books as service
from Librairie.Templates import *
from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="Librairie\Templates")

# Define the router for books
router = APIRouter(prefix="/books", tags=["Books"])

#################################################
@router.get("/")
async def name(request: Request):
    return templates.TemplateResponse("main.html",{"request":request, "name" : "Notre librairie"})

"""def show_home_page(request: Request):
    return templates.TemplateResponse(request, "home.html", context={"message": "Hello World"})"""

@router.get('/testing/{test}')
def test(test):
    return templates.TemplateResponse("main.html", {"request": Request, "test": test})
#################################################

# Define a GET route to retrieve all books
@router.get('/list')
def get_all_books():
    """
    Retrieve all books.

    Returns:
        JSONResponse: The response containing the list of all books.
    """
    books = service.get_all_books()
    return templates.TemplateResponse(
        "books.html",
        context={'request': request, 'tasks': book}    )


@router.post('/add{name}/{author}/{editor}')
def add_book(name: str, author: str, editor: str) -> JSONResponse:
    """
    Adds a new book to the library.

    Args:
        name (str): The name of the book.
        author (str): The author of the book.
        editor (str): The editor of the book.

    Returns:
        JSONResponse: The response containing the newly added book's data.

    Raises:
        ValueError: If any of the fields (name, author, editor) is None.
        HTTPException: If the new book data fails validation.
    """
    if (name is None or author is None or editor is None):
        raise ValueError("All fields must be filled in order to add a new book")
    new_book_data = {
        "id": str(uuid4()),
        "name": name,
        "author": author,
        "editor": editor,
    }     
    try:
        new_book = books.BaseModel(new_book_data)
          
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(),
        )
    service.save_book(new_book)  # Save the validated book
    return JSONResponse(new_book.model_dump())


@router.post('/update/{id}')
def update_book(id, name: str = None, author: str = None, editor: str = None) -> JSONResponse:
    """
    Update a book with the given ID.

    Args:
        id (int): The ID of the book to update.
        name (str, optional): The new name of the book. Defaults to None.
        author (str, optional): The new author of the book. Defaults to None.
        editor (str, optional): The new editor of the book. Defaults to None.

    Returns:
        JSONResponse: The response containing the message and updated book data.

    Raises:
        HTTPException: If the book with the given ID does not exist.
        ValueError: If no fields are provided to update or if any field is filled with spaces only.
    """
    if (name,author,editor) == (None,None,None):
        raise ValueError("At least one of the fields (name/author/editor) should be provided for updating.")
    try:
        book = service.get_book_by_id(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The book with the given id does not exist."
        )    
    if (name is None and author is None and editor is None):
        raise ValueError("At least one field must be provided to update.")
    service.check_input_validity(name,author,editor)  
    updated_fields = {
        "id" : id,
        "name": name,
        "author": author,
        "editor": editor
    }
    service.update_book_data(updated_fields)
    return JSONResponse(content={"message": "Book updated successfully", "data": updated_fields})


@router.post('/delete/{id}')
def delete_book(id : str) -> JSONResponse:
    """
    Deletes a book with the given id from the library.

    Args:
        id (str): The id of the book to be deleted.
    Raises:
        HTTPException: If the book with the given ID does not exist.

    Returns:
        JSONResponse: A JSON response indicating the success of the deletion operation.
    """
    try:
        book = service.get_book_by_id(id)
    except:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The book with the given id does not exist."
    )
    service.delete_book_data(id)
    return JSONResponse(content={"message": "Successfully deleted book", "data": book})
