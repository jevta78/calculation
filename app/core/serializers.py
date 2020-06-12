from rest_framework import serializers
from .models import InputNumbers, Sums, Sve
class InputNumbersSerializer(serializers.ModelSerializer):

    class Meta:
        model = InputNumbers
        fields = ('list_num',)

class SumCalcSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sums
        fields = ('calcSum',)

class AllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sve
        fields = ('id', 'numbers', 'sums')
