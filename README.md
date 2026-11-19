# 🌍 App Atlas – Global App Installs Intelligence Dashboard
## 📌 Project Overview
**App Atlas** is an interactive data analytics dashboard built using Python and Streamlit. It helps users explore Google Play Store application install patterns, category-wise performance, and app statistics through interactive visualizations.
The dashboard provides insights into the top application categories based on total installs, category performance, and other key metrics.
It also includes time-based visualization access, allowing selected analytical charts to be displayed only during a specified time window.
## 🎯 Key Features
- **Interactive Dashboard:** Explore app installation data through a user-friendly interface.
- **Top 5 Categories:** Identify the five eligible categories with the highest total installs.
- **Total Installs:** View the combined installation count across eligible categories.
- **Category Analysis:** Compare category-wise app installation performance.
- **Interactive Charts:** Explore data using bar charts, donut charts, and other visualizations.
- **Time-Based Visualization:** Selected charts are displayed only between 6:00 PM and 8:00 PM IST.
- **CSV Upload:** Upload a custom Google Play Store dataset for analysis.
- **Data Filtering:** Excludes categories beginning with A, C, G, and S from the eligible category analysis.
- **Geographical Insights:** Supports country-level visualizations when a separate country-wise dataset is provided.
## 🛠️ Technologies Used
- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Streamlit Autorefresh
## 📂 Project Structure
```text
Global-Installs-Dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
└── data/
    ├── Play Store Data.csv
    └── country_category_installs.csv  (Optional)
```
## ⚙️ Installation and Execution
### 1. Clone the Repository
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```
### 2. Navigate to the Project Folder
```bash
cd Global-Installs-Dashboard
```
### 3. Create a Virtual Environment
```bash
python -m venv venv
```
### 4. Activate the Virtual Environment

**Windows – Git Bash:**
```bash
source venv/Scripts/activate
```
**Windows – Command Prompt:**
```cmd
venv\Scripts\activate
```
**Windows – PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```
### 5. Install Required Dependencies
```bash
pip install -r requirements.txt
```
### 6. Run the Streamlit Application
```bash
streamlit run app.py
```
### 7. Open the Dashboard
After execution, Streamlit will provide a local URL:

```text
http://localhost:8501
```

Open this URL in your browser to access the dashboard.

## 📊 Dataset Requirements

The primary dataset should contain the following columns:

- `App`
- `Category`
- `Rating`
- `Reviews`
- `Size`
- `Installs`
- `Type`
- `Price`
- `Content Rating`
- `Genres`
- `Last Updated`

The application uses the `Category` and `Installs` columns for its main category-level installation analysis.

### Optional Geographical Dataset

For geographical analysis, provide a separate CSV file containing:

- `Country`
- `Category`
- `Installs`

**Note:** The standard Google Play Store dataset does not contain country-wise installation records. The geographical visualization therefore requires a separate genuine country-level dataset.

## ⏰ Time-Based Visualization

Selected analytical visualizations are available only during:

- **Start Time:** 6:00 PM IST
- **End Time:** 8:00 PM IST

Outside this time window, the dashboard continues to display the overview and other available information, while the restricted visualizations remain hidden.

## ▶️ Execution Commands – Quick Reference

```bash
# Create virtual environment
python -m venv venv

# Activate environment (Git Bash)
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py
```

## 🚀 Deployment

The application can be deployed using Streamlit Community Cloud or another hosting platform that supports Streamlit applications.

For deployment:

1. Push the project files to GitHub.
2. Open your hosting platform.
3. Connect your GitHub repository.
4. Select `app.py` as the application entry point.
5. Deploy the application.

## 👩‍💻 Project Objective

The objective of App Atlas is to transform raw Google Play Store data into meaningful visual insights, helping users understand app installation patterns, category performance, and application trends through interactive data visualization.

---

**Built with Python, Streamlit, Pandas, and Plotly.**
