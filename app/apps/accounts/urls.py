from django.urls import path

from apps.accounts.views import LandingView, UploadAccountsView, AccountDetailView, TransferFundsView

app_name = 'accounts'

urlpatterns = [
    path('', LandingView.as_view(), name='index'),
    path('upload', UploadAccountsView.as_view(), name='upload'),
    path('<int:pk>/', AccountDetailView.as_view(), name='account_details'),
    path('transfer/', TransferFundsView.as_view(), name='transfer'),
]
