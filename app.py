import streamlit as st
import pandas as pd
import io

# ==========================================
# 1. REUSABLE HELPER FUNCTIONS
# ==========================================

def calculate_percentage(df, part_col, total_col):
    """Safely calculates a percentage if the columns exist."""
    # Bulletproof check: If the column is missing, return 0% instead of crashing
    if part_col not in df.columns or total_col not in df.columns:
        return pd.Series(["0%"] * len(df), index=df.index)
    
    return (df[part_col] / df[total_col].replace(0, pd.NA) * 100).fillna(0).round(2).astype(str) + '%'

# ==========================================
# 2. UNIVERSAL CRLA PROCESSOR 
# ==========================================

def process_crla(df, group_column):
    # CLEAN DATA: Strip any hidden trailing/leading spaces from CSV headers
    df.columns = df.columns.str.strip()

    # The ideal columns we want to process
    ideal_columns_to_sum = [
        'Total Assessed', 'Total Low Emerging', 'Total High Emerging', 'Total Developing', 'Total Transitioning', 'Total At Grade Level',
        'G1 Total Assessed', 'G1 Lower Emergent', 'G1 Higher Emergent', 'G1 Developing', 'G1 Transitioning', 'G1 Grade Level',
        'G2 Total Fil Assessed', 'G2 Fil Lower Emergent', 'G2 FIl Higher Emergent', 'G2 Fil Developing', 'G2 Fil Transitioning', 'G2 Fil Grade Level',
        'G3 Total Eng Assessed', 'G3 Eng Lower Emergent', 'G3 Eng Higher Emergent', 'G3 Eng Developing', 'G3 Eng Transitioning', 'G3 Eng Grade Level'
    ]

    # BULLETPROOFING: Only attempt to sum columns that actually exist in the uploaded CSV
    columns_to_sum = [col for col in ideal_columns_to_sum if col in df.columns]

    grouped = df.groupby(group_column)[columns_to_sum].sum()
    grouped['total_schools'] = df.groupby(group_column)['School ID'].nunique()
    grouped.loc['Grand Total'] = grouped.sum()

    # Overall
    grouped['% Total Low Emerging'] = calculate_percentage(grouped, 'Total Low Emerging', 'Total Assessed')
    grouped['% Total High Emerging'] = calculate_percentage(grouped, 'Total High Emerging', 'Total Assessed')
    grouped['% Total Developing'] = calculate_percentage(grouped, 'Total Developing', 'Total Assessed')
    grouped['% Total Transitioning'] = calculate_percentage(grouped, 'Total Transitioning', 'Total Assessed')
    grouped['% Total At Grade Level'] = calculate_percentage(grouped, 'Total At Grade Level', 'Total Assessed')

    # Grade 1
    grouped['% G1 Lower Emergent'] = calculate_percentage(grouped, 'G1 Lower Emergent', 'G1 Total Assessed')
    grouped['% G1 Higher Emergent'] = calculate_percentage(grouped, 'G1 Higher Emergent', 'G1 Total Assessed')
    grouped['% G1 Developing'] = calculate_percentage(grouped, 'G1 Developing', 'G1 Total Assessed')
    grouped['% G1 Transitioning'] = calculate_percentage(grouped, 'G1 Transitioning', 'G1 Total Assessed')
    grouped['% G1 Grade Level'] = calculate_percentage(grouped, 'G1 Grade Level', 'G1 Total Assessed')

    # Grade 2 (Filipino)
    grouped['% G2 Fil Lower Emergent'] = calculate_percentage(grouped, 'G2 Fil Lower Emergent', 'G2 Total Fil Assessed')
    grouped['% G2 FIl Higher Emergent'] = calculate_percentage(grouped, 'G2 FIl Higher Emergent', 'G2 Total Fil Assessed')
    grouped['% G2 Fil Developing'] = calculate_percentage(grouped, 'G2 Fil Developing', 'G2 Total Fil Assessed')
    grouped['% G2 Fil Transitioning'] = calculate_percentage(grouped, 'G2 Fil Transitioning', 'G2 Total Fil Assessed')
    grouped['% G2 Fil Grade Level'] = calculate_percentage(grouped, 'G2 Fil Grade Level', 'G2 Total Fil Assessed')

    # Grade 3 (English)
    grouped['% G3 Eng Lower Emergent'] = calculate_percentage(grouped, 'G3 Eng Lower Emergent', 'G3 Total Eng Assessed')
    grouped['% G3 Eng Higher Emergent'] = calculate_percentage(grouped, 'G3 Eng Higher Emergent', 'G3 Total Eng Assessed')
    grouped['% G3 Eng Developing'] = calculate_percentage(grouped, 'G3 Eng Developing', 'G3 Total Eng Assessed')
    grouped['% G3 Eng Transitioning'] = calculate_percentage(grouped, 'G3 Eng Transitioning', 'G3 Total Eng Assessed')
    grouped['% G3 Eng Grade Level'] = calculate_percentage(grouped, 'G3 Eng Grade Level', 'G3 Total Eng Assessed')

    ideal_final_layout = [
        'total_schools', 'Total Assessed', 'Total Low Emerging', '% Total Low Emerging', 'Total High Emerging', '% Total High Emerging', 'Total Developing', '% Total Developing', 'Total Transitioning', '% Total Transitioning', 'Total At Grade Level', '% Total At Grade Level',
        'G1 Total Assessed', 'G1 Lower Emergent', '% G1 Lower Emergent', 'G1 Higher Emergent', '% G1 Higher Emergent', 'G1 Developing', '% G1 Developing', 'G1 Transitioning', '% G1 Transitioning', 'G1 Grade Level', '% G1 Grade Level',
        'G2 Total Fil Assessed', 'G2 Fil Lower Emergent', '% G2 Fil Lower Emergent', 'G2 FIl Higher Emergent', '% G2 FIl Higher Emergent', 'G2 Fil Developing', '% G2 Fil Developing', 'G2 Fil Transitioning', '% G2 Fil Transitioning', 'G2 Fil Grade Level', '% G2 Fil Grade Level',
        'G3 Total Eng Assessed', 'G3 Eng Lower Emergent', '% G3 Eng Lower Emergent', 'G3 Eng Higher Emergent', '% G3 Eng Higher Emergent', 'G3 Eng Developing', '% G3 Eng Developing', 'G3 Eng Transitioning', '% G3 Eng Transitioning', 'G3 Eng Grade Level', '% G3 Eng Grade Level'
    ]

    # BULLETPROOFING: Only output columns that were successfully created
    final_layout = [col for col in ideal_final_layout if col in grouped.columns]

    return grouped[final_layout]

# ==========================================
# 3. INTERACTIVE WEB WORKFLOW
# ==========================================

st.title("CRLA Automated Report Generator")

# Ask the user which term they are processing
term_name = st.radio("Which term are you processing?", ("BoSY", "EoSY"))

# Web File Uploader
uploaded_file = st.file_uploader(f"Upload your {term_name} Assessment CSV", type=["csv"])

if uploaded_file is not None:
    try:
        st.info("Processing data... Please wait.")
        
        # Read the data from the uploaded file
        raw_data = pd.read_csv(uploaded_file)
        
        # Process for Region and Division
        summary_table_region = process_crla(raw_data, 'Region')
        summary_table_division = process_crla(raw_data, 'Division')
        
        st.success("Success! Your reports have been created.")
        
        # Show a quick preview on the website
        st.subheader("Preview: Regional Pivot")
        st.dataframe(summary_table_region.head())
        
        # Convert dataframes to CSVs in memory for downloading
        region_csv = summary_table_region.to_csv().encode('utf-8')
        division_csv = summary_table_division.to_csv().encode('utf-8')
        
        # Provide download buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Regional Pivot CSV",
                data=region_csv,
                file_name=f'CRLA_{term_name}_Regional_Pivot.csv',
                mime='text/csv',
            )
        with col2:
            st.download_button(
                label="Download Division Pivot CSV",
                data=division_csv,
                file_name=f'CRLA_{term_name}_Division_Pivot.csv',
                mime='text/csv',
            )
            
    except Exception as e:
        # If any other error happens, show it nicely on the website instead of a red crash box
        st.error(f"Data Processing Error: {e}")
        st.write("Please check your CSV file to ensure it is the correct format.")
