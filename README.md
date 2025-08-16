
# OnlineFoodPlaza - Backend (Django + DRF + Celery)

This repository is a ready-to-share Django project implementing the assignment:
- Orders with through-model `OrderItem` capturing quantity, unit_price, subtotal
- Models: Customer, Seller, Product, Order, OrderItem, PlatformApiCall
- Timestamps and soft-deletes
- DRF APIs (CRUD for Orders & Products) under `/api/v1/`
- JWT authentication (DRF SimpleJWT)
- Role-based permissions (Admin, Seller, Customer)
- Pagination (LimitOffset), django-filter, search, sorting, top-5
- Celery integration and a scheduled daily sales report at 14:30
- Management command to import products from Excel using pandas (prevents duplicates)
- PlatformApiCall logging mixin for all API views
- Validation, tests placeholders, linting configs, and deployment instructions for localhost

## How to run locally (quick)
1. Create and activate a virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Apply migrations:
   ```bash
   python manage.py migrate
   ```
3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
4. Start Redis (for celery broker). If you don't have Redis, you can use `redis-server` locally.
5. Start Celery worker and beat:
   ```bash
   celery -A online_foodplaza worker -l info
   celery -A online_foodplaza beat -l info
   ```
6. Run Django dev server:
   ```bash
   python manage.py runserver
   ```

## Importing products via management command
Place your Excel file at `data/products.xlsx` and run:
```bash
python manage.py import_products data/products.xlsx
```
This enqueues a Celery task which will import and email (placeholder) a report when complete.

## Notes
- This project uses SQLite for simplicity and is configured for local development.
- Sensitive keys are in `settings.py` only for demo; replace them before sharing publicly.
- See code for implementation details and comments.
