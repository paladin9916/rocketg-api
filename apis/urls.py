from apis.api_view import auth
from django.urls import path


urlpatterns = [
    path('auth/sign_in', auth.signIn),
    path('auth/sign_out', auth.signOut),

    path('user/users/check_email', auth.checkEmail),
]