import requests
import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self):

        login_user_request = LoginUserRequest(username='admin', password='123456')

        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get('token')

        create_user_request = CreateUserRequest(username='Max26971', password='Pas!sw0rd', role='ROLE_USER')

        response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'authorization': f'Bearer {token}'
            }
        )

        assert response.status_code == 200

        create_user_response = CreateUserResponse(**response.json())
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

    @pytest.mark.parametrize(
        'username, password',
        [
            ('Бдс', 'Pas!sw0rd'),
            ('ab', 'Pas!sw0rd'),
            ('ab!', 'Pas!sw0rd'),
            ('Maxx202', 'Pas!sw0rд'),
            ('Maxx203', 'Pas!sw0'),
            ('Maxx204', 'pas!sw0rd'),
            ('Maxx205', 'PAS!SW0RD'),
            ('Maxx206', 'passsw0rd'),
            ('Maxx207', 'pas!sword')
        ]
    )
    def test_create_user_invalid(self, username, password):

        login_user_request = LoginUserRequest(username='admin', password='123456')

        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        )

        token = login_admin_response.json().get('token')

        create_user_request = CreateUserRequest(username=username, password=password, role='ROLE_USER')

        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'authorization': f'Bearer {token}'
            }
        )

        assert create_user_response.status_code == 400

