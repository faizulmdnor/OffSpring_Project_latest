
# 🏫 OffSpring Academic Record Management System

A web-based academic record management system built using **Flask**, **Pandas**, and **SQL Server** via **pyodbc**. This system manages students, teachers, schools, classes, exams, subjects, schedules, results, and feedback.

---

## 📌 Features

### 🔹 Student Management
- View and edit student profiles
- Calculate and display student age
- Manage academic history (classes, school year)

### 🔹 School Administration
- Add/edit/delete schools, classes, and teachers
- Assign teachers and schools to classes

### 🔹 Exam & Subject Management
- Create and manage exams
- Register subjects for each exam
- Schedule subject-specific exam dates

### 🔹 Results & Analysis
- Insert and update exam marks
- View result summaries (total, average, percentage)
- Add qualitative comments per exam
- Perform analysis and reporting

---

## 🛠 Tech Stack

| Component        | Technology     |
|------------------|----------------|
| Backend          | Flask (Python) |
| Data Processing  | Pandas         |
| Database         | SQL Server     |
| ORM Layer        | Custom (via `sql_offsprings`) |
| UI               | HTML + Jinja Templates |
| Other Packages   | `dateutil`, `pyodbc`, `logging` |

---

## 📁 Project Structure

```
OffSpring_Project/
│
├── templates/                     # HTML Templates
│   └── *.html
│
├── static/                        # Static assets (if any)
│
├── OffSprings_DB.py              # Custom DB utility class
├── app.py                        # Main Flask application
├── requirements.txt              # List of Python dependencies
└── README.md                     # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/faizulmdnor/OffSpring_Project_latest.git
cd OffSpring_Project_latest
```

### 2. Set up a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # on Linux/Mac
venv\Scripts\activate     # on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Update the `sql_offsprings` class in `OffSprings_DB.py` with your SQL Server connection string.

```python
# Example connection string
self.conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=your_server;"
    "DATABASE=OffSprings;"
    "UID=your_user;"
    "PWD=your_password"
)
```

Ensure the required views and tables (e.g. `vw_offsprings_details`, `vw_peperiksaan`, etc.) exist in your database.

### 5. Run the app

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## ✅ Routes Overview

| URL | Function |
|-----|----------|
| `/` | Home page with student list |
| `/persekolahan` | Manage student's academic year/class |
| `/tambah_sekolah`, `/edit_sekolah/<id>` | Manage schools |
| `/tambah_guru`, `/edit_guru/<id>` | Manage teachers |
| `/tambah_kelas`, `/edit_kelas/<id>` | Manage classes |
| `/peperiksaan`, `/add_peperiksaan`, `/edit_peperiksaan/<id>` | Exam CRUD |
| `/add_subject`, `/daftar_subjek/<id>` | Subject registration |
| `/view_results/<id>` | View exam result summary |
| `/insert_exam_results`, `/edit_exam_results`, `/delete_exam_result` | Marks entry |
| `/add_jadual`, `/edit_jadual` | Exam scheduling |
| `/add_comments`, `/edit_comments` | Feedback/comments |

---

## 🧪 Sample SQL Objects (Required Views)

Please ensure your DB contains these views and tables:
- `vw_offsprings_details`
- `vw_persekolahan`
- `vw_keputusan_peperiksaan`
- `vw_analisa_keputusan`
- `vw_peperiksaan`
- `vw_daftar_peperiksaan`

You can adjust the SQL logic in `OffSprings_DB.py` if your schema is different.

---

## 📧 Contact

Created by [Faizul Md Nor](https://github.com/faizulmdnor)  
For inquiries, suggestions or collaboration — feel free to reach out.

---

## 📜 License

This project is open-sourced under the [MIT License](LICENSE).
