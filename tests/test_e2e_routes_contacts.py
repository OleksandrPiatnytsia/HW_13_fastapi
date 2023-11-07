from unittest.mock import patch

from starlette import status


def test_get_unauthorized(client, contact):
    response = client.get("/api/contacts/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_contact(client, contact, token):

    response = client.post(
        "/api/contacts",
        json=contact,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Перевірка
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
