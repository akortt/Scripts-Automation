from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create application instance
app = FastAPI()

class Book(BaseModel): # Book Model using Pydantic's BaseModel for input validation and serialization
    title: str
    author: str
    price: float
    description: str | None = None
    # The Title, Author and Price are required fields
    # We are using the colon (:) as a Type Hint - telling Pydantic that the attribute must be a str
    # We would not use an equals (=) as this would be a standard variable assign (creating variable title, and setting value to literal Python str class object)
    # This would break Pydantic Input Validation 
    # Description syntax of str | None = None means it can be a string or absent

class BookResponse(Book): # Inheritance - All fields from Book and adds an ID field (this is what your API returns on the client)
    id: int

# In-Memory 'DataBase'
books: list[dict] = [ # this is legit a list of dictionaries acting as database. 
    {
        'id': 1,
        'title': "1984",
        'author': "George Orwell",
        'price': 9.99,
        'description': "Dystopian novel about totalitarianism",
    },
    {
        "id": 2,
        'title': "BBW",
        'author': 'Charlie Kirk',
        'price': 19.99,
        'description': "I have a dream.",
    },
]

next_id = 3 

# Defining a GET endpoint at root URL "/"
@app.get("/") # a decorator that tells FastAPI to run function below whenever someone visits root URL with GET requests
def root():
    return{
        'message':'Welcome to the Bookstore API'
    } # NOTE: as we are turning a Python dictionary, FASTAPI will automatically convert this to a JSON response

@app.get("/books", response_model=list[BookResponse]) 
#response_model tells FastAPI to validate response as a list of BookResponse objects

# Query Parameters 
# FastAPI treats function parameters which are not path and are not Pydantic models ... as (below)
# As query parameters automatically - if you add a parameter with a default value of None, it becomes optional
# E.g. Parameter like author: str | None = None becomes an optional query parameter that users can pass into the query
# E.g. /books?author=Orwell in the URL (functional parameter of Author)

def get_books(
    author: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
):
    results = books

    if author:
        results = [b for b in results if author.lower() in b['author'].lower()] 
        # We are using lower() to ensure case-sensitive substring matching
        # Keep this (b) for each item (b) in results if condition is true (author.lower = b[line in result of author])
        
        # instead of writing:
        # filtered_results = [] # where we first initialise an empty list 
        # for b in results: # go through each line in results [database]
        #     if author.lower() in b['author'].lower(): #check whether author provided in query.lower = lower in database
        #         filtered_results.append(b) # we append to the empty list
        # results = filtered_results # get rid of anything in results and change all values to the filtered list 

    if min_price is not None:
        results = [b for b in results if b['price'] >= min_price]
        # Use List comprehension for filtering

    if max_price is not None:
        results = [b for b in results if b['price'] <= max_price]

    return results #returns the books list directly and FastAPI converts this to JSON automatically. 


@app.get("/books/{book_id}", response_model=BookResponse) 
# The {book_id} is a path parameter which FastAPI extracts from the URL and passes it into the function as an argument


def get_book(book_id: int): #we use a Type Hint to ensure FastAPI validates value is an integer, if not then FastAPI automatically returns an error.
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not Found. Please try another Book ID.")

# Defining a POST endpoint to add new books to the catalog.
# Endpoint will accept that data and assign unique ID (@ next_id)
@app.post("/books", response_model=BookResponse)
def create_book(book: Book):
    # We set next_id global so we can modify it inside the function.
    global next_id 

    #book: Book tells FastAPI to expect JSON body in request and validate it against the Book Model.
    # If validation passes, FastAPI will create a Book instance and pass it to the function as 'book' argument.

    new_book = {
        'id': next_id,
        **book.model_dump() # This method converts Pydantic's model into a dictionary - With the '**' unpacking it and merging it with the id key
    } 

    books.append(new_book)
    next_id += 1
    return new_book


# Creating a PUT endpoint to update books
# We will need both a path parameter (which book to update) and a request body (for new data)
# FastAPI can automatically figure out which parameter comes from the URL and the JSON body.

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: Book): # book_id: int comes from URL path, and book:Book comes from JSON request (FastAPI matches them and treats Pydantic model as request bodies automatically)
    for i, existing_book in enumerate(books): #enumerate() through books in database gives both index and position value as you loop through. 
        if existing_book['id'] == book_id:
            books[i] = { # we are replacing old book data with new updated data.
                'id': book_id,
                **book.model_dump()
            } 
            return books[i]
    raise HTTPException(status_code=404, detail=f'Book not found using {book_id}')

@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    # Loop through to find matching
    for i, existing_book in enumerate(books):
        if existing_book['id'] == book_id:
            books.pop(i)
            return {
                'message': "Book has been deleted successfully"
            }
    raise HTTPException(status_code=404, detail=f"Book ID {book_id} was not found.")