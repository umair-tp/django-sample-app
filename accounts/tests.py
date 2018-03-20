from django.contrib.auth.models import User
from django.test import TestCase

class LogInTest(TestCase):
    def setUp(self):
        self.correct_credentials = {
            'username': 'demo',
            'password': '1$welcome'}
        User.objects.create_user(**self.correct_credentials)
        self.incorrect_credentials = {
            'username': 'demo1',
            'password': 'incorrect'}
        User.objects.create_user(**self.incorrect_credentials)

    def test_login_correct(self):
        # send login data
        response = self.client.post('/accounts/login/', self.correct_credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_incorrect(self):
        # send login data
        login = self.client.login(username=self.incorrect_credentials['username'], password='password')
        # Check login
        self.assertEqual(login, False)

    def test_login_url(self):
        # send login data
        response = self.client.post('/login/', self.correct_credentials, follow=True)
        # should return 404 ; because it's wrong url
        self.assertEqual(response.status_code, 404)