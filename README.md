# QuickBite POS Backend

A simple Point of Sale (POS) backend for a Quick Service Restaurant (QSR), built with Django and Django REST Framework.

## Features
- Manage menu items (name, price, available quantity/stock)
- Place orders with one or more menu items
- Track order status (pending, in progress, completed)
- Prevent orders when requested quantity exceeds available stock
- Filter orders by status
- Analytics: Get average daily sales for each of the last 4 weekdays (Mon-Fri, completed orders only)
- Admin interface for managing menu and orders


## Setup & Usage Instructions

## 1. Requirements
- **Python 3.10.x** (recommended: 3.10.4)
- [pip](https://pip.pypa.io/en/stable/)
- [git](https://git-scm.com/)

## 2. Project Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd quickbite_pos_backend

# (Optional but recommended) Set Python version with pyenv
pyenv local 3.10.4

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate    # On Windows

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

---

## 3. Authentication & API Usage

- **Access the API and admin:**
   - API Root: `http://localhost:8000/api/`
   - Admin: `http://localhost:8000/admin/`
- **All API endpoints (except `/api/login/`) require a valid JWT access token in the `Authorization` header.**
- **Obtain your tokens via the login endpoint:**

### Login (Get JWT Token)
**POST** `/api/login/`
```json
{
  "username": "<your-username>",
  "password": "<your-password>"
}
```
**Response:**
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```
- Use the `access` token in the header:
  - `Authorization: Bearer <access_token>`

---

## 4. API Endpoints & Request Models
## API Endpoints

- `GET /api/menu-items/` — List all available menu items
- `POST /api/orders/` — Place a new order
- `GET /api/orders/` — List all orders
- `GET /api/orders/filter/?status=pending` — Filter orders by status
- `PATCH /api/orders/<order_id>/status/` — Update status of a specific order
- `GET /api/analytics/average-daily-sales/` — Get average daily sales for each of the last 4 weekdays

### Menu Items
- **GET** `/api/menu-items/` — List all available menu items

### Orders
- **GET** `/api/orders/` — List all orders
- **GET** `/api/orders/?status=<status>` — Filter orders by status (`pending`, `in_progress`, `completed`)
- **POST** `/api/orders/` — Place a new order
    ```json
    {
      "items": [
        { "menu_item": <menu_item_id>, "quantity": <int> },
        { "menu_item": <menu_item_id>, "quantity": <int> }
      ]
    }
    ```
- **PATCH** `/api/orders/<order_id>/status/` — Update order status
    ```json
    {
      "status": "pending" | "in_progress" | "completed"
    }
    ```

### Analytics
- **GET** `/api/analytics/average-daily-sales/` — Get average daily sales for last 4 weekdays

---

## 5. Django Admin
- Access at `/admin/` (requires superuser account)
- Manage menu items, orders, and users.
- Inventory and deduplication logic is enforced for all orders (admin and API).

---

## 6. Troubleshooting & Best Practices

- **Admin login fails?**
    - Make sure you ran `python manage.py createsuperuser` and are using the correct credentials.
    - If you migrated a fresh DB, you must create a new superuser.
- **Static files not loading in admin with `DEBUG=False`?**
    - Run `python manage.py collectstatic` and configure static file serving (see Django docs for production setup).
- **Virtual environment not activated?**
    - Always run `source venv/bin/activate` before using `python` or `pip` commands.
- **Database issues?**
    - Ensure you ran `python manage.py migrate` before starting the server.
- **Dependency issues?**
    - Run `pip install -r requirements.txt` in your venv.
- **API authentication fails?**
    - Ensure you’re including the `Authorization: Bearer <access_token>` header.
    - Use `/api/login/` to get a fresh token.

---

## 7. General Notes
- Project uses SQLite by default for easy local setup.
- All business logic (deduplication, inventory) is enforced at the model layer for consistency.
- For production, configure environment variables for secrets and static/media files as per Django best practices.
- For any issues, check logs, and consult the Django and DRF documentation.

---

**This project is ready for production and local development. Follow these steps exactly for a smooth setup!**
