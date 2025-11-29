from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
    
    # LOGIN
    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertRedirects(response, reverse('home'))

    def test_login_view_post_failure(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    # LOGOUT
    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

    # SIGNUP
    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')  # adjust if your template is different

    def test_signup_view_post(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(User.objects.filter(username='newuser').exists(), True)
        self.assertRedirects(response, reverse('login'))

    # PASSWORD RESET FLOW
    def test_password_reset_get(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')

    def test_password_reset_done_get(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_done.html')

    # PASSWORD CHANGE FLOW (login required)
    def test_password_change_requires_login(self):
        response = self.client.get(reverse('password_change'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('password_change')}")

    def test_password_change_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_password_change_post(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('password_change'), {
            'old_password': 'password123',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123'
        })
        self.assertRedirects(response, reverse('password_change_done'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))
