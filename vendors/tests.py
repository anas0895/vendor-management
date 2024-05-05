from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone 
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Vendor, PurchaseOrder

class VendorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='vendor1@example.com', address='123 Main St', username='vendor1', email='vendor1@mailinator.com')
        self.vendor2 = Vendor.objects.create(name='Vendor 2', contact_details='vendor2@example.com', address='456 Elm St', username='vendor2', email='vendor2@mailinator.com')

    @property
    def bearer_token(self):
        user = Vendor.objects.create(username="admin", password="test@1235")
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION":f'Bearer {refresh.access_token}'}

    def test_list_vendors(self):
        url = reverse('vendor_create_list')
        response = self.client.get(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        url = reverse('vendor_create_list')
        data = {'name': 'Vendor', 'contact_details': 'newvendor@example.com', 'address': '789 Oak St', 'username':'vendor3', 'email':'vendor3@mailinator.com', 'password': 'As@12345', 'password2': 'As@12345'}
        response = self.client.post(url, data, format='json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PurchaseOrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='vendor1@example.com', address='123 Main St', username='vendor1', email='vendor1@mailinator.com')
        self.po1 = PurchaseOrder.objects.create(vendor=self.vendor1, delivery_date=timezone.now(), items=["chair", "table"],quantity=5, status='completed')

    @property
    def bearer_token(self):
        user = Vendor.objects.create(username="admin", password="test@1235")
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION":f'Bearer {refresh.access_token}'}

    def test_list_purchase_orders(self):
        url = reverse('po_create_list')
        response = self.client.get(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_order(self):
        url = reverse('po_create_list')
        data = {'vendor': self.vendor1.id, 'delivery_date' : timezone.now(), 'items' : ["chair", "table"], 'quantity' : 5, 'quality_rating':5, 'acknowledgment_date': timezone.now(), 'status': 'completed'}
        response = self.client.post(url, data, format='json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)  # Assuming the setup has 1 purchase order and we created 1 new purchase order