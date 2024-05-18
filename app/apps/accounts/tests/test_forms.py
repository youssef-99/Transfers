from django import forms
from django.test import TestCase

from apps.accounts.forms import TransferForm
from apps.accounts.models import Account


class TransferFormTest(TestCase):
    def setUp(self):
        self.sender = Account.objects.create(uuid="sender_uuid", name="Sender", balance=100.0)
        self.recipient = Account.objects.create(uuid="recipient_uuid", name="Recipient", balance=0.0)

    def test_form_has_sender_field(self):
        form = TransferForm()
        self.assertTrue('sender' in form.fields)

    def test_sender_field_is_model_choice_field(self):
        form = TransferForm()
        self.assertIsInstance(form.fields['sender'], forms.ModelChoiceField)

    def test_form_has_recipient_field(self):
        form = TransferForm()
        self.assertTrue('recipient' in form.fields)

    def test_recipient_field_is_model_choice_field(self):
        form = TransferForm()
        self.assertIsInstance(form.fields['recipient'], forms.ModelChoiceField)

    def test_form_has_amount_field(self):
        form = TransferForm()
        self.assertTrue('amount' in form.fields)

    def test_amount_field_type(self):
        form = TransferForm()
        self.assertIsInstance(form.fields['amount'], forms.DecimalField)

    def test_amount_should_be_more_than_1(self):
        form_data = {
            'sender': self.sender.pk,
            'recipient': self.recipient.pk,
            'amount': 0.5  # Less than 1, should fail validation
        }
        form = TransferForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data['amount'] = 1.5  # Valid amount
        form = TransferForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_data(self):
        sender = Account.objects.create(uuid="sender_uuid", name="Sender", balance=100.0)
        recipient = Account.objects.create(uuid="recipient_uuid", name="Recipient", balance=0.0)

        form_data = {
            'sender': sender.pk,
            'recipient': recipient.pk,
            'amount': 50.0
        }

        form = TransferForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            'sender': 1,
            'recipient': 2,
            'amount': -50.0
        }

        form = TransferForm(data=form_data)

        self.assertFalse(form.is_valid())
