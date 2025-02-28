"""
Visualization functions for AI Readiness Assessment App
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import base64
from matplotlib.colors import LinearSegmentedColormap

# Define theme colors
theme_colors = {
    "primary": "#0284C7",
    "secondary": "#38BDF8",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "text": "#1E293B",
    "background": "#F1F5F9"
}

def create_radar_chart(categories, values):
    """
    Create a radar chart for displaying category scores
    """
    # Convert values to numpy array
    values = np.array(values)
    
    # Number of variables
    N = len(categories)
    
    # What will be the angle of each axis in the plot
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    
    # Make the plot close on itself
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    categories = np.concatenate((categories, [categories[0]]))
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories[:-1], fontsize=11, fontweight='bold')
    
    # Draw the labels for the y-axis (score values)
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80], ["20%", "40%", "60%", "80%"], fontsize=9, color="grey")
    plt.ylim(0, 100)
    
    # Plot the values
    ax.plot(angles, values, linewidth=2, linestyle='solid', color=theme_colors["primary"])
    
    # Fill the area
    ax.fill(angles, values, alpha=0.25, color=theme_colors["secondary"])
    
    # Add value labels at each point
    for angle, value, category in zip(angles[:-1], values[:-1], categories[:-1]):
        ax.text(angle, value + 10, f"{int(value)}%", 
                ha='center', va='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9, edgecolor=theme_colors["primary"]))
    
    # Remove axis lines and set grid color
    ax.spines['polar'].set_visible(False)
    ax.grid(color='#E2E8F0')
    
    return fig

def create_gauge_chart(score):
    """
    Create a gauge chart for displaying the overall score
    """
    # Start and end angle for the gauge
    start_angle = np.pi/2 + np.pi/4
    end_angle = np.pi/2 - np.pi/4
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw=dict(polar=True))
    
    # Define ranges for different color segments
    ranges = [
        (0, 30, theme_colors["error"]), 
        (30, 60, theme_colors["warning"]), 
        (60, 80, theme_colors["success"]), 
        (80, 100, theme_colors["primary"])
    ]
    
    # Draw color segments
    for i, (start_range, end_range, color) in enumerate(ranges):
        # Convert percentage to radians
        start_rad = start_angle - (start_range/100) * (start_angle - end_angle)
        end_rad = start_angle - (end_range/100) * (start_angle - end_angle)
        
        # Create the colored arc
        ax.barh(0, 1, left=start_rad, width=start_rad-end_rad, height=0.1, color=color, alpha=0.8)
    
    # Draw the score needle
    score_rad = start_angle - (score/100) * (start_angle - end_angle)
    ax.plot([0, np.cos(score_rad)], [0, np.sin(score_rad)], color=theme_colors["text"], linewidth=2)
    
    # Add a circle at the center
    circle = plt.Circle((0, 0), 0.1, transform=ax.transData._b, color='white', zorder=10)
    ax.add_artist(circle)
    
    # Set the limits and remove ticks
    ax.set_rlim(0, 1)
    ax.set_rticks([])
    ax.set_xticks([])
    
    # Add the score text
    ax.text(0, -0.3, f"{int(score)}%", ha='center', va='center', fontsize=24, fontweight='bold', color=theme_colors["text"])
    
    # Display category labels
    labels = ["Low", "Moderate", "High", "Excellent"]
    positions = [15, 45, 70, 90]
    for i, label in enumerate(labels):
        angle = start_angle - (positions[i]/100) * (start_angle - end_angle)
        x = 0.7 * np.cos(angle)
        y = 0.7 * np.sin(angle)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, color="#475569")
    
    return fig

def create_bar_chart(categories, values):
    """
    Create a bar chart for displaying category scores
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Format categories for display (remove 'AI ' prefix if present)
    display_categories = [cat.replace('AI ', '') if 'AI ' in cat else cat for cat in categories]
    
    # Create horizontal bar chart with colors based on values
    colors = [theme_colors["primary"] if v >= 60 else theme_colors["warning"] if v >= 30 else theme_colors["error"] for v in values]
    bars = ax.barh(display_categories, values, color=colors)
    
    # Add data labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2, f"{int(width)}%", 
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    # Customize grid
    ax.grid(axis='x', linestyle='--', alpha=0.7, color='#E2E8F0')
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Set x-axis limits
    ax.set_xlim(0, 105)
    
    # Make y-tick labels bold
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
    
    return fig
