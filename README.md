# ETL Weather Data Project

This project implements an ETL (Extract, Transform, Load) pipeline using **Apache Airflow** to fetch weather data from the **Open Meteo API**, transform it, and load it into a **PostgreSQL database**.

The project is containerized with **Docker Compose**, making it easy to deploy and run locally.

---

## 🚀 Project Structure

```
.
├── dags/
│   └── etlweather.py         # Airflow DAG for ETL
├── tests/
│   └── dags/
│       └── test_dag_example.py  # Basic DAG tests
├── .astro/
│   ├── config.yaml
│   ├── dag_integrity_exceptions.txt
│   └── test_dag_integrity_default.py
├── docker-compose.yml        # Docker services (Postgres)
├── Dockerfile                # Base image configuration
├── requirements.txt          # Python dependencies
├── packages.txt              # (Optional) System packages
├── .dockerignore             # Ignore files for Docker
└── README.md                 # This file
```

---

## 🛆 Main Components

- **Apache Airflow** — Workflow orchestration.
- **PostgreSQL** — Data warehouse to store weather data.
- **Open Meteo API** — Weather data provider.
- **Docker Compose** — For running Airflow and Postgres locally.
- **Astro Runtime** — Lightweight Airflow runtime base (optional).

---

## 🔥 How It Works

1. **Extract** weather data from Open Meteo API using Airflow `HttpHook`.
2. **Transform** the raw API data into a structured format (filter and flatten).
3. **Load** the transformed data into a PostgreSQL database using `PostgresHook`.
4. **Schedule**: The DAG is triggered **daily** (`@daily`).

---

## 🛠️ Prerequisites

- Docker and Docker Compose installed
- (Optional) Python 3.8+ for local DAG testing

---

## 🐳 Running Locally

1. Clone the repository:

```bash
git clone https://github.com/yourusername/etl-weather.git
cd etl-weather
```

2. Build and start services:

```bash
docker-compose up -d
```

3. Start Airflow (if using Astro CLI):

```bash
astro dev start
```

4. Access Airflow UI:

- URL: `http://localhost:8080`
- Default credentials: 
  - Username: `admin`
  - Password: `admin` (or depending on your setup)

5. In Airflow UI:
- Enable the **etl_weather_data** DAG
- Trigger the DAG manually or wait for scheduled execution.

---

## ⚙️ Configuration

- **Postgres Connection ID:** `postgres_default`
- **API Connection ID:** `open_meteo_api`
- **Database:** Postgres (runs on `localhost:5432` inside docker)
- **Table created:** `weather_data`

---

## 📜 Environment Variables

Set these if needed (in `.env` file or directly in your Docker environment):

| Variable | Description |
|:---------|:------------|
| `POSTGRES_USER` | Postgres username |
| `POSTGRES_PASSWORD` | Postgres password |
| `POSTGRES_DB` | Postgres database name |

---

## 💪 Testing

Tests are located under `tests/dags/`.

Run with pytest:

```bash
pytest tests/
```

The test file checks:
- DAG imports without errors
- DAGs have tags and retries set

---

## 🛡️ Notes

- This project uses `astro` runtime Docker image.
- **Database volumes** are persisted under `postgres_data/`.
- Make sure your Airflow `Connections` (API + Postgres) are properly set up before running the DAG.

---

## 📚 Useful Links

- [Open Meteo API Documentation](https://open-meteo.com/en/docs)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

## 👨‍💼 Author

- GitHub: [maher24m](https://github.com/maher24m)

---
