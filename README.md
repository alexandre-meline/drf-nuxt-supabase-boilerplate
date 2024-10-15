# 🌟 DRF Supabase Boilerplate

## Project Context

This Django project is designed to manage user profiles and their service subscriptions using data stored in a Supabase database. The main goal is to efficiently handle user information and subscription details linked to Stripe, while facilitating integration with other backend or frontend systems such as Nuxt.js applications utilizing the same data backend.

## ✨ Features

- **User Profile Management:** Model user profiles with the ability to store names and manage authentication.
  
- **Subscription Tracking:** Manage user subscriptions, integrated with Stripe to handle subscriptions, customers, and current periods.

- **Supabase Integration:** Access and manipulate data via a connection to a Supabase database, leveraging PostgreSQL's capabilities to scale ETL processes.

## 🚀 Installation

To correctly set up this project, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/alexandre-meline/drf-supabase-boilerplate.git
   cd drf-supabase-boilerplate
   ```

2. **Set Up Python Environment**

   Ensure you are using a virtual environment:

   ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

   Or with Poetry:

   ```bash
   poetry shell
   ```

3. **Install Dependencies**

   Install dependencies using pip or poetry:

   ```bash
   pip install -r requirements.txt
   ```

   Or with Poetry:

   ```bash
   poetry install
   ```

4. **Configure Settings**

   Create a `.env` file from the example, and set up your Supabase database and other secrets.

   ```text
    # Debug mode
    DEBUG=True

    # Using SQLite
    USE_SQLITE=True

    # Secret key 
    # Create secret key use this command: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    SECRET_KEY=h1s6mqcuiwb+dqib@(v3yjwo)@t6%y_%+rh79(p6%@5qkco805

    # Language code 
    LANGUAGE_CODE=fr-FR

    # Time zone
    TIME_ZONE=Europe/Paris

    # Database
    DATABASE_URL=postgresql://

    # Authentification: Supabase JWT secret for decode JWT token from Supabase
    SUPABASE_JWT_SECRET=uV1qr0hTLy6k3yjz+$==

    # Redis: cache
    REDIS_CACHE_URL=redis://127.0.0.1:6379/1

    # Broker worker celery
    CELERY_BROKER_URL=redis://127.0.0.1:6379/2

    # Result backend celery methodes: use django-db for save result in database
    CELERY_RESULT_BACKEND=django-db
   ```

5. **Run Migrations**

   Set up the database:

   ```bash
   python manage.py migrate
   ```

6. **Start the Server**

   Launch the Django server:

   ```bash
   python manage.py runserver
   ```

## 🛠️ Using the Models

### `User`

The `User` model represents user profiles, capturing personal data such as first and last names. This model is directly mapped to a database table named `profiles` in Supabase.

- **ID Field:** Utilizes a UUID as the unique identifier for the user profile.
- **Authentication:** Includes an `is_authenticated` property that is always true for internal validation.

### `UserSubscription`

The `UserSubscription` model handles Stripe subscription details for each user.

- **User ID Field:**
  Specifies which user the subscription is linked to, uniquely ensuring that a user cannot have more than one active subscription per type.
- **Stripe Fields:**
  Multiple fields such as `stripe_customer_id`, `stripe_subscription_id`, and `stripe_price_id` handle Stripe integration.
- **Subscription Expiration:** Managed by `stripe_current_period_end` to indicate the end of the current billing period.

## 🤝 Contributing

Contributions are welcome! Please open an issue for significant changes, and submit pull requests for direct contributions.

## 📜 License

This project is licensed under the MIT License - feel free to modify it according to your needs while respecting the terms of the license.

## 📬 Contact

For any questions, please contact us at [alexandre.meline.dev@gmail.com].
