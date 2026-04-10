"""
DGE Regional Sammenligning
Streamlit app til sammenligning af DGE-data på tværs af 5 regioner
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PIL import Image

# ============================================================================
# KONFIGURATION
# ============================================================================

st.set_page_config(page_title="📊 DGE Regional Sammenligning", layout="wide")

REGIONS = {
    'Nord': {'population': 600000, 'color': '#1f77b4'},
    'Midt': {'population': 1350000, 'color': '#ff7f0e'},
    'Syd': {'population': 1250000, 'color': '#2ca02c'},
    'Hovedstaden': {'population': 1900000, 'color': '#d62728'},
    'Sjælland': {'population': 850000, 'color': '#9467bd'},
    'Øst': {'population': 2750000, 'color': '#8c564b'}  # Kombineret Hovedstaden+Sjælland
}

REGION_ORDER_5 = ['Nord', 'Midt', 'Syd', 'Hovedstaden', 'Sjælland']
REGION_ORDER_4 = ['Nord', 'Midt', 'Syd', 'Øst']

BASE_REGION = 'Midt'

# Farver til gruppetyper (Tabel 1)
GROUP_TYPE_COLORS = {
    'DGE': '#2B6CB0',  # Blå
    'SUP': '#DC2626',  # Rød
    'JUN': '#10B981'   # Grøn
}

# Farver til kategori-visualisering
CATEGORY_COLORS = {
    'red': '#DC2626',
    'orange': '#F59E0B',
    'yellow': '#FCD34D',
    'green': '#10B981',
    'gray': '#9CA3AF'
}

# ============================================================================
# HJÆLPEFUNKTIONER
# ============================================================================

def parse_danish_date(date_str):
    """Parser danske datoformater"""
    if pd.isna(date_str) or str(date_str).strip() in ['-', '', 'nan']:
        return pd.NaT
    
    if isinstance(date_str, datetime):
        return date_str
    
    date_str = str(date_str).strip().replace('kl.', '').replace(',', '')
    
    months = {
        'januar': '01', 'februar': '02', 'marts': '03', 'april': '04',
        'maj': '05', 'juni': '06', 'juli': '07', 'august': '08',
        'september': '09', 'oktober': '10', 'november': '11', 'december': '12'
    }
    
    for dk_month, num_month in months.items():
        if dk_month in date_str.lower():
            date_str = date_str.lower().replace(dk_month, num_month)
    
    date_str = date_str.replace('.', ' ')
    
    try:
        return pd.to_datetime(date_str, dayfirst=True, errors='coerce')
    except:
        return pd.NaT

def map_region_name(full_name):
    """Map fuld regionsnavn til kort navn"""
    name = str(full_name).lower()
    if 'nordjylland' in name:
        return 'Nord'
    elif 'midtjylland' in name:
        return 'Midt'
    elif 'syddanmark' in name:
        return 'Syd'
    elif 'hovedstaden' in name:
        return 'Hovedstaden'
    elif 'sjælland' in name:
        return 'Sjælland'
    elif 'øst' in name:
        return 'Øst'
    return None

def standardize_group_type(group_type_str):
    """Standardiser gruppetype"""
    if pd.isna(group_type_str):
        return 'Andet'
    
    s = str(group_type_str).strip().upper()
    
    if 'DGE' in s:
        return 'DGE'
    elif 'SUPERVISION' in s or 'SUP' in s:
        return 'SUP'
    elif 'JUNIOR' in s or 'JUN' in s:
        return 'JUN'
    
    return 'Andet'

def calculate_index(value, region, base_region='Midt'):
    """Beregn indbygger-justeret index med base_region = 100"""
    if value == 0:
        return 0
    
    region_pop = REGIONS[region]['population']
    base_pop = REGIONS[base_region]['population']
    
    # Per capita
    region_per_capita = value / region_pop
    base_per_capita = 1 / base_pop
    
    index = (region_per_capita / base_per_capita) * 100
    
    return round(index, 1)

# ============================================================================
# DATA PARSING
# ============================================================================

def load_regional_data(uploaded_files):
    """Load og kombiner data fra alle regioner"""
    groups_list = []
    meetings_list = []
    
    for file in uploaded_files:
        try:
            df = pd.read_excel(file)
            
            # Identificer type baseret på kolonner
            cols = [c.lower() for c in df.columns]
            
            if 'gruppe id' in cols and 'gruppenavn' in cols:
                groups_list.append(df)
            elif 'gruppenavn' in cols and 'starttidspunkt' in cols:
                meetings_list.append(df)
                
        except Exception as e:
            st.warning(f"Kunne ikke læse {file.name}: {e}")
    
    groups_df = pd.concat(groups_list, ignore_index=True) if groups_list else pd.DataFrame()
    meetings_df = pd.concat(meetings_list, ignore_index=True) if meetings_list else pd.DataFrame()
    
    return groups_df, meetings_df

# ============================================================================
# MAIN
# ============================================================================

def main():
    st.title("📊 DGE Regional Sammenligning")
    st.caption("Sammenligning af mødeaktivitet på tværs af 5 danske regioner")
    
    # FILE UPLOAD
    st.header("Upload datafiler")
    
    # Mode selection
    region_mode = st.radio(
        "Antal regioner:",
        options=["5 regioner (Nord, Midt, Syd, Hovedstaden, Sjælland)", 
                 "4 regioner (Nord, Midt, Syd, Øst)"],
        index=0
    )
    
    is_5_regions = "5 regioner" in region_mode
    expected_files = 10 if is_5_regions else 8
    
    if is_5_regions:
        st.info("📁 Upload 10 Excel-filer: 2 filer per region (groups + meetings)")
        REGION_ORDER = REGION_ORDER_5
    else:
        st.info("📁 Upload 8 Excel-filer: 2 filer per region (groups + meetings)")
        REGION_ORDER = REGION_ORDER_4
    
    uploaded_files = st.file_uploader(
        "Vælg filer",
        type=['xlsx', 'xls'],
        accept_multiple_files=True
    )
    
    if len(uploaded_files) < expected_files:
        st.warning(f"⚠️ Upload venligst {expected_files} filer. Du har uploadet {len(uploaded_files)}.")
        return
    
    # LOAD DATA
    with st.spinner("Indlæser data..."):
        groups_df, meetings_df = load_regional_data(uploaded_files)
    
    if groups_df.empty or meetings_df.empty:
        st.error("Kunne ikke indlæse data korrekt")
        return
    
    # Parse datoer
    if 'Starttidspunkt' in meetings_df.columns:
        meetings_df['Starttidspunkt'] = meetings_df['Starttidspunkt'].apply(parse_danish_date)
    
    # Map regionsnavne
    if 'Region' in groups_df.columns:
        groups_df['Region_short'] = groups_df['Region'].apply(map_region_name)
    
    if 'Region' in meetings_df.columns:
        meetings_df['Region_short'] = meetings_df['Region'].apply(map_region_name)
    
    # Standardiser gruppetyper
    if 'Gruppetyper' in groups_df.columns:
        groups_df['Gruppetype_std'] = groups_df['Gruppetyper'].apply(standardize_group_type)
    
    st.success(f"✅ Data indlæst: {len(groups_df)} grupper, {len(meetings_df)} møder fra {groups_df['Region_short'].nunique()} regioner")
    
    # PERIODE VALG
    st.header("Vælg analyseperiode")
    
    current_year = datetime.now().year
    selected_year = st.selectbox(
        "Vælg år",
        list(range(2020, current_year + 1)),
        index=list(range(2020, current_year + 1)).index(current_year - 1)
    )
    
    start_date = datetime(selected_year, 1, 1)
    end_date = datetime(selected_year, 12, 31, 23, 59, 59)
    
    st.info(f"Analyserer: {start_date.strftime('%d-%m-%Y')} til {end_date.strftime('%d-%m-%Y')}")
    
    # FILTRER DATA
    meetings_period = meetings_df[
        (meetings_df['Starttidspunkt'] >= start_date) & 
        (meetings_df['Starttidspunkt'] <= end_date)
    ].copy()
    
    meetings_approved = meetings_period[
        meetings_period['Status'].astype(str).str.strip().str.lower() == 'godkendt'
    ].copy()
    
    # Tilføj gruppetype til møder (bruges i alle tabeller)
    if 'Gruppe ID' in meetings_approved.columns and 'Gruppe ID' in groups_df.columns:
        meetings_with_type = meetings_approved.merge(
            groups_df[['Gruppe ID', 'Gruppetype_std']],
            on='Gruppe ID',
            how='left'
        )
    elif 'Gruppenavn' in meetings_approved.columns and 'Gruppenavn' in groups_df.columns:
        # Fallback: brug Gruppenavn hvis Gruppe ID ikke findes
        meetings_with_type = meetings_approved.merge(
            groups_df[['Gruppenavn', 'Region_short', 'Gruppetype_std']].drop_duplicates(),
            on=['Gruppenavn', 'Region_short'],
            how='left'
        )
    else:
        meetings_with_type = meetings_approved.copy()
        meetings_with_type['Gruppetype_std'] = 'Ukendt'
    
    st.markdown("---")
    
    # ===========================================
    # TABEL 1: ANTAL GODKENDTE MØDER (INDEXERET)
    # ===========================================
    
    st.header("📊 Tabel 1: Antal godkendte møder (indbygger-justeret)")
    st.caption(f"Indexeret med {BASE_REGION} = 100")
    
    # Tæl møder per region og gruppetype
    meeting_counts = meetings_with_type.groupby(['Region_short', 'Gruppetype_std']).size().reset_index(name='Antal')
    
    # Beregn index
    meeting_counts['Index'] = meeting_counts.apply(
        lambda row: calculate_index(row['Antal'], row['Region_short']),
        axis=1
    )
    
    # Lav stacked bar chart
    fig = go.Figure()
    
    # Reverser rækkefølge: DGE, SUP, JUN
    for gtype in ['DGE', 'SUP', 'JUN']:
        y_values = []
        for region in REGION_ORDER:
            data = meeting_counts[
                (meeting_counts['Region_short'] == region) &
                (meeting_counts['Gruppetype_std'] == gtype)
            ]
            val = data['Index'].values[0] if len(data) > 0 else 0
            y_values.append(val)
        
        fig.add_trace(go.Bar(
            name=gtype,
            x=REGION_ORDER,
            y=y_values,
            marker_color=GROUP_TYPE_COLORS[gtype]
        ))
    
    fig.update_layout(
        barmode='stack',
        height=500,
        xaxis_title='Region',
        yaxis_title=f'Index ({BASE_REGION} = 100)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Farveforklaring:**  
    🔵 DGE | 🔴 SUP | 🟢 JUN
    """)
    
    # Vis også rå tal
    with st.expander("📋 Se detaljerede tal"):
        pivot = meeting_counts.pivot_table(
            index='Region_short',
            columns='Gruppetype_std',
            values=['Antal', 'Index'],
            fill_value=0
        )
        st.dataframe(pivot, use_container_width=True)
    
    st.markdown("---")
    
    # ==========================================
    # TABEL 2A: GRUPPESTØRRELSE - SUP (%)
    # ==========================================
    
    st.header("📊 Tabel 2A: Gruppestørrelse SUP-grupper (procentfordeling)")
    st.caption("Fordeling af SUP-gruppers medlemstal")
    
    # Filtrer kun SUP grupper
    sup_groups = groups_df[groups_df['Gruppetype_std'] == 'SUP'].copy()
    
    # Kategoriser gruppestørrelse
    def categorize_group_size(n):
        if pd.isna(n) or n == 0:
            return None
        n = int(n)
        if n <= 4:
            return '0-4'
        elif n <= 7:
            return '5-7'
        elif n <= 10:
            return '8-10'
        elif n <= 13:
            return '11-13'
        else:
            return '14+'
    
    sup_groups['Size_cat'] = sup_groups['Antal medlemmer'].apply(categorize_group_size)
    
    # Tæl grupper per region og kategori
    size_dist_sup = sup_groups[sup_groups['Size_cat'].notna()].groupby(
        ['Region_short', 'Size_cat']
    ).size().reset_index(name='Count')
    
    # Beregn procent per region
    totals_sup = size_dist_sup.groupby('Region_short')['Count'].sum()
    size_dist_sup['Percent'] = size_dist_sup.apply(
        lambda row: (row['Count'] / totals_sup[row['Region_short']]) * 100 if row['Region_short'] in totals_sup else 0,
        axis=1
    )
    
    # Lav 100% stacked bar
    fig2a = go.Figure()
    
    categories = ['0-4', '5-7', '8-10', '11-13', '14+']
    cat_colors = {
        '0-4': CATEGORY_COLORS['red'],
        '5-7': CATEGORY_COLORS['orange'],
        '8-10': CATEGORY_COLORS['yellow'],
        '11-13': CATEGORY_COLORS['green'],
        '14+': CATEGORY_COLORS['gray']
    }
    
    for cat in categories:
        y_values = []
        for region in REGION_ORDER:
            data = size_dist_sup[
                (size_dist_sup['Region_short'] == region) &
                (size_dist_sup['Size_cat'] == cat)
            ]
            val = data['Percent'].values[0] if len(data) > 0 else 0
            y_values.append(val)
        
        fig2a.add_trace(go.Bar(
            name=f'{cat} medlemmer',
            x=REGION_ORDER,
            y=y_values,
            marker_color=cat_colors[cat]
        ))
    
    fig2a.update_layout(
        barmode='stack',
        height=500,
        xaxis_title='Region',
        yaxis_title='Procent (%)',
        yaxis=dict(range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig2a, use_container_width=True)
    
    st.markdown("""
    **Farveforklaring:**  
    🔴 0-4 medlemmer | 🟠 5-7 medlemmer | 🟡 8-10 medlemmer | 🟢 11-13 medlemmer | ⚪ 14+ medlemmer
    """)
    
    st.markdown("---")
    
    # ==========================================
    # TABEL 2B: GRUPPESTØRRELSE - DGE+JUN (%)
    # ==========================================
    
    st.header("📊 Tabel 2B: Gruppestørrelse DGE og JUN-grupper (procentfordeling)")
    st.caption("Fordeling af DGE og JUN-gruppers medlemstal")
    
    # Filtrer DGE og JUN grupper
    dge_jun_groups = groups_df[groups_df['Gruppetype_std'].isin(['DGE', 'JUN'])].copy()
    dge_jun_groups['Size_cat'] = dge_jun_groups['Antal medlemmer'].apply(categorize_group_size)
    
    # Tæl grupper per region og kategori
    size_dist_dge_jun = dge_jun_groups[dge_jun_groups['Size_cat'].notna()].groupby(
        ['Region_short', 'Size_cat']
    ).size().reset_index(name='Count')
    
    # Beregn procent per region
    totals_dge_jun = size_dist_dge_jun.groupby('Region_short')['Count'].sum()
    size_dist_dge_jun['Percent'] = size_dist_dge_jun.apply(
        lambda row: (row['Count'] / totals_dge_jun[row['Region_short']]) * 100 if row['Region_short'] in totals_dge_jun else 0,
        axis=1
    )
    
    # Lav 100% stacked bar
    fig2b = go.Figure()
    
    for cat in categories:
        y_values = []
        for region in REGION_ORDER:
            data = size_dist_dge_jun[
                (size_dist_dge_jun['Region_short'] == region) &
                (size_dist_dge_jun['Size_cat'] == cat)
            ]
            val = data['Percent'].values[0] if len(data) > 0 else 0
            y_values.append(val)
        
        fig2b.add_trace(go.Bar(
            name=f'{cat} medlemmer',
            x=REGION_ORDER,
            y=y_values,
            marker_color=cat_colors[cat]
        ))
    
    fig2b.update_layout(
        barmode='stack',
        height=500,
        xaxis_title='Region',
        yaxis_title='Procent (%)',
        yaxis=dict(range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig2b, use_container_width=True)
    
    st.markdown("""
    **Farveforklaring:**  
    🔴 0-4 medlemmer | 🟠 5-7 medlemmer | 🟡 8-10 medlemmer | 🟢 11-13 medlemmer | ⚪ 14+ medlemmer
    """)
    
    st.markdown("---")
    
    # ==========================================
    # TABEL 3: DELTAGERE PR MØDE - SUP GRUPPER
    # ==========================================
    
    st.header("📊 Tabel 3: Deltagere pr. møde i SUP-grupper")
    st.caption("Fordeling af møders deltagerantal")
    
    # Filtrer SUP møder
    sup_meetings = meetings_with_type[
        meetings_with_type['Gruppetype_std'] == 'SUP'
    ].copy()
    
    def categorize_sup_participants(n):
        if pd.isna(n) or n == 0:
            return None
        n = int(n)
        if n <= 2:
            return '0-2'
        elif n <= 5:
            return '3-5'
        elif n <= 8:
            return '6-8'
        elif n <= 11:
            return '9-11'
        else:
            return '12+'
    
    sup_meetings['Part_cat'] = sup_meetings['Antal deltagere'].apply(categorize_sup_participants)
    
    # Tæl møder per region og kategori
    sup_dist = sup_meetings[sup_meetings['Part_cat'].notna()].groupby(
        ['Region_short', 'Part_cat']
    ).size().reset_index(name='Count')
    
    # Beregn procent
    totals_sup = sup_dist.groupby('Region_short')['Count'].sum()
    sup_dist['Percent'] = sup_dist.apply(
        lambda row: (row['Count'] / totals_sup[row['Region_short']]) * 100 if row['Region_short'] in totals_sup else 0,
        axis=1
    )
    
    # Lav chart
    fig3 = go.Figure()
    
    sup_categories = ['0-2', '3-5', '6-8', '9-11', '12+']
    sup_colors = {
        '0-2': CATEGORY_COLORS['red'],
        '3-5': CATEGORY_COLORS['orange'],
        '6-8': CATEGORY_COLORS['yellow'],
        '9-11': CATEGORY_COLORS['green'],
        '12+': CATEGORY_COLORS['gray']
    }
    
    for cat in sup_categories:
        y_values = []
        for region in REGION_ORDER:
            data = sup_dist[
                (sup_dist['Region_short'] == region) &
                (sup_dist['Part_cat'] == cat)
            ]
            val = data['Percent'].values[0] if len(data) > 0 else 0
            y_values.append(val)
        
        fig3.add_trace(go.Bar(
            name=f'{cat} deltagere',
            x=REGION_ORDER,
            y=y_values,
            marker_color=sup_colors[cat]
        ))
    
    fig3.update_layout(
        barmode='stack',
        height=500,
        xaxis_title='Region',
        yaxis_title='Procent (%)',
        yaxis=dict(range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("""
    **Farveforklaring:**  
    🔴 0-2 deltagere | 🟠 3-5 deltagere | 🟡 6-8 deltagere | 🟢 9-11 deltagere | ⚪ 12+ deltagere
    """)
    
    st.markdown("---")
    
    # ==========================================
    # TABEL 4: DELTAGERE PR MØDE - DGE+JUN
    # ==========================================
    
    st.header("📊 Tabel 4: Deltagere pr. møde i DGE og JUN-grupper")
    st.caption("Fordeling af møders deltagerantal")
    
    # Filtrer DGE + JUN møder
    dge_jun_meetings = meetings_with_type[
        meetings_with_type['Gruppetype_std'].isin(['DGE', 'JUN'])
    ].copy()
    
    def categorize_dge_participants(n):
        if pd.isna(n) or n == 0:
            return None
        n = int(n)
        if n <= 4:
            return '0-4'
        elif n <= 7:
            return '5-7'
        elif n <= 10:
            return '8-10'
        elif n <= 13:
            return '11-13'
        else:
            return '14+'
    
    dge_jun_meetings['Part_cat'] = dge_jun_meetings['Antal deltagere'].apply(categorize_dge_participants)
    
    # Tæl og beregn procent
    dge_dist = dge_jun_meetings[dge_jun_meetings['Part_cat'].notna()].groupby(
        ['Region_short', 'Part_cat']
    ).size().reset_index(name='Count')
    
    totals_dge = dge_dist.groupby('Region_short')['Count'].sum()
    dge_dist['Percent'] = dge_dist.apply(
        lambda row: (row['Count'] / totals_dge[row['Region_short']]) * 100 if row['Region_short'] in totals_dge else 0,
        axis=1
    )
    
    # Lav chart
    fig4 = go.Figure()
    
    dge_categories = ['0-4', '5-7', '8-10', '11-13', '14+']
    dge_colors = {
        '0-4': CATEGORY_COLORS['red'],
        '5-7': CATEGORY_COLORS['orange'],
        '8-10': CATEGORY_COLORS['yellow'],
        '11-13': CATEGORY_COLORS['green'],
        '14+': CATEGORY_COLORS['gray']
    }
    
    for cat in dge_categories:
        y_values = []
        for region in REGION_ORDER:
            data = dge_dist[
                (dge_dist['Region_short'] == region) &
                (dge_dist['Part_cat'] == cat)
            ]
            val = data['Percent'].values[0] if len(data) > 0 else 0
            y_values.append(val)
        
        fig4.add_trace(go.Bar(
            name=f'{cat} deltagere',
            x=REGION_ORDER,
            y=y_values,
            marker_color=dge_colors[cat]
        ))
    
    fig4.update_layout(
        barmode='stack',
        height=500,
        xaxis_title='Region',
        yaxis_title='Procent (%)',
        yaxis=dict(range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("""
    **Farveforklaring:**  
    🔴 0-4 deltagere | 🟠 5-7 deltagere | 🟡 8-10 deltagere | 🟢 11-13 deltagere | ⚪ 14+ deltagere
    """)
    
    st.markdown("---")
    
    # ==========================================
    # TABEL 5: ANTAL MØDER PR GRUPPE
    # ==========================================
    
    st.header("📊 Tabel 5: Antal godkendte møder pr. gruppe")
    st.caption("Fordeling af gruppers mødeaktivitet")
    
    # Tæl møder per gruppe - brug Gruppe ID hvis tilgængelig, ellers Gruppenavn
    if 'Gruppe ID' in meetings_with_type.columns:
        group_key = 'Gruppe ID'
    else:
        group_key = 'Gruppenavn'
    
    meeting_counts_per_group = meetings_with_type.groupby([group_key, 'Region_short']).size().reset_index(name='Num_meetings')
    
    def categorize_meeting_count(n):
        if pd.isna(n) or n == 0:
            return None
        n = int(n)
        if n <= 2:
            return '1-2'
        elif n <= 4:
            return '3-4'
        elif n <= 6:
            return '5-6'
        elif n <= 8:
            return '7-8'
        else:
            return '9+'
    
    meeting_counts_per_group['Meeting_cat'] = meeting_counts_per_group['Num_meetings'].apply(categorize_meeting_count)
    
    # Tæl grupper per region og kategori
    meeting_freq_dist = meeting_counts_per_group[meeting_counts_per_group['Meeting_cat'].notna()].groupby(
        ['Region_short', 'Meeting_cat']
    ).size().reset_index(name='Count')
    
    # Beregn procent
    totals_freq = meeting_freq_dist.groupby('Region_short')['Count'].sum()
    meeting_freq_dist['Percent'] = meeting_freq_dist.apply(
        lambda row: (row['Count'] / totals_freq[row['Region_short']]) * 100 if row['Region_short'] in totals_freq else 0,
        axis=1
    )
    
    # Lav chart
    fig5 = go.Figure()
    
    freq_categories = ['1-2', '3-4', '5-6', '7-8', '9+']
    freq_colors = {
        '1-2': CATEGORY_COLORS['red'],
        '3-4': CATEGORY_COLORS['orange'],
        '5-6': CATEGORY_COLORS['yellow'],
        '7-8': CATEGORY_COLORS['green'],
        '9+': CATEGORY_COLORS['gray']
    }
    
    for cat in freq_categories:
        y_values = []
        for region in REGION_ORDER:
            data = meeting_freq_dist[
                (meeting_freq_dist['Region_short'] == region) &
                (meeting_freq_dist['Meeting_cat'] == cat)
            ]
            val = data['Percent'].values[0] if len(data) > 0 else 0
            y_values.append(val)
        
        fig5.add_trace(go.Bar(
            name=f'{cat} møder',
            x=REGION_ORDER,
            y=y_values,
            marker_color=freq_colors[cat]
        ))
    
    fig5.update_layout(
        barmode='stack',
        height=500,
        xaxis_title='Region',
        yaxis_title='Procent (%)',
        yaxis=dict(range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("""
    **Farveforklaring:**  
    🔴 1-2 møder | 🟠 3-4 møder | 🟡 5-6 møder | 🟢 7-8 møder | ⚪ 9+ møder
    """)
    
    st.markdown("---")
    
    # ==========================================
    # TABEL 6: AKTIVE GRUPPER UDEN GODKENDTE MØDER
    # ==========================================
    
    st.header("📊 Tabel 6: Aktive grupper uden godkendte møder")
    st.caption("Antal grupper med status 'aktiv' der ikke har holdt godkendte møder i perioden")
    
    # Find aktive grupper
    active_groups = groups_df[
        (groups_df['Status'].astype(str).str.strip().str.lower() == 'aktiv') |
        (groups_df['Status'].astype(str).str.strip().str.lower() == 'active')
    ].copy()
    
    # Find hvilke grupper der HAR godkendte møder
    if 'Gruppe ID' in meetings_with_type.columns:
        groups_with_meetings = meetings_with_type['Gruppe ID'].unique()
        active_groups['Has_meetings'] = active_groups['Gruppe ID'].isin(groups_with_meetings)
    else:
        groups_with_meetings_names = meetings_with_type['Gruppenavn'].unique()
        active_groups['Has_meetings'] = active_groups['Gruppenavn'].isin(groups_with_meetings_names)
    
    # Filtrer grupper UDEN møder
    groups_without_meetings = active_groups[~active_groups['Has_meetings']].copy()
    
    # Tæl per region og gruppetype
    no_meetings_counts = groups_without_meetings.groupby(
        ['Region_short', 'Gruppetype_std']
    ).size().reset_index(name='Antal')
    
    # Lav stacked bar chart (ikke indexeret)
    fig6 = go.Figure()
    
    for gtype in ['DGE', 'SUP', 'JUN']:
        y_values = []
        for region in REGION_ORDER:
            data = no_meetings_counts[
                (no_meetings_counts['Region_short'] == region) &
                (no_meetings_counts['Gruppetype_std'] == gtype)
            ]
            val = data['Antal'].values[0] if len(data) > 0 else 0
            y_values.append(val)
        
        fig6.add_trace(go.Bar(
            name=gtype,
            x=REGION_ORDER,
            y=y_values,
            marker_color=GROUP_TYPE_COLORS[gtype]
        ))
    
    fig6.update_layout(
        barmode='stack',
        height=500,
        xaxis_title='Region',
        yaxis_title='Antal grupper',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown("""
    **Farveforklaring:**  
    🔵 DGE | 🔴 SUP | 🟢 JUN
    """)
    
    # Vis også rå tal
    with st.expander("📋 Se detaljerede tal"):
        pivot_no_meetings = no_meetings_counts.pivot_table(
            index='Region_short',
            columns='Gruppetype_std',
            values='Antal',
            fill_value=0
        )
        st.dataframe(pivot_no_meetings, use_container_width=True)
    
    st.markdown("---")
    
    # ==========================================
    # TABEL 7: GRUPPER DER KUN HAR HOLDT SGE-MODUL MØDER
    # ==========================================
    
    st.header("📊 Tabel 7: Grupper med udelukkende SGE-modul møder")
    st.caption("Aktive grupper der kun har holdt møder af typen 'SGE-modul' i perioden")
    
    # Find alle møder per gruppe (både godkendte og ikke-godkendte)
    if 'Mødetype' in meetings_period.columns:
        # Identificer nøgle-kolonne
        if 'Gruppe ID' in meetings_period.columns:
            group_key = 'Gruppe ID'
        else:
            group_key = 'Gruppenavn'
        
        # Tæl mødetyper per gruppe
        meeting_types_per_group = meetings_period.groupby([group_key, 'Region_short', 'Mødetype']).size().reset_index(name='Count')
        
        # Find grupper der KUN har SGE-modul møder
        groups_with_any_meetings = meeting_types_per_group.groupby([group_key, 'Region_short'])['Mødetype'].apply(list).reset_index()
        
        sge_only_groups = []
        for _, row in groups_with_any_meetings.iterrows():
            meeting_types = row['Mødetype']
            # Tjek om ALLE møder er SGE-modul
            all_sge = all('sge' in str(mt).lower() and 'modul' in str(mt).lower() for mt in meeting_types)
            
            if all_sge and len(meeting_types) > 0:
                # Tjek at gruppen er aktiv
                if group_key == 'Gruppe ID':
                    group_info = active_groups[active_groups['Gruppe ID'] == row[group_key]]
                else:
                    group_info = active_groups[
                        (active_groups['Gruppenavn'] == row[group_key]) &
                        (active_groups['Region_short'] == row['Region_short'])
                    ]
                
                if not group_info.empty:
                    # Tæl antal SGE-modul møder
                    sge_count = meeting_types_per_group[
                        (meeting_types_per_group[group_key] == row[group_key]) &
                        (meeting_types_per_group['Region_short'] == row['Region_short']) &
                        (meeting_types_per_group['Mødetype'].astype(str).str.lower().str.contains('sge')) &
                        (meeting_types_per_group['Mødetype'].astype(str).str.lower().str.contains('modul'))
                    ]['Count'].sum()
                    
                    gruppenavn = group_info['Gruppenavn'].values[0]
                    
                    sge_only_groups.append({
                        'Region': row['Region_short'],
                        'Gruppenavn': gruppenavn,
                        'Antal SGE-modul møder': int(sge_count)
                    })
        
        if sge_only_groups:
            sge_df = pd.DataFrame(sge_only_groups)
            
            # Sorter efter region (samme rækkefølge som REGION_ORDER)
            sge_df['Region'] = pd.Categorical(sge_df['Region'], categories=REGION_ORDER, ordered=True)
            sge_df = sge_df.sort_values('Region')
            
            st.dataframe(sge_df, use_container_width=True, hide_index=True)
        else:
            st.info("Ingen grupper har udelukkende afholdt SGE-møder i perioden")
    else:
        st.warning("Mødetype-kolonne ikke fundet i data")
    
    st.markdown("---")
    
    if st.button("Download som PDF", type="primary"):
        with st.spinner("Genererer PDF..."):
            try:
                # Gem alle figurer
                all_figures = [
                    (fig, "Tabel 1: Godkendte møder (indexeret)"),
                    (fig2a, "Tabel 2A: Gruppestørrelse SUP"),
                    (fig2b, "Tabel 2B: Gruppestørrelse DGE+JUN"),
                    (fig3, "Tabel 3: Deltagere SUP"),
                    (fig4, "Tabel 4: Deltagere DGE+JUN"),
                    (fig5, "Tabel 5: Møder pr. gruppe"),
                    (fig6, "Tabel 6: Aktive grupper uden godkendte møder")
                ]
                
                pdf_buffer = generate_pdf_with_charts(all_figures, selected_year)
                
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_buffer,
                    file_name=f"DGE_Regional_Sammenligning_{selected_year}.pdf",
                    mime="application/pdf"
                )
                
                st.success("✅ PDF klar til download!")
            except Exception as e:
                st.error(f"Fejl ved generering af PDF: {e}")

def generate_pdf_with_charts(all_figures, year):
    """Generér PDF med alle grafer"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor='#2B6CB0',
        spaceAfter=20,
        alignment=1  # Center
    )
    
    story.append(Paragraph(f"DGE Regional Sammenligning {year}", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Tilføj hver graf
    for fig, title in all_figures:
        # Lav titel
        story.append(Paragraph(title, styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        try:
            # Konverter Plotly fig til billede
            img_bytes = fig.to_image(format="png", width=1000, height=500, engine="kaleido")
            
            # Gem som temp fil
            img_buffer = io.BytesIO(img_bytes)
            img = Image.open(img_buffer)
            
            # Resize til at passe på siden
            img.thumbnail((700, 350), Image.Resampling.LANCZOS)
            
            # Gem igen
            img_buffer2 = io.BytesIO()
            img.save(img_buffer2, format='PNG')
            img_buffer2.seek(0)
            
            # Brug ImageReader
            from reportlab.platypus import Image as RLImage
            rl_img = RLImage(img_buffer2, width=7*inch, height=3.5*inch)
            story.append(rl_img)
            
        except Exception as e:
            story.append(Paragraph(f"Kunne ikke inkludere graf: {e}", styles['Normal']))
        
        story.append(PageBreak())
    
    doc.build(story)
    buffer.seek(0)
    return buffer

if __name__ == "__main__":
    main()
