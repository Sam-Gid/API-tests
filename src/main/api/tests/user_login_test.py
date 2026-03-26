import requests
import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self):

        login_user_request = LoginUserRequest(username='admin', password='123456')
        response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        )

        assert response.status_code == 200

        login_user_response = LoginUserResponse(**response.json())
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role

    def test_login_user(self):

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

        create_user_request = CreateUserRequest(username='Max26323', password='Pas!sw0rd', role='ROLE_USER')
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'authorization': f'Bearer {token}'
            }
        )

        assert create_user_response.status_code == 200

        login_user_request = LoginUserRequest(username='Max26323', password='Pas!sw0rd')
        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        )

        assert login_user_response.status_code == 200
        login_user_response = LoginUserResponse(**login_user_response.json())

        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == 'ROLE_USER'