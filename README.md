# **Fitness Data Pipeline on GCP**  

## **Project Overview**  
This project demonstrates an **end-to-end fitness data pipeline** on **Google Cloud Platform (GCP)**. It processes **real-time and batch fitness data**, applies transformations, and visualizes insights using **Looker Studio**. The pipeline is built using **Terraform for infrastructure automation**, **Pub/Sub for streaming ingestion**, **Airflow for batch processing**, **BigQuery for data warehousing**, **dbt for transformation**, and **Docker for containerized workflow management**.

## **Architecture Diagram**  
![Architecture Diagram](/Screenshots/project_archi.png)

## **Tools & Technologies Used**  
| Component                | Tool/Technology                | Purpose  |
|--------------------------|--------------------------------|----------|
| **Infrastructure**       | Terraform                      | Automate GCP resources |
| **Workflow Management**  | Docker, Airflow                | DAG execution & orchestration |
| **Streaming Data**       | Pub/Sub                        | Real-time data ingestion |
| **Batch Processing**     | Airflow, Cloud Storage         | Scheduled data ingestion (Cloud Storage as Data Lake) |
| **Data Warehouse**       | BigQuery                       | Data storage & analytics |
| **Data Transformation**  | dbt                            | Data cleaning & modeling |
| **Visualization**        | Looker Studio                  | Fitness data dashboard |

## **Step-by-Step Workflow**  

### **1. Infrastructure Setup (Terraform)**  
- Used **Terraform** to provision **Pub/Sub, BigQuery datasets, and IAM roles**.
- Deployed **Pub/Sub topic & subscription** for streaming ingestion.
- Created **BigQuery dataset (`fitness_data`) and tables**.

### **2. Streaming Data Ingestion (Pub/Sub)**  
- Developed `streaming_producer.py` to generate **random fitness data**.
- **Published messages to Pub/Sub** in JSON format.  
  ![Pub/Sub Subscription](/Screenshots/pub_sub.png)

- Configured **Pub/Sub BigQuery Subscription** (No Code) to **store streaming data in BigQuery** (`fitness_metrics` table).  
  ![BigQuery Table](/Screenshots/bigquery.png)

### **3. Batch Data Ingestion (Airflow & Cloud Storage as Data Lake)**  
- Created an **Airflow DAG (`batch_ingestion.py`)** to load batch data into **Cloud Storage**.
- Cloud Storage acts as a **lightweight data lake**, staging batch fitness data before ingestion into BigQuery.
- Data is then **loaded into BigQuery (`fitness_metrics` table)**.

  ![Airflow UI](/Screenshots/airflow_batch_data.png)

### **4. Data Processing & Transformation (dbt)**  
- Implemented a **dbt model (`fitness_transformation.sql`)** to:
  - **Aggregate and clean data** (average steps, heart rate, total calories, etc.).
  - Add **derived metrics** (e.g., **calories per minute, intensity level**).
  - Store transformed data in **BigQuery (`fitness_transformation` table)**.  
  ![BigQuery - Transformed Data Table](/Screenshots/bigquery_transformation.png)

### **5. Data Visualization (Looker Studio)**  
- **Created an interactive dashboard** using the `fitness_transformation` table.
- **Dashboard Sections:**  
  1. **Key Metrics** (Total Steps, Distance, Calories Burned)
  2. **Activity Insights** (Activity Distribution, Workout Duration)
  3. **Intensity & Efficiency** (Heart Rate vs. Calories Burned)  
  ![Looker Studio Dashboard](/Screenshots/Dashboard.png)

### **6. Docker Integration**  
- Used **Docker** to containerize the entire project, including **Airflow, Python scripts, dbt**.
- Ensured consistent and reproducible environments across all components.

## **Key Learnings & Takeaways**  
✅ **Real-time & batch data ingestion into BigQuery**  
✅ **Cloud Storage as a lightweight data lake for batch processing**  
✅ **Automated data transformation using dbt**  
✅ **End-to-end cloud-native data pipeline on GCP**  
✅ **Insightful fitness dashboard for decision-making**  
