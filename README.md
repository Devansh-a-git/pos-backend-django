# QuickBite POS Backend

A simple Point of Sale (POS) backend for a Quick Service Restaurant (QSR), built with Django and Django REST Framework.

## Features
- Manage menu items (name, price, availability)
- Place orders with one or more menu items
- Track order status (pending, in progress, completed)
- Prevent orders with unavailable menu items
- Filter orders by status
- Analytics: Get average daily sales for each of the last 4 weekdays (Mon-Fri, completed orders only)
- Admin interface for managing menu and orders

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd quickbite_pos_backend
   ```

2. **Set Python version (if using pyenv):**
   ```sh
   pyenv local 3.10.4
   ```

3. **Install dependencies:**
   ```sh
   pip install django djangorestframework
   ```

4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

7. **Access the API and admin:**
   - API Root: `http://localhost:8000/api/`
   - Admin: `http://localhost:8000/admin/`

## API Endpoints

- `GET /api/menu-items/` — List all available menu items
- `POST /api/orders/` — Place a new order
- `GET /api/orders/` — List all orders
- `GET /api/orders/filter/?status=pending` — Filter orders by status
- `PATCH /api/orders/<order_id>/status/` — Update status of a specific order
- `GET /api/analytics/average-daily-sales/` — Get average daily sales for each of the last 4 weekdays

### Example: Place a New Order
```json
POST /api/orders/
{
  "items": [
    {"menu_item_id": 1, "quantity": 2},
    {"menu_item_id": 3, "quantity": 1}
  ]
}
```

### Example: Update Order Status
```json
PATCH /api/orders/5/status/
{
  "status": "completed"
}
```

## Notes
- Orders cannot be placed with unavailable menu items.
- Analytics endpoint only includes completed orders, and only weekdays (Mon-Fri).

## License
MIT
