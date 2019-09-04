import unittest
from unittest.mock import patch
import json
import copy

from src.app import app, prefix
from src.auth.services.auth_service import UserService
from src.auth.auth_exception import UserNotFoundException

mock_user = {
    "username": "realuser",
    "email": "realuser@real.com",
    "password": "password"
}

mock_login = {
    "username": "realuser",
    "password": "password"
}


class AuthControllerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('src.auth.services.auth_service.UserService.compare_password')
    def test_success_login(self, compare_password_mock):
        compare_password_mock.return_value = True
        with patch.object(UserService, 'get_user_by', return_value=copy.deepcopy(mock_user)):
            response = self.app.post(
                f'{prefix}/auth/login',
                data=json.dumps(mock_login),
                content_type='application/json'
            )
        assert response._status_code == 200

    def test_wrong_extra_fields_login(self):
        response = self.app.post(
            f'{prefix}/auth/login',
            data=json.dumps({
                "username": "realuser",
                "extra_field": "extra",
                "password": "password"
            }),
            content_type='application/json'
        )

        assert response._status_code == 400

    @patch('src.auth.services.auth_service.UserService.compare_password')
    def test_wrong_password_login(self, compare_password_mock):
        compare_password_mock.return_value = False
        with patch.object(UserService, 'get_user_by', return_value=copy.deepcopy(mock_user)):
            response = self.app.post(
                f'{prefix}/auth/login',
                data=json.dumps(mock_login),
                content_type='application/json'
            )
        assert response._status_code == 401

    def test_wrong_user_login(self):
        with patch.object(UserService, 'get_user_by', side_effect=UserNotFoundException("User not found")):
            response = self.app.post(
                f'{prefix}/auth/login',
                data=json.dumps(mock_login),
                content_type='application/json'
            )
        assert response._status_code == 401
