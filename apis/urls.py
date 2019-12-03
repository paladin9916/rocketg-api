from apis.api_view import auth, company, user
from django.urls import path

from apis.api_view.upload_image import ImageUploadView

urlpatterns = [
    path('auth/sign_in', auth.signIn),
    path('auth/sign_out', auth.signOut),

    path('user/users/check_email', auth.checkEmail),

    path('admin/companies', company.componyGetSave),
    path('admin/companies/<int:pk>', company.componyUpdate),

    path('admin/users', user.userGetSave),
    path('admin/users/<int:pk>', user.userDetailUpdate),
    path('admin/users/upload_avatar', ImageUploadView.as_view()),
    path('admin/users/reset_password', user.resetPassword),
]