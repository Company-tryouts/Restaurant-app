from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail

@override_settings(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class SignUpTestCase(TestCase):

    def test_signup_page_loads(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_signup(self):
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_fails_with_mismatched_passwords(self):
        url = reverse('signup')
        data = {
            'username': 'newuser2',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  
        self.assertFalse(User.objects.filter(username='newuser2').exists())

@override_settings(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class LoginLogoutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='StrongPass123!')

    def test_login_page_loads(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'StrongPass123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue('_auth_user_id' in self.client.session)  

    def test_login_fails_with_wrong_credentials(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'WrongPass!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  
        self.assertFalse('_auth_user_id' in self.client.session)  

    def test_logout(self):
        self.client.login(username='testuser', password='StrongPass123!')
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  
        self.assertFalse('_auth_user_id' in self.client.session) 

@override_settings(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class PasswordChangeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='OldPass123!')
        self.client.login(username='testuser', password='OldPass123!')  # user must be logged in

    def test_password_change_page_loads(self):
        url = reverse('password_change')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # page loads

    def test_user_can_change_password(self):
        url = reverse('password_change')
        data = {
            'old_password': 'OldPass123!',
            'new_password1': 'NewPass123!',
            'new_password2': 'NewPass123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  

        
        self.client.logout()
        login_success = self.client.login(username='testuser', password='NewPass123!')
        self.assertTrue(login_success)  

    def test_password_change_fails_with_wrong_old_password(self):
        url = reverse('password_change')
        data = {
            'old_password': 'WrongOldPass!',
            'new_password1': 'NewPass123!',
            'new_password2': 'NewPass123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  

@override_settings(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='OldPass123!')

    def test_password_reset_page_loads(self):
        url = reverse('password_reset')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_sends_email(self):
        url = reverse('password_reset')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # redirect after submitting
        self.assertEqual(len(mail.outbox), 1)  # one email sent
        self.assertIn('test@example.com', mail.outbox[0].to)  # correct recipient
