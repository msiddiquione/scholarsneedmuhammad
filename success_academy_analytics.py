#!/usr/bin/env python3
"""
Success Academy Analytics

Analyzes NYC school enrollment data for market analysis,
5-year enrollment projections, and dashboard requirements.
"""

import os
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Paths
DATA_DIR = Path(__file__).parent
ENROLLMENT_FILE = DATA_DIR / "Success_Academy_Analytics___Data_Science_Case_Study_v2_(1).xlsx - Enrollment.csv"
OUTPUT_DIR = DATA_DIR / "analysis_output"

# Visualization Settings
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = [12, 6]

# Gemini setup
GEMINI_AVAILABLE = False
gemini_model = None

try:
    import google.generativeai as genai
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        GEMINI_AVAILABLE = True
except Exception as e:
    print(f"Note: Gemini AI not available ({e})")


def clean_percentage(value):
    """Convert percentage strings to float."""
    text = str(value).strip()
    
    if 'Above 95' in text: return 0.95
    if 'Below 5' in text: return 0.05
    if pd.isna(value) or text == '' or text.lower() == 'nan': return np.nan
    
    try:
        return float(text.replace('%', '').replace(',', '')) / 100.0
    except ValueError:
        return np.nan

def get_school_type(row):
    """Classify school as Success Academy (SA), Other Charter (C), or District (DS)."""
    school_name = str(row.get('School', '')).lower()
    charter_flag = str(row.get('Charter  (Y/N) ?', '')).upper().strip()
    
    if 'success academy' in school_name:
        return 'SA'
    if charter_flag == 'Y':
        return 'C'
    return 'DS'

def parse_school_year(value):
    """Parse school year (e.g., '2018-19' -> 2018)."""
    text = str(value).strip()
    if '-' in text:
        try:
            return int(text.split('-')[0])
        except ValueError:
            return None
    try:
        return int(float(text))
    except (ValueError, TypeError):
        return None


def load_enrollment_data():
    """Load and preprocess enrollment data."""
    print("Loading enrollment data...")
    
    df = pd.read_csv(ENROLLMENT_FILE)
    df['Year'] = df['Year'].apply(parse_school_year)
    df['Total Enrollment'] = pd.to_numeric(df['Total Enrollment'], errors='coerce')
    
    percent_columns = ['% Poverty', 'Economic Need Index', '% Female', '% Male',
                       '% Asian', '% Black', '% Hispanic', '% White',
                       '% Students with Disabilities', '% English Language Learners']
    
    for col in percent_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_percentage)
    
    df['School_Type'] = df.apply(get_school_type, axis=1)
    
    print(f"Loaded {len(df):,} records.")
    return df




def analyze_overall_market(df):
    """Analyze market trends including enrollment by school type and borough."""
    print("Analyzing market trends...")
    
    # Get enrollment by school type and year
    trends = df.groupby(['Year', 'School_Type']).agg({
        'Total Enrollment': ['sum', 'mean', 'count']
    }).round(2)
    trends.columns = ['Total_Enrollment', 'Avg_Enrollment', 'School_Count']
    trends = trends.reset_index()
    
    # Also grab borough breakdown if available
    borough_trends = None
    if 'Borough' in df.columns:
        borough_trends = df.groupby(['Year', 'Borough'])['Total Enrollment'].sum().unstack()
    
    # SA-specific numbers
    sa_data = df[df['School_Type'] == 'SA']
    sa_by_year = sa_data.groupby('Year')['Total Enrollment'].agg(['sum', 'mean', 'count'])
    sa_by_year.columns = ['Total', 'Average', 'School_Count']
    
    return {
        'trends': trends,
        'borough_trends': borough_trends,
        'sa_trends': sa_by_year
    }


def project_enrollment(df, years_to_project=5):
    """Generate 5-year enrollment projections using 3-year average growth rate."""
    print("Generating projections...")
    
    sa_data = df[df['School_Type'] == 'SA']
    yearly = sa_data.groupby('Year')['Total Enrollment'].sum()
    
    # Use last 3 years to get growth rate
    avg_growth_rate = 0
    if len(yearly) >= 3:
        recent_years = yearly.tail(3)
        growth_rates = recent_years.pct_change().dropna()
        avg_growth_rate = growth_rates.mean()
    
    print(f"Growth rate (3-year avg): {avg_growth_rate:.1%}")
    
    # Build out projections
    last_year = yearly.index.max()
    current = yearly.iloc[-1]
    
    projections = {'Year': [], 'Projected_Enrollment': [], 'Method': []}
    
    for i in range(1, years_to_project + 1):
        current = current * (1 + avg_growth_rate)
        projections['Year'].append(last_year + i)
        projections['Projected_Enrollment'].append(round(current))
        projections['Method'].append('3-Year Avg Growth')
    
    return {
        'historical': yearly,
        'projections': pd.DataFrame(projections),
        'growth_rate': avg_growth_rate
    }


def create_visualizations(df, market_data, projections, output_dir):
    """Generate and save visualization charts."""
    print("Creating visualizations...")
    
    # Enrollment trends chart
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    trends = market_data['trends']
    for school_type in ['SA', 'C', 'DS']:
        data = trends[trends['School_Type'] == school_type]
        label = {'SA': 'Success Academy', 'C': 'Other Charter', 'DS': 'District'}[school_type]
        axes[0].plot(data['Year'], data['Total_Enrollment'], marker='o', label=label, linewidth=2)
    
    axes[0].set_title('Total Enrollment by School Type', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Total Enrollment')
    axes[0].legend()
    axes[0].ticklabel_format(style='plain', axis='y')
    
    # Projection chart
    hist = projections['historical']
    proj = projections['projections']
    
    axes[1].plot(hist.index, hist.values, marker='o', label='Historical', linewidth=2, color='blue')
    axes[1].plot(proj['Year'], proj['Projected_Enrollment'], marker='s', 
                 linestyle='--', label='Projected', linewidth=2, color='orange')
    axes[1].axvline(x=hist.index.max(), color='gray', linestyle=':', alpha=0.5)
    
    axes[1].set_title('Success Academy 5-Year Projection', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Total Enrollment')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'enrollment_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Demographics chart
    demo_cols = ['% Asian', '% Black', '% Hispanic', '% White']
    available = [c for c in demo_cols if c in df.columns]
    
    if available:
        demo = df.groupby('School_Type')[available].mean()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        demo.T.plot(kind='bar', ax=ax)
        ax.set_title('Demographic Breakdown by School Type', fontsize=14, fontweight='bold')
        ax.set_xlabel('Demographic Category')
        ax.set_ylabel('Percentage')
        ax.set_xticklabels([c.replace('% ', '') for c in available], rotation=45)
        ax.legend(['Other Charter', 'District', 'Success Academy'])
        
        plt.tight_layout()
        plt.savefig(output_dir / 'demographics.png', dpi=150, bbox_inches='tight')
        plt.close()

    # Economic Analysis Chart
    econ_cols = ['% Poverty', 'Economic Need Index']
    available_econ = [c for c in econ_cols if c in df.columns]
    
    if available_econ:
        print("   Generating economic analysis chart...")
        econ = df.groupby(['Year', 'School_Type'])[available_econ].mean().reset_index()
        
        # Melt for easier plotting with seaborn if multiple metrics, but separate plots are cleaner
        fig, axes = plt.subplots(1, len(available_econ), figsize=(7 * len(available_econ), 5))
        if len(available_econ) == 1:
            axes = [axes]
            
        for i, col in enumerate(available_econ):
            sns.lineplot(data=econ, x='Year', y=col, hue='School_Type', ax=axes[i], marker='o', linewidth=2)
            axes[i].set_title(f'Average {col} by School Type', fontsize=12, fontweight='bold')
            axes[i].set_xlabel('Year')
            axes[i].legend(title='School Type')
            
        plt.tight_layout()
        plt.savefig(output_dir / 'economic_analysis.png', dpi=150, bbox_inches='tight')
        plt.close()


def generate_ai_analysis(df, market_data, projections):
    """Generate executive summary using Gemini AI."""
    if not GEMINI_AVAILABLE:
        return None
    
    print("Generating AI insights...")
    
    trends = market_data['trends']
    sa_trends = market_data['sa_trends']
    proj = projections['projections']
    
    data_summary = f"""
NYC School Enrollment Analysis (5-Year Period)
TRENDS:
{trends.to_string()}

SA TRENDS:
{sa_trends.to_string()}

PROJECTIONS:
{proj.to_string()}

Growth Rate: {projections['growth_rate']:.1%}
"""
    
    prompt = f"""As a data analyst for Success Academy, provide a concise executive summary based on:
{data_summary}

Include:
1. MARKET OBSERVATIONS (3-4 bullets)
2. RECOMMENDED ADDITIONAL DATA (4 items)
3. 5-YEAR PROJECTION SUMMARY (Assumptions/Risks)
4. DASHBOARD RECOMMENDATIONS (Target users, metrics, features)
"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"AI analysis failed: {e}")
        return None


def save_outputs(df, market_data, projections, ai_analysis, output_dir):
    """Save analysis results to CSV and text files."""
    print("Saving outputs...")
    
    # CSVs
    df.to_csv(output_dir / 'cleaned_enrollment_data.csv', index=False)
    market_data['trends'].to_csv(output_dir / 'enrollment_trends.csv', index=False)
    projections['projections'].to_csv(output_dir / 'projections.csv', index=False)
    
    # AI summary
    if ai_analysis:
        with open(output_dir / 'executive_summary.md', 'w') as f:
            f.write("# Success Academy Analytics - Executive Summary\n\n")
            f.write(ai_analysis)
    
    # Text report
    with open(output_dir / 'analysis_report.txt', 'w') as f:
        f.write("SUCCESS ACADEMY ENROLLMENT ANALYSIS\n")
        f.write("===================================\n\n")
        
        f.write("DATA SUMMARY\n")
        f.write("------------\n")
        f.write(f"Total records: {len(df):,}\n")
        f.write(f"Years: {df['Year'].min()} - {df['Year'].max()}\n")
        f.write(f"Schools: {df['DBN'].nunique():,}\n\n")
        
        f.write("SCHOOL TYPE BREAKDOWN\n")
        f.write("---------------------\n")
        for stype, count in df['School_Type'].value_counts().items():
            label = {'SA': 'Success Academy', 'C': 'Other Charter', 'DS': 'District'}[stype]
            f.write(f"  {label}: {count:,}\n")
        f.write("\n")
        
        f.write("5-YEAR PROJECTIONS (SA)\n")
        f.write("-----------------------\n")
        f.write(projections['projections'].to_string(index=False))
        f.write("\n")
    
    print(f"Outputs saved to: {output_dir}")


def main():
    """Execute analysis pipeline."""
    print("Starting analysis...")
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Run analysis
    df = load_enrollment_data()
    market_data = analyze_overall_market(df)
    projections = project_enrollment(df)
    
    create_visualizations(df, market_data, projections, OUTPUT_DIR)
    ai_analysis = generate_ai_analysis(df, market_data, projections)
    save_outputs(df, market_data, projections, ai_analysis, OUTPUT_DIR)
    
    print("Analysis complete.")



if __name__ == "__main__":
    main()
