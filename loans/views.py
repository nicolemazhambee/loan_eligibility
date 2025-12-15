from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoanApplicationSerializer
from .services import EligibilityService

class LoanEligibilityView(APIView):
    def post(self, request):
        serializer = LoanApplicationSerializer(data=request.data)
        if serializer.is_valid():
            service = EligibilityService()
            result = service.check_eligibility(serializer.validated_data)
            
            # If eligible, return 200. If declined, return 200 (with eligible: False) or 400? 
            # Usually 200 OK with decision body is better for decision APIs.
            return Response(result, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
