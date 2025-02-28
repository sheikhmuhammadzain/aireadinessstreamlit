# AI Readiness Assessment Application

This Streamlit application helps organizations assess their readiness for AI adoption across multiple dimensions:

- AI Governance
- AI Culture
- AI Data
- AI Infrastructure
- AI Strategy
- AI Talent

## Features

- Comprehensive questionnaire covering all aspects of AI readiness
- Interactive UI with sliders for easy response input
- Automatic calculation of readiness scores using Q-learning algorithm
- Visualizations including radar charts and bar graphs
- Detailed results for each assessment category
- Personalized recommendations for improvement

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:

```bash
streamlit run ai_readiness_assessment_app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## How to Use

1. Navigate through each assessment category tab
2. Answer all questions using the sliders (1 = Strongly Disagree, 4 = Strongly Agree)
3. Click "Submit Assessment" when finished
4. View your results and recommendations in the Results page

## Technical Details

- The application uses Q-learning, a reinforcement learning technique, to weight different assessment categories
- Scores are normalized and presented as percentages for easy interpretation
- The radar chart provides a visual overview of readiness across all dimensions
- Detailed breakdowns are available for each assessment category

## Requirements

- Python 3.7+
- Streamlit 1.31.0+
- NumPy
- Pandas
- Plotly
