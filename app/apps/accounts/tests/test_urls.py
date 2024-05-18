from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.accounts.views import LandingView, UploadAccountsView, AccountDetailView, TransferFundsView


class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('accounts:index')
        self.assertEqual(resolve(url).func.view_class, LandingView)

    def test_upload_url_resolves(self):
        url = reverse('accounts:upload')
        self.assertEqual(resolve(url).func.view_class, UploadAccountsView)

    def test_account_details_url_resolves(self):
        url = reverse('accounts:account_details', args=[1])  # Assuming pk=1
        self.assertEqual(resolve(url).func.view_class, AccountDetailView)

    def test_transfer_url_resolves(self):
        url = reverse('accounts:transfer')
        self.assertEqual(resolve(url).func.view_class, TransferFundsView)
