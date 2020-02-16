from apis.api_view import auth, company, user, expense, industry, country, report
from django.urls import path

from apis.api_view.upload_image import ImageUploadView
from apis.api_view.upload_attachment import AttachmentUploadView

urlpatterns = [
    path('auth/sign_in', auth.signIn),
    path('auth/sign_out', auth.signOut),

    path('user/users/check_email', auth.checkEmail),

    path('admin/companies', company.componyGetSave),
    path('admin/companies/<int:pk>', company.componyUpdate),
    path('admin/companies/<int:pk>/special_privilege', company.specialUsers),
    path('admin/companies/<int:pk>/special_privilege/<slug:privilege>', company.specialUser),

    path('admin/users', user.userGetSave),
    path('admin/users/<int:pk>', user.userDetailUpdate),
    path('admin/users/upload_avatar', ImageUploadView.as_view()),
    path('admin/users/reset_password', user.resetPassword),

    path('admin/industries', industry.industryGet),
    path('admin/countries', country.countryGet),

    path('user/expenses_month', expense.expenseMonthList),
    path('user/expenses_month/<int:month>', expense.expenseByMonth),
    path('user/expenses', expense.expenseSave),
    path('user/expenses/count', expense.expenseCount),
    path('user/expenses/<int:pk>', expense.expenseUpdate),
    path('user/expenses/change_status', expense.expenseChangeStatus),
    path('user/expenses/upload_file', AttachmentUploadView.as_view()),

    path('user/reports', report.reports),
    path('user/reports/<int:pk>', report.deleteReport),
    path('user/reports/<int:report>/expenses', expense.expensesInReport),
]