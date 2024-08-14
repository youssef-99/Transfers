from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Account
        fields = ['uuid', 'name', 'balance', 'image']
