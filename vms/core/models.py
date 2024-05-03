from django.db import models
from django.utils import timezone
from django.db.models import Avg
from datetime import timedelta

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    st=( 
         ('0','---Select Staus---'),
         ('Canceled','Canceled'),
         ('Completed','Completed'),
         ('Pending','Pending'),        
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=100, unique=True)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(choices= st,max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    
    def save(self, *args, **kwargs):
        # Check if the status is changing
        if self.pk:  # If the instance already exists
            old_status = PurchaseOrder.objects.get(pk=self.pk).status
            if self.status != old_status:  # Status is changing
                self.update_vendor_on_time_delivery_rate()
                self.update_quality_rating_avg()
                self.update_average_response_time()
                self.update_fulfillment_rate()
        
        # Call the parent class's save method
        super().save(*args, **kwargs)

    def update_vendor_on_time_delivery_rate(self):
        if self.status == 'Completed':
            # Get all completed POs for the vendor
            completed_pos = PurchaseOrder.objects.filter(vendor=self.vendor, status='Completed')
           
            # Filter completed POs delivered on or before their delivery dates
            on_time_deliveries = completed_pos.filter(delivery_date__lte=self.delivery_date).count()
            
            # Calculate the total number of completed POs for the vendor
            total_completed_pos = completed_pos.count()
            
            # Calculate on-time delivery rate and update the vendor
            if total_completed_pos > 0:
                vendor = self.vendor
                vendor.on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
                vendor.save()

    def update_quality_rating_avg(self):
        if self.status == 'Completed' and self.quality_rating is not None:
            # Get all completed POs with quality ratings for the vendor
            completed_pos_with_ratings = PurchaseOrder.objects.filter(vendor=self.vendor, status='Completed', quality_rating__isnull=False)
            
            # Calculate the average quality rating
            avg_rating = completed_pos_with_ratings.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']

            # Update the vendor's quality rating average
            if avg_rating is not None:
                self.vendor.quality_rating_avg = avg_rating
                self.vendor.save()

    def acknowledge_po(self):
        self.acknowledgment_date = timezone.now()
        self.save()
        self.calculate_average_response_time()

    def update_average_response_time(self):
        if self.acknowledgment_date:
            # Get all acknowledged POs for the vendor
            acknowledged_pos = PurchaseOrder.objects.filter(vendor=self.vendor, acknowledgment_date__isnull=False)
            print(acknowledged_pos)
            # Calculate response times for acknowledged POs
            response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos]
            print(response_times)
            # Calculate the average response time
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                
                # Update the vendor's average response time
                self.vendor.average_response_time = avg_response_time
                self.vendor.save()

    def update_fulfillment_rate(self):
        # Get all POs issued to the vendor
        total_pos = PurchaseOrder.objects.filter(vendor=self.vendor).count()
        
        if total_pos > 0:
            # Get the count of successfully fulfilled POs
            fulfilled_pos = PurchaseOrder.objects.filter(vendor=self.vendor, status='Completed').count()
            
            # Calculate the fulfilment rate
            fulfillment_rate = (fulfilled_pos / total_pos) * 100
            
            # Update the vendor's fulfilment rate
            self.vendor.fulfillment_rate = fulfillment_rate
            self.vendor.save()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"