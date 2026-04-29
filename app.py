import streamlit as st
import pandas as pd
import io

# ==========================================
# 1. REUSABLE HELPER FUNCTIONS
# ==========================================

def calculate_percentage(df, part_col, total_col):
    """Safely calculates a percentage if the columns exist."""
    if part_col not in df.columns or total_col not in df.columns:
        return pd.Series(["0%"] * len(df), index=df.index)
    
    return (df[part_col] / df[total_col].replace(0, pd.NA) * 100).fillna(0).round(2).astype(str) + '%'

# ==========================================
# 2. SPECIFIC ASSESSMENT PROCESSORS
# ==========================================

# --- CRLA ---
def process_crla(df, group_column):
    df.columns = df.columns.str.strip()
    
    ideal_columns_to_sum = [
        'Total Assessed', 'Total Low Emerging', 'Total High Emerging', 'Total Developing', 'Total Transitioning', 'Total At Grade Level',
        'G1 Total Assessed', 'G1 Lower Emergent', 'G1 Higher Emergent', 'G1 Developing', 'G1 Transitioning', 'G1 Grade Level',
        'G2 Total Fil Assessed', 'G2 Fil Lower Emergent', 'G2 FIl Higher Emergent', 'G2 Fil Developing', 'G2 Fil Transitioning', 'G2 Fil Grade Level',
        'G3 Total Eng Assessed', 'G3 Eng Lower Emergent', 'G3 Eng Higher Emergent', 'G3 Eng Developing', 'G3 Eng Transitioning', 'G3 Eng Grade Level'
    ]

    columns_to_sum = [col for col in ideal_columns_to_sum if col in df.columns]

    for col in columns_to_sum:
        clean_col = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(clean_col, errors='coerce').fillna(0)

    grouped = df.groupby(group_column)[columns_to_sum].sum()
    grouped['total_schools'] = df.groupby(group_column)['School ID'].nunique()
    grouped.loc['Grand Total'] = grouped.sum()

    grouped['% Total Low Emerging'] = calculate_percentage(grouped, 'Total Low Emerging', 'Total Assessed')
    grouped['% Total High Emerging'] = calculate_percentage(grouped, 'Total High Emerging', 'Total Assessed')
    grouped['% Total Developing'] = calculate_percentage(grouped, 'Total Developing', 'Total Assessed')
    grouped['% Total Transitioning'] = calculate_percentage(grouped, 'Total Transitioning', 'Total Assessed')
    grouped['% Total At Grade Level'] = calculate_percentage(grouped, 'Total At Grade Level', 'Total Assessed')

    grouped['% G1 Lower Emergent'] = calculate_percentage(grouped, 'G1 Lower Emergent', 'G1 Total Assessed')
    grouped['% G1 Higher Emergent'] = calculate_percentage(grouped, 'G1 Higher Emergent', 'G1 Total Assessed')
    grouped['% G1 Developing'] = calculate_percentage(grouped, 'G1 Developing', 'G1 Total Assessed')
    grouped['% G1 Transitioning'] = calculate_percentage(grouped, 'G1 Transitioning', 'G1 Total Assessed')
    grouped['% G1 Grade Level'] = calculate_percentage(grouped, 'G1 Grade Level', 'G1 Total Assessed')

    grouped['% G2 Fil Lower Emergent'] = calculate_percentage(grouped, 'G2 Fil Lower Emergent', 'G2 Total Fil Assessed')
    grouped['% G2 FIl Higher Emergent'] = calculate_percentage(grouped, 'G2 FIl Higher Emergent', 'G2 Total Fil Assessed')
    grouped['% G2 Fil Developing'] = calculate_percentage(grouped, 'G2 Fil Developing', 'G2 Total Fil Assessed')
    grouped['% G2 Fil Transitioning'] = calculate_percentage(grouped, 'G2 Fil Transitioning', 'G2 Total Fil Assessed')
    grouped['% G2 Fil Grade Level'] = calculate_percentage(grouped, 'G2 Fil Grade Level', 'G2 Total Fil Assessed')

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
    
    final_layout = [col for col in ideal_final_layout if col in grouped.columns]
    return grouped[final_layout]

# --- PHIL-IRI KS2 ---
def process_philiri_ks2_bosy(df, group_column):
    df.columns = df.columns.str.strip()
    ideal_columns_to_sum = [
        'Total Assessed (G4-G6)',
        'G4 Assessed', 'G4 Eng Grade Ready', 'G4 2LD Eng Frustration', 'G4 2LD Eng Instructional', 'G4 2LD Eng Independent', 'G4 3LD Eng Frustration', 'G4 3LD Eng Instructional', 'G4 3LD Eng Independent',
        'G5 Assessed', 'G5 Eng Grade Ready', 'G5 2LD Eng Frustration', 'G5 2LD Eng Instructional', 'G5 2LD Eng Independent', 'G5 3LD Eng Frustration', 'G5 3LD Eng Instructional', 'G5 3LD Eng Independent',
        'G6 Assessed', 'G6 Eng Grade Ready', 'G6 2LD Eng Frustration', 'G6 2LD Eng Instructional', 'G6 2LD Eng Independent', 'G6 3LD Eng Frustration', 'G6 3LD Eng Instructional', 'G6 3LD Eng Independent'
    ]
    
    columns_to_sum = [col for col in ideal_columns_to_sum if col in df.columns]

    for col in columns_to_sum:
        clean_col = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(clean_col, errors='coerce').fillna(0)

    grouped = df.groupby(group_column)[columns_to_sum].sum()
    grouped['total_schools'] = df.groupby(group_column)['School ID'].nunique()
    grouped.loc['Grand Total'] = grouped.sum()

    grouped['% G4 Eng Grade Ready'] = calculate_percentage(grouped, 'G4 Eng Grade Ready', 'G4 Assessed')
    grouped['% G4 2LD Eng Frustration'] = calculate_percentage(grouped, 'G4 2LD Eng Frustration', 'G4 Assessed')
    grouped['% G4 2LD Eng Instructional'] = calculate_percentage(grouped, 'G4 2LD Eng Instructional', 'G4 Assessed')
    grouped['% G4 2LD Eng Independent'] = calculate_percentage(grouped, 'G4 2LD Eng Independent', 'G4 Assessed')
    grouped['% G4 3LD Eng Frustration'] = calculate_percentage(grouped, 'G4 3LD Eng Frustration', 'G4 Assessed')
    grouped['% G4 3LD Eng Instructional'] = calculate_percentage(grouped, 'G4 3LD Eng Instructional', 'G4 Assessed')
    grouped['% G4 3LD Eng Independent'] = calculate_percentage(grouped, 'G4 3LD Eng Independent', 'G4 Assessed')

    grouped['% G5 Eng Grade Ready'] = calculate_percentage(grouped, 'G5 Eng Grade Ready', 'G5 Assessed')
    grouped['% G5 2LD Eng Frustration'] = calculate_percentage(grouped, 'G5 2LD Eng Frustration', 'G5 Assessed')
    grouped['% G5 2LD Eng Instructional'] = calculate_percentage(grouped, 'G5 2LD Eng Instructional', 'G5 Assessed')
    grouped['% G5 2LD Eng Independent'] = calculate_percentage(grouped, 'G5 2LD Eng Independent', 'G5 Assessed')
    grouped['% G5 3LD Eng Frustration'] = calculate_percentage(grouped, 'G5 3LD Eng Frustration', 'G5 Assessed')
    grouped['% G5 3LD Eng Instructional'] = calculate_percentage(grouped, 'G5 3LD Eng Instructional', 'G5 Assessed')
    grouped['% G5 3LD Eng Independent'] = calculate_percentage(grouped, 'G5 3LD Eng Independent', 'G5 Assessed')

    grouped['% G6 Eng Grade Ready'] = calculate_percentage(grouped, 'G6 Eng Grade Ready', 'G6 Assessed')
    grouped['% G6 2LD Eng Frustration'] = calculate_percentage(grouped, 'G6 2LD Eng Frustration', 'G6 Assessed')
    grouped['% G6 2LD Eng Instructional'] = calculate_percentage(grouped, 'G6 2LD Eng Instructional', 'G6 Assessed')
    grouped['% G6 2LD Eng Independent'] = calculate_percentage(grouped, 'G6 2LD Eng Independent', 'G6 Assessed')
    grouped['% G6 3LD Eng Frustration'] = calculate_percentage(grouped, 'G6 3LD Eng Frustration', 'G6 Assessed')
    grouped['% G6 3LD Eng Instructional'] = calculate_percentage(grouped, 'G6 3LD Eng Instructional', 'G6 Assessed')
    grouped['% G6 3LD Eng Independent'] = calculate_percentage(grouped, 'G6 3LD Eng Independent', 'G6 Assessed')

    ideal_final_layout = [
        'total_schools', 'Total Assessed (G4-G6)',
        'G4 Assessed', 'G4 Eng Grade Ready', '% G4 Eng Grade Ready', 'G4 2LD Eng Frustration', '% G4 2LD Eng Frustration', 'G4 2LD Eng Instructional', '% G4 2LD Eng Instructional', 'G4 2LD Eng Independent', '% G4 2LD Eng Independent', 'G4 3LD Eng Frustration', '% G4 3LD Eng Frustration', 'G4 3LD Eng Instructional', '% G4 3LD Eng Instructional', 'G4 3LD Eng Independent', '% G4 3LD Eng Independent',
        'G5 Assessed', 'G5 Eng Grade Ready', '% G5 Eng Grade Ready', 'G5 2LD Eng Frustration', '% G5 2LD Eng Frustration', 'G5 2LD Eng Instructional', '% G5 2LD Eng Instructional', 'G5 2LD Eng Independent', '% G5 2LD Eng Independent', 'G5 3LD Eng Frustration', '% G5 3LD Eng Frustration', 'G5 3LD Eng Instructional', '% G5 3LD Eng Instructional', 'G5 3LD Eng Independent', '% G5 3LD Eng Independent',
        'G6 Assessed', 'G6 Eng Grade Ready', '% G6 Eng Grade Ready', 'G6 2LD Eng Frustration', '% G6 2LD Eng Frustration', 'G6 2LD Eng Instructional', '% G6 2LD Eng Instructional', 'G6 2LD Eng Independent', '% G6 2LD Eng Independent', 'G6 3LD Eng Frustration', '% G6 3LD Eng Frustration', 'G6 3LD Eng Instructional', '% G6 3LD Eng Instructional', 'G6 3LD Eng Independent', '% G6 3LD Eng Independent'
    ]
    final_layout = [col for col in ideal_final_layout if col in grouped.columns]
    return grouped[final_layout]

def process_philiri_ks2_eosy(df, group_column):
    df.columns = df.columns.str.strip()
    ideal_columns_to_sum = [
        'Total Assessed (G4-G6)', 'Total Eng Assessed', 'Total Eng Frustration', 'Total Eng Instructional', 'Total Eng Independent',
        'G4 Assessed', 'G4 Eng Frustration', 'G4 Eng Instructional', 'G4 Eng Independent',
        'G5 Assessed', 'G5 Eng Frustration', 'G5 Eng Instructional', 'G5 Eng Independent',
        'G6 Assessed', 'G6 Eng Frustration', 'G6 Eng Instructional', 'G6 Eng Independent'
    ]

    columns_to_sum = [col for col in ideal_columns_to_sum if col in df.columns]

    for col in columns_to_sum:
        clean_col = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(clean_col, errors='coerce').fillna(0)

    grouped = df.groupby(group_column)[columns_to_sum].sum()
    grouped['total_schools'] = df.groupby(group_column)['School ID'].nunique()
    grouped.loc['Grand Total'] = grouped.sum()

    grouped['% Total Eng Frustration'] = calculate_percentage(grouped, 'Total Eng Frustration', 'Total Eng Assessed')
    grouped['% Total Eng Instructional'] = calculate_percentage(grouped, 'Total Eng Instructional', 'Total Eng Assessed')
    grouped['% Total Eng Independent'] = calculate_percentage(grouped, 'Total Eng Independent', 'Total Eng Assessed')

    grouped['% G4 Eng Frustration'] = calculate_percentage(grouped, 'G4 Eng Frustration', 'G4 Assessed')
    grouped['% G4 Eng Instructional'] = calculate_percentage(grouped, 'G4 Eng Instructional', 'G4 Assessed')
    grouped['% G4 Eng Independent'] = calculate_percentage(grouped, 'G4 Eng Independent', 'G4 Assessed')

    grouped['% G5 Eng Frustration'] = calculate_percentage(grouped, 'G5 Eng Frustration', 'G5 Assessed')
    grouped['% G5 Eng Instructional'] = calculate_percentage(grouped, 'G5 Eng Instructional', 'G5 Assessed')
    grouped['% G5 Eng Independent'] = calculate_percentage(grouped, 'G5 Eng Independent', 'G5 Assessed')

    grouped['% G6 Eng Frustration'] = calculate_percentage(grouped, 'G6 Eng Frustration', 'G6 Assessed')
    grouped['% G6 Eng Instructional'] = calculate_percentage(grouped, 'G6 Eng Instructional', 'G6 Assessed')
    grouped['% G6 Eng Independent'] = calculate_percentage(grouped, 'G6 Eng Independent', 'G6 Assessed')

    ideal_final_layout = [
        'total_schools', 'Total Assessed (G4-G6)',
        'Total Eng Assessed', 'Total Eng Frustration', '% Total Eng Frustration', 'Total Eng Instructional', '% Total Eng Instructional', 'Total Eng Independent', '% Total Eng Independent',
        'G4 Assessed', 'G4 Eng Frustration', '% G4 Eng Frustration', 'G4 Eng Instructional', '% G4 Eng Instructional', 'G4 Eng Independent', '% G4 Eng Independent',
        'G5 Assessed', 'G5 Eng Frustration', '% G5 Eng Frustration', 'G5 Eng Instructional', '% G5 Eng Instructional', 'G5 Eng Independent', '% G5 Eng Independent',
        'G6 Assessed', 'G6 Eng Frustration', '% G6 Eng Frustration', 'G6 Eng Instructional', '% G6 Eng Instructional', 'G6 Eng Independent', '% G6 Eng Independent'
    ]
    final_layout = [col for col in ideal_final_layout if col in grouped.columns]
    return grouped[final_layout]

# --- PHIL-IRI KS3 ---
def process_philiri_ks3_bosy(df, group_column):
    df.columns = df.columns.str.strip()
    ideal_columns_to_sum = [
        'Total Assessed (G7-G10)',
        'G7 Eng Assessed', 'G7 Eng Grade Ready', 'G7 Eng Frustration 2Level', 'G7 Eng Instructional 2Level', 'G7 Eng Independent 2Level', 'G7 Eng Frustration 3Level', 'G7 Eng Instructional 3Level', 'G7 Eng Independent 3Level',
        'G8 Eng Assessed', 'G8 Eng Grade Ready', 'G8 Eng Frustration 2Level', 'G8 Eng Instructional 2Level', 'G8 Eng Independent 2Level', 'G8 Eng Frustration 3Level', 'G8 Eng Instructional 3Level', 'G8 Eng Independent 3Level',
        'G9 Eng Assessed', 'G9 Eng Grade Ready', 'G9 Eng Frustration 2Level', 'G9 Eng Instructional 2Level', 'G9 Eng Independent 2Level', 'G9 Eng Frustration 3Level', 'G9 Eng Instructional 3Level', 'G9 Eng Independent 3Level',
        'G10 Eng Assessed', 'G10 Eng Grade Ready', 'G10 Eng Frustration 2Level', 'G10 Eng Instructional 2Level', 'G10 Eng Independent 2Level', 'G10 Eng Frustration 3Level', 'G10 Eng Instructional 3Level', 'G10 Eng Independent 3Level'
    ]

    columns_to_sum = [col for col in ideal_columns_to_sum if col in df.columns]

    for col in columns_to_sum:
        clean_col = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(clean_col, errors='coerce').fillna(0)

    grouped = df.groupby(group_column)[columns_to_sum].sum()
    grouped['total_schools'] = df.groupby(group_column)['School ID'].nunique()
    grouped.loc['Grand Total'] = grouped.sum()

    grouped['% G7 Eng Grade Ready'] = calculate_percentage(grouped, 'G7 Eng Grade Ready', 'G7 Eng Assessed')
    grouped['% G7 Eng Frustration 2Level'] = calculate_percentage(grouped, 'G7 Eng Frustration 2Level', 'G7 Eng Assessed')
    grouped['% G7 Eng Instructional 2Level'] = calculate_percentage(grouped, 'G7 Eng Instructional 2Level', 'G7 Eng Assessed')
    grouped['% G7 Eng Independent 2Level'] = calculate_percentage(grouped, 'G7 Eng Independent 2Level', 'G7 Eng Assessed')
    grouped['% G7 Eng Frustration 3Level'] = calculate_percentage(grouped, 'G7 Eng Frustration 3Level', 'G7 Eng Assessed')
    grouped['% G7 Eng Instructional 3Level'] = calculate_percentage(grouped, 'G7 Eng Instructional 3Level', 'G7 Eng Assessed')
    grouped['% G7 Eng Independent 3Level'] = calculate_percentage(grouped, 'G7 Eng Independent 3Level', 'G7 Eng Assessed')

    grouped['% G8 Eng Grade Ready'] = calculate_percentage(grouped, 'G8 Eng Grade Ready', 'G8 Eng Assessed')
    grouped['% G8 Eng Frustration 2Level'] = calculate_percentage(grouped, 'G8 Eng Frustration 2Level', 'G8 Eng Assessed')
    grouped['% G8 Eng Instructional 2Level'] = calculate_percentage(grouped, 'G8 Eng Instructional 2Level', 'G8 Eng Assessed')
    grouped['% G8 Eng Independent 2Level'] = calculate_percentage(grouped, 'G8 Eng Independent 2Level', 'G8 Eng Assessed')
    grouped['% G8 Eng Frustration 3Level'] = calculate_percentage(grouped, 'G8 Eng Frustration 3Level', 'G8 Eng Assessed')
    grouped['% G8 Eng Instructional 3Level'] = calculate_percentage(grouped, 'G8 Eng Instructional 3Level', 'G8 Eng Assessed')
    grouped['% G8 Eng Independent 3Level'] = calculate_percentage(grouped, 'G8 Eng Independent 3Level', 'G8 Eng Assessed')

    grouped['% G9 Eng Grade Ready'] = calculate_percentage(grouped, 'G9 Eng Grade Ready', 'G9 Eng Assessed')
    grouped['% G9 Eng Frustration 2Level'] = calculate_percentage(grouped, 'G9 Eng Frustration 2Level', 'G9 Eng Assessed')
    grouped['% G9 Eng Instructional 2Level'] = calculate_percentage(grouped, 'G9 Eng Instructional 2Level', 'G9 Eng Assessed')
    grouped['% G9 Eng Independent 2Level'] = calculate_percentage(grouped, 'G9 Eng Independent 2Level', 'G9 Eng Assessed')
    grouped['% G9 Eng Frustration 3Level'] = calculate_percentage(grouped, 'G9 Eng Frustration 3Level', 'G9 Eng Assessed')
    grouped['% G9 Eng Instructional 3Level'] = calculate_percentage(grouped, 'G9 Eng Instructional 3Level', 'G9 Eng Assessed')
    grouped['% G9 Eng Independent 3Level'] = calculate_percentage(grouped, 'G9 Eng Independent 3Level', 'G9 Eng Assessed')

    grouped['% G10 Eng Grade Ready'] = calculate_percentage(grouped, 'G10 Eng Grade Ready', 'G10 Eng Assessed')
    grouped['% G10 Eng Frustration 2Level'] = calculate_percentage(grouped, 'G10 Eng Frustration 2Level', 'G10 Eng Assessed')
    grouped['% G10 Eng Instructional 2Level'] = calculate_percentage(grouped, 'G10 Eng Instructional 2Level', 'G10 Eng Assessed')
    grouped['% G10 Eng Independent 2Level'] = calculate_percentage(grouped, 'G10 Eng Independent 2Level', 'G10 Eng Assessed')
    grouped['% G10 Eng Frustration 3Level'] = calculate_percentage(grouped, 'G10 Eng Frustration 3Level', 'G10 Eng Assessed')
    grouped['% G10 Eng Instructional 3Level'] = calculate_percentage(grouped, 'G10 Eng Instructional 3Level', 'G10 Eng Assessed')
    grouped['% G10 Eng Independent 3Level'] = calculate_percentage(grouped, 'G10 Eng Independent 3Level', 'G10 Eng Assessed')

    ideal_final_layout = [
        'total_schools', 'Total Assessed (G7-G10)',
        'G7 Eng Assessed', 'G7 Eng Grade Ready', '% G7 Eng Grade Ready', 'G7 Eng Frustration 2Level', '% G7 Eng Frustration 2Level', 'G7 Eng Instructional 2Level', '% G7 Eng Instructional 2Level', 'G7 Eng Independent 2Level', '% G7 Eng Independent 2Level', 'G7 Eng Frustration 3Level', '% G7 Eng Frustration 3Level', 'G7 Eng Instructional 3Level', '% G7 Eng Instructional 3Level', 'G7 Eng Independent 3Level', '% G7 Eng Independent 3Level',
        'G8 Eng Assessed', 'G8 Eng Grade Ready', '% G8 Eng Grade Ready', 'G8 Eng Frustration 2Level', '% G8 Eng Frustration 2Level', 'G8 Eng Instructional 2Level', '% G8 Eng Instructional 2Level', 'G8 Eng Independent 2Level', '% G8 Eng Independent 2Level', 'G8 Eng Frustration 3Level', '% G8 Eng Frustration 3Level', 'G8 Eng Instructional 3Level', '% G8 Eng Instructional 3Level', 'G8 Eng Independent 3Level', '% G8 Eng Independent 3Level',
        'G9 Eng Assessed', 'G9 Eng Grade Ready', '% G9 Eng Grade Ready', 'G9 Eng Frustration 2Level', '% G9 Eng Frustration 2Level', 'G9 Eng Instructional 2Level', '% G9 Eng Instructional 2Level', 'G9 Eng Independent 2Level', '% G9 Eng Independent 2Level', 'G9 Eng Frustration 3Level', '% G9 Eng Frustration 3Level', 'G9 Eng Instructional 3Level', '% G9 Eng Instructional 3Level', 'G9 Eng Independent 3Level', '% G9 Eng Independent 3Level',
        'G10 Eng Assessed', 'G10 Eng Grade Ready', '% G10 Eng Grade Ready', 'G10 Eng Frustration 2Level', '% G10 Eng Frustration 2Level', 'G10 Eng Instructional 2Level', '% G10 Eng Instructional 2Level', 'G10 Eng Independent 2Level', '% G10 Eng Independent 2Level', 'G10 Eng Frustration 3Level', '% G10 Eng Frustration 3Level', 'G10 Eng Instructional 3Level', '% G10 Eng Instructional 3Level', 'G10 Eng Independent 3Level', '% G10 Eng Independent 3Level'
    ]
    final_layout = [col for col in ideal_final_layout if col in grouped.columns]
    return grouped[final_layout]

def process_philiri_ks3_eosy(df, group_column):
    df.columns = df.columns.str.strip()
    ideal_columns_to_sum = [
        'Total Assessed (G7-G10)', 'Total  Eng Frustration', 'Total Eng Instructional', 'Total Eng Independent',
        'G7 Eng Assessed', 'G7 Eng Frustration', 'G7 Eng Instructional', 'G7 Eng Independent',
        'G8 Eng Assessed', 'G8 Eng Frustration', 'G8 Eng Instructional', 'G8 Eng Independent',
        'G9 Eng Assessed', 'G9 Eng Frustration', 'G9 Eng Instructional', 'G9 Eng Independent',
        'G10 Eng Assessed', 'G10 Eng Frustration', 'G10 Eng Instructional', 'G10 Eng Independent'
    ]

    columns_to_sum = [col for col in ideal_columns_to_sum if col in df.columns]

    for col in columns_to_sum:
        clean_col = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(clean_col, errors='coerce').fillna(0)

    grouped = df.groupby(group_column)[columns_to_sum].sum()
    
    # Calculate Total Eng Assessed (since it wasn't in the raw columns but needed for % base)
    grouped['Total Eng Assessed'] = grouped.get('G7 Eng Assessed', 0) + grouped.get('G8 Eng Assessed', 0) + grouped.get('G9 Eng Assessed', 0) + grouped.get('G10 Eng Assessed', 0)
    
    grouped['total_schools'] = df.groupby(group_column)['School ID'].nunique()
    grouped.loc['Grand Total'] = grouped.sum()

    grouped['% Total  Eng Frustration'] = calculate_percentage(grouped, 'Total  Eng Frustration', 'Total Eng Assessed')
    grouped['% Total Eng Instructional'] = calculate_percentage(grouped, 'Total Eng Instructional', 'Total Eng Assessed')
    grouped['% Total Eng Independent'] = calculate_percentage(grouped, 'Total Eng Independent', 'Total Eng Assessed')

    grouped['% G7 Eng Frustration'] = calculate_percentage(grouped, 'G7 Eng Frustration', 'G7 Eng Assessed')
    grouped['% G7 Eng Instructional'] = calculate_percentage(grouped, 'G7 Eng Instructional', 'G7 Eng Assessed')
    grouped['% G7 Eng Independent'] = calculate_percentage(grouped, 'G7 Eng Independent', 'G7 Eng Assessed')

    grouped['% G8 Eng Frustration'] = calculate_percentage(grouped, 'G8 Eng Frustration', 'G8 Eng Assessed')
    grouped['% G8 Eng Instructional'] = calculate_percentage(grouped, 'G8 Eng Instructional', 'G8 Eng Assessed')
    grouped['% G8 Eng Independent'] = calculate_percentage(grouped, 'G8 Eng Independent', 'G8 Eng Assessed')

    grouped['% G9 Eng Frustration'] = calculate_percentage(grouped, 'G9 Eng Frustration', 'G9 Eng Assessed')
    grouped['% G9 Eng Instructional'] = calculate_percentage(grouped, 'G9 Eng Instructional', 'G9 Eng Assessed')
    grouped['% G9 Eng Independent'] = calculate_percentage(grouped, 'G9 Eng Independent', 'G9 Eng Assessed')

    grouped['% G10 Eng Frustration'] = calculate_percentage(grouped, 'G10 Eng Frustration', 'G10 Eng Assessed')
    grouped['% G10 Eng Instructional'] = calculate_percentage(grouped, 'G10 Eng Instructional', 'G10 Eng Assessed')
    grouped['% G10 Eng Independent'] = calculate_percentage(grouped, 'G10 Eng Independent', 'G10 Eng Assessed')

    ideal_final_layout = [
        'total_schools', 'Total Assessed (G7-G10)',
        'Total Eng Assessed', 'Total  Eng Frustration', '% Total  Eng Frustration', 'Total Eng Instructional', '% Total Eng Instructional', 'Total Eng Independent', '% Total Eng Independent',
        'G7 Eng Assessed', 'G7 Eng Frustration', '% G7 Eng Frustration', 'G7 Eng Instructional', '% G7 Eng Instructional', 'G7 Eng Independent', '% G7 Eng Independent',
        'G8 Eng Assessed', 'G8 Eng Frustration', '% G8 Eng Frustration', 'G8 Eng Instructional', '% G8 Eng Instructional', 'G8 Eng Independent', '% G8 Eng Independent',
        'G9 Eng Assessed', 'G9 Eng Frustration', '% G9 Eng Frustration', 'G9 Eng Instructional', '% G9 Eng Instructional', 'G9 Eng Independent', '% G9 Eng Independent',
        'G10 Eng Assessed', 'G10 Eng Frustration', '% G10 Eng Frustration', 'G10 Eng Instructional', '% G10 Eng Instructional', 'G10 Eng Independent', '% G10 Eng Independent'
    ]
    final_layout = [col for col in ideal_final_layout if col in grouped.columns]
    return grouped[final_layout]

# --- RMA PROCESSORS ---
def process_rma_ks1(df, group_column):
    df.columns = df.columns.str.strip()
    ideal_columns_to_sum = [
        'Total Assessed', 'Total Emerging - Not Proficient', 'Total Emerging - Low Proficient', 'Total Developing - Nearly Proficient', 'Total Transitioning - Proficient', 'Total At Grade Level - Highly Proficient',
        'G1 Assessed', 'G1 Emerging Not Proficient', 'G1 Emerging - Low Proficient', 'G1 Developing - Nearly Proficient', 'G1 Transitioning - Proficient', 'G1 At Grade Level - Highly Proficient',
        'G2 Assessed', 'G2 Emerging Not Proficient', 'G2 Emerging - Low Proficient', 'G2 Developing - Nearly Proficient', 'G2 Transitioning - Proficient', 'G2 At Grade Level - Highly Proficient',
        'G3 Assessed', 'G3 Emerging Not Proficient', 'G3 Emerging - Low Proficient', 'G3 Developing - Nearly Proficient', 'G3 Transitioning - Proficient', 'G3 At Grade Level - Highly Proficient'
    ]
    columns_to_sum = [col for col in ideal_columns_to_sum if col in df.columns]

    for col in columns_to_sum:
        clean_col = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(clean_col, errors='coerce').fillna(0)

    grouped = df.groupby(group_column)[columns_to_sum].sum()
    grouped['total_schools'] = df.groupby(group_column)['School ID'].nunique()
    grouped.loc['Grand Total'] = grouped.sum()

    grouped['% Total Emerging - Not Proficient'] = calculate_percentage(grouped, 'Total Emerging - Not Proficient', 'Total Assessed')
    grouped['% Total Emerging - Low Proficient'] = calculate_percentage(grouped, 'Total Emerging - Low Proficient', 'Total Assessed')
    grouped['% Total Developing - Nearly Proficient'] = calculate_percentage(grouped, 'Total Developing - Nearly Proficient', 'Total Assessed')
    grouped['% Total Transitioning - Proficient'] = calculate_percentage(grouped, 'Total Transitioning - Proficient', 'Total Assessed')
    grouped['% Total At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'Total At Grade Level - Highly Proficient', 'Total Assessed')

    grouped['% G1 Emerging Not Proficient'] = calculate_percentage(grouped, 'G1 Emerging Not Proficient', 'G1 Assessed')
    grouped['% G1 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G1 Emerging - Low Proficient', 'G1 Assessed')
    grouped['% G1 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G1 Developing - Nearly Proficient', 'G1 Assessed')
    grouped['% G1 Transitioning - Proficient'] = calculate_percentage(grouped, 'G1 Transitioning - Proficient', 'G1 Assessed')
    grouped['% G1 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G1 At Grade Level - Highly Proficient', 'G1 Assessed')

    grouped['% G2 Emerging Not Proficient'] = calculate_percentage(grouped, 'G2 Emerging Not Proficient', 'G2 Assessed')
    grouped['% G2 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G2 Emerging - Low Proficient', 'G2 Assessed')
    grouped['% G2 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G2 Developing - Nearly Proficient', 'G2 Assessed')
    grouped['% G2 Transitioning - Proficient'] = calculate_percentage(grouped, 'G2 Transitioning - Proficient', 'G2 Assessed')
    grouped['% G2 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G2 At Grade Level - Highly Proficient', 'G2 Assessed')

    grouped['% G3 Emerging Not Proficient'] = calculate_percentage(grouped, 'G3 Emerging Not Proficient', 'G3 Assessed')
    grouped['% G3 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G3 Emerging - Low Proficient', 'G3 Assessed')
    grouped['% G3 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G3 Developing - Nearly Proficient', 'G3 Assessed')
    grouped['% G3 Transitioning - Proficient'] = calculate_percentage(grouped, 'G3 Transitioning - Proficient', 'G3 Assessed')
    grouped['% G3 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G3 At Grade Level - Highly Proficient', 'G3 Assessed')

    ideal_final_layout = [
        'total_schools', 'Total Assessed', 
        'Total Emerging - Not Proficient', '% Total Emerging - Not Proficient', 'Total Emerging - Low Proficient', '% Total Emerging - Low Proficient', 'Total Developing - Nearly Proficient', '% Total Developing - Nearly Proficient', 'Total Transitioning - Proficient', '% Total Transitioning - Proficient', 'Total At Grade Level - Highly Proficient', '% Total At Grade Level - Highly Proficient',
        'G1 Assessed', 'G1 Emerging Not Proficient', '% G1 Emerging Not Proficient', 'G1 Emerging - Low Proficient', '% G1 Emerging - Low Proficient', 'G1 Developing - Nearly Proficient', '% G1 Developing - Nearly Proficient', 'G1 Transitioning - Proficient', '% G1 Transitioning - Proficient', 'G1 At Grade Level - Highly Proficient', '% G1 At Grade Level - Highly Proficient',
        'G2 Assessed', 'G2 Emerging Not Proficient', '% G2 Emerging Not Proficient', 'G2 Emerging - Low Proficient', '% G2 Emerging - Low Proficient', 'G2 Developing - Nearly Proficient', '% G2 Developing - Nearly Proficient', 'G2 Transitioning - Proficient', '% G2 Transitioning - Proficient', 'G2 At Grade Level - Highly Proficient', '% G2 At Grade Level - Highly Proficient',
        'G3 Assessed', 'G3 Emerging Not Proficient', '% G3 Emerging Not Proficient', 'G3 Emerging - Low Proficient', '% G3 Emerging - Low Proficient', 'G3 Developing - Nearly Proficient', '% G3 Developing - Nearly Proficient', 'G3 Transitioning - Proficient', '% G3 Transitioning - Proficient', 'G3 At Grade Level - Highly Proficient', '% G3 At Grade Level - Highly Proficient'
    ]
    final_layout = [col for col in ideal_final_layout if col in grouped.columns]
    return grouped[final_layout]


def process_rma_ks2(df, group_column):
    df.columns = df.columns.str.strip()
    ideal_columns_to_sum = [
        'Total Assessed', 'Total Emerging - Not Proficient', 'Total Emerging - Low Proficient', 'Total Developing - Nearly Proficient', 'Total Transitioning - Proficient', 'Total At Grade Level - Highly Proficient',
        'G4 Assessed', 'G4 Emerging Not Proficient', 'G4 Emerging - Low Proficient', 'G4 Developing - Nearly Proficient', 'G4 Transitioning - Proficient', 'G4 At Grade Level - Highly Proficient',
        'G5 Assessed', 'G5 Emerging Not Proficient', 'G5 Emerging - Low Proficient', 'G5 Developing - Nearly Proficient', 'G5 Transitioning - Proficient', 'G5 At Grade Level - Highly Proficient',
        'G6 Assessed', 'G6 Emerging Not Proficient', 'G6 Emerging - Low Proficient', 'G6 Developing - Nearly Proficient', 'G6 Transitioning - Proficient', 'G6 At Grade Level - Highly Proficient'
    ]
    columns_to_sum = [col for col in ideal_columns_to_sum if col in df.columns]

    for col in columns_to_sum:
        clean_col = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(clean_col, errors='coerce').fillna(0)

    grouped = df.groupby(group_column)[columns_to_sum].sum()
    grouped['total_schools'] = df.groupby(group_column)['School ID'].nunique()
    grouped.loc['Grand Total'] = grouped.sum()

    grouped['% Total Emerging - Not Proficient'] = calculate_percentage(grouped, 'Total Emerging - Not Proficient', 'Total Assessed')
    grouped['% Total Emerging - Low Proficient'] = calculate_percentage(grouped, 'Total Emerging - Low Proficient', 'Total Assessed')
    grouped['% Total Developing - Nearly Proficient'] = calculate_percentage(grouped, 'Total Developing - Nearly Proficient', 'Total Assessed')
    grouped['% Total Transitioning - Proficient'] = calculate_percentage(grouped, 'Total Transitioning - Proficient', 'Total Assessed')
    grouped['% Total At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'Total At Grade Level - Highly Proficient', 'Total Assessed')

    grouped['% G4 Emerging Not Proficient'] = calculate_percentage(grouped, 'G4 Emerging Not Proficient', 'G4 Assessed')
    grouped['% G4 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G4 Emerging - Low Proficient', 'G4 Assessed')
    grouped['% G4 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G4 Developing - Nearly Proficient', 'G4 Assessed')
    grouped['% G4 Transitioning - Proficient'] = calculate_percentage(grouped, 'G4 Transitioning - Proficient', 'G4 Assessed')
    grouped['% G4 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G4 At Grade Level - Highly Proficient', 'G4 Assessed')

    grouped['% G5 Emerging Not Proficient'] = calculate_percentage(grouped, 'G5 Emerging Not Proficient', 'G5 Assessed')
    grouped['% G5 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G5 Emerging - Low Proficient', 'G5 Assessed')
    grouped['% G5 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G5 Developing - Nearly Proficient', 'G5 Assessed')
    grouped['% G5 Transitioning - Proficient'] = calculate_percentage(grouped, 'G5 Transitioning - Proficient', 'G5 Assessed')
    grouped['% G5 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G5 At Grade Level - Highly Proficient', 'G5 Assessed')

    grouped['% G6 Emerging Not Proficient'] = calculate_percentage(grouped, 'G6 Emerging Not Proficient', 'G6 Assessed')
    grouped['% G6 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G6 Emerging - Low Proficient', 'G6 Assessed')
    grouped['% G6 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G6 Developing - Nearly Proficient', 'G6 Assessed')
    grouped['% G6 Transitioning - Proficient'] = calculate_percentage(grouped, 'G6 Transitioning - Proficient', 'G6 Assessed')
    grouped['% G6 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G6 At Grade Level - Highly Proficient', 'G6 Assessed')

    ideal_final_layout = [
        'total_schools', 'Total Assessed', 
        'Total Emerging - Not Proficient', '% Total Emerging - Not Proficient', 'Total Emerging - Low Proficient', '% Total Emerging - Low Proficient', 'Total Developing - Nearly Proficient', '% Total Developing - Nearly Proficient', 'Total Transitioning - Proficient', '% Total Transitioning - Proficient', 'Total At Grade Level - Highly Proficient', '% Total At Grade Level - Highly Proficient',
        'G4 Assessed', 'G4 Emerging Not Proficient', '% G4 Emerging Not Proficient', 'G4 Emerging - Low Proficient', '% G4 Emerging - Low Proficient', 'G4 Developing - Nearly Proficient', '% G4 Developing - Nearly Proficient', 'G4 Transitioning - Proficient', '% G4 Transitioning - Proficient', 'G4 At Grade Level - Highly Proficient', '% G4 At Grade Level - Highly Proficient',
        'G5 Assessed', 'G5 Emerging Not Proficient', '% G5 Emerging Not Proficient', 'G5 Emerging - Low Proficient', '% G5 Emerging - Low Proficient', 'G5 Developing - Nearly Proficient', '% G5 Developing - Nearly Proficient', 'G5 Transitioning - Proficient', '% G5 Transitioning - Proficient', 'G5 At Grade Level - Highly Proficient', '% G5 At Grade Level - Highly Proficient',
        'G6 Assessed', 'G6 Emerging Not Proficient', '% G6 Emerging Not Proficient', 'G6 Emerging - Low Proficient', '% G6 Emerging - Low Proficient', 'G6 Developing - Nearly Proficient', '% G6 Developing - Nearly Proficient', 'G6 Transitioning - Proficient', '% G6 Transitioning - Proficient', 'G6 At Grade Level - Highly Proficient', '% G6 At Grade Level - Highly Proficient'
    ]
    final_layout = [col for col in ideal_final_layout if col in grouped.columns]
    return grouped[final_layout]


def process_rma_ks3(df, group_column):
    df.columns = df.columns.str.strip()
    ideal_columns_to_sum = [
        'Total Assessed', 'Total Emerging - Not Proficient', 'Total Emerging - Low Proficient', 'Total Developing - Nearly Proficient', 'Total Transitioning - Proficient', 'Total At Grade Level - Highly Proficient',
        'G7 Assessed', 'G7 Emerging Not Proficient', 'G7 Emerging - Low Proficient', 'G7 Developing - Nearly Proficient', 'G7 Transitioning - Proficient', 'G7 At Grade Level - Highly Proficient',
        'G8 Assessed', 'G8 Emerging Not Proficient', 'G8 Emerging - Low Proficient', 'G8 Developing - Nearly Proficient', 'G8 Transitioning - Proficient', 'G8 At Grade Level - Highly Proficient',
        'G9 Assessed', 'G9 Emerging Not Proficient', 'G9 Emerging - Low Proficient', 'G9 Developing - Nearly Proficient', 'G9 Transitioning - Proficient', 'G9 At Grade Level - Highly Proficient',
        'G10 Assessed', 'G10 Emerging Not Proficient', 'G10 Emerging - Low Proficient', 'G10 Developing - Nearly Proficient', 'G10 Transitioning - Proficient', 'G10 At Grade Level - Highly Proficient'
    ]
    columns_to_sum = [col for col in ideal_columns_to_sum if col in df.columns]

    for col in columns_to_sum:
        clean_col = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(clean_col, errors='coerce').fillna(0)

    grouped = df.groupby(group_column)[columns_to_sum].sum()
    grouped['total_schools'] = df.groupby(group_column)['School ID'].nunique()
    grouped.loc['Grand Total'] = grouped.sum()

    grouped['% Total Emerging - Not Proficient'] = calculate_percentage(grouped, 'Total Emerging - Not Proficient', 'Total Assessed')
    grouped['% Total Emerging - Low Proficient'] = calculate_percentage(grouped, 'Total Emerging - Low Proficient', 'Total Assessed')
    grouped['% Total Developing - Nearly Proficient'] = calculate_percentage(grouped, 'Total Developing - Nearly Proficient', 'Total Assessed')
    grouped['% Total Transitioning - Proficient'] = calculate_percentage(grouped, 'Total Transitioning - Proficient', 'Total Assessed')
    grouped['% Total At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'Total At Grade Level - Highly Proficient', 'Total Assessed')

    grouped['% G7 Emerging Not Proficient'] = calculate_percentage(grouped, 'G7 Emerging Not Proficient', 'G7 Assessed')
    grouped['% G7 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G7 Emerging - Low Proficient', 'G7 Assessed')
    grouped['% G7 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G7 Developing - Nearly Proficient', 'G7 Assessed')
    grouped['% G7 Transitioning - Proficient'] = calculate_percentage(grouped, 'G7 Transitioning - Proficient', 'G7 Assessed')
    grouped['% G7 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G7 At Grade Level - Highly Proficient', 'G7 Assessed')

    grouped['% G8 Emerging Not Proficient'] = calculate_percentage(grouped, 'G8 Emerging Not Proficient', 'G8 Assessed')
    grouped['% G8 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G8 Emerging - Low Proficient', 'G8 Assessed')
    grouped['% G8 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G8 Developing - Nearly Proficient', 'G8 Assessed')
    grouped['% G8 Transitioning - Proficient'] = calculate_percentage(grouped, 'G8 Transitioning - Proficient', 'G8 Assessed')
    grouped['% G8 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G8 At Grade Level - Highly Proficient', 'G8 Assessed')

    grouped['% G9 Emerging Not Proficient'] = calculate_percentage(grouped, 'G9 Emerging Not Proficient', 'G9 Assessed')
    grouped['% G9 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G9 Emerging - Low Proficient', 'G9 Assessed')
    grouped['% G9 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G9 Developing - Nearly Proficient', 'G9 Assessed')
    grouped['% G9 Transitioning - Proficient'] = calculate_percentage(grouped, 'G9 Transitioning - Proficient', 'G9 Assessed')
    grouped['% G9 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G9 At Grade Level - Highly Proficient', 'G9 Assessed')

    grouped['% G10 Emerging Not Proficient'] = calculate_percentage(grouped, 'G10 Emerging Not Proficient', 'G10 Assessed')
    grouped['% G10 Emerging - Low Proficient'] = calculate_percentage(grouped, 'G10 Emerging - Low Proficient', 'G10 Assessed')
    grouped['% G10 Developing - Nearly Proficient'] = calculate_percentage(grouped, 'G10 Developing - Nearly Proficient', 'G10 Assessed')
    grouped['% G10 Transitioning - Proficient'] = calculate_percentage(grouped, 'G10 Transitioning - Proficient', 'G10 Assessed')
    grouped['% G10 At Grade Level - Highly Proficient'] = calculate_percentage(grouped, 'G10 At Grade Level - Highly Proficient', 'G10 Assessed')

    ideal_final_layout = [
        'total_schools', 'Total Assessed', 
        'Total Emerging - Not Proficient', '% Total Emerging - Not Proficient', 'Total Emerging - Low Proficient', '% Total Emerging - Low Proficient', 'Total Developing - Nearly Proficient', '% Total Developing - Nearly Proficient', 'Total Transitioning - Proficient', '% Total Transitioning - Proficient', 'Total At Grade Level - Highly Proficient', '% Total At Grade Level - Highly Proficient',
        'G7 Assessed', 'G7 Emerging Not Proficient', '% G7 Emerging Not Proficient', 'G7 Emerging - Low Proficient', '% G7 Emerging - Low Proficient', 'G7 Developing - Nearly Proficient', '% G7 Developing - Nearly Proficient', 'G7 Transitioning - Proficient', '% G7 Transitioning - Proficient', 'G7 At Grade Level - Highly Proficient', '% G7 At Grade Level - Highly Proficient',
        'G8 Assessed', 'G8 Emerging Not Proficient', '% G8 Emerging Not Proficient', 'G8 Emerging - Low Proficient', '% G8 Emerging - Low Proficient', 'G8 Developing - Nearly Proficient', '% G8 Developing - Nearly Proficient', 'G8 Transitioning - Proficient', '% G8 Transitioning - Proficient', 'G8 At Grade Level - Highly Proficient', '% G8 At Grade Level - Highly Proficient',
        'G9 Assessed', 'G9 Emerging Not Proficient', '% G9 Emerging Not Proficient', 'G9 Emerging - Low Proficient', '% G9 Emerging - Low Proficient', 'G9 Developing - Nearly Proficient', '% G9 Developing - Nearly Proficient', 'G9 Transitioning - Proficient', '% G9 Transitioning - Proficient', 'G9 At Grade Level - Highly Proficient', '% G9 At Grade Level - Highly Proficient',
        'G10 Assessed', 'G10 Emerging Not Proficient', '% G10 Emerging Not Proficient', 'G10 Emerging - Low Proficient', '% G10 Emerging - Low Proficient', 'G10 Developing - Nearly Proficient', '% G10 Developing - Nearly Proficient', 'G10 Transitioning - Proficient', '% G10 Transitioning - Proficient', 'G10 At Grade Level - Highly Proficient', '% G10 At Grade Level - Highly Proficient'
    ]
    final_layout = [col for col in ideal_final_layout if col in grouped.columns]
    return grouped[final_layout]


# ==========================================
# 3. INTERACTIVE WEB WORKFLOW
# ==========================================

st.title("DepEd Automated Report Generator ARAL SY25-26")

# Set up a "Session State" memory key to allow us to reset the file uploader
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = str(0)

# Interactive selections replacing the command-line inputs
assessment_choice = st.selectbox(
    "Which assessment are you processing?",
    (
        "CRLA (Grades 1-3)", 
        "Phil-IRI KS2 (Grades 4-6)", 
        "Phil-IRI KS3 (Grades 7-10)",
        "RMA KS1 (Grades 1-3)",
        "RMA KS2 (Grades 4-6)",
        "RMA KS3 (Grades 7-10)"
    )
)

term_choice = st.radio("Which term are you processing?", ("BoSY", "EoSY"))

# Determine the prefix based on choices
if assessment_choice == "CRLA (Grades 1-3)":
    assessment_name = "CRLA"
elif assessment_choice == "Phil-IRI KS2 (Grades 4-6)":
    assessment_name = "PhilIRI_KS2"
elif assessment_choice == "Phil-IRI KS3 (Grades 7-10)":
    assessment_name = "PhilIRI_KS3"
elif assessment_choice == "RMA KS1 (Grades 1-3)":
    assessment_name = "RMA_KS1"
elif assessment_choice == "RMA KS2 (Grades 4-6)":
    assessment_name = "RMA_KS2"
elif assessment_choice == "RMA KS3 (Grades 7-10)":
    assessment_name = "RMA_KS3"

report_prefix = f"{assessment_name}_{term_choice}"

# -----------------------------
st.info(f"💡 **Reminder:** Please make sure the CSV you upload exactly matches your selection above (**{assessment_choice} - {term_choice}**) to prevent processing errors.")
# -----------------------------

# Web File Uploader dynamically updates its label
uploaded_file = st.file_uploader(f"Upload your {report_prefix} CSV", type=["csv"], key=st.session_state.uploader_key)

if uploaded_file is not None:
    try:
        with st.spinner("Cleaning dirty data, formatting numbers, and processing... Please wait."):
            
            # Read the data - Added low_memory=False to prevent mixed-type warnings
            raw_data = pd.read_csv(uploaded_file, low_memory=False)
            
            # ==========================================
            # AUTOMATED DATA CLEANING
            # ==========================================
            # Keep these specific columns as text
            text_columns = ['Region', 'Division', 'District', 'Municipality', 'School ID', 'School Name']
            
            # Force all other columns to be numeric globally.
            for col in raw_data.columns:
                if col not in text_columns:
                    raw_data[col] = pd.to_numeric(raw_data[col], errors='coerce').fillna(0)
            # ==========================================
            
            # Route the data to the correct processor based on user choices
            if assessment_name == 'CRLA':
                summary_table_region = process_crla(raw_data, 'Region')
                summary_table_division = process_crla(raw_data, 'Division')
                
            elif assessment_name == 'PhilIRI_KS2':
                if term_choice == 'BoSY':
                    summary_table_region = process_philiri_ks2_bosy(raw_data, 'Region')
                    summary_table_division = process_philiri_ks2_bosy(raw_data, 'Division')
                elif term_choice == 'EoSY':
                    summary_table_region = process_philiri_ks2_eosy(raw_data, 'Region')
                    summary_table_division = process_philiri_ks2_eosy(raw_data, 'Division')
                    
            elif assessment_name == 'PhilIRI_KS3':
                if term_choice == 'BoSY':
                    summary_table_region = process_philiri_ks3_bosy(raw_data, 'Region')
                    summary_table_division = process_philiri_ks3_bosy(raw_data, 'Division')
                elif term_choice == 'EoSY':
                    summary_table_region = process_philiri_ks3_eosy(raw_data, 'Region')
                    summary_table_division = process_philiri_ks3_eosy(raw_data, 'Division')
                    
            elif assessment_name == 'RMA_KS1':
                summary_table_region = process_rma_ks1(raw_data, 'Region')
                summary_table_division = process_rma_ks1(raw_data, 'Division')
                
            elif assessment_name == 'RMA_KS2':
                summary_table_region = process_rma_ks2(raw_data, 'Region')
                summary_table_division = process_rma_ks2(raw_data, 'Division')
                
            elif assessment_name == 'RMA_KS3':
                summary_table_region = process_rma_ks3(raw_data, 'Region')
                summary_table_division = process_rma_ks3(raw_data, 'Division')
        
        st.success("Success! Your reports have been created.")

        # The Centered Reset Button
        spacer_left, center_col, spacer_right = st.columns([1, 2, 1])
        with center_col:
            if st.button("🔄 Reset / Start Over", use_container_width=True):
                st.session_state.uploader_key = str(int(st.session_state.uploader_key) + 1)
                st.rerun()

        # Convert dataframes to CSVs in memory
        region_csv = summary_table_region.to_csv().encode('utf-8')
        division_csv = summary_table_division.to_csv().encode('utf-8')

        # Centered download buttons
        spacer1, col1, col2, spacer2 = st.columns([1, 2, 2, 1])
        with col1:
            st.download_button(
                label="Download Region-Pivot CSV",
                data=region_csv,
                file_name=f'{report_prefix}_Regional_Pivot.csv',
                mime='text/csv',
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="Download Division-Pivot CSV",
                data=division_csv,
                file_name=f'{report_prefix}_Division_Pivot.csv',
                mime='text/csv',
                use_container_width=True
            )

        # Full, scrollable dataframes
        st.subheader("Preview: Regional Pivot")
        st.dataframe(summary_table_region)
        st.subheader("Preview: Divisional Pivot")
        st.dataframe(summary_table_division)
            
    except Exception as e:
        st.error(f"Data Processing Error: {e}")
        st.write("Please check your CSV file to ensure it matches the chosen assessment format.")
        
        # Centered Try Again Button
        err_spacer_left, err_center_col, err_spacer_right = st.columns([1, 2, 1])
        with err_center_col:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.uploader_key = str(int(st.session_state.uploader_key) + 1)
                st.rerun()
