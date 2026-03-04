# Real-Time Psychological Questionnaire Analysis Dashboard

**Live web app for a clinical psychologist in Prague**  
Automatically fetches, scores, and interprets psychological questionnaires the moment patients submit them.

![Dashboard Overview](images/dashboard-main.png)

## What It Does
Patients fill out standard questionnaires (BDI-II, GAD-7, OCD, CORE-OM, BPD) via Tally.so.  
This dashboard instantly pulls the responses, calculates scores, applies gender-specific percentiles and clinical interpretations, and displays everything in a clean, real-time interface.

The psychologist now gets immediate clinical insights instead of spending hours on manual scoring.

## Key Features
- Real-time updates every 20 seconds
- Full automated scoring + interpretation for 5 clinical questionnaires
- Advanced CORE-OM processing (W/P/F/R categories, gender-specific percentiles, clinical vs non-clinical benchmarks)
- Patient details extraction (name, birth number, insurance code)
- Clickable cards with detailed modal views
- Clean, responsive Streamlit UI

## Screenshots

### Main Dashboard (live view)
![Main Dashboard](images/dashboard-main.png)

### Detail Modals

<div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 12px; margin-top: 20px;">
  <div style="text-align: center; flex: 1; min-width: 280px;">
    <strong>BDI Detail View</strong><br>
    <img src="https://github.com/user-attachments/assets/9fad3997-4957-4758-ba48-8c109b7cde8d" width="300" alt="BDI Example">
  </div>
  <div style="text-align: center; flex: 1; min-width: 280px;">
    <strong>CORE-OM Detail View</strong><br>
    <img src="https://github.com/user-attachments/assets/5c959176-0059-4469-97d3-f5b9d0a99bd9" width="300" alt="CORE-OM Example">
  </div>
  <div style="text-align: center; flex: 1; min-width: 280px;">
    <strong>GAD Detail View</strong><br>
    <img src="https://github.com/user-attachments/assets/b22520be-408a-490d-ac17-4451b819f311" width="300" alt="GAD Example">
  </div>
</div>

## Technologies
- **Python** + **Streamlit**
- Tally.so REST API
- JSON processing & custom scoring algorithms
- Percentile table calculations (clinical & non-clinical)
- Real-time polling

## Impact
- Saves the psychologist **hours of manual work**
- Enables faster and more accurate clinical decision-making
- Production-ready tool actively used in private practice

---

**Built in March 2026** as a freelance project for a clinical psychologist in Prague.

Feel free to reach out if you'd like to see the code or discuss similar projects!
