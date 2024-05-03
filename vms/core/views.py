from rest_framework import generics
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer,VendorPerformanceSerializer,PurchaseOrderSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.http import JsonResponse

class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
@action(detail=True, methods=['put'])
class VendorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
   

class VendorUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class VendorDestroyAPIView(generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class CreatePurchaseOrderAPIView(generics.CreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class ListPurchaseOrdersAPIView(generics.ListAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor=vendor_id)
        return queryset

class RetrievePurchaseOrderAPIView(generics.RetrieveAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class UpdatePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class DeletePurchaseOrderAPIView(generics.DestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer




class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    print(queryset)
    serializer_class = VendorPerformanceSerializer
    lookup_url_kwarg = 'vendor_code'

def vendor_performance_view(request, vendor_code):
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_code)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)

    # Calculate performance metrics
    performance_metrics = {
        'on_time_delivery_rate': vendor.on_time_delivery_rate,
        'quality_rating_avg': vendor.quality_rating_avg,
        'average_response_time': vendor.average_response_time,
        'fulfillment_rate': vendor.fulfillment_rate,
    }

    return JsonResponse(performance_metrics)

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_number'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()  # Assuming you're using timezone from django.utils
        instance.save()

        # Trigger recalculation of average_response_time for the vendor
        vendor = instance.vendor
        purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_time_sum = sum((acknowledged_po.acknowledgment_date - acknowledged_po.order_date).total_seconds() for acknowledged_po in purchase_orders)
        average_response_time = response_time_sum / purchase_orders.count() if purchase_orders else 0
        vendor.average_response_time = average_response_time
        vendor.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

'''
class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

    def perform_update(self, serializer):
        serializer.save(acknowledgment_date=timezone.now())
'''