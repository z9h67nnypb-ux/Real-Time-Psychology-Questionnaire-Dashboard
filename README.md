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

### Individual Submission Cards
![Submission Cards](images/cards-overview.png)

### Detail Modal – BDI Example
![BDI Detail View](images/bdi-detail.png)

### Detail Modal – CORE-OM (with percentiles)
![CORE-OM Detail View](images/coreom-detail.png)

### Detail Modal – GAD Example
![GAD Detail View](images/gad-detail.png)

## Technologies
- **Python** + **Streamlit**
- Tally.so REST API
- JSON processing & custom scoring algorithms
- Percentile table calculations (clinical & non-clinical)
- Real-time polling

## Impact
- Saves the psychologist **several hours of manual work per week**
- Enables faster and more accurate clinical decision-making
- Production-ready tool actively used in private practice

## Repository
https://github.com/YOUR-USERNAME/psych-questionnaire-dashboard

---

**Built in March 2026** as a freelance project for a clinical psychologist in Prague.

Feel free to reach out if you'd like to see the code or discuss similar projects!
