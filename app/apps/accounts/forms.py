from django import forms
from .models import Account


class TransferForm(forms.Form):
    sender = forms.ModelChoiceField(queryset=Account.objects.all(), label='Sender',
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    recipient = forms.ModelChoiceField(queryset=Account.objects.all(), label='Recipient',
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(label='Amount', min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        sender = cleaned_data.get('sender')
        cleaned_data.get('recipient')
        amount = cleaned_data.get('amount')

        if sender and amount:
            if amount > sender.balance:
                raise forms.ValidationError("Amount exceeds sender's balance.")

    def save(self):
        sender = self.cleaned_data['sender']
        recipient = self.cleaned_data['recipient']
        amount = self.cleaned_data['amount']

        sender.balance -= amount
        recipient.balance += amount
        sender.save()
        recipient.save()

