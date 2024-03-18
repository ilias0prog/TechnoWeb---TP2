# Import necessary modules and classes
from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException, status, Request, Form
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import ValidationError
from app.schemas import books
import app.services.books as service
from Templates import *
from fastapi import Request
from fastapi.templating import Jinja2Templates
from typing import Optional

templates = Jinja2Templates(directory="Librairie\Templates")

# Define the router for books
router = APIRouter(prefix="/books", tags=["Books"])


# Define a GET route to retrieve all books
@router.get('/all')
def get_all_books(request: Request):
    """
    Retrieve all books.

    Returns:
        JSONResponse: The response containing the list of all books.
    """
    books = service.get_all_books()
    return templates.TemplateResponse(
        "all_books.html",
        context={'request': request, 'books': books}
    )

@router.get('/new')
def ask_to_create_new_book(request: Request):
    return templates.TemplateResponse(
        "new_book.html",
        context={'request': request}
    )

@router.post('/new')
def add_book(name: Annotated[str, Form()], author: Annotated[str, Form()], editor: Annotated[str, Form()]) :
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
        new_book = books.Book(**new_book_data)
          
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(),
        )
    service.save_book(new_book)  # Save the validated book
    return RedirectResponse(url="/books/all", status_code=302)

@router.get('/update/{id}', response_class=HTMLResponse)
def update_book_form(request: Request, id: str):
    try:
        book = service.get_book_by_id(id)
        return templates.TemplateResponse("update_book.html", context={"request": request, "book": book})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The book with the given id does not exist."
        )

# Route pour traiter la soumission du formulaire de mise à jour du livre
@router.put('/update/{id}', response_class=HTMLResponse)
def update_book(id: str , name: Optional[str] = Form(None), author: Optional[str] = Form(None), editor: Optional[str] = Form(None)):
    try:
        book = service.get_book_by_id(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The book with the given id does not exist."
        )

    if name is None and author is None and editor is None:
        raise ValueError("At least one of the fields (name/author/editor) should be provided for updating.")

    updated_fields = {}

    if name is not None:
        updated_fields["name"] = name
    if author is not None:
        updated_fields["author"] = author
    if editor is not None:
        updated_fields["editor"] = editor

    service.update_book_data(id, updated_fields)

    return RedirectResponse(url="/books/all")

@router.get('/delete/{id}')
def ask_to_delete_book(request : Request):
    return templates.TemplateResponse(
        "delete_book.html",
        context={"request": request}
    )

@router.post('/delete/{id}', response_class=HTMLResponse)
def delete_book(id: str ):
    """
    Deletes a book with the given id from the library.

    Args:
        id (str): The id of the book to be deleted.
    Raises:
        HTTPException: If the book with the given ID does not exist.

    Returns:
        HTMLResponse: A HTML response indicating the success of the deletion operation.
    """
    try:
        book = service.get_book_by_id(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The book with the given id does not exist."
        )
    service.delete_book_data(id)
    return RedirectResponse(url="/books/all")