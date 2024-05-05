# Vendor Management System with Performance Metrics

This is a Vendor Management System (VMS) developed using Django and Django REST Framework. The system handles vendor profiles, purchase orders (POs), and calculates vendor performance metrics such as on-time delivery rate, average quality rating, response time, and fulfillment rate.

## Core Features

1. **Vendor Profile Management:**
   - Allows creating, updating, listing, and deleting vendor profiles.
   - Tracks vendor information including name, contact details, address, and a unique vendor code.

2. **Purchase Order Tracking:**
   - Manages purchase orders with fields like PO number, vendor reference, order date, delivery date, items, quantity, and status.
   - Provides endpoints to create, update, list, and delete purchase orders.

3. **Vendor Performance Evaluation:**
   - Calculates performance metrics including on-time delivery rate, average quality rating, response time, and fulfillment rate.
   - Performance metrics are updated based on interactions recorded in the Purchase Order model.

## Technical Details

- **Python Version:** 3.10
- **Django Version:** 5.0.3
- **Django REST Framework Version:** 
- **Database:** SQLite (can be changed to other databases like PostgreSQL, MySQL, etc.)
- **Authentication:** Token-based authentication

## Setup Instructions

1. Clone the repository:
   git clone https://github.com/anas0895/vendor-management

2. Install dependencies:
    pip install -r requirements.txt

3. Apply database migrations:
    python manage.py migrate

4. Run the development server:
    python manage.py runserver

5. Access the API endpoints at http://localhost:8000/api/


6. For API Testing use Test Suite created by running : python manage.py test