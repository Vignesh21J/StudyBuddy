from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url

User = get_user_model()

# ✅ For linking existing users via email during social login
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Skip if user is already logged in
        if request.user.is_authenticated:
            return

        # Get email from social provider
        email = sociallogin.account.extra_data.get('email')

        if email:
            try:
                # Try to find an existing user with this email
                user = User.objects.get(email=email)
                sociallogin.user = user  # ✅ Link the existing user
            except User.DoesNotExist:
                pass  # Let Allauth create a new user if not found


    # Add this method
    def get_login_redirect_url(self, request):
        return resolve_url('update-user')


# ✅ For redirecting user after login
class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):

        # Redirect all users to update-users page
        return resolve_url('update-user')  # Make sure this name exists in urls.py

        # return resolve_url('/')
