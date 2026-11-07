# 🏏 Cricket Analytics Web Application

A full-stack, responsive Cricket Analytics and Tournament Intelligence application built with **Python, Streamlit, PostgreSQL, Pandas, and Plotly**.

---

## 📖 What the Database is About

The application is powered by the **`cricket_analytics`** PostgreSQL database, a normalized relational system designed to capture real-world cricket operations:

- **Master Tournament Data**: Stores official franchise profiles (10 IPL teams including CSK, MI, RCB, KKR) with coaching staff, home stadiums, and active squad rosters (60 registered athletes with roles, batting styles, and bowling styles).
- **Match Telemetry & Venues**: Tracks tournament fixtures held across 8 iconic international stadiums, capturing match formats (`T20`), dates, participating home/away teams, and match outcomes.
- **Innings & Performance Breakdown**: Records two sequential innings per limited-overs fixture, including team totals, wickets lost, overs played, and granular individual batting, bowling, and fielding scorecards.
- **Ball-by-Ball Event Telemetry**: Logs discrete delivery-level data (over number, ball number, batter runs, extras, and dismissal events) for in-depth phase-by-phase cricket analytics.

> **Note on Technical Database Documentation**:
> All detailed technical specifications—including relational schemas, attribute dictionaries, 3NF normalization proofs, cardinalities, participation constraints (total vs. partial), database triggers, and the complete Crow's Foot ER diagram—are documented in the official project report PDF:
> 👉 **[`database_documentation/Cricket_Analytics_Project_Report.pdf`](./database_documentation/Cricket_Analytics_Project_Report.pdf)**

---

## 📂 Project File Structure

```text
Cricket_v2/
├── .env                              # Local database credentials (ignored by Git)
├── .env.example                      # Template for database credentials
├── requirements.txt                  # Python package dependencies
├── config.py                         # Environment configuration & settings
├── database.py                       # Safe parameterized query runner & connection manager
├── queries.py                        # Comprehensive SQL queries and database views
├── app.py                            # Main Streamlit application entrypoint
├── README.md                         # Project overview, file structure & run guide
├── components/                       # Reusable UI & navigation components
│   ├── __init__.py
│   ├── navbar.py                     # Top horizontal navigation bar & state router
│   └── ui_cards.py                   # Custom CSS, KPI cards, badges, and layout helpers
├── views/                            # Application view modules
│   ├── __init__.py
│   ├── home.py                       # Home Dashboard view
│   ├── search.py                     # Global Search view
│   ├── match_centre.py               # Match Centre & detailed scorecards
│   ├── player_profile.py             # Player Profiles & performance charts
│   ├── teams.py                      # Team Pages & squad rosters
│   └── analytics.py                  # Player/team comparisons & leaderboards
├── database/                         # Relational database scripts (DDL, DML, Views, Triggers)
│   ├── 01_create_database.sql        # Database initialization script
│   ├── 02_create_tables.sql          # 9 core tables (PKs, FKs, CHECK constraints)
│   ├── 03_insert_sample_data.sql     # ~515 realistic IPL records
│   ├── 04_create_views.sql           # 10 tournament analytical views
│   ├── 05_create_triggers.sql        # 4 PL/pgSQL domain triggers
│   └── setup_all.sql                 # Master execution script for psql
└── database_documentation/           # Academic report and high-resolution schema diagram
    ├── Cricket_Analytics_Project_Report.pdf  # 8-page academic report (Times New Roman, monochrome)
    ├── Cricket_Analytics_ER_Diagram.png      # 7170x4770 px (300 DPI) Crow's Foot ER diagram
    ├── generate_pdf_report.py                # Report generation script (fpdf2)
    └── generate_er_diagram.py                # ER diagram generation script (matplotlib)
```

---

## 💻 How to Run the Application Locally

Follow these step-by-step instructions to set up and run the application on your computer (**Windows, macOS, or Linux**).

### 1. Prerequisites
- **Python**: Version 3.10 or 3.11 installed.
- **PostgreSQL**: Version 14 or higher installed and running.

---

### Step 1: Open the Project Directory
Open your terminal (PowerShell, Command Prompt, or bash) and navigate to the project directory:

```bash
cd Cricket_v2
```

---

### Step 2: Initialize the PostgreSQL Database

Ensure your local PostgreSQL server is running. If setting up on a fresh machine, create and populate the database using either **Method A** or **Method B**:

#### Method A: Using Command Line (`psql`)
```bash
psql -U postgres -f database/setup_all.sql
```
*(Enter your PostgreSQL superuser password when prompted).*

#### Method B: Using `pgAdmin 4`
1. Open **pgAdmin 4** and connect to your local PostgreSQL server.
2. Right-click **Databases** -> **Create** -> **Database...** -> Name it `cricket_analytics`.
3. Select `cricket_analytics`, open the **Query Tool**, and run the SQL scripts in `database/` in this exact sequence (**F5**):
   1. `02_create_tables.sql` (Creates 9 tables)
   2. `03_insert_sample_data.sql` (Inserts ~515 sample records)
   3. `04_create_views.sql` (Creates 10 analytical views)
   4. `05_create_triggers.sql` (Creates 4 domain triggers)

---

### Step 3: Configure Environment Credentials (`.env`)

Copy the provided `.env.example` template to create your local `.env` file:

- **Windows (PowerShell)**:
  ```powershell
  Copy-Item .env.example .env
  ```
- **macOS / Linux**:
  ```bash
  cp .env.example .env
  ```

Open `.env` in any text editor and update `DB_PASSWORD` with your local PostgreSQL password:

```ini
# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cricket_analytics
DB_USER=postgres
DB_PASSWORD=your_actual_postgres_password
```

---

### Step 4: Set Up a Python Virtual Environment (Recommended)

#### On Windows:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

#### On macOS / Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

---

### Step 5: Install Python Dependencies

Install the required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### Step 6: Launch the Web Application

Start the Streamlit development server:

```bash
streamlit run app.py
```

The application will launch and automatically open in your default browser at:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## ❓ Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| **`Database Connection Error: connection failed`** | PostgreSQL service stopped or port incorrect | Verify PostgreSQL is running and check `DB_PORT=5432` in `.env`. |
| **`password authentication failed for user "postgres"`** | Incorrect password in `.env` | Update `DB_PASSWORD` in `.env` with the password set during PostgreSQL installation. |
| **`Port 8501 is already in use`** | Another Streamlit instance is running | Run on a different port: `streamlit run app.py --server.port 8502`. |
| **`ModuleNotFoundError: No module named 'psycopg'`** | Dependencies not installed in active environment | Ensure virtual environment is activated (`venv\Scripts\activate`) and re-run `pip install -r requirements.txt`. |
| **`relation "..." does not exist`** | Tables not created in `cricket_analytics` | Ensure you ran the SQL scripts in the `cricket_analytics` database, not the default `postgres` database. |
#   C r i c k e t - a n a l y s i s  
 