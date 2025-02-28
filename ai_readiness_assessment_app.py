import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import io
import os
import re
import json
from PIL import Image
from helper_functions import get_color_for_score, get_strength_comment, get_improvement_comment, get_recommendations
from visualization_functions import create_radar_chart, create_gauge_chart, create_bar_chart
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import base64
from io import BytesIO
from matplotlib.colors import LinearSegmentedColormap

# Set page configuration
st.set_page_config(
    page_title="Enterprise AI Readiness Assessment",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to style buttons
st.markdown("""
<style>
/* General button styling */
button, .stButton>button, div.stButton>button, .stButton>button:focus, .stButton>button:active {
    background-color: #0284C7 !important;
    color: #FFFFFF !important;
    border: none !important;
}

/* Make sure hover states maintain styling */
.stButton>button:hover {
    background-color: #0369a1 !important;
    color: #FFFFFF !important;
}

/* Target primary buttons specifically */
button[kind="primary"], 
div[data-testid="stButton"] button {
    background-color: #0284C7 !important;
    color: #FFFFFF !important;
    font-weight: 500 !important;
}

/* Target "Start Assessment" and "Generate PDF Report" buttons specifically */
.element-container:has(button:contains("Start Assessment")) button, 
.element-container:has(button:contains("Generate PDF Report")) button {
    background-color: #0284C7 !important; 
    color: #FFFFFF !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# Define color theme for the app - enterprise palette
theme_colors = {
    'primary': '#1E293B',     # Slate 800
    'secondary': '#475569',   # Slate 600
    'accent': '#0284C7',      # Sky 600
    'success': '#059669',     # Emerald 600
    'warning': '#D97706',     # Amber 600
    'error': '#EF4444',       # Red 600
    'background': '#F8FAFC',  # Slate 50
    'card': '#FFFFFF',        # White
    'text': '#334155',        # Slate 700
    'muted': '#94A3B8',       # Slate 400
    'border': '#E2E8F0',      # Slate 200
    'highlight': '#EFF6FF',   # Blue 50
}

# Add custom CSS for enterprise-level design
st.markdown("""
<style>
    /* Google Fonts - Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Base styles */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Global typography */
    html, body, p, div, h1, h2, h3, h4, h5, h6, li, span {
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        font-size: 2rem;
        font-weight: 700;
        color: #1E293B;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E293B;
        letter-spacing: -0.01em;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1E293B;
        margin-top: 0.75rem;
        margin-bottom: 0.5rem;
    }
    
    h4 {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1E293B;
        margin-top: 0.5rem;
        margin-bottom: 0.25rem;
    }
    
    p, li {
        font-size: 0.9375rem;
        line-height: 1.5;
        color: #334155;
        margin-top: 0.25rem;
        margin-bottom: 0.25rem;
    }
    
    /* Container refinements */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] a, [data-testid="stSidebar"] label {
        color: #1E293B !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #1E293B !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] [data-testid="stImage"] {
        margin-bottom: 1.5rem;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 0.375rem;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
        background-color: #1E293B !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton button:focus {
        box-shadow: none;
    }
    
    .stButton button:hover {
        opacity: 0.9;
        background-color: #334155 !important;
    }
    
    /* Make text white on red buttons */
    .stButton button[style*="background-color: #EF4444"], 
    .stButton button[style*="background-color: rgb(239, 68, 68)"] {
        color: white !important;
    }
    
    /* Dashboard metrics */
    .metric-card {
        padding: 1rem;
        border-radius: 0.375rem;
        text-align: center;
        background: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0284C7;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.025em;
        font-weight: 500;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 0.9375rem;
        font-weight: 600;
        color: #1E293B;
        background-color: #F8FAFC;
        border-radius: 0.25rem;
        padding: 0.75rem 1rem;
        border: 1px solid #E2E8F0;
    }
    
    .streamlit-expanderContent {
        border: 1px solid #E2E8F0;
        border-top: none;
        padding: 1rem;
        border-radius: 0 0 0.25rem 0.25rem;
    }
    
    /* Radio button & checkbox styling */
    .stRadio > div {
        margin-top: 0.25rem;
        margin-bottom: 0.25rem;
    }
    
    .stRadio label {
        font-size: 0.875rem;
        padding: 0.25rem 0;
        color: #334155;
    }
    
    /* Input widgets */
    .stSelectbox > div > div, .stNumberInput > div > div {
        padding: 0.25rem 0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.125rem;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.25rem 0.25rem 0 0;
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
        font-weight: 500;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        font-weight: 600;
        color: #0284C7;
        border-bottom: 2px solid #0284C7;
    }
    
    /* Dataframe styling */
    .dataframe {
        border: none;
        font-size: 0.875rem;
    }
    
    .dataframe th {
        font-weight: 600;
        border-bottom: 1px solid #E2E8F0;
        background-color: #F8FAFC;
    }
    
    .dataframe td {
        border-bottom: 1px solid #E2E8F0;
    }
    
    /* Alert/info boxes */
    .stAlert {
        padding: 0.75rem 1rem;
        border-radius: 0.25rem;
        border-left: 3px solid;
    }
    
    .stAlert[data-baseweb="notification"] {
        background-color: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .stAlert div[data-testid="stImage"] {
        margin-right: 0.75rem;
    }
    
    /* Fix for checkbox alignment */
    .stCheckbox > div {
        align-items: center;
    }
    
    /* Remove padding from st.columns */
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Footer refinement */
    footer {
        display: none;
    }
    
    /* Custom question card */
    .question-card {
        background-color: white;
        border-radius: 0.375rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        position: relative;
        border-left: 4px solid #0284C7;
    }
    
    .question-card h3 {
        margin-top: 0;
        font-size: 1.25rem;
        color: #1E293B;
    }
    
    .question-card p {
        margin-bottom: 1.25rem;
        color: #1E293B;
    }
    
    .question-number {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background-color: #0284C7;
        color: white;
        width: 2rem;
        height: 2rem;
        border-radius: 9999px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
    }
    
    /* Option styling */
    .option-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #334155;
        padding: 0.25rem 0;
    }
    
    /* Progress indicator */
    .progress-container {
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 0.5rem;
        background-color: #E2E8F0;
        border-radius: 1rem;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%);
        border-radius: 1rem;
    }
    
    /* Section divider */
    .divider {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background-color: #E2E8F0;
    }
    
    /* Data visualization container */
    .viz-container {
        background-color: white;
        border-radius: 0.375rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
    }
    
    .viz-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E2E8F0;
    }
    
    /* Executive dashboard styling */
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .dashboard-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1E293B;
    }
    
    .dashboard-subtitle {
        font-size: 0.875rem;
        color: #64748B;
    }
    
    /* KPI indicators */
    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .kpi-card {
        flex: 1;
        min-width: 150px;
        background: white;
        border-radius: 0.375rem;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
    }
    
    .kpi-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0284C7;
        margin: 0.25rem 0;
    }
    
    .kpi-label {
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    /* Category header */
    .category-header {
        margin-bottom: 1rem;
    }
    
    /* Subcategory header */
    .subcategory-header {
        margin-bottom: 0.5rem;
    }
    
    /* Question number */
    .question-number {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748B;
        margin-bottom: 0.25rem;
    }
    
    /* Question divider */
    .question-divider {
        margin: 1rem 0;
        opacity: 0.2;
    }
    
    /* Submit container */
    .submit-container {
        text-align: center;
        margin-top: 2rem;
    }
    
    .submit-message {
        font-size: 0.875rem;
        color: #64748B;
        margin-bottom: 0.5rem;
    }
    
    /* Feature cards */
    .feature-card {
        background-color: white;
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 0.375rem;
        background-color: #0284C7;
        color: white;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        font-size: 0.875rem;
        color: #64748B;
        line-height: 1.5;
    }
    
    /* Card styling - enterprise level */
    .card {
        background-color: white;
        border-radius: 0.375rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        transition: all 200ms ease;
    }
    
    .card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.02);
    }
    
    .card h1, .card h2, .card h3, .card h4 {
        color: #1E293B;
        margin-top: 0;
    }
    
    .card p {
        color: #1E293B;
        margin-bottom: 0;
    }
    
    .card.primary {
        background-color: #0284C7;
        border: none;
    }
    
    .card.primary h1, .card.primary h2, .card.primary h3, .card.primary h4, .card.primary p {
        color: white;
    }
    
    .card.success {
        background-color: #10B981;
        border: none;
    }
    
    .card.success h1, .card.success h2, .card.success h3, .card.success h4, .card.success p {
        color: white;
    }
    
    .card.warning {
        background-color: #F59E0B;
        border: none;
    }
    
    .card.warning h1, .card.warning h2, .card.warning h3, .card.warning h4, .card.warning p {
        color: #1E293B;
    }
    
    .card.error {
        background-color: #EF4444;
        border: none;
    }
    
    .card.error h1, .card.error h2, .card.error h3, .card.error h4, .card.error p {
        color: white;
    }
    
    .card.info {
        background-color: #0284C7;
        border: none;
    }
    
    .card.info h1, .card.info h2, .card.info h3, .card.info h4, .card.info p {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Add custom CSS for enhanced styling
st.markdown("""
<style>
    /* Google Fonts - Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Color palette */
    :root {
        --primary: #0284C7;
        --primary-light: #EFF6FF;
        --secondary: #475569;
        --accent: #10B981;
        --background: #F8FAFC;
        --card-bg: #FFFFFF;
        --text-primary: #1E293B;
        --text-secondary: #64748B;
        --border: #E2E8F0;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --button-bg: #EF4444;
        --button-text: #FFFFFF;
    }
    
    /* Global styles */
    .stApp {
        background-color: var(--background);
    }
    .stButton > button p { color: white !important; }
.stButton > button * { color: white !important; }
button p { color: white !important; }
        
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    h1 {
        font-size: 1.875rem;
        letter-spacing: -0.025em;
    }
    
    h2 {
        font-size: 1.5rem;
        letter-spacing: -0.025em;
    }
    
    h3 {
        font-size: 1.25rem;
    }
    
    p {
        color: var(--text-secondary);
        line-height: 1.5;
        font-size: 0.875rem;
    }
    
    /* Dashboard header */
    .dashboard-header {
        margin-bottom: 1.5rem;
    }
    
    .dashboard-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .dashboard-subtitle {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    /* Cards */
    .card {
        background-color: var(--card-bg);
        border-radius: 0.5rem;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        border: 1px solid var(--border);
        transition: all 200ms ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .card h1, .card h2, .card h3, .card h4 {
        color: var(--text-primary);
        margin-top: 0;
    }
    
    .card p {
        color: var(--text-primary);
        margin-bottom: 0;
    }
    
    .card.primary {
        border-left: 4px solid var(--primary);
    }
    
    .card.success {
        border-left: 4px solid var(--success);
    }
    
    .card.warning {
        border-left: 4px solid var(--warning);
    }
    
    .card.error {
        border-left: 4px solid var(--error);
    }
    
    .card.info {
        background-color: var(--primary-light);
        border: none;
    }
    
    /* Sidebar */
    .css-1cypcdb, .css-1rs6os {
        background: linear-gradient(180deg, #0C4A6E 0%, #0284C7 100%);
        color: white;
    }
    
    /* Question card */
    .question-card {
        background-color: var(--card-bg);
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-radius: 0.375rem;
        border: 1px solid var(--border);
    }
    
    .question-text {
        font-size: 0.9375rem;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
        font-weight: 500;
    }
    
    .question-title {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-bottom: 0.375rem;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    /* Category header */
    .category-header {
        margin-bottom: 1rem;
    }
    
    /* Subcategory header */
    .subcategory-header {
        margin-bottom: 0.5rem;
    }
    
    /* Question number */
    .question-number {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748B;
        margin-bottom: 0.25rem;
    }
    
    /* Question divider */
    .question-divider {
        margin: 1rem 0;
        opacity: 0.2;
    }
    
    /* Submit container */
    .submit-container {
        text-align: center;
        margin-top: 2rem;
    }
    
    .submit-message {
        font-size: 0.875rem;
        color: #64748B;
        margin-bottom: 0.5rem;
    }
    
    /* Progress bar */
    .progress-container {
        margin-bottom: 1.5rem;
    }
    
    .progress-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.25rem;
    }
    
    .progress-header span {
        font-size: 0.75rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    .progress-percentage {
        color: var(--primary) !important;
        font-weight: 600 !important;
    }
    
    .progress-bar {
        height: 0.5rem;
        background-color: #E2E8F0;
        border-radius: 9999px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background-color: var(--primary);
        border-radius: 9999px;
        transition: width 0.3s ease;
    }
    
    /* Option label */
    .option-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    /* Custom radio buttons */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .stRadio label {
        display: flex;
        align-items: center;
        padding: 0.5rem 0.75rem;
        border: 1px solid var(--border);
        border-radius: 0.375rem;
        transition: all 0.15s ease;
        background-color: white;
    }
    
    .stRadio label:hover {
        background-color: var(--primary-light);
        border-color: var(--primary);
    }
    
    .stRadio [data-baseweb="radio"] {
        margin-right: 0.5rem;
    }
    
    /* Selected radio button */
    .stRadio [aria-checked="true"] {
        background-color: var(--primary-light);
        border-color: var(--primary);
        font-weight: 500;
    }
    
    /* Feature cards */
    .feature-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid var(--border);
        transition: all 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    .feature-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 0.375rem;
        background-color: var(--primary-light);
        color: var(--primary);
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        font-size: 0.875rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    
    /* Card styling - enterprise level */
    .card {
        background-color: white;
        border-radius: 0.375rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        transition: all 200ms ease;
    }
    
    .card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.02);
    }
    
    .card h1, .card h2, .card h3, .card h4 {
        color: #1E293B;
        margin-top: 0;
    }
    
    .card p {
        color: #1E293B;
        margin-bottom: 0;
    }
    
    .card.primary {
        background-color: #0284C7;
        border: none;
    }
    
    .card.primary h1, .card.primary h2, .card.primary h3, .card.primary h4, .card.primary p {
        color: white;
    }
    
    .card.success {
        background-color: #10B981;
        border: none;
    }
    
    .card.success h1, .card.success h2, .card.success h3, .card.success h4, .card.success p {
        color: white;
    }
    
    .card.warning {
        background-color: #F59E0B;
        border: none;
    }
    
    .card.warning h1, .card.warning h2, .card.warning h3, .card.warning h4, .card.warning p {
        color: #1E293B;
    }
    
    .card.error {
        background-color: #EF4444;
        border: none;
    }
    
    .card.error h1, .card.error h2, .card.error h3, .card.error h4, .card.error p {
        color: white;
    }
    
    .card.info {
        background-color: #0284C7;
        border: none;
    }
    
    .card.info h1, .card.info h2, .card.info h3, .card.info h4, .card.info p {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Define the questionnaire categories and their files
questionnaire_files = {
    "AI Governance": "ai-governance-scoring-with-qlearning-questionnaire.py",
    "AI Culture": "culture-scoring-with-qlearning-questionnaire.py",
    "AI Data": "data-scoring-with-qlearning-questionnaire.py",
    "AI Infrastructure": "infra-scoring-with-qlearning-questionnaire.py",
    "AI Strategy": "strategy-scoring-with-qlearning-questionnaire.py",
    "AI Talent": "talen-scoring-with-qlearning-questionnaire.py"
}

# Fallback questionnaires in case file parsing fails
fallback_questionnaires = {
    "AI Governance": {
        "AI Roles & Responsibilities": [
            "Do you have policies for ethical AI development?",
            "Are all stakeholders educated on AI governance policies?",
            "Do you have regular AI governance board meetings?",
            "Is algorithmic accountability explicitly assigned?"
        ],
        "Regulatory Compliance": [
            "Does your AI system comply with GDPR, EU AI Act, ISO 42001, or other laws?",
            "Are your AI policies updated with changing regulations?",
            "Do you evaluate third-party AI tools for compliance risks?",
            "Do you adhere to AI transparency standards globally?",
            "Is your organization part of any AI governance consortiums?",
            "Do you engage in forums to influence AI policymaking?"
        ],
        "Bias & Fairness Mitigation": [
            "Do you actively monitor and reduce bias in AI models?",
            "Is there a mechanism to validate fairness in AI outcomes?",
            "Do you have bias mitigation mechanisms for deployed AI models?",
            "Are your governance measures tailored for AI's unique challenges?"
        ],
        "AI Transparency & Explainability": [
            "Are AI decisions interpretable, auditable, and well-documented?",
            "Are your AI algorithms subject to peer review before deployment?",
            "Do you maintain an audit trail for AI decisions?",
            "Do you employ explainable AI techniques to enhance transparency?",
            "How mature is your AI governance framework?"
        ],
        "AI Risk Management": [
            "Do you have a structured AI risk assessment framework?",
            "Are external audits conducted on AI systems?",
            "Is there a whistleblowing mechanism for unethical AI use?",
            "How regularly are your AI governance policies reviewed?"
        ]
    },
    "AI Culture": {
        "AI Leadership & Vision": [
            "Does the organization have a clear AI strategy?",
            "Is there an AI champions program in your organization?",
            "Do you integrate AI into day-to-day organizational workflows?"
        ],
        "AI Experimentation & Innovation": [
            "Are AI pilots and innovation hubs encouraged?",
            "Do you celebrate AI project milestones publicly?",
            "Do you have a platform for sharing AI-related innovations?",
            "Is there a culture of experimentation for AI adoption?"
        ],
        "Cross-Functional AI Collaboration": [
            "Are employees receiving AI upskilling?",
            "How open are employees to learning about AI?",
            "Do employees feel supported during AI-driven organizational changes?",
            "Do you measure the sentiment toward AI across teams?"
        ],
        "AI Change Management": [
            "Are AI adoption challenges being actively addressed?",
            "Do employees feel supported during AI-driven organizational changes?"
        ]
    }
}

# Helper function to convert matplotlib fig to a format Streamlit can display
def matplotlib_to_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{img_str}"

# Function to create a premium-looking radar chart with matplotlib
def create_radar_chart(categories, values, title):
    # Convert values to 0-100 scale
    values_100 = [v * 100 / 4 for v in values]
    
    # Number of categories
    N = len(categories)
    
    # Create angles for each category (in radians)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Values also need to close the loop
    values_100_closed = values_100 + values_100[:1]
    
    # Create figure and polar axis
    plt.figure(figsize=(10, 8), facecolor='white')
    ax = plt.subplot(111, polar=True)
    
    # Set background color
    ax.set_facecolor('#F8F9FA')
    
    # Draw grid lines with custom style
    plt.grid(color='gray', alpha=0.15)
    
    # Plot data
    ax.plot(angles, values_100_closed, 'o-', linewidth=2.5, color=theme_colors["primary"], 
            markersize=10, markerfacecolor=theme_colors["secondary"], markeredgecolor=theme_colors["primary"])
    
    # Fill area
    ax.fill(angles, values_100_closed, alpha=0.25, color=theme_colors["secondary"])
    
    # Set radar chart axis limits
    ax.set_ylim(0, 100)
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
    
    # Add a title
    plt.title(title, fontsize=16, fontweight='bold', pad=20, color=theme_colors["primary"])
    
    # Add score labels at each point
    for angle, value in zip(angles[:-1], values_100):
        ax.text(angle, value + 5, f"{value:.1f}%", 
                ha='center', va='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor=theme_colors["primary"]))
    
    # Adjust radial axes
    ax.set_rgrids([20, 40, 60, 80, 100], angle=45, fontsize=9)
    
    # Convert to image
    img = matplotlib_to_image(plt)
    plt.close()
    
    return img

# Function to create a bar chart with matplotlib for category scores
def create_category_bar_chart(categories, scores, title):
    # Set seaborn style
    sns.set_style("whitegrid")
    
    # Create a color gradient
    colors = sns.color_palette("Blues_r", len(categories))
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    
    # Create horizontal bar chart
    bars = ax.barh(categories, [score * 100 / 4 for score in scores], color=colors, height=0.6)
    
    # Add data labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f"{width:.1f}%", 
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    # Set chart title and labels
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color=theme_colors["primary"])
    ax.set_xlabel('Score (%)', fontsize=12, fontweight='bold', labelpad=10)
    
    # Customize grid
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Set x-axis limits
    ax.set_xlim(0, 105)
    
    # Add a subtle background color to the y-axis labels for better readability
    for i, label in enumerate(ax.get_yticklabels()):
        label.set_fontweight('bold')
        if i % 2 == 0:
            label.set_backgroundcolor("#F8F9FA")
    
    # Convert to image
    img = matplotlib_to_image(fig)
    plt.close()
    
    return img

# Function to create a heatmap for Q-values and weights
def create_qvalue_weight_heatmap(categories, q_values, weights, title):
    # Prepare data for heatmap
    data = []
    for category, q_val, weight in zip(categories, q_values, weights):
        data.append({
            'Category': category,
            'Q-Value': q_val,
            'Weight (%)': weight * 100
        })
    
    df = pd.DataFrame(data)
    
    # Set seaborn style
    sns.set_style("white")
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, len(categories) * 0.8 + 2), facecolor='white')
    
    # Create a heatmap for Q-values
    sns.heatmap(df.set_index('Category')[['Q-Value']], annot=True, cmap='Blues', fmt='.3f', 
                linewidths=1, ax=ax1, cbar=True, cbar_kws={"shrink": 0.8})
    ax1.set_title('Q-Values after Learning', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('')
    ax1.set_ylabel('')
    
    # Create a heatmap for weights
    sns.heatmap(df.set_index('Category')[['Weight (%)']], annot=True, cmap='Greens', fmt='.1f', 
                linewidths=1, ax=ax2, cbar=True, cbar_kws={"shrink": 0.8})
    ax2.set_title('Softmax Weights (%)', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('')
    ax2.set_ylabel('')
    
    # Set overall title
    fig.suptitle(title, fontsize=16, fontweight='bold', color=theme_colors["primary"], y=0.98)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Convert to image
    img = matplotlib_to_image(fig)
    plt.close()
    
    return img

# Function to create a gauge chart for the overall score
def create_gauge_chart(score, title):
    # Configure the figure
    fig = plt.figure(figsize=(10, 6), facecolor='white')
    ax = fig.add_subplot(111)
    
    # Hide axes
    ax.set_axis_off()
    
    # Set score (0-100 scale)
    score_100 = score * 100 / 4
    
    # Define gauge colors and ranges
    cmap = LinearSegmentedColormap.from_list('gauge_colors', ['#FF5252', '#FFAB40', '#FFEE58', '#66BB6A'])
    norm = mpl.colors.Normalize(vmin=0, vmax=100)
    
    # Create the gauge background
    theta = np.linspace(3*np.pi/4, 9*np.pi/4, 100)
    radius = 1.0
    
    # Draw the gauge outline
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color='black', linewidth=2.5)
    
    # Draw colored segments
    for t in np.linspace(3*np.pi/4, 9*np.pi/4, 100):
        segment_value = 100 * (t - 3*np.pi/4) / (6*np.pi/4)
        color = cmap(norm(segment_value))
        segment_width = 0.1
        ax.plot([radius * np.cos(t), (radius - segment_width) * np.cos(t)],
                [radius * np.sin(t), (radius - segment_width) * np.sin(t)],
                color=color, linewidth=3)
    
    # Draw segment labels
    labels = ["Low", "Moderate", "High", "Excellent"]
    positions = [15, 45, 70, 90]
    for i, label in enumerate(labels):
        angle = 3*np.pi/4 + (positions[i] / 100) * (6*np.pi/4)
        ax.text(angle, radius + 0.1, label, 
                ha='center', va='center', fontsize=10, 
                color='#475569', fontweight='medium',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor=theme_colors["primary"]))
    
    # Draw tick marks
    for value, angle in zip([0, 25, 50, 75, 100], [3*np.pi/4, 3*np.pi/4 + (25/100) * (6*np.pi/4), 3*np.pi/4 + (50/100) * (6*np.pi/4), 3*np.pi/4 + (75/100) * (6*np.pi/4), 9*np.pi/4]):
        ax.text(0.95 * np.cos(angle), 0.95 * np.sin(angle), f"{value}%", 
                ha='center', va='center', fontsize=9)
    
    # Draw the needle
    needle_angle = 3*np.pi/4 + (score_100/100) * (6*np.pi/4)
    ax.plot([0, 0.7 * np.cos(needle_angle)], [0, 0.7 * np.sin(needle_angle)], 
            color='#E53935', linewidth=4)
    
    # Draw the center circle
    circle = plt.Circle((0, 0), 0.1, color='#E53935', fill=True)
    ax.add_patch(circle)
    
    # Add score text in the center
    ax.text(0, -0.2, f"{score_100:.1f}%", ha='center', va='center', 
            fontsize=24, fontweight='bold', color='#212121')
    
    # Add title
    ax.text(0, -0.5, title, ha='center', va='center', 
            fontsize=16, fontweight='bold', color=theme_colors["primary"])
    
    # Set limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    
    # Convert to image
    img = matplotlib_to_image(fig)
    plt.close()
    
    return img

# Function to extract questionnaire data directly from a Python file
def extract_questionnaire_data(file_path):
    # Initial questionnaire structure
    questionnaire = {}
    
    try:
        # Try with utf-8 encoding first
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # Fall back to latin-1 if utf-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()
    
    # Extract categories using a simpler approach
    lines = content.split('\n')
    current_category = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Find the start of questionnaire definition
        if line.startswith("questionnaire = {"):
            continue
            
        # Find category lines
        if ":" in line and "[" in line and not line.startswith("#"):
            # Extract category name
            category_name = line.split(":")[0].strip().strip('"\'')
            if category_name:
                current_category = category_name
                questionnaire[current_category] = []
        
        # Find question lines when we have a current category
        elif current_category and '"' in line and "," in line and not line.startswith("#"):
            # Extract question text
            question_start = line.find('"')
            question_end = line.rfind('"')
            if question_start != -1 and question_end != -1 and question_end > question_start:
                question = line[question_start+1:question_end]
                questionnaire[current_category].append(question)
        
        # End of category or questionnaire
        elif line.startswith("],") or line.startswith("}"):
            current_category = None
    
    return questionnaire

# Function to load all questionnaires
def load_all_questionnaires():
    all_questionnaires = {}
    for category, file_name in questionnaire_files.items():
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        questionnaire = extract_questionnaire_data(file_path)
        if questionnaire:
            all_questionnaires[category] = questionnaire
    
    # If no questionnaires were loaded, use fallback
    if not all_questionnaires:
        st.warning("Could not load questionnaires from files. Using embedded questionnaires.")
        all_questionnaires = fallback_questionnaires
    
    return all_questionnaires

# Function to calculate scores using Q-learning
def calculate_scores(responses):
    category_scores = {}
    q_values = {}
    softmax_weights = {}
    overall_scores = {}
    
    # For each assessment category (Governance, Culture, etc.)
    for assessment_category, assessment_data in responses.items():
        # Initialize category scores for this assessment
        category_scores[assessment_category] = {}
        
        # Calculate mean score for each question category
        for question_category, answers in assessment_data.items():
            if answers:  # Only calculate if there are answers
                category_scores[assessment_category][question_category] = np.mean(answers)
        
        # Initialize Q-values for this assessment
        q_values[assessment_category] = {cat: np.random.uniform(0, 1) for cat in assessment_data.keys()}
        
        # Q-learning parameters
        alpha = 0.1  # Learning rate
        gamma = 0.9  # Discount factor
        reward = 1  # Assume a reward of 1 for simplicity
        
        # Update Q-values
        for _ in range(10):
            for cat in assessment_data.keys():
                if cat in q_values[assessment_category]:
                    q_values[assessment_category][cat] = q_values[assessment_category][cat] + alpha * (
                        reward + gamma * max(q_values[assessment_category].values()) - q_values[assessment_category][cat]
                    )
        
        # Calculate softmax weights
        eta = 1.0
        q_vals = np.array(list(q_values[assessment_category].values()))
        exp_q_values = np.exp(eta * q_vals)
        softmax_weights[assessment_category] = exp_q_values / np.sum(exp_q_values)
        
        # Calculate overall score for this assessment
        if category_scores[assessment_category]:
            overall_scores[assessment_category] = sum(
                category_scores[assessment_category][cat] * softmax_weights[assessment_category][i] 
                for i, cat in enumerate(assessment_data.keys())
                if cat in category_scores[assessment_category]
            )
    
    return category_scores, q_values, softmax_weights, overall_scores

# Helper functions for results visualization

def get_color_for_score(score):
    """Return a color based on the score value."""
    if score < 30:
        return "#EF4444"  # Red for low scores
    elif score < 60:
        return "#F59E0B"  # Amber for medium scores
    elif score < 80:
        return "#10B981"  # Green for good scores
    else:
        return "#0284C7"  # Blue for excellent scores

def create_radar_chart(categories, scores):
    """Create a radar chart for the category scores."""
    # Number of variables
    N = len(categories)
    
    # What will be the angle of each axis in the plot
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Scores need to be in the same order and length as angles
    scores_for_plot = scores.copy()
    scores_for_plot += scores_for_plot[:1]  # Close the loop
    
    # Initialize the figure
    fig = plt.figure(figsize=(8, 6), facecolor='white')
    ax = fig.add_subplot(111, polar=True)
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories, color='#475569', size=10)
    
    # Draw the y-axis labels (0-100)
    ax.set_rlabel_position(0)
    plt.yticks([25, 50, 75, 100], ["25", "50", "75", "100"], color="#475569", size=8)
    plt.ylim(0, 100)
    
    # Plot the scores on the radar chart
    ax.plot(angles, scores_for_plot, linewidth=2, linestyle='solid', color='#0284C7')
    ax.fill(angles, scores_for_plot, alpha=0.1, color='#0284C7')
    
    # Add a grid
    ax.grid(True, color='#E2E8F0')
    
    # Set the background color
    ax.set_facecolor('#F8FAFC')
    
    # Add a title
    plt.title('AI Readiness by Dimension', size=14, color='#1E293B', pad=20)
    
    # Adjust the layout
    plt.tight_layout()
    
    return fig

def create_bar_chart(categories, scores):
    """Create a horizontal bar chart for category scores."""
    # Format categories for display
    display_categories = [cat.replace('AI ', '') for cat in categories]
    
    # Create the bar chart
    fig, ax = plt.figure(figsize=(10, 6)), plt.axes()
    
    # Plot horizontal bars
    bars = ax.barh(display_categories, scores, color='#0284C7', alpha=0.7, height=0.5)
    
    # Add value labels to the right of each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2, f'{int(width)}%',
                ha='left', va='center', color='#475569', fontweight='bold')
    
    # Customize the chart
    ax.set_xlim(0, 100)
    ax.set_xlabel('Score (%)', color='#475569')
    ax.set_title('Dimension Scores', color='#1E293B', pad=20)
    
    # Customize the grid
    ax.grid(axis='x', linestyle='--', alpha=0.7, color='#E2E8F0')
    ax.set_axisbelow(True)
    
    # Remove the frame
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Set background color
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    
    plt.tight_layout()
    return fig

def create_gauge_chart(score):
    """Create a gauge chart for the overall score."""
    # Define the score ranges and colors
    ranges = [0, 30, 60, 80, 100]
    colors = ['#EF4444', '#F59E0B', '#10B981', '#0284C7']
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'projection': 'polar'})
    
    # Set the gauge limits (in radians)
    start_angle = 3*np.pi/4
    end_angle = -np.pi/4
    
    # Define radius for consistent use
    radius = 1.0
    
    # Plot the colored ranges
    for i in range(len(ranges)-1):
        # Convert score range to angles in radians
        angle1 = start_angle - (ranges[i] / 100) * (start_angle - end_angle)
        angle2 = start_angle - (ranges[i+1] / 100) * (start_angle - end_angle)
        
        # Create a colored region
        arc = patches.Wedge(
            (0, 0), radius * 0.9, 
            np.degrees(angle1), np.degrees(angle2),
            width=0.2, color=colors[i], alpha=0.6
        )
        ax.add_patch(arc)
    
    # Create the pointer for the current score
    score_angle = start_angle - (score / 100) * (start_angle - end_angle)
    arrow_length = 0.75
    
    # Plot the arrow
    ax.arrow(0, 0, arrow_length * np.cos(score_angle), arrow_length * np.sin(score_angle),
             width=0.05, head_width=0.15, head_length=0.15, fc='#1E293B', ec='#1E293B')
    
    # Add a circle at the arrow base
    circle = plt.Circle((0, 0), 0.1, fc='#1E293B', ec='#1E293B')
    ax.add_patch(circle)
    
    # Add score text
    ax.text(0, -0.2, f'{int(score)}%', ha='center', va='center', fontsize=24, fontweight='bold', color='#1E293B')
    
    # Add a label
    labels = ["Low", "Moderate", "High", "Excellent"]
    label_positions = [15, 45, 70, 90]
    for i, label in enumerate(labels):
        angle = start_angle - (label_positions[i] / 100) * (start_angle - end_angle)
        ax.text(angle, radius + 0.1, label, 
                ha='center', va='center', fontsize=8, 
                color='#475569', fontweight='medium',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor=theme_colors["primary"]))
    
    # Draw tick marks
    for value, angle in zip([0, 25, 50, 75, 100], [3*np.pi/4, 3*np.pi/4 + (25/100) * (6*np.pi/4), 3*np.pi/4 + (50/100) * (6*np.pi/4), 3*np.pi/4 + (75/100) * (6*np.pi/4), 9*np.pi/4]):
        ax.text(0.95 * np.cos(angle), 0.95 * np.sin(angle), f"{value}%", 
                ha='center', va='center', fontsize=9)
    
    # Remove ticks, labels, and grid
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    # Set limits to ensure proper aspect ratio
    ax.set_ylim(-1, 1)
    
    # Set background color
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    
    return fig

def get_strength_comment(category, score):
    """Return a comment about the organization's strength in a specific category."""
    if "Data" in category:
        return "Strong data management practices and governance provide a solid foundation for AI initiatives."
    elif "Infrastructure" in category:
        return "Robust technical infrastructure and computing resources enable efficient AI model training and deployment."
    elif "Talent" in category:
        return "Well-developed AI talent acquisition, training, and retention strategies support AI capabilities."
    elif "Strategy" in category:
        return "Clear AI strategy aligned with business objectives provides direction for AI initiatives."
    elif "Culture" in category:
        return "Strong innovation culture and change management capabilities enable AI adoption."
    elif "Governance" in category:
        return "Established governance frameworks ensure ethical and responsible AI implementation."
    else:
        return "Your organization demonstrates significant strengths in this area."

def get_improvement_comment(category, score):
    """Return a comment about areas for improvement in a specific category."""
    if "Data" in category:
        return "Enhance data quality, accessibility, governance, and management practices to build a stronger foundation for AI."
    elif "Infrastructure" in category:
        return "Invest in technical infrastructure, cloud resources, and MLOps capabilities to support AI initiatives."
    elif "Talent" in category:
        return "Develop structured talent acquisition, upskilling programs, and retention strategies for AI professionals."
    elif "Strategy" in category:
        return "Create a more comprehensive AI strategy aligned with business objectives and develop clear roadmaps."
    elif "Culture" in category:
        return "Foster a more innovative culture with stronger change management capabilities to accelerate AI adoption."
    elif "Governance" in category:
        return "Establish more robust governance frameworks to ensure ethical, responsible AI implementation."
    else:
        return "Focus on improving capabilities in this area to enhance overall AI readiness."

def get_recommendations(category, score):
    """Return specific recommendations based on category and score."""
    recommendations = []
    
    if "Data" in category:
        recommendations = [
            "Implement a comprehensive data governance framework with clear ownership and quality standards",
            "Develop a centralized data catalog to improve accessibility and discoverability",
            "Establish data quality monitoring processes specific to AI use cases",
            "Create standardized data preparation pipelines for common AI scenarios"
        ]
    elif "Infrastructure" in category:
        recommendations = [
            "Evaluate and scale cloud infrastructure to support AI workloads effectively",
            "Implement MLOps practices for model deployment, monitoring, and lifecycle management",
            "Establish a standardized AI development environment with necessary tools and frameworks",
            "Create clear infrastructure scaling strategies to handle growing AI demands"
        ]
    elif "Talent" in category:
        recommendations = [
            "Develop a structured AI talent acquisition strategy with clear role definitions",
            "Create internal upskilling programs for existing technical staff",
            "Establish partnerships with academic institutions or AI research centers",
            "Implement knowledge sharing mechanisms for AI expertise across teams"
        ]
    elif "Strategy" in category:
        recommendations = [
            "Define a clear enterprise AI strategy with specific business outcomes",
            "Create a prioritized roadmap for AI use cases aligned with business value",
            "Establish processes to measure and communicate AI initiative ROI",
            "Develop a structured approach to AI security and risk management"
        ]
    elif "Culture" in category:
        recommendations = [
            "Foster executive-level AI championship and visible leadership support",
            "Implement structured change management processes for AI initiatives",
            "Create mechanisms for cross-functional collaboration on AI projects",
            "Establish innovation channels for employees to propose AI use cases"
        ]
    elif "Governance" in category:
        recommendations = [
            "Create a comprehensive AI ethics framework and review process",
            "Establish AI governance committee with clear responsibilities",
            "Develop processes for ongoing compliance monitoring of AI systems",
            "Implement transparent AI documentation standards and model cards"
        ]
    
    # Return top 3 recommendations based on score
    if score < 30:
        return recommendations[:3]  # Return first 3 for low scores
    elif score < 60:
        return recommendations[1:4]  # Return middle 3 for medium scores
    else:
        return recommendations[1:]  # Return last 3 for higher scores

# Main application function
def main():
    # Setup session state for storing responses if not already present
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    if 'assessment_started' not in st.session_state:
        st.session_state.assessment_started = False
    
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # Initialize navigation if not already set
    if 'nav' not in st.session_state:
        st.session_state.nav = "Home"
    
    # App title and description
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #1E293B; font-size: 2.5rem; margin-bottom: 0.5rem;">Enterprise AI Readiness Assessment</h1>
        <p style="font-size: 1.2rem; color: #666; max-width: 800px; margin: 0 auto 1.5rem auto;">
            Evaluate your organization's capacity to implement and scale AI solutions 
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with app information and navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: white; margin-bottom: 10px;">AI Readiness Dashboard</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Add a company logo placeholder
        logo_html = """
        <div style="background-color: white; border-radius: 10px; padding: 15px; margin-bottom: 20px; text-align: center;">
            <h1 style="color: #1E293B; font-size: 1.8rem; margin: 0;">AI READY</h1>
            <p style="color: #0284C7; margin: 0; font-weight: 500;">Enterprise Assessment</p>
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
        
        # Navigation options
        nav_options = ["Home", "Assessment", "Results", "About"]
        selected_nav = st.radio("Navigation", nav_options, index=nav_options.index(st.session_state.nav))
        
        # Update session state based on selection
        if selected_nav != st.session_state.nav:
            st.session_state.nav = selected_nav
            st.experimental_rerun()
        
        # Reset button
        if st.button("Reset Assessment", type="secondary"):
            st.session_state.responses = {}
            st.session_state.assessment_started = False
            st.session_state.show_results = False
            st.session_state.nav = "Home"
            st.experimental_rerun()
    
    # Load all questionnaires
    questionnaires = load_all_questionnaires()
    
    # Display different sections based on navigation
    if st.session_state.nav == "Home":
        show_home_page()
    elif st.session_state.nav == "Assessment":
        if not questionnaires:
            st.error("No questionnaires could be loaded. Please check your installation.")
        else:
            st.session_state.assessment_started = True
            show_questionnaire(questionnaires)
    elif st.session_state.nav == "Results":
        if not st.session_state.responses:
            st.warning("Please complete the assessment first.")
            st.markdown('<style>div.stButton > button:first-child { background-color: #FFFFFF !important; color: #0284C7 !important; }</style>', unsafe_allow_html=True)
            st.button("Start Assessment", on_click=lambda: setattr(st.session_state, 'nav', 'Assessment'))
        else:
            st.session_state.show_results = True
            show_results()
    elif st.session_state.nav == "About":
        show_about_page()

# Function to show the home page
def show_home_page():
    # Header with logo
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">AI Readiness Assessment</h1>
        <p class="dashboard-subtitle">Evaluate your organization's capacity to implement and scale AI solutions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview section
    st.markdown("""
    <div class="card primary">
        <h3>About the Assessment</h3>
        <p>This enterprise-grade AI Readiness Assessment evaluates your organization across six key dimensions 
        that are critical for successful AI implementation. Using Q-learning algorithms, the assessment 
        adapts to your specific context and provides tailored recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h4 class="feature-title">Comprehensive Analysis</h4>
            <p class="feature-description">Get a detailed assessment of your organization's AI readiness across 6 critical dimensions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h4 class="feature-title">Advanced Diagnostics</h4>
            <p class="feature-description">Our assessment uses Q-learning algorithms to identify the most impactful areas for your AI initiatives.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h4 class="feature-title">Executive Dashboard</h4>
            <p class="feature-description">Visualize your AI readiness with professional charts that highlight strengths and opportunities.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h4 class="feature-title">Actionable Recommendations</h4>
            <p class="feature-description">Receive practical recommendations to enhance your organization's AI capabilities and accelerate transformation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("<div style='text-align: center; margin-top: 2rem;'>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: #0284C7 !important;
        color: white !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("Start Assessment", type="primary", use_container_width=True):
        st.session_state.nav = "Assessment"
        st.session_state.assessment_started = True
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Dimension section
    st.markdown("<h3 style='margin-top: 2rem;'>Assessment Dimensions</h3>", unsafe_allow_html=True)
    
    # First row of dimensions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card primary" style="height: 100%;">
            <h4 style="color: var(--primary);">Data</h4>
            <p>Evaluates data quality, accessibility, governance, and management practices.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card primary" style="height: 100%;">
            <h4 style="color: var(--primary);">Infrastructure</h4>
            <p>Assesses compute resources, MLOps capabilities, and cloud readiness.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card primary" style="height: 100%;">
            <h4 style="color: var(--primary);">Talent</h4>
            <p>Measures AI talent acquisition, retention, and skills development strategies.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row of dimensions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card primary" style="height: 100%;">
            <h4 style="color: var(--primary);">Strategy</h4>
            <p>Evaluates AI vision, roadmap, and alignment with business objectives.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card primary" style="height: 100%;">
            <h4 style="color: var(--primary);">Culture</h4>
            <p>Assesses organizational culture, innovation mindset, and change management.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card primary" style="height: 100%;">
            <h4 style="color: var(--primary);">Governance</h4>
            <p>Measures ethical AI practices, risk management, and regulatory compliance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a download button for the report
    st.subheader("Download Full Report")
    st.markdown("""
    <div class="card">
        <p>Download a comprehensive report of your AI readiness assessment results, including detailed scores, 
        charts, and personalized recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a PDF report (placeholder for now)
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: #0284C7 !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button p { color: white !important; }
.stButton > button * { color: white !important; }
button p { color: white !important; }
    </style>
    """, unsafe_allow_html=True)
    if st.button("Generate PDF Report", type="primary"):
        st.success("Report generation feature will be available in the next update.")

# Function to show about page
def show_about_page():
    st.markdown("""
    <div class="card">
        <h2>About the AI Readiness Assessment Tool</h2>
        <p>
            This enterprise-grade assessment tool helps organizations evaluate their AI readiness 
            across six critical dimensions using a sophisticated Q-Learning algorithm.
        </p>
        <h3>Methodology</h3>
        <p>
            Our assessment framework is based on industry best practices and research in organizational AI readiness.
            The tool employs Q-Learning, a reinforcement learning technique, to weight different aspects of AI readiness
            based on their relative importance for your specific organizational context.
        </p>
        <h3>Q-Learning Algorithm</h3>
        <p>
            The Q-Learning algorithm used in this assessment enables adaptive weighting of different readiness categories:
        </p>
        <ul>
            <li><b>Dynamic Weights:</b> The algorithm learns which factors are most important for your organization's AI readiness.</li>
            <li><b>Softmax Transformation:</b> Converts learned values into probability weights that sum to 100%.</li>
            <li><b>Contextual Adaptation:</b> Adjusts based on the interrelationships between different readiness dimensions.</li>
        </ul>
        <p>This approach allows the assessment to adapt and emphasize the most critical areas for your organization.</p>
        <h3>Privacy & Data</h3>
        <p>
            All assessment data remains local to your device. No information is transmitted to external servers.
            You can safely use this tool for internal organizational assessments without data privacy concerns.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Function to show the questionnaire
def show_questionnaire(all_questionnaires):
    st.header("AI Readiness Questionnaire")
    
    # Check if we have any questionnaires to display
    if not all_questionnaires:
        st.warning("No questionnaires were loaded successfully. Please check your installation.")
        return
    
    st.markdown("""
    <div class="dashboard-header">
        <h2 class="dashboard-title">AI Readiness Questionnaire</h2>
        <p class="dashboard-subtitle">Evaluate your organization's AI readiness across key dimensions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Define the answer options with descriptions
    answer_options = [
        "Not Implemented - No evidence of implementation",
        "Initial - Basic or ad-hoc implementation with limited scope",
        "Defined - Formalized but inconsistent implementation",
        "Managed - Consistent implementation with monitoring",
        "Optimized - Fully implemented with continuous improvement"
    ]
    
    # Create tabs for each questionnaire category
    tabs = st.tabs(list(all_questionnaires.keys()))
    
    # Display questions for each category
    for i, (category, questionnaire) in enumerate(all_questionnaires.items()):
        with tabs[i]:
            st.markdown(f"""
            <div class="category-header">
                <h3>{category} Assessment</h3>
                <p>Answer all questions to evaluate your organization's {category.replace('AI ', '')} readiness.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize the category in responses if not exists
            if category not in st.session_state.responses:
                st.session_state.responses[category] = {}
            
            # Calculate progress for this category
            total_questions = sum(len(questions) for _, questions in questionnaire.items())
            answered_questions = 0
            for q_category in questionnaire.keys():
                if q_category in st.session_state.responses.get(category, {}):
                    answered_questions += sum(1 for ans in st.session_state.responses[category].get(q_category, []) if ans is not None)
            
            progress_percentage = int((answered_questions / total_questions) * 100) if total_questions > 0 else 0
            
            # Display progress bar
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-header">
                    <span>Progress</span>
                    <span class="progress-percentage">{progress_percentage}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_percentage}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display each question category
            for q_category, questions in questionnaire.items():
                # Initialize the question category in responses if not exists
                if q_category not in st.session_state.responses[category]:
                    st.session_state.responses[category][q_category] = []
                
                with st.expander(f"{q_category}", expanded=True):
                    st.markdown(f"""
                    <div class="subcategory-header">
                        <p>{q_category}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for j, question in enumerate(questions):
                        # Create response key
                        response_key = f"{category}_{q_category}_{j}"
                        
                        # Ensure the response array is long enough
                        while len(st.session_state.responses.get(category, {}).get(q_category, [])) <= j:
                            st.session_state.responses.setdefault(category, {}).setdefault(q_category, []).append(None)
                        
                        # Set default value from session state if exists
                        default_val = st.session_state.responses[category][q_category][j] if j < len(st.session_state.responses[category][q_category]) else None
                        
                        # Display the question with custom styling
                        st.markdown(f"""
                        <div class="question-card">
                            <div class="question-number">Question {j+1}</div>
                            <div class="question-text">{question}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add option label
                        st.markdown('<div class="option-label">Select your organization\'s current state:</div>', unsafe_allow_html=True)
                        
                        # Get response with radio buttons
                        response = st.radio(
                            label=f"Select answer for Question {j+1}",
                            options=range(5),
                            format_func=lambda x: answer_options[x],
                            key=response_key,
                            index=default_val if default_val is not None else None,
                            label_visibility="collapsed"
                        )
                        
                        # Add a divider between questions
                        st.markdown('<hr class="question-divider">', unsafe_allow_html=True)
                        
                        # Store the response in session state
                        if response is not None:
                            question_index = j
                            
                            # Ensure the response array is long enough
                            while len(st.session_state.responses.get(category, {}).get(q_category, [])) <= question_index:
                                st.session_state.responses.setdefault(category, {}).setdefault(q_category, []).append(None)
                            
                            # Store the response
                            st.session_state.responses[category][q_category][question_index] = response
    
    # Submit button with enhanced styling
    st.markdown("""
    <div class="submit-container">
        <p class="submit-message">Please ensure all questions are answered before submitting</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit = st.button("Submit Assessment", type="primary", use_container_width=True)
    
    if submit:
        # Check if all questions have been answered
        all_answered = True
        unanswered_categories = []
        
        for category, category_responses in st.session_state.responses.items():
            for q_category, responses in category_responses.items():
                if None in responses or len(responses) == 0:
                    all_answered = False
                    unanswered_categories.append(f"{category} - {q_category}")
        
        if all_answered:
            st.session_state.show_results = True
            st.session_state.assessment_started = False
            # Update navigation to Results page
            st.session_state.nav = "Results"
            st.experimental_rerun()
        else:
            st.error(f"Please answer all questions before submitting. Unanswered sections: {', '.join(unanswered_categories[:3])}{'...' if len(unanswered_categories) > 3 else ''}")

# Function to show the results
def show_results():
    # Calculate the overall score and category scores
    overall_score = 0
    category_scores = {}
    
    for category, category_responses in st.session_state.responses.items():
        category_score = 0
        question_count = 0
        
        for q_category, responses in category_responses.items():
            for response in responses:
                if response is not None:
                    category_score += response
                    question_count += 1
        
        if question_count > 0:
            avg_category_score = (category_score / question_count) * 25  # Scale to 100
            category_scores[category] = avg_category_score
            overall_score += avg_category_score
    
    overall_score = overall_score / len(category_scores) if category_scores else 0

    # Header
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">AI Readiness Assessment Results</h1>
        <p class="dashboard-subtitle">Your organization's AI readiness profile with insights and recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Executive summary
    st.markdown("""
    <div class="card primary">
        <h3>Executive Summary</h3>
        <p>This assessment provides a comprehensive view of your organization's readiness to implement and scale AI solutions. 
        The results are based on your responses across six key dimensions that are critical for AI success.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overall score and radar chart in the same row
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display the overall score with a gauge chart
        st.markdown("<h3>Overall Readiness Score</h3>", unsafe_allow_html=True)
        
        # Create a gauge chart
        fig_gauge = create_gauge_chart(overall_score)
        st.pyplot(fig_gauge)
        
        # Readiness level text
        readiness_level = "Low" if overall_score < 30 else "Moderate" if overall_score < 60 else "High" if overall_score < 80 else "Advanced"
        st.markdown(f"""
        <div class="card" style="margin-top: 1rem;">
            <h4>AI Readiness Level: <span style="color:{get_color_for_score(overall_score)};">{readiness_level}</span></h4>
            <p>Your organization is at a <strong>{readiness_level.lower()}</strong> level of AI readiness.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Display the radar chart
        st.markdown("<h3>Dimension Analysis</h3>", unsafe_allow_html=True)
        
        # Create and display the radar chart
        categories = list(category_scores.keys())
        scores = [category_scores[cat] for cat in categories]
        
        # Format categories for display (remove 'AI ' prefix)
        display_categories = [cat.replace('AI ', '') for cat in categories]
        
        fig_radar = create_radar_chart(display_categories, scores)
        st.pyplot(fig_radar)
    
    # Strength and improvement areas
    st.markdown("<h3>Strengths & Improvement Areas</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Find the top 2 highest scoring categories
        sorted_scores = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        st.markdown("""
        <div class="card success">
            <h4>Key Strengths</h4>
            <p>Your organization demonstrates strong capabilities in these areas:</p>
        </div>
        """, unsafe_allow_html=True)
        
        for i, (category, score) in enumerate(sorted_scores[:2]):
            display_name = category.replace('AI ', '')
            score_percent = int(score)
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0;">{display_name}</h4>
                    <span style="background-color: #10B981; color: white; padding: 0.25rem 0.5rem; border-radius: 9999px; font-weight: 600; font-size: 0.75rem;">{score_percent}%</span>
                </div>
                <div style="height: 0.5rem; background-color: #E2E8F0; border-radius: 9999px; overflow: hidden;">
                    <div style="height: 100%; width: {score_percent}%; background-color: #10B981; border-radius: 9999px;"></div>
                </div>
                <p style="margin-top: 0.75rem; font-size: 0.875rem;">{get_strength_comment(category, score_percent)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Find the 2 lowest scoring categories
        st.markdown("""
        <div class="card error">
            <h4>Improvement Areas</h4>
            <p>Focus on enhancing capabilities in these dimensions:</p>
        </div>
        """, unsafe_allow_html=True)
        
        for i, (category, score) in enumerate(sorted_scores[-2:]):
            display_name = category.replace('AI ', '')
            score_percent = int(score)
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0;">{display_name}</h4>
                    <span style="background-color: #EF4444; color: white; padding: 0.25rem 0.5rem; border-radius: 9999px; font-weight: 600; font-size: 0.75rem;">{score_percent}%</span>
                </div>
                <div style="height: 0.5rem; background-color: #E2E8F0; border-radius: 9999px; overflow: hidden;">
                    <div style="height: 100%; width: {score_percent}%; background-color: #EF4444; border-radius: 9999px;"></div>
                </div>
                <p style="margin-top: 0.75rem; font-size: 0.875rem;">{get_improvement_comment(category, score_percent)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Detailed scores section
    st.markdown("<h3>Detailed Dimension Scores</h3>", unsafe_allow_html=True)
    
    # Create a bar chart for all categories
    fig_bar = create_bar_chart(categories, scores)
    st.pyplot(fig_bar)
    
    # Create columns for the detailed scores with circular visualizations
    cols = st.columns(3)
    
    for i, (category, score) in enumerate(category_scores.items()):
        with cols[i % 3]:
            score_percent = int(score)
            color = get_color_for_score(score_percent)
            display_name = category.replace('AI ', '')
            
            st.markdown(f"""
            <div class="card" style="text-align: center; padding: 1.25rem;">
                <h4>{display_name}</h4>
                <div style="position: relative; width: 120px; height: 120px; margin: 0 auto; background: conic-gradient({color} {score_percent * 3.6}deg, #E2E8F0 0deg); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                    <div style="position: absolute; width: 90px; height: 90px; background-color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 1.5rem; font-weight: 600; color: {color};">{score_percent}%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Recommendations section
    st.markdown("<h3>Recommended Actions</h3>", unsafe_allow_html=True)
    
    # Sort categories by score (lowest first)
    priority_categories = sorted(category_scores.items(), key=lambda x: x[1])
    
    for i, (category, score) in enumerate(priority_categories[:3]):
        display_name = category.replace('AI ', '')
        recommendations = get_recommendations(category, score)
        
        st.markdown(f"""
        <div class="card primary">
            <h4>Priority {i+1}: Enhance {display_name}</h4>
            <p style="font-size: 0.875rem;">Current score: <strong>{int(score)}%</strong></p>
            <ul style="margin-top: 0.75rem;">
                {''.join([f'<li style="margin-bottom: 0.5rem; font-size: 0.875rem;">{rec}</li>' for rec in recommendations])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Q-Learning explanation
    with st.expander("Understanding the Assessment Methodology"):
        st.markdown("""
        <div class="card">
            <h4>Q-Learning Algorithm</h4>
            <p>This assessment uses a Q-Learning algorithm to evaluate your organization's AI readiness. The algorithm:</p>
            <ul>
                <li><b>Learns from patterns</b> in your responses to identify critical areas for improvement</li>
                <li><b>Weights different dimensions</b> based on their interdependencies</li>
                <li><b>Adapts to your specific context</b> to provide more relevant recommendations</li>
            </ul>
            <p>The scoring model emphasizes practical implementation readiness rather than theoretical capability.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Next steps and export options
    st.markdown("<h3>Next Steps</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4>Re-take Assessment</h4>
            <p>Update your responses or re-evaluate after implementing changes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("New Assessment", type="primary", use_container_width=True):
            st.session_state.responses = {}
            st.session_state.show_results = False
            st.session_state.assessment_started = True
            st.session_state.nav = "Assessment"
            st.experimental_rerun()
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4>Export Results</h4>
            <p>Download your assessment results as a PDF report.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <style>
        div.stButton > button {
            background-color: #0284C7 !important;
            color: white !important;
            border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("Export as PDF", use_container_width=True):
            st.info("PDF export functionality will be available in the next version.")

if __name__ == "__main__":
    main()
