from rest_framework import serializers

class LoanApplicationSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=20)
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=1.00)
    term_months = serializers.IntegerField(min_value=1, max_value=360) 
