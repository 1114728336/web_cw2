
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import db
from tests import tester


class Test_auth:
    def test_get_login(self, test_client):
        """
        Test GET request to the /login route to assert the login page is returned.
        """
        response = test_client.get("/login")

        assert response is not None
        assert response.status_code == 200
        assert b"Log In" in response.data

    def test_post_login(self, test_client):
        """
        Test POST request to the /login route to assert the user is successfully logged
        in.
        """
        username = "testusername"
        password = "Mockpassword123!"
        app_user = User(email="123456789@qq.com", username=username, password=generate_password_hash(password,
                                                                                                     method='Sha256'),)
        db.session.add(app_user)
        db.session.commit()

        response = test_client.post(
            "/login",
            data={"email": app_user.email, "password": password},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Home" in response.data

    def test_get_register(self, test_client):
        """
        Tests GET request to the /register route to assert the registration page is
        returned.
        """
        response = test_client.get("/sign-up")

        assert response is not None
        assert response.status_code == 200
        assert b"Home" in response.data

    def test_post_register(self, test_client):
        """
        Test POST request to the /register route to assert the user is successfully
        registered.
        """
        response = test_client.post(
            "/sign-up",
            data={
                "email": "123456789@qq.com",
                "username": "testusername",
                "password1": "Mockpassword123!",
                "password2": "Mockpassword123!",
            },
            follow_redirects=True,
        )
        assert response is not None
        assert response.status_code == 200

    def test_post_logout(self, test_client):
        """
        Test POST request to the /logout route to assert the user is successfully
        logged out.
        """
        username = "testusername"
        password = "Mockpassword123!"
        app_user = User(email="123456789@qq.com", username=username, password=generate_password_hash(password,
                                                                                                     method='Sha256'), )
        db.session.add(app_user)
        db.session.commit()
        tester.login(test_client, app_user.email, password)

        response = test_client.get("/logout", follow_redirects=True)

        assert response is not None
        assert response.status_code == 200
        assert b"Home" in response.data


