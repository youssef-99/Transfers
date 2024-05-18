from django.contrib.messages import get_messages
from django.test import Client

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User  # Import the User model if needed

from apps.accounts.forms import TransferForm
from apps.accounts.models import Account  # Import the Account model
from apps.accounts.views import UploadAccountsView
import pandas as pd
from unittest.mock import patch


class LandingViewTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create(uuid="uuid1", name="Account 1", balance=100.0)
        self.account2 = Account.objects.create(uuid="uuid2", name="Account 2", balance=200.0)
        self.client = Client()

    def test_get_accounts(self):
        response = self.client.get(reverse('accounts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.account1.name)
        self.assertContains(response, self.account2.name)


class UploadAccountsViewTest(TestCase):
    def setUp(self):
        self.csv_data = b"ID,Name,Balance\n1,Account1,100.0\n2,Account2,200.0\n"
        self.invalid_csv_data = b"Ias,Name,Balance\n1,Account1,100.0\n2,Account2,200.0\n"
        self.valid_csv_file = SimpleUploadedFile("accounts.csv", self.csv_data, content_type="text/csv")
        self.invalid_csv_file = SimpleUploadedFile("accounts.csv", self.invalid_csv_data, content_type="text/csv")
        self.request = RequestFactory().post(reverse('accounts:upload'), {'accountFile': self.valid_csv_file})

    def test_valid_csv_upload(self):
        with patch('apps.accounts.views.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame(
                {'ID': [1, 2], 'Name': ['Account1', 'Account2'], 'Balance': [100.0, 200.0]})
            UploadAccountsView.as_view()(self.request)

        self.assertEqual(Account.objects.count(), 2)

    def test_it_redirects_on_success(self):
        with patch('apps.accounts.views.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame(
                {'ID': [1, 2], 'Name': ['Account1', 'Account2'], 'Balance': [100.0, 200.0]})
            response = UploadAccountsView.as_view()(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:index'))

    def test_invalid_csv_upload(self):
        request = RequestFactory().post(reverse('accounts:upload'), {'accountFile': 'invalid_file'})
        response = UploadAccountsView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_csv_format(self):
        request = RequestFactory().post(reverse('accounts:upload'), {'accountFile': self.invalid_csv_file})
        response = UploadAccountsView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_file_extension(self):
        invalid_file = SimpleUploadedFile("accounts.txt", b"ID,Name,Balance\n1,Account1,100.0\n2,Account2,200.0\n",
                                          content_type="text/plain")
        request = RequestFactory().post(reverse('accounts:upload'), {'accountFile': invalid_file})

        response = UploadAccountsView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("File must be a CSV file.", response.content.decode())

    def test_exception_handling(self):
        request = RequestFactory().post(reverse('accounts:upload'), {'accountFile': self.valid_csv_file})
        with patch('apps.accounts.views.pd.read_csv') as mock_read_csv:
            mock_read_csv.side_effect = Exception("Test exception")
            response = UploadAccountsView.as_view()(request)
        self.assertEqual(response.status_code, 400)


class AccountDetailViewTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(uuid='123456', name='Test Account', balance=1000.00)

    def test_account_detail_view(self):
        url = reverse('accounts:account_details', kwargs={'pk': self.account.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.account.name)
        self.assertContains(response, str(self.account.balance))


class TransferFundsViewTest(TestCase):
    def setUp(self):
        self.sender = Account.objects.create(uuid='123', name='Sender', balance=1000.00)
        self.recipient = Account.objects.create(uuid='456', name='Recipient', balance=2000.00)
        self.data = {'sender': self.sender.id, 'recipient': self.recipient.id, 'amount': 500.00}

    def test_get_transfer_form(self):
        response = self.client.get(reverse('accounts:transfer'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TransferForm)

    def test_post_transfer_funds(self):
        response = self.client.post(reverse('accounts:transfer'), self.data)
        self.assertRedirects(response, reverse('accounts:transfer'))
        self.sender.refresh_from_db()
        self.recipient.refresh_from_db()
        self.assertEqual(self.sender.balance, 500.00)
        self.assertEqual(self.recipient.balance, 2500.00)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"Successfully transferred 500.0 from {self.sender} to {self.recipient}.")

    def test_it_redirect_on_success(self):
        response = self.client.post(reverse('accounts:transfer'), self.data)
        self.assertEqual(response.url, reverse('accounts:transfer'))

    def test_post_insufficient_funds(self):
        data = {'sender': self.sender.id, 'recipient': self.recipient.id, 'amount': 1500.00}
        response = self.client.post(reverse('accounts:transfer'), data)

        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
