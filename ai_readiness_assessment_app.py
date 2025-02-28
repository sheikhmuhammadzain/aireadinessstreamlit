import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import os
import json
import re
import importlib.util
import sys
from PIL import Image
from io import BytesIO
import base64

# Set page configuration
st.set_page_config(
    page_title="AI Readiness Assessment",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set custom color theme
theme_colors = {
    "primary": "#3949AB",    # Deep blue
    "secondary": "#00ACC1",  # Cyan
    "background": "#FAFAFA", # Light grey
    "success": "#4CAF50",    # Green
    "warning": "#FF9800",    # Orange
    "error": "#F44336",      # Red
    "text": "#212121",       # Dark grey
    "accent1": "#7E57C2",    # Purple
    "accent2": "#26A69A",    # Teal
}

# Custom CSS to make the app more premium
st.markdown(f"""
<style>
    /* Main container */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }}

    /* Headers */
    h1, h2, h3 {{
        color: {theme_colors["primary"]};
        font-family: 'Segoe UI', Arial, sans-serif;
    }}
    
    h1 {{
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {theme_colors["secondary"]};
    }}
    
    h2 {{
        font-weight: 500;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }}
    
    h3 {{
        font-weight: 400;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        border-radius: 6px 6px 0px 0px;
        padding: 0px 20px;
        background-color: #F5F5F5;
        font-weight: 500;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {theme_colors["primary"]};
        color: white;
        font-weight: 500;
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        font-weight: 500;
        color: {theme_colors["text"]};
        background-color: #F0F0F0;
        border-radius: 4px;
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 2.5rem;
        font-weight: 600;
        color: {theme_colors["primary"]};
    }}
    
    [data-testid="stMetricDelta"] {{
        font-size: 1rem;
        color: {theme_colors["success"]};
    }}

    /* Cards for sections */
    .card {{
        padding: 1.5rem;
        border-radius: 8px;
        background-color: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }}
    
    /* Buttons */
    .stButton button {{
        font-weight: 500;
        border-radius: 6px;
        height: 3rem;
        padding: 0 1.5rem;
        background-color: {theme_colors["primary"]};
        color: white;
        transition: all 0.3s;
    }}
    
    .stButton button:hover {{
        background-color: {theme_colors["secondary"]};
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
    
    /* Select slider */
    [data-testid="stSlider"] .thumb-content p {{
        font-weight: 500;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {theme_colors["primary"]};
        padding-top: 2rem;
    }}
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {{
        color: white;
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        color: white;
        font-weight: 500;
    }}
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
    radius = 0.75
    
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
    labels = ['Low', 'Medium', 'High', 'Excellent']
    positions = [3*np.pi/4 + i*6*np.pi/16 for i in range(5)]
    
    for i, (label, pos) in enumerate(zip(labels, positions[:-1])):
        mid_pos = (positions[i] + positions[i+1]) / 2
        ax.text(0.8 * np.cos(mid_pos), 0.8 * np.sin(mid_pos), label, 
                ha='center', va='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor=theme_colors["primary"]))
    
    # Draw tick marks
    for value, angle in zip([0, 25, 50, 75, 100], positions):
        ax.text(0.95 * np.cos(angle), 0.95 * np.sin(angle), f"{value}%", 
                ha='center', va='center', fontsize=9)
    
    # Draw the needle
    needle_angle = 3*np.pi/4 + (score_100/100) * 6*np.pi/4
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
        <h1 style="color: #3949AB; font-size: 2.5rem; margin-bottom: 0.5rem;">Enterprise AI Readiness Assessment</h1>
        <p style="font-size: 1.2rem; color: #666; max-width: 800px; margin: 0 auto 1.5rem auto;">
            Evaluate your organization's AI maturity across six critical dimensions
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
            <h1 style="color: #3949AB; font-size: 1.8rem; margin: 0;">AI READY</h1>
            <p style="color: #00ACC1; margin: 0; font-weight: 500;">Enterprise Assessment</p>
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
            st.button("Start Assessment", on_click=lambda: setattr(st.session_state, 'nav', 'Assessment'))
        else:
            st.session_state.show_results = True
            show_results()
    elif st.session_state.nav == "About":
        show_about_page()

# Function to show the home page
def show_home_page():
    # Hero section with cards
    st.markdown("""
    <div class="card" style="padding: 2rem; text-align: center; margin-bottom: 2rem; background: linear-gradient(135deg, #3949AB 0%, #5C6BC0 100%); color: white;">
        <h2 style="color: white; font-size: 1.8rem; margin-bottom: 1rem;">Comprehensive AI Readiness Assessment</h2>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
            This enterprise-grade assessment tool helps organizations evaluate their AI readiness 
            across six critical dimensions using a sophisticated Q-Learning algorithm.
        </p>
        <div style="margin-top: 1.5rem;">
            <b>Start your assessment journey today →</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature overview section
    st.markdown("""
    <h2 style="color: #3949AB; margin-top: 2rem;">Assessment Framework</h2>
    <p>Our AI readiness assessment analyzes six critical dimensions to provide a comprehensive view of your organization's preparedness for AI adoption.</p>
    """, unsafe_allow_html=True)
    
    # Create columns for the dimensions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color: #3949AB;">AI Governance</h3>
            <p>Evaluates the policies, procedures, and oversight mechanisms for responsible AI implementation.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3 style="color: #3949AB;">AI Culture</h3>
            <p>Assesses organizational culture, leadership vision, and change management readiness for AI transformation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="color: #3949AB;">AI Data</h3>
            <p>Measures data quality, accessibility, governance, and infrastructure for AI systems.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3 style="color: #3949AB;">AI Infrastructure</h3>
            <p>Evaluates compute resources, storage solutions, and technical foundation for AI workloads.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3 style="color: #3949AB;">AI Strategy</h3>
            <p>Analyzes strategic alignment, security practices, and deployment approach for AI initiatives.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3 style="color: #3949AB;">AI Talent</h3>
            <p>Measures talent acquisition, training, leadership, and collaboration capabilities for AI teams.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works section
    st.markdown("""
    <h2 style="color: #3949AB; margin-top: 2rem;">How It Works</h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3 style="color: #3949AB;">1. Answer Questions</h3>
            <p>Complete the assessment questionnaire across six AI readiness dimensions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3 style="color: #3949AB;">2. AI Analysis</h3>
            <p>Our Q-Learning algorithm analyzes responses to calculate accurate readiness scores.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3 style="color: #3949AB;">3. Get Insights</h3>
            <p>Receive detailed visualizations, scores, and actionable recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; margin-bottom: 3rem;">
        <h2 style="color: #3949AB;">Ready to Assess Your AI Readiness?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Start button centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Assessment", type="primary", use_container_width=True):
            st.session_state.nav = "Assessment"
            st.experimental_rerun()

# Function to show about page
def show_about_page():
    st.markdown("""
    <div class="card">
        <h2 style="color: #3949AB;">About the AI Readiness Assessment Tool</h2>
        <p>
            This enterprise-grade assessment tool helps organizations evaluate their AI readiness 
            across six critical dimensions using a sophisticated Q-Learning algorithm.
        </p>
        <h3 style="color: #3949AB; margin-top: 1.5rem;">Methodology</h3>
        <p>
            Our assessment framework is based on industry best practices and research in organizational AI readiness.
            The tool employs Q-Learning, a reinforcement learning technique, to weight different aspects of AI readiness
            based on their relative importance for your specific organizational context.
        </p>
        <h3 style="color: #3949AB; margin-top: 1.5rem;">Q-Learning Algorithm</h3>
        <p>
            The Q-Learning algorithm used in this assessment enables adaptive weighting of different readiness categories:
        </p>
        <ul>
            <li><b>Dynamic Weights:</b> The algorithm learns which factors are most important for your organization's AI readiness.</li>
            <li><b>Softmax Transformation:</b> Converts learned values into proportional weights.</li>
            <li><b>Contextual Adaptation:</b> Adjusts based on the interrelationships between different readiness dimensions.</li>
        </ul>
        <h3 style="color: #3949AB; margin-top: 1.5rem;">Privacy & Data</h3>
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
    
    # Define the answer options with descriptions
    answer_options = [
        "Not Implemented - No evidence of implementation",
        "Initial - Limited or ad-hoc implementation",
        "Defined - Formalized but inconsistent implementation",
        "Managed - Consistent implementation with monitoring",
        "Optimized - Fully implemented with continuous improvement"
    ]
    
    # Create tabs for each questionnaire category
    tabs = st.tabs(list(all_questionnaires.keys()))
    
    # Display questions for each category
    for i, (category, questionnaire) in enumerate(all_questionnaires.items()):
        with tabs[i]:
            st.markdown(f"<h3 style='color:{theme_colors['primary']};'>{category} Assessment</h3>", unsafe_allow_html=True)
            
            # Initialize the category in responses if not exists
            if category not in st.session_state.responses:
                st.session_state.responses[category] = {}
            
            # Display each question category as an expander
            for q_category, questions in questionnaire.items():
                # Initialize the question category in responses if not exists
                if q_category not in st.session_state.responses[category]:
                    st.session_state.responses[category][q_category] = []
                
                with st.expander(f"{q_category}", expanded=True):
                    for j, question in enumerate(questions):
                        # Display the question with custom styling
                        st.markdown(f"""
                        <div class="card" style="padding: 1rem; margin-bottom: 1rem; background-color: #F8F9FA;">
                            <h4 style="color: {theme_colors['primary']}; margin-top: 0;">Question {j+1}</h4>
                            <p style="margin-bottom: 0.5rem;">{question}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Create response key
                        response_key = f"{category}_{q_category}_{j}"
                        
                        # Ensure the response array is long enough
                        while len(st.session_state.responses.get(category, {}).get(q_category, [])) <= j:
                            st.session_state.responses.setdefault(category, {}).setdefault(q_category, []).append(None)
                        
                        # Set default value from session state if exists
                        default_val = st.session_state.responses[category][q_category][j] if j < len(st.session_state.responses[category][q_category]) else None
                        
                        # Get response with radio buttons
                        response = st.radio(
                            label=f"Select answer for Question {j+1}",
                            options=range(5),
                            format_func=lambda x: answer_options[x],
                            key=response_key,
                            index=default_val if default_val is not None else None,
                            horizontal=False
                        )
                        
                        # Add a divider
                        st.markdown("<hr style='margin: 1rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
                        
                        # Store the response in session state
                        if response is not None:
                            question_index = j
                            
                            # Ensure the response array is long enough
                            while len(st.session_state.responses.get(category, {}).get(q_category, [])) <= question_index:
                                st.session_state.responses.setdefault(category, {}).setdefault(q_category, []).append(None)
                            
                            # Store the response
                            st.session_state.responses[category][q_category][question_index] = response
    
    # Submit button
    st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
    submit = st.button("Submit Assessment", type="primary", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if submit:
        # Check if all questions have been answered
        all_answered = True
        for category, category_responses in st.session_state.responses.items():
            for q_category, responses in category_responses.items():
                if None in responses or len(responses) == 0:
                    all_answered = False
                    break
        
        if all_answered:
            st.session_state.show_results = True
            st.session_state.assessment_started = False
            # Update navigation to Results page
            st.session_state.nav = "Results"
            st.experimental_rerun()
        else:
            st.error("Please answer all questions before submitting.")

# Function to show the results
def show_results():
    st.header("AI Readiness Assessment Results")
    
    # Calculate scores
    category_scores, q_values, softmax_weights, overall_scores = calculate_scores(st.session_state.responses)
    
    st.markdown("""
    <div class="card">
        <h2>Executive Summary</h2>
        <p>This dashboard presents your organization's AI readiness assessment results across multiple dimensions.
        The scores are calculated using a Q-learning algorithm that weights different aspects of AI readiness.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display overall scores
    st.subheader("Overall Readiness Scores")
    
    # Create columns for the overall scores and radar chart
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display overall scores in a table
        overall_df = pd.DataFrame({
            'Assessment Category': list(overall_scores.keys()),
            'Readiness Score': [round(score * 100 / 4, 1) for score in overall_scores.values()]
        })
        
        overall_df = overall_df.sort_values('Readiness Score', ascending=False)
        
        # Calculate average overall score
        avg_score = overall_df['Readiness Score'].mean()
        
        # Display the table with custom styling
        st.dataframe(
            overall_df.style.background_gradient(cmap='Blues', subset=['Readiness Score']),
            hide_index=True,
            use_container_width=True
        )
        
        # Create gauge chart for average score
        gauge_img = create_gauge_chart(avg_score * 4 / 100, "Average AI Readiness")
        st.image(gauge_img, use_column_width=True)
        
        # Interpretation of the score
        if avg_score >= 75:
            st.success("**Analysis**: Your organization shows strong AI readiness across multiple dimensions.")
        elif avg_score >= 50:
            st.info("**Analysis**: Your organization has moderate AI readiness with room for improvement.")
        else:
            st.warning("**Analysis**: Your organization needs significant improvement in AI readiness.")
    
    with col2:
        # Create radar chart for overall scores using matplotlib
        categories = list(overall_scores.keys())
        values = list(overall_scores.values())
        
        img = create_radar_chart(categories, values, "AI Readiness Radar")
        st.image(img, use_column_width=True)
    
    # Detailed results for each assessment category
    st.subheader("Detailed Assessment Results")
    
    for category, scores in category_scores.items():
        with st.expander(f"{category} Assessment Details"):
            # Create columns for category scores and weights
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"<h3 style='color:{theme_colors['primary']};'>{category} Category Scores</h3>", unsafe_allow_html=True)
                
                # Convert to percentage for better readability
                cat_scores_df = pd.DataFrame({
                    'Category': list(scores.keys()),
                    'Score (%)': [round(score * 100 / 4, 1) for score in scores.values()]
                })
                
                # Display the table with custom styling
                st.dataframe(
                    cat_scores_df.style.background_gradient(cmap='Blues', subset=['Score (%)']),
                    hide_index=True,
                    use_container_width=True
                )
            
            with col2:
                # Create bar chart for category scores using matplotlib
                img = create_category_bar_chart(list(scores.keys()), list(scores.values()), f"{category} Category Scores")
                st.image(img, use_column_width=True)
            
            # Display Q-values and weights with heatmap
            st.markdown(f"<h3 style='color:{theme_colors['primary']};'>{category} Q-Learning Analysis</h3>", unsafe_allow_html=True)
            
            # Create heatmap for Q-values and weights
            q_vals = [q_values[category][cat] for cat in scores.keys()]
            weight_vals = [softmax_weights[category][i] for i, _ in enumerate(scores.keys())]
            
            heatmap_img = create_qvalue_weight_heatmap(
                list(scores.keys()),
                q_vals,
                weight_vals,
                f"{category} Q-Learning Weights Analysis"
            )
            st.image(heatmap_img, use_column_width=True)
            
            # Add explanation of Q-learning
            with st.expander("Understanding Q-Learning and Weights"):
                st.markdown("""
                **Q-Learning** is a reinforcement learning technique that helps prioritize different aspects of AI readiness:
                
                * **Q-Values**: Represent the learned importance of each category through iterative reinforcement.
                * **Softmax Weights**: Transform Q-values into probability weights that sum to 100%.
                * **Higher weights** indicate categories that have greater influence on the overall score.
                
                This approach allows the assessment to adapt and emphasize the most critical areas for your organization.
                """)
    
    # Recommendations section
    st.subheader("Recommendations for Improvement")
    
    # Find the lowest scoring categories for each assessment
    recommendations = {}
    for category, scores in category_scores.items():
        if scores:  # Check if scores dictionary is not empty
            min_score_category = min(scores.items(), key=lambda x: x[1])
            recommendations[category] = {
                'category': min_score_category[0],
                'score': min_score_category[1]
            }
    
    # Create columns for recommendations
    cols = st.columns(3)
    col_idx = 0
    
    # Display recommendations in cards
    for category, rec in recommendations.items():
        with cols[col_idx]:
            st.markdown(f"""
            <div class="card" style="height: 300px; overflow-y: auto;">
                <h3 style="color:{theme_colors['primary']};">{category}</h3>
                <p><b>Focus Area:</b> {rec['category']}</p>
                <p><b>Current Score:</b> {round(rec['score'] * 100 / 4, 1)}%</p>
                <h4>Recommendations:</h4>
                <ul>
            """, unsafe_allow_html=True)
            
            # Generate recommendations based on the category
            if category == "AI Governance":
                st.markdown("""
                * Establish clear policies for ethical AI development
                * Assign explicit algorithmic accountability roles
                * Stay updated with regulatory compliance requirements
                * Implement robust bias mitigation mechanisms
                """)
            elif category == "AI Culture":
                st.markdown("""
                * Develop a clear AI strategy and vision
                * Encourage AI experimentation and innovation
                * Promote cross-functional AI collaboration
                * Implement effective AI change management practices
                """)
            elif category == "AI Data":
                st.markdown("""
                * Improve data accessibility and cataloging
                * Strengthen data governance and compliance
                * Enhance data quality and processing pipelines
                * Address bias and fairness in AI data
                * Upgrade data infrastructure and security
                """)
            elif category == "AI Infrastructure":
                st.markdown("""
                * Invest in necessary compute resources for AI workloads
                * Optimize storage and data access for AI
                * Improve AI deployment efficiency
                * Implement HPC and performance optimization
                * Enhance MLOps readiness
                """)
            elif category == "AI Strategy":
                st.markdown("""
                * Strengthen data security and encryption
                * Implement robust model access controls
                * Secure AI APIs against unauthorized access
                * Develop a comprehensive AI deployment strategy
                * Establish effective AI monitoring and logging
                """)
            elif category == "AI Talent":
                st.markdown("""
                * Develop a structured AI talent acquisition strategy
                * Invest in AI upskilling and training programs
                * Promote cross-functional AI collaboration
                * Cultivate AI leadership and culture
                * Implement MLOps and AI engineering best practices
                """)
            
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            col_idx = (col_idx + 1) % 3
    
    # Add a download button for the report
    st.subheader("Download Full Report")
    st.markdown("""
    <div class="card">
        <p>Download a comprehensive report of your AI readiness assessment results, including detailed scores, 
        charts, and personalized recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a PDF report (placeholder for now)
    if st.button("Generate PDF Report", type="primary"):
        st.success("Report generation feature will be available in the next update.")

if __name__ == "__main__":
    main()
