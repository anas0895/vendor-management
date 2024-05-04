from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken    
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from datetime import timedelta
from django.db.models import Q
from django.utils import timezone

from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer, TokenSerializer,CustomTokenRefreshSerializer, VendordataSerializer

class VendorCreateListView(generics.ListCreateAPIView):
    serializer_class = VendorSerializer
    pagination_class = PageNumberPagination
    # permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        search_keyword = self.request.query_params.get('q', '')
        if '@' in search_keyword:
            # Exact email match
            return Vendor.objects.filter(email=search_keyword).exclude(is_superuser=True) 
        else:
            # Partial name match
            return Vendor.objects.filter(username__icontains=search_keyword).exclude(is_superuser=True) 

class LoginView(TokenObtainPairView):
    """ View for user login """
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """Custom Refresh token View"""
    serializer_class = CustomTokenRefreshSerializer


class LogoutView(APIView):
    """View to logout """
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.POST.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": 'Logout Success.'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VendorAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendordataSerializer
    lookup_field = 'vendor_id'


class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_number'

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'vendor_id'