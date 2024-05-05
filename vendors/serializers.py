from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class TokenSerializer(TokenObtainPairSerializer):
    """ User Login Serializer """
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """User Token Refresh Serializer"""
    def validate(self, attrs):
        data = super().validate(attrs)
        return data

class VendorSerializer(serializers.ModelSerializer):
    """ Signup Serializer """
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Vendor.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Vendor
        fields = ('username', 'password', 'password2', 'email', 'name', 'contact_details', 'address')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Vendor.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            contact_details=validated_data['contact_details'],
            address=validated_data['address']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class VendordataSerializer(serializers.ModelSerializer):
    vendor_id = serializers.CharField(read_only=True)

    class Meta:
        model = Vendor
        fields = ("username", "name", "vendor_id", "contact_details", "address", "on_time_delivery_rate", "quality_rating_avg", "average_response_time", "fulfillment_rate")

class PurchaseOrderSerializer(serializers.ModelSerializer):
    po_number = serializers.CharField(read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("name", "on_time_delivery_rate", "quality_rating_avg", "average_response_time", "fulfillment_rate")