from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from fastapi_limiter.depends import RateLimiter
from pydantic import EmailStr
from sqlalchemy.orm import Session

import src.repository.contacts as res_contacts
from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactSchema, ContactSchemaResponse
from src.services.auth import auth_service

router = APIRouter(prefix='/api/contacts', tags=["contacts"])
birthday_router = APIRouter(prefix='/api/week_birthday', tags=["birthday"])


@router.get("/", response_model=List[ContactSchemaResponse], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def get_contacts(user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts for the current user.
        The function takes in two parameters:
            - user: A User object that represents the currently logged-in user. This is passed in by default from auth_service.get_current_user().
            - session: A Session object that represents an active database connection to be used for querying data from the database.

    :param user: User: Get the user from the auth_service
    :param session: Session: Pass the database session to the function
    :return: A list of contacts
    """
    return res_contacts.get_contacts(user=user, session=session)


@router.get("/{contact_id}", response_model=ContactSchemaResponse)
def get_contact_by_id(contact_id: int = Path(ge=1), user: User = Depends(auth_service.get_current_user),
                      session: Session = Depends(get_db)):
    """
    The get_contact_by_id function returns a contact by its id.
        The function takes in the following parameters:
            - contact_id: int = Path(ge=0)
                This is the id of the contact to be returned. It must be greater than or equal to 0.

    :param contact_id: int: Get the contact_id from the url
    :param user: User: Get the current user, and the session: session parameter is used to get a database
    :param session: Session: Get the database session
    :return: A single contact object
    """
    contact = res_contacts.get_contact_by_id(contact_id=contact_id, user=user, session=session)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.get("/name/{name}", response_model=ContactSchemaResponse)
def get_contact_by_name(name: str = Path(min_length=3, max_length=100),
                        user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_db)):
    """
    The get_contact_by_name function is used to retrieve a contact by name.
        The function takes in the following parameters:
            - name (str): The name of the contact to be retrieved.
            - user (User): A User object containing information about the current user, such as their ID and email address.  This is passed in via dependency injection from auth_service's get_current_user() function, which uses JWT authentication to verify that a valid token was provided with this request and then returns an object representing that user if it was successful or raises an exception otherwise.  If you're not familiar with dependency injection, check out

    :param name: str: Get the contact name from the request body
    :param max_length: Limit the length of the name parameter
    :param user: User: Get the current user from the auth_service
    :param session: Session: Access the database
    :return: A contact object, which is a pydantic model
    """
    contact = res_contacts.get_contact_by_name(name=name, user=user, session=session)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.get("/email/{email}", response_model=ContactSchemaResponse)
def get_contact_by_email(email: EmailStr, user: User = Depends(auth_service.get_current_user),
                         session: Session = Depends(get_db)):
    """
    The get_contact_by_email function is a GET request that returns the contact with the given email.
    If no such contact exists, it will return a 404 NOT FOUND error.

    :param email: EmailStr: Validate the email address
    :param user: User: Get the current user
    :param session: Session: Pass the database session to the function
    :return: A contact object, which is a dictionary
    """
    contact = res_contacts.get_contact_by_email(email=email, user=user, session=session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.get("/sur_name/{sur_name}", response_model=ContactSchemaResponse)
def get_contact_by_sur_name(sur_name: str = Path(min_length=3, max_length=100),
                            user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_db)):
    """
    The get_contact_by_sur_name function is used to retrieve a contact by their sur_name.
        The function takes in the sur_name of the contact as an argument and returns a JSON object containing all of the
        information about that particular contact.

    :param sur_name: str: Get the contact by sur_name
    :param max_length: Limit the length of a string
    :param user: User: Get the current user
    :param session: Session: Get the database session
    :return: A contact object, which is a pydantic model
    """
    contact = res_contacts.get_contact_by_sur_name(sur_name=sur_name, user=user, session=session)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.post("/", response_model=ContactSchemaResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))],
             status_code=status.HTTP_201_CREATED)
def create_contact(body: ContactSchema, user: User = Depends(auth_service.get_current_user),
                   session: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the request body
    :param user: User: Get the current user
    :param session: Session: Pass the database session to the function
    :return: A contact instance
    """
    if res_contacts.get_contact_by_phone(phone=body.phone, user=user, session=session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Phone {body.phone} already exist!"
        )

    return res_contacts.create_contact(body=body, user=user, session=session)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int = Path(ge=1), user: User = Depends(auth_service.get_current_user),
                   session: Session = Depends(get_db)):
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: int: Specify the id of the contact to be deleted
    :param user: User: Get the current user
    :param session: Session: Get the database session
    :return: A contact object
    """
    contact = res_contacts.get_contact_by_id(contact_id=contact_id, user=user, session=session)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )

    return res_contacts.delete_contact(contact=contact, session=session)


@router.patch("/{contact_id}", response_model=ContactSchemaResponse)
def update_contact(body: ContactSchema, contact_id: int = Path(ge=1),
                   user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.

    :param body: ContactSchema: Get the data from the request body
    :param contact_id: int: Get the contact_id from the path
    :param user: User: Get the current user from the auth_service
    :param session: Session: Get the database session
    :return: A contact object
    """
    contact = res_contacts.get_contact_by_id(contact_id=contact_id, user=user, session=session)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )

    contact_phone = res_contacts.get_contact_by_phone(phone=body.phone, session=session)

    if contact_phone and contact.id != contact_phone.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Another contact id={contact_phone.id} already had phone {body.phone}!"
        )

    return res_contacts.update_contact(body=body, contact=contact, session=session)


@birthday_router.get("/", response_model=List[ContactSchemaResponse])
def get_contact_week_birthdays(user: User = Depends(auth_service.get_current_user), session: Session = Depends(get_db)):
    """
    The get_contact_week_birthdays function returns a list of contacts that have birthdays in the next 7 days.
        The function takes two parameters: user and session.  User is the current logged-in user, and session is an SQLAlchemy Session object.

    :param user: User: Get the user from the auth_service
    :param session: Session: Pass the database session to the function
    :return: A list of contacts with their birthdays in the next 7 days
    """
    return res_contacts.get_contact_week_birthdays(user=user, session=session)
