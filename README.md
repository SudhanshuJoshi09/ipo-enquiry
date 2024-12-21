# README: PAN and IPO Search Service

---

## Introduction
Simple IPO enquiry service, this service provides a simple interface to check ipo allotments against a PAN

---

## Features

1. **Register PAN and Name**:
   - Users can register their PAN and name using the following `curl` command:

     ```bash
     curl --location 'localhost:5001/pan' \
     --header 'Content-Type: application/json' \
     --data '{
         "name": "sudhanshu9",
         "pan": "AAACU0564G"
     }'
     ```

2. **Search for IPO Listings**:
   - To search for IPOs associated with registered PANs, visit the following URL:

     [http://localhost:5001](http://localhost:5001)

---

## Quick Start

To get the service running:

1. Run the following command:
   ```bash
   docker-compose up
   ```

2. That’s it! The service will be up and running, ready to register PANs and search for IPOs.

---

## Endpoints

### 1. Register PAN
- **URL**: `localhost:5001/pan`
- **Method**: POST
- **Headers**:
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
      "name": "<name>",
      "pan": "<pan_number>"
  }
  ```

### 2. Search IPO Listings
- **URL**: `http://localhost:5001`
- **Method**: GET
- **Description**: Use the web interface to perform searches for IPOs associated with registered PANs.


