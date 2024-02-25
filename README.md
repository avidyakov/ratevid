# Ratevid

## Getting Started

### Prerequisites

-  Docker
-  Docker-compose

### Running the project

Use the following command to build and run the project:

```bash
docker-compose up --build
# This command will also automatically apply the migrations.
# In case you want to apply the migrations manually, here is the command you need:
alembic upgrade head
```

## API Documentation
Once the application is running, you can view the API documentation at this URL, and by default it is: http://localhost:8000/api/docs

## API Usage Examples

Here are some examples of how to use the API:

### Update Currency Rates
This endpoint is used to update currency rates:

```http request
POST http://localhost:8000/api/updates
Content-Type: application/json

{}
```

### Checking the Last Updated Currency Rates
You can use this endpoint to check when the currency rates were last updated:
```http request
GET http://localhost:8000/api/updates/last
Accept: application/json
```

### Exchanging Currency
This endpoint allows you to exchange one type of currency for another:

```http request
POST http://localhost:8000/api/exchanges
Content-Type: application/json

{
    "from_currency": "EUR",
    "to_currency": "RUB",
    "amount": 1000
}
```
Please replace the "from_currency", "to_currency" and "amount" fields with your desired currency types and amount.
