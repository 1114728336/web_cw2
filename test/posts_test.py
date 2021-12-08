from tests import tester
from website import db
from website.models import User, Post
from werkzeug.security import generate_password_hash
import datetime

class TestPost:
    def test_post_create_post(self, test_client):
        """
        Test POST request to the /community/_/post/create route to assert the post is
        created successfully.
        """
        username = "testusername"
        password = "Mockpassword123!"
        app_user = User(email="123456789@qq.com", username=username, password=generate_password_hash(password,
                                                                                                     method='Sha256'), )
        db.session.add(app_user)
        db.session.commit()
        tester.login(test_client, app_user.username, password)

        response = test_client.post(
            "/create-post",
            data={"text": "mockposttitle"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Home" in response.data

    def test_post_delete_post(self, test_client):
        """
        Test POST request to the /community/_/post/_/delete route to assert the post is
        deleted successfully.
        """
        username = "testusername"
        password = "Mockpassword123!"
        app_user = User(email="123456789@qq.com", username=username, password=generate_password_hash(password,
                                                                                                     method='Sha256'), )
        db.session.add(app_user)
        db.session.commit()
        tester.login(test_client, app_user.email, password)

        response = test_client.get(
            "/delete-post/<post.id>",
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Home" in response.data

    def test_get_comment(self, test_client):
        """
        Test GET request to the / route to assert posts from the users joined
        communities are displayed.
        """
        username = "testusername"
        password = "Mockpassword123!"
        app_user = User(email="123456789@qq.com", username=username, password=generate_password_hash(password,
                                                                                                     method='Sha256'), )
        db.session.add(app_user)
        db.session.commit()
        tester.login(test_client, app_user.username, password)

        response = test_client.post(
            "/create-comment/<post_id>",
            data={"text": "mockposttitle"},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Home" in response.data

    def test_delete_comment(self, test_client):
        """
        Test GET request to the / route to assert posts from the users joined
        communities are displayed.
        """
        username = "testusername"
        password = "Mockpassword123!"
        app_user = User(email="123456789@qq.com", username=username, password=generate_password_hash(password,
                                                                                                     method='Sha256'), )
        db.session.add(app_user)
        db.session.commit()
        tester.login(test_client, app_user.username, password)

        response = test_client.get(
            "/delete-post/<post.id>",
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Home" in response.data
