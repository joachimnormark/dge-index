"""
DGE Regional Sammenligning
Streamlit app til sammenligning af DGE-data på tværs af 5 regioner
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ============================================================================
# KONFIGURATION
# ============================================================================

st.set_page_config(page_title="📊 DGE Regional Sammenligning", layout="wide")

REGIONS = {
    'Nord': {'population': 600000, 'color': '#1f77b4'},
    'Midt': {'population': 1350000, 'color': '#ff7f0e'},
    'Syd': {'population': 1250000, 'color': '#2ca02c'},
    'Hovedstaden': {'population': 1900000, 'color': '#d62728'},
    'Sjælland': {'population': 850000, 'color': '#9467bd'}
}

REGION_ORDER = ['Nord', 'Midt', 'Syd', 'Hovedstaden', 'Sjælland']

BASE_REGION = 'Midt'

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
    st.info("📁 Upload 10 Excel-filer: 2 filer per region (groups + meetings)")
    
    uploaded_files = st.file_uploader(
        "Vælg filer",
        type=['xlsx', 'xls'],
        accept_multiple_files=True
    )
    
    if len(uploaded_files) < 10:
        st.warning(f"⚠️ Upload venligst 10 filer. Du har uploadet {len(uploaded_files)}.")
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
            y=y_values
        ))
    
    fig.update_layout(
        barmode='stack',
        height=500,
        xaxis_title='Region',
        yaxis_title=f'Index ({BASE_REGION} = 100)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
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
    # TABEL 2: GRUPPESTØRRELSE (%)
    # ==========================================
    
    st.header("📊 Tabel 2: Gruppestørrelse (procentfordeling)")
    st.caption("Fordeling af gruppers medlemstal")
    
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
    
    groups_df['Size_cat'] = groups_df['Antal medlemmer'].apply(categorize_group_size)
    
    # Tæl grupper per region og kategori
    size_dist = groups_df[groups_df['Size_cat'].notna()].groupby(
        ['Region_short', 'Size_cat']
    ).size().reset_index(name='Count')
    
    # Beregn procent per region
    totals = size_dist.groupby('Region_short')['Count'].sum()
    size_dist['Percent'] = size_dist.apply(
        lambda row: (row['Count'] / totals[row['Region_short']]) * 100,
        axis=1
    )
    
    # Lav 100% stacked bar
    fig2 = go.Figure()
    
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
            data = size_dist[
                (size_dist['Region_short'] == region) &
                (size_dist['Size_cat'] == cat)
            ]
            val = data['Percent'].values[0] if len(data) > 0 else 0
            y_values.append(val)
        
        fig2.add_trace(go.Bar(
            name=f'{cat} medlemmer',
            x=REGION_ORDER,
            y=y_values,
            marker_color=cat_colors[cat]
        ))
    
    fig2.update_layout(
        barmode='stack',
        height=500,
        xaxis_title='Region',
        yaxis_title='Procent (%)',
        yaxis=dict(range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
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

if __name__ == "__main__":
    main()
