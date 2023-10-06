from datetime import datetime

from sqlalchemy import text

from src.database.models import Contact
from sqlalchemy.orm import Session
from src.database.models import User


def get_contacts(user: User, session: Session):
    contacts = session.query(Contact).filter_by(user=user).all()
    return contacts


def get_contact_by_id(contact_id, user: User, session: Session):
    contact = session.query(Contact).filter_by(id=contact_id, user=user).first()

    return contact


def get_contact_by_phone(phone, user: User, session: Session):
    return session.query(Contact).filter_by(phone=phone, user=user).first()


def get_contact_by_name(name, user: User, session: Session):
    return session.query(Contact).filter_by(name=name).first()


def get_contact_by_email(email, user: User, session: Session):
    return session.query(Contact).filter_by(email=email).first()


def get_contact_by_sur_name(sur_name, user: User, session: Session):
    return session.query(Contact).filter_by(sur_name=sur_name).first()


def create_contact(body, user: User, session: Session):
    contact = Contact()
    contact.phone = body.phone
    contact.email = body.email
    contact.name = body.name
    contact.sur_name = body.sur_name
    contact.birthday = body.birthday
    contact.user = user
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


def delete_contact(contact, session: Session):
    session.delete(contact)
    session.commit()

    return contact


def update_contact(body, contact, session):
    contact.phone = body.phone
    contact.email = body.email
    contact.name = body.name
    contact.sur_name = body.sur_name
    contact.birthday = body.birthday
    session.add(contact)
    session.commit()

    return contact


def get_contact_week_birthdays(user: User, session: Session):
    current_date = datetime.now()
    current_month = current_date.month

    contacts = session.execute(text("""
            SELECT *
            FROM contacts AS con
            WHERE user_id = :userid
                AND EXTRACT(WEEK FROM con.birthday) = EXTRACT(WEEK FROM :current_date)
              AND EXTRACT(MONTH FROM con.birthday) = :current_month;
            """), {"userid":user.id, "current_date": current_date, "current_month": current_month}).all()

    return contacts
