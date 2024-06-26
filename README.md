# Transactions API Documentation

This API allows users to manage transactions.

## Base URL

The base URL for all endpoints is `http://localhost:5000` (assuming the Flask app is running on port 5000).

## Endpoints

### Get All Transactions

- **URL:** `/transactions/`
- **Method:** `GET`
- **Description:** Retrieves details of all transactions.
- **Response:** An array of transaction objects containing TransactionID, CustomerName, TransactionDate, Amount, Status, and InvoiceURL.

### Upload a Transaction File

- **URL:** `/transactions/`
- **Method:** `POST`
- **Description:** Uploads a CSV file containing transaction data. Expects a file with the key `file` in the request form-data.
- **Response:** Success message if the file is uploaded successfully.

### Get a Transaction

- **URL:** `/transactions/<transaction_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific transaction identified by its TransactionID.
- **Parameters:**
  - `transaction_id` (string): The unique identifier of the transaction.
- **Response:** Details of the transaction in JSON format if found, otherwise an error message with status code 404.

### Update a Transaction

- **URL:** `/transactions/<transaction_id>`
- **Method:** `PUT`
- **Description:** Updates details of a specific transaction identified by its TransactionID.
- **Parameters:**
  - `transaction_id` (string): The unique identifier of the transaction.
- **Request Body:** JSON object with fields to be updated (CustomerName, TransactionDate, Amount, Status, InvoiceURL).
- **Response:** Success message if the transaction is updated successfully, otherwise an error message with status code 404.

### Delete a Transaction

- **URL:** `/transactions/<transaction_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific transaction identified by its TransactionID.
- **Parameters:**
  - `transaction_id` (string): The unique identifier of the transaction.
- **Response:** Success message if the transaction is deleted successfully, otherwise an error message with status code 404.
