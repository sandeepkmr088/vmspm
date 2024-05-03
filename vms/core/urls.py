from django.urls import path
from .views import vendor_performance_view,AcknowledgePurchaseOrderView,VendorPerformanceAPIView,VendorListCreateAPIView,VendorRetrieveAPIView,VendorUpdateAPIView,VendorDestroyAPIView, CreatePurchaseOrderAPIView,ListPurchaseOrdersAPIView,RetrievePurchaseOrderAPIView,UpdatePurchaseOrderAPIView,DeletePurchaseOrderAPIView

urlpatterns = [
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorRetrieveAPIView.as_view(), name='vendor-retrieve'),
    path('api/vendors/<int:pk>/update/', VendorUpdateAPIView.as_view(), name='vendor-update'),
    path('api/vendors/<int:pk>/delete/', VendorDestroyAPIView.as_view(), name='vendor-destroy'),
    #path('api/vendors/<str:vendor_code>/performance', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    path('api/vendors/<str:vendor_code>/performance/', vendor_performance_view, name='vendor_performance'),
    path('api/purchase_orders/', ListPurchaseOrdersAPIView.as_view(), name='purchase_order_list'),
    path('api/purchase_orders/', CreatePurchaseOrderAPIView.as_view(), name='create_purchase_order'),
    path('api/purchase_orders/<int:pk>/', RetrievePurchaseOrderAPIView.as_view(), name='retrieve_purchase_order'),
    path('api/purchase_orders/<int:pk>/', UpdatePurchaseOrderAPIView.as_view(), name='update_purchase_order'),
    path('api/purchase_orders/<int:pk>/', DeletePurchaseOrderAPIView.as_view(), name='delete_purchase_order'),
 
    
    
    path('api/purchase_orders/<int:po_number>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),
    
]