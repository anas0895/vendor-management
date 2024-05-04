from django.urls import path

from . import views

urlpatterns = [
    path('vendors/', views.VendorCreateListView.as_view(), name='vendor_create_list'),
    path('vendors/<slug:vendor_id>/', views.VendorAPIView.as_view(), name='vendor_details'),
    path('login/', views.LoginView.as_view(), name='auth_login'),
    path('login/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    path('purchase_orders/', views.PurchaseOrderListCreateAPIView.as_view(), name='po_create_list'),
    path('purchase_orders/<slug:po_number>/', views.PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='po_manage'),
    path('vendors/<slug:vendor_id>/performance', views.VendorPerformanceAPIView.as_view(), name='vendor_performance'),
    path('purchase_orders/<slug:po_number>/acknowledge/', views.VendorPerformanceAPIView.as_view(), name='vendor_performance'),
]