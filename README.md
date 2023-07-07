## CONTACT BOOK API
This the contacts book RESTful API built for example with FastAPI, SQLAlchemy and SQLite database

## INSTALLATION
- Install Python
- Clone the project: ``` git clone https://github.com/karolk53/contacts_book.git```
- Create your virtualenv with `Pipenv` or `virtualenv` and activate it.
- Install the requirements: ``` pip install -r requirements.txt ```
- Finally, run the API ``` uvicorn main:app ```

## ROUTES
| METHOD   | ROUTE                                | FUNCTIONALITY               | ACCESS      |
|----------|--------------------------------------|-----------------------------|-------------|
| *POST*   | ```/auth/signup/```                  | _Register new user_         | _All users_ |
| *POST*   | ```/auth/token/```                   | _Get user token_            | _All users_ |
| *GET*    | ```/auth/users/me/```                | _Get user data_             | _All users_ |
| *POST*   | ```/contacts/```                     | _Create new contact_        | _All users_ |
| *GET*    | ```/contacts/user/all/```            | _Get all users contacts_    | _All users_ |
| *GET*    | ```/contacts/user/{contact_id}/```   | _Get single users contact_  | _All users_ |
| *PUT*    | ```/contacts/update/{contact_id}/``` | _Update an contact_         | _All users_ |
| *DELETE* | ```/contact/delete/{contact_id}/```  | _Delete an contact_         | _All users_ |