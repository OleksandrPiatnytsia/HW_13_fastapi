import unittest
from unittest.mock import Mock

from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.repository.contacts import create_contact, get_contacts, delete_contact, update_contact


class TestContactsRepository(unittest.TestCase):
    def setUp(self):
        self.session = Mock(spec=Session)
        self.user = User(
            id=1, email="test@gmail.com", password="qwerty!234", confirmed=True
        )
        self.contact = Contact(
            name="Borys",
            sur_name="Johnson",
            email="bj@gmail.com",
            phone="+380123456789",
            birthday="1988-01-01",
            user_id=self.user.id,
        )

    def test_create_contact(self):
        body = self.contact
        result = create_contact(body, self.user, self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.sur_name, body.sur_name)

    def test_get_contacts(self):
        expected_contacts = [self.contact]
        mock_contacts = Mock()
        mock_contacts.all.return_value = expected_contacts
        self.session.query.return_value.filter_by.return_value = mock_contacts
        result = get_contacts(self.user, self.session)
        self.assertEqual(result, expected_contacts)

    def test_update_contact(self):
        contact_id = 1
        contact_create = self.contact
        existing_contact = Contact(id=contact_id, user_id=self.user.id)

        session_mock = Mock(spec=Session)
        session_mock.query.return_value.get.return_value = existing_contact

        updated_contact = update_contact(self.contact
             , existing_contact, session_mock)

        self.assertEqual(updated_contact.name, contact_create.name)
        self.assertEqual(updated_contact.sur_name, contact_create.sur_name)
        self.assertEqual(updated_contact.email, contact_create.email)
        # self.assertEqual(updated_contact.phone, "+38012312312")
        self.assertEqual(updated_contact.phone, contact_create.phone)
        self.assertEqual(str(updated_contact.birthday), contact_create.birthday)

    def test_delete_contact(self):
        contact_id = 1
        contact = Contact(id=contact_id, user_id=self.user.id)

        session_mock = Mock(spec=Session)
        session_mock.query.return_value.get.return_value = contact

        result = delete_contact(contact, session_mock)

        self.assertEqual(result, contact)


if __name__ == "__main__":
    unittest.main()
