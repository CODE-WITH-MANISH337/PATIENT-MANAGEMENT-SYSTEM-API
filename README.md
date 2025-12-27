# Patient Management System

A FastAPI-based application for managing patient data, including automatic BMI calculation and health verdicts using Pydantic models. The application stores patient information in a JSON file (`patient_clone.json`) and provides RESTful API endpoints for CRUD operations.

## Features

- **Patient Data Management**: Create, read, update, and delete patient records.
- **Automatic BMI Calculation**: Computed field that calculates BMI based on height and weight.
- **Health Verdict**: Computed field providing health status based on BMI (Underweight, Normal, Overweight, Obese).
- **Sorting**: Sort patients by height, weight, or BMI in ascending or descending order.
- **Data Persistence**: Data is stored in and loaded from `patient_clone.json`.

## Installation

1. Ensure you have Python 3.8+ installed.
2. Clone or download the project files.
3. Navigate to the `FASTAPI` directory.
4. Install the required dependencies:

   ```
   pip install -r requirement.txt
   ```

   Key dependencies include:
   - FastAPI
   - Pydantic
   - Uvicorn (for running the server)

## Running the Application

1. Navigate to the `FASTAPI` directory.
2. Run the application using Uvicorn:

   ```
   uvicorn main:app --reload
   ```

3. Open your browser and go to `http://127.0.0.1:8000/docs` to access the interactive API documentation (Swagger UI).

## API Endpoints

### 1. Root Endpoint
- **GET** `/`
- **Description**: Returns a welcome message.
- **Response**: `{"message": "PATIENTS MANAGEMENT SYSTEM"}`

### 2. View All Patients
- **GET** `/view`
- **Description**: Retrieves all patient data from `patient_clone.json`.
- **Response**: JSON object with all patients keyed by ID.

### 3. About
- **GET** `/about`
- **Description**: Provides information about the application.
- **Response**: `{"message": "This is a simple FastAPI application."}`

### 4. View Specific Patient
- **GET** `/patient/{patient_id}`
- **Description**: Retrieves data for a specific patient by ID.
- **Parameters**:
  - `patient_id` (path): The ID of the patient (e.g., "P001").
- **Response**: Patient data as JSON.
- **Error**: 404 if patient not found.
- **Example**: `GET /patient/P001`

### 5. Sort Patients
- **GET** `/sort`
- **Description**: Sorts patients by a specified field.
- **Query Parameters**:
  - `sort_by` (required): Field to sort by ("height", "weight", "bmi").
  - `order` (optional, default "asc"): Sort order ("asc" or "desc").
- **Response**: List of sorted patient data.
- **Error**: 400 for invalid sort field or order.
- **Example**: `GET /sort?sort_by=bmi&order=desc`

### 6. Create Patient
- **POST** `/create`
- **Description**: Creates a new patient record.
- **Body**: JSON object matching the Patient model (see below).
- **Response**: 201 with success message.
- **Error**: 400 if patient ID already exists.
- **Example Body**:
  ```json
  {
    "id": "P006",
    "name": "New Patient",
    "city": "New City",
    "age": 30,
    "gender": "male",
    "height": 1.75,
    "weight": 70
  }
  ```

### 7. Update Patient
- **PUT** `/edit/{patient_id}`
- **Description**: Updates an existing patient record.
- **Parameters**:
  - `patient_id` (path): The ID of the patient to update.
- **Body**: JSON object with fields to update (PatientUpdate model).
- **Response**: 200 with success message.
- **Error**: 404 if patient not found.
- **Example Body**:
  ```json
  {
    "name": "Updated Name",
    "weight": 75
  }
  ```

### 8. Delete Patient
- **DELETE** `/delete/{patient_id}`
- **Description**: Deletes a patient record.
- **Parameters**:
  - `patient_id` (path): The ID of the patient to delete.
- **Response**: 200 with success message.
- **Error**: 404 if patient not found.
- **Example**: `DELETE /delete/P001`

## Data Structure

### patient_clone.json
This JSON file serves as the data store for patient records. It is a dictionary where keys are patient IDs (e.g., "P001") and values are patient data objects.

**Example Structure**:
```json
{
  "P001": {
    "name": "John Doe",
    "city": "New York",
    "age": 30,
    "gender": "male",
    "height": 1.75,
    "weight": 70,
    "bmi": 22.86,
    "verdict": "Normal"
  },
  ...
}
```

- **Fields**:
  - `id`: Unique patient identifier (string).
  - `name`: Patient's name (optional string).
  - `city`: City of residence (optional string).
  - `age`: Age in years (optional int, 1-119).
  - `gender`: Gender ("male", "female", "other"; optional).
  - `height`: Height in meters (optional float).
  - `weight`: Weight in kg (optional float).
  - `bmi`: Computed BMI (optional float, calculated as weight / (height^2)).
  - `verdict`: Computed health status (optional string, based on BMI).

## Pydantic Models

### Patient Model
Defines the structure for patient data with validation and computed fields.

- **Fields**: As described in the data structure.
- **Computed Fields**:
  - `bmi`: Automatically calculated if height and weight are provided.
  - `verdict`: Health status based on BMI thresholds.

### PatientUpdate Model
Used for partial updates, allowing optional fields.

## Notes

- BMI is calculated only if both height and weight are provided.
- Verdicts are based on standard BMI categories:
  - Underweight: BMI < 18.5
  - Normal: 18.5 ≤ BMI < 25
  - Overweight: 25 ≤ BMI < 30
  - Obese: BMI ≥ 30
- The application uses FastAPI's automatic validation and OpenAPI documentation.
- Data is persisted to `patient_clone.json` on create, update, and delete operations.
