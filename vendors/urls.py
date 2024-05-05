from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='auth_login'),
    path('login/refresh/', views.CustomTokenRefreshAPIView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='auth_logout'),
    path('vendors/', views.VendorCreateListAPIView.as_view(), name='vendor_create_list'),
    path('vendors/<slug:vendor_id>/', views.VendorAPIView.as_view(), name='vendor_manage'),
    path('purchase_orders/', views.PurchaseOrderListCreateAPIView.as_view(), name='po_create_list'),
    path('purchase_orders/<slug:po_number>/', views.PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='po_manage'),
    path('vendors/<slug:vendor_id>/performance', views.VendorPerformanceAPIView.as_view(), name='vendor_performance'),
    path('purchase_orders/<slug:po_number>/acknowledge/', views.VendorAcknowledgeAPIView.as_view(), name='vendor_acknowledge'),
]