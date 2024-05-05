from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken    
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import TokenSerializer, CustomTokenRefreshSerializer, VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer, VendordataSerializer

class LoginAPIView(TokenObtainPairView):
    """ View for user login """
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class CustomTokenRefreshAPIView(TokenRefreshView):
    """Custom Refresh token View"""
    serializer_class = CustomTokenRefreshSerializer


class VendorCreateListAPIView(generics.ListCreateAPIView):
    """ Create and List Vendor """
    serializer_class = VendorSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()

    def get_queryset(self):
        search_keyword = self.request.query_params.get('q', '')
        if '@' in search_keyword:
            # Exact email match
            return Vendor.objects.filter(email=search_keyword).exclude(is_superuser=True) 
        else:
            # Partial name match
            return Vendor.objects.filter(username__icontains=search_keyword).exclude(is_superuser=True) 

class LogoutAPIView(APIView):
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
    """ Vendor Retrieve / Update / Delete """
    queryset = Vendor.objects.all()
    serializer_class = VendordataSerializer
    lookup_field = 'vendor_id'
    permission_classes = (IsAuthenticated,)


class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    """ Purchase order create and listing """
    queryset = PurchaseOrder.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = PurchaseOrderSerializer
    permission_classes = (IsAuthenticated,)

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Purchase order Retrieve / Update / Delete """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_number'
    permission_classes = (IsAuthenticated,)

class VendorAcknowledgeAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_number'
    permission_classes = (IsAuthenticated,)

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    """ Vendor performance view """
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'vendor_id'
    permission_classes = (IsAuthenticated,)