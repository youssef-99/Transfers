import pandas as pd
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from apps.accounts.forms import TransferForm
from apps.accounts.models import Account


class LandingView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/index.html', context={'accounts': Account.objects.all()})


class UploadAccountsView(View):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('accountFile', None)
        if not uploaded_file or not uploaded_file.name.endswith('.csv'):
            return HttpResponseBadRequest("File must be a CSV file.")

        try:
            df = pd.read_csv(uploaded_file)

            accounts = [
                Account(uuid=row['ID'], name=row['Name'], balance=row['Balance'])
                for index, row in df.iterrows()
            ]
            Account.objects.bulk_create(accounts)
        except Exception as e:
            return HttpResponseBadRequest("Error processing CSV file: {}".format(str(e)))
        return redirect(reverse('accounts:index'))


class AccountDetailView(DetailView):
    model = Account
    template_name = 'accounts/account_details.html'
    context_object_name = 'account'


class TransferFundsView(View):
    def post(self, request, *args, **kwargs):
        form = TransferForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             f"Successfully transferred {form.cleaned_data['amount']} from {form.cleaned_data['sender']} to {form.cleaned_data['recipient']}.")
            form.save()
            return redirect('accounts:transfer')
        else:
            messages.error(request, "Insufficient funds in the sender's account.")
            return render(request, 'accounts/funds.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = TransferForm()
        return render(request, 'accounts/funds.html', {'form': form})
