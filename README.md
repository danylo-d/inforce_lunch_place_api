# Lunch Place API

This is a Django-based Lunch App that allows users to create and manage restaurants and menus. Users can vote for menus, view voting results, and retrieve today's menu based on the highest number of votes.

## Setup and Installation

To run the Lunch App, follow the instructions below:

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Steps

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/danylo-d/inforce_lunch_place_api.git
   ```

2. Navigate to the project's root directory:

   ```
   cd inforce_lunch_place_api
   ```

3. Rename a `.env.sample` file to `.env` in the project's root directory and provide the following environment variables:

   ```
   POSTGRES_HOST=db
   POSTGRES_DB=your_database_name
   POSTGRES_USER=your_database_user
   POSTGRES_PASSWORD=your_database_password
   DJANGO_SECRET_KEY=your_django_secret_key
   ```

   Replace the values with your own database and Django secret key configurations.


4. Build and run the Docker containers:

   ```
   docker-compose up -d --build
   ```
5. Create a superuser account(optional):

    ```
    docker-compose exec app python manage.py createsuperuser
    ```

6. The Lunch App should now be running on `http://localhost:8000`. You can access the admin interface at `http://localhost:8000/admin`.

## API Endpoints

The Lunch App provides the following API endpoints:

### Restaurants

- `GET /api/lunch/restaurants/` - Retrieve a list of all restaurants.
- `POST /api/lunch/restaurants/` - Create a new restaurant.
- `GET /api/lunch/restaurants/{id}/` - Retrieve details of a specific restaurant.
- `PUT /api/lunch/restaurants/{id}/` - Update a specific restaurant.
- `DELETE /api/lunch/restaurants/{id}/` - Delete a specific restaurant.

### Menus

- `GET /api/lunch/menus/` - Retrieve a list of all menus.
- `POST /api/lunch/menus/` - Create a new menu.
- `GET /api/lunch/menus/{id}/` - Retrieve details of a specific menu.
- `PUT /api/lunch/menus/{id}/` - Update a specific menu.
- `DELETE /api/lunch/menus/{id}/` - Delete a specific menu.
- `POST /api/lunch/menus/{id}/vote/` - Vote for a specific menu.
- `GET /api/lunch/menus/voting-results/` - Retrieve the voting results for all menus.
- `GET /api/lunch/menus/today-menu/` - Retrieve today's menu based on the highest number of votes.

### User

- `POST /api/user/register/` - Register a new user.
- `POST /api/user/token/` - Obtain a JWT token.
- `POST /api/user/token/refresh/` - Refresh a JWT token.
- `POST /api/user/token/verify/` - Verify a JWT token.
- `GET /api/user/me/` - Retrieve the authenticated user's details.
- `PUT /api/user/me/` - Update the authenticated user's details.

### Documentation
You can also see and try all these endpoints in the SWAGGER documentation
- `/api/doc/swagger/`
## Authentication

The Lunch App uses JSON Web Tokens (JWT) for authentication. To access protected endpoints, include the JWT token in the `Authorization` header of the request using the format: `Bearer <token>`. Tokens can be obtained by authenticating with valid user credentials.
