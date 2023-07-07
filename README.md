## CONTACT BOOK API
This the contacts book RESTful API built for example with FastAPI, SQLAlchemy and SQLite database

## INSTALLATION
- Install Python
- Clone the project: ``` git clone https://github.com/karolk53/contacts_book.git```
- Go to the project directory 
- Create your virtualenv for example with ```python -m venv venv``` and activate it.
- Install the requirements: ``` pip install -r requirements.txt ```
- Copy environment variables from .env.example ``` copy .env.example .env ```
- Set variables in the .env file: KEY could be generated with ```ssh-keygen -t rsa -b 4096 -m PEM -f private.key```, ALGORITHM could be HS256
- Finally, run the API ``` uvicorn main:app ```

## ROUTES
| METHOD   | ROUTE                                     | FUNCTIONALITY              | ACCESS      | AUTHORIZED |
|----------|-------------------------------------------|----------------------------|-------------|------------|
| *GET*    | ``` / ```                                 | _Hello endpoint_           | _All users_ | _NO_       |
| *POST*   | ```/auth/signup/```                       | _Register new user_        | _All users_ | _NO_       |
| *POST*   | ```/auth/token/```                        | _Get user token_           | _All users_ | _NO_       |
| *GET*    | ```/auth/users/me/```                     | _Get user data_            | _All users_ | _YES_      |
| *GET*    | ```/auth/users/all/```                    | _Get list of users_        | _Superuser_ | _YES_      |
| *POST*   | ```/contacts/```                          | _Create new contact_       | _All users_ | _YES_      |
| *GET*    | ```/contacts/user/all/```                 | _Get all users contacts_   | _All users_ | _YES_      |
| *GET*    | ```/contacts/user/{contact_id}/```        | _Get single users contact_ | _All users_ | _YES_      |
| *PUT*    | ```/contacts/update/{contact_id}/```      | _Update an contact_        | _All users_ | _YES_      |
| *DELETE* | ```/contact/delete/{contact_id}/```       | _Delete an contact_        | _All users_ | _YES_      |
| *PATCH*  | ```/contact/image/upload/{contact_id}/``` | _Upload contact's image_   | _All users_ | _YES_      |
| *GET*    | ```/contact/image/show/{contact_id}/```   | _Get contact's image_      | _All users_ | _YES_      |