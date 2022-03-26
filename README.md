# SideBoard API

Capstone project for Udacity's Full Stack Software Development nanodegree.

## What is it?
The idea for SideBoard is a craft focused refurbished furniture marketplace. It connects merchants and their wares to customers looking for incredible, unique pieces.

This is the backend API for SideBoard that implements the necessary database models, endpoints, and authentication via Auth0.

## Local Setup
Run the following to setup the application for local development.

Setup your environment and install dependencies.
```
python3 -m venv env
source env/bin/activate
pip install requirements.txt
```

Check the setup script and edit the database url to match your own Postgres account. Then run the following to create the db and run migrations.
```
createdb sideboarddb
source setup.sh
python manage.py db upgrade
```
Then you're all set to run the app!
```
flask run
```

## Authentication & Role Based Access
The API restricts access via permissions that are divided among three user roles -- Admin, Merchant, and Customer. Each role has JWTs assigned to them that are set using the setup script. Use one of those valid JWTs in the request header to access the APIs endpoints. Each role has permissions as follows.

#### Admin
Admin users have full access with all possible permissions given to them.
- `get:merchants`
- `get:customers`
- `get:items`
- `create:merchants`
- `create:items`
- `create:customers`
- `patch:merchants`
- `patch:items`
- `patch:customers`
- `delete:merchants`
- `delete:items`
- `delete:customers`

#### Merchant
Merchant users have full access to item endpoints and read access to all others.
- `get:merchants`
- `get:items`
- `get:customers`
- `create:items`
- `patch:items`
- `delete:items`

#### Customer
Customer users have read access only to items and merchants.
- `get:merchants`
- `get:items`

## Hosting
The application is also hosted on Heroku:
https://super-cool-app-34314324234.herokuapp.comd
You can use the JWTs in the setup script in order to make authorized requests. This would be under the Bearer Token auth field using a tool like Postman to make requests to the API.

## Testing
Run the following to run unit tests.
```
python unit_tests.py
```
Each endpoint can also be tested manually using a tool such as Postman or curl as seen below.

## Endpoints

`BASE URL: http://localhost:5000`

The available resources for the API are merchants, items, and customers.
The following HTTP methods are supported: GET, POST, PATCH, DELETE.

- `GET /merchants`
- `GET /items`
- `GET /customers`
- `POST /merchants`
- `POST /items`
- `POST /customers`
- `PATCH /merchants/<merchant_id>`
- `PATCH /items/<item_id>`
- `PATCH /customer/<customer_id>`
- `DELETE /merchants/<merchant_id>`
- `DELETE /items/<item_id>`
- `DELETE /customers/<customer_id>`

## Merchant
This is an object representing a seller's account information and inventory of items.

### GET /merchants
Fetches a list of merchant objects.

```
curl -X GET 'http://localhost:5000/merchants' \
--header 'Authorization: Bearer '$ADMIN_TOKEN

{
  "merchants": [
    {
      "city": "San Francisco",
      "description": "I refurbish antique furniture into beautiful chic pieces.",
      "email": "sharna@jive.com",
      "fb_link": null,
      "id": 1,
      "image_link": null,
      "insta_link": null,
      "items": "[]",
      "name": "Sharna",
      "phone": "1234567890",
      "state": "California"
    }
  ],
  "success": true
}
```

### POST /merchants
Creates a new merchant object

```
curl -X POST 'http://localhost:5000/merchants' \
--header 'Authorization: Bearer '$ADMIN_TOKEN'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Sharna",
    "city": "San Francisco",
    "description": "I refurbish antique furniture into beautiful chic pieces.",
    "email": "sharna@jive.com",
    "phone": 1234567890,
    "state": "California"
}'

{
    "merchant": {
        "city": "San Francisco",
        "description": "I refurbish antique furniture into beautiful chic pieces.",
        "email": "sharna@jive.com",
        "fb_link": null,
        "id": 1,
        "image_link": null,
        "insta_link": null,
        "items": "[]",
        "name": "Sharna",
        "phone": "1234567890",
        "state": "California"
    },
    "success": true
}
```

### PATCH /merchants
Updates a merchant object.

```
curl -X PATCH 'http://localhost:5000/merchants/1' \
--header 'Authorization: Bearer '$ADMIN_TOKEN'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Shaquonda",
}'

{
    "merchant": {
        "city": "San Francisco",
        "description": "I refurbish antique furniture into beautiful chic pieces.",
        "email": "sharna@jive.com",
        "fb_link": null,
        "id": 1,
        "image_link": null,
        "insta_link": null,
        "items": [
            {
                "id": 1,
                "image_link": null,
                "merchant_id": 1,
                "name": "old sideboard",
                "price": 25.0
            }
        ],
        "name": "Shaquonda",
        "phone": "1234567890",
        "state": "California"
    },
    "success": true
}
```

### DELETE /merchants
Deletes a merchant object.

```
curl -X DELETE 'http://localhost:5000/merchants/1' \
--header 'Authorization: Bearer '$ADMIN_TOKEN

{
    "merchant": {
        "city": "San Francisco",
        "description": "I refurbish antique furniture into beautiful chic pieces.",
        "email": "sharna@jive.com",
        "fb_link": null,
        "id": 1,
        "image_link": null,
        "insta_link": null,
        "items": [
            {
                "id": 1,
                "image_link": null,
                "merchant_id": 1,
                "name": "old sideboard",
                "price": 25.0
            }
        ],
        "name": "Shaquonda",
        "phone": "1234567890",
        "state": "California"
    },
    "success": true
}
```

## Item
This is an object representing an item for sale.

### GET /items
Fetches a list of item objects.

```
curl -X GET 'http://localhost:5000/items' \
--header 'Authorization: Bearer '$ADMIN_TOKEN

{
    "items": [
        {
            "id": 1,
            "image_link": null,
            "merchant_id": 1,
            "name": "old sideboard",
            "price": 25.0
        }
    ],
    "success": true
}
```

### POST /items
Creates a new item object.

```
curl -X POST 'http://localhost:5000/items' \
--header 'Authorization: Bearer '$ADMIN_TOKEN'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "old sideboard",
    "price": "25.00",
    "description": "Refurbished antique sideboard",
    "merchant_id": 1
}'

{
    "item": {
        "id": 1,
        "image_link": null,
        "merchant_id": 1,
        "name": "old sideboard",
        "price": 25.0
    },
    "success": true
}
```

### PATCH /items
Updates an item object.

```
curl -X PATCH 'http://localhost:5000/items/1' \
--header 'Authorization: Bearer '$ADMIN_TOKEN'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "new sideboard"
}'

{
    "item": {
        "id": 1,
        "image_link": null,
        "merchant_id": 1,
        "name": "new sideboard",
        "price": 25.0
    },
    "success": true
}
```

### DELETE /items
Deletes an item object.

```
curl -X DELETE 'http://localhost:5000/items/1' \
--header 'Authorization: Bearer '$ADMIN_TOKEN

{
    "item": {
        "id": 1,
        "image_link": null,
        "merchant_id": 1,
        "name": "new sideboard",
        "price": 25.0
    },
    "success": true
}
```

## Customer
This is an object representing a customer who can buy items from merchants.

### GET /customers
Fetches a list of customer objects.

```
curl -X GET 'http://localhost:5000/customers' \
--header 'Authorization: Bearer '$ADMIN_TOKEN

{
    "customers": [
        {
            "email": "frank@bball.com",
            "favorites": [],
            "id": 1,
            "name": "Frank",
            "purchases": []
        }
    ],
    "success": true
}
```

### POST /customers
Creates a new customer object.

```
curl -X POST 'http://localhost:5000/customers' \
--header 'Authorization: Bearer '$ADMIN_TOKEN'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Frank",
    "email": "frank@bball.com"
}'

{
    "customer": {
        "email": "frank@bball.com",
        "favorites": [],
        "id": 1,
        "name": "Frank",
        "purchases": []
    },
    "success": true
}
```

### PATCH /customers
Updates a customer object.

```
curl -X PATCH 'http://localhost:5000/customers/1' \
--header 'Authorization: Bearer '$ADMIN_TOKEN'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Franklin"
}'

{
    "customer": {
        "email": "frank@bball.com",
        "favorites": [],
        "id": 1,
        "name": "Franklin",
        "purchases": []
    },
    "success": true
}
```

### DELETE /customers
Deletes a customer object.

```
curl -X DELETE 'http://localhost:5000/customers/1' \
--header 'Authorization: Bearer '$ADMIN_TOKEN

{
    "customer": {
        "email": "frank@bball.com",
        "favorites": [],
        "id": 1,
        "name": "Frank",
        "purchases": []
    },
    "success": true
}
```









