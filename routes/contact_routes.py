from fastapi import APIRouter, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.params import File
from fastapi.responses import Response, FileResponse
from authenticate import *
from database import SessionLocal
from routes.auth_routes import oauth2_scheme, get_current_user, get_db
from schemas import ContactCreate
from models import User as UserModel, Contact


contacts_router = APIRouter(
    prefix="/contacts",
    tags=["CONTACTS"]
)

IMAGEDIR = "images/"

@contacts_router.post('/', status_code=status.HTTP_201_CREATED)
async def add_new_contact(token: Annotated[str, Depends(oauth2_scheme)], contact: ContactCreate, user: Annotated[UserModel, Depends(get_current_user)], db: Session = Depends(get_db)):

    """
        ## Add new contact
       This endpoint allows user to add his new contact, but he has to be authenticated first.
       Also requires:
        - first_name: string
        - last_name: string
        - email: string
        - phone_number: string
    """

    new_contact = Contact(**contact.dict())
    new_contact.user = user

    db.add(new_contact)
    db.commit()

    return jsonable_encoder(contact)


@contacts_router.get("/user/all")
async def get_all_users_contacts(token: Annotated[str, Depends(oauth2_scheme)], user: Annotated[UserModel, Depends(get_current_user)]):

    """
        ## Get all user's contacts
        This endpoint return all the authenticated user's contacts
    """

    contacts = user.contacts
    return jsonable_encoder(contacts)


@contacts_router.get("/user/{contact_id}")
async def get_user_single_contact(contact_id: int, token: Annotated[str, Depends(oauth2_scheme)], user: Annotated[UserModel, Depends(get_current_user)]):

    """
        ## Get single user's contact
        This endpoint return single contact for authenticated user. You have to pass in the path the contact id from database.
    """

    contacts = user.contacts
    for c in contacts:
        if c.id == contact_id:
            return jsonable_encoder(c)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cant find the contact"
    )


@contacts_router.put("/update/{contact_id}")
async def update_contact(contact_id: int, contact: ContactCreate, token: Annotated[str, Depends(oauth2_scheme)], user: Annotated[UserModel, Depends(get_current_user)], db: Session = Depends(get_db)):

    """
        ## Update a contact
        This endpoint allows user to update his single contact.
    """

    contact_to_update = db.query(Contact).filter(Contact.id == contact_id).first()

    if contact_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cant find the contact"
        )

    contact_to_update.first_name = contact.first_name
    contact_to_update.last_name = contact.last_name
    contact_to_update.email = contact.email
    contact_to_update.phone_number = contact.phone_number
    contact_to_update.image = contact.image

    db.commit()

    return jsonable_encoder(contact_to_update)


@contacts_router.delete("/delete/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_by_id(contact_id: int, token: Annotated[str, Depends(oauth2_scheme)], user: Annotated[UserModel, Depends(get_current_user)], db: Session = Depends(get_db)):
    """
        ## Update a contact
        This endpoint allows user to delete his single contact.
    """

    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cant find the contact"
        )

    db.delete(contact)
    db.commit()

    return jsonable_encoder({"message": "Contact successfully deleted"})


@contacts_router.patch("/image/upload/{contact_id}")
async def upload_image_to_contact(contact_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db), file: UploadFile = File(...)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cant find the contact"
        )

    contents = await file.read()

    with open(f'{IMAGEDIR}{file.filename}', "wb") as f:
        f.write(contents)

    contact.image = f'{IMAGEDIR}{file.filename}'
    db.commit()

    return {"filename": file.filename}


@contacts_router.get("/show/{contact_id}")
async def show_contact_image(contact_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cant find the contact"
        )

    path = contact.image

    return FileResponse(path)