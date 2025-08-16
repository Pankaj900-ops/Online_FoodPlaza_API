
from celery import shared_task
from .models import Order
from django.core.mail import send_mail

@shared_task
def import_products_task(file_path, user_id=None):
    # Placeholder: actual import handled via management command + task
    return {'status':'ok','file':file_path}

@shared_task
def daily_sales_report():
    # Simple aggregate example and placeholder for email sending
    from django.db.models import Sum
    total = Order.objects.filter(is_deleted=False).aggregate(sum=Sum('amount'))['sum'] or 0
    # send_mail subject/body/replacements as needed (configured email required)
    print("Daily sales total:", total)
    return {'total': float(total)}
