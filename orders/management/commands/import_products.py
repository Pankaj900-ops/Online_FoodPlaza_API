
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Product
import pandas as pd
from orders.tasks import import_products_task

class Command(BaseCommand):
    help = 'Import products from excel and enqueue celery task'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to excel file')

    def handle(self, *args, **options):
        file = options['file']
        # read excel to ensure file exists and preview count
        df = pd.read_excel(file)
        # enqueue celery task to import (task will do actual work to keep management command fast)
        res = import_products_task.delay(file)
        self.stdout.write(self.style.SUCCESS(f'Enqueued import task for {file}. Task id: {res.id}'))
