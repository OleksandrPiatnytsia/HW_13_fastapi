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

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data


def test_get_contact(client, contact, token):
    response = client.get(
        "/api/contacts",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == 1
    assert "id" in data[0]
    assert data[0].get("id") == 1



def test_repeat_create_contact(client, contact, token):
    response = client.post(
        "/api/contacts",
        json=contact,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    data = response.json()
    assert data["detail"] == f"Phone {contact.get('phone')} already exist!"


def test_delete_contact(client, contact, token):
    response = client.delete(
        f"/api/contacts/{contact.get('contact_id')}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_contact_not_existed(client, contact, token):
    response = client.delete(
        f"/api/contacts/{contact.get('contact_id')}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
