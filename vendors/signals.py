from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from django.utils import timezone 
from django.db.models import Avg, F, ExpressionWrapper, fields, Count, Case, When, FloatField

@receiver(post_save, sender=PurchaseOrder)
def purchase_order_post_save(sender, instance, created, **kwargs):
    """
    Function to be executed after a PurchaseOrder instance is saved.
    """
    query = PurchaseOrder.objects.filter(status='completed')
    completed_po = query.count()
    total_po = PurchaseOrder.objects.count()
    vendor = instance.vendor
    if instance.status == 'completed':
        #On-Time Delivery Rate
        on_time_delivery_rate, avg_quality_rating, fulfillment_rate = calculate_performance(instance.vendor)
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.avg_quality_rating = avg_quality_rating
        vendor.fulfillment_rate = fulfillment_rate

    # Average Response Time
    if instance.acknowledgment_date:
        vendor.average_response_time = calculate_average_response_time(instance.vendor)
    vendor.save()

def calculate_performance(vendor):
    vendor_pos = PurchaseOrder.objects.filter(vendor=vendor)
    completed_pos = vendor_pos.filter(status='completed')

    # on_time_delivery_rate
    now = timezone.now()
    on_time_deliveries = completed_pos.filter(delivery_date__lte=now.date())
    total_completed_pos = completed_pos.count()
    on_time_delivery_count = on_time_deliveries.count()
    if total_completed_pos > 0:
        on_time_delivery_rate = (on_time_delivery_count / total_completed_pos) * 100
    else:
        on_time_delivery_rate = 0

    #avg_quality_rating
    completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
    average_quality_rating = completed_pos_with_rating.aggregate(avg_quality_rating=Avg('quality_rating'))
    avg_quality_rating = average_quality_rating['avg_quality_rating'] or 0

    # fulfillment_rate
    total_pos_count = vendor_pos.count()
    if total_pos_count > 0:
        fulfillment_rate = (total_completed_pos / total_pos_count) * 100
    else:
        fulfillment_rate = 0

    return on_time_delivery_rate, avg_quality_rating, fulfillment_rate


def calculate_average_response_time(vendor):
    vendor_pos = PurchaseOrder.objects.filter(vendor=vendor).exclude(acknowledgment_date=None)
    time_diff_expr = ExpressionWrapper(
        F('acknowledgment_date') - F('issue_date'),
        output_field=fields.DurationField()
    )
    vendor_pos_with_time_diff = vendor_pos.annotate(time_diff=time_diff_expr)
    average_response_time = vendor_pos_with_time_diff.aggregate(avg_response_time=Avg('time_diff'))
    average_response_time_in_hours = average_response_time['avg_response_time'].total_seconds() / 3600
    return average_response_time_in_hours