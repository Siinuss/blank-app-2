import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# =====================================================
# SEITENEINSTELLUNGEN
# =====================================================

st.set_page_config(
    page_title="Reservoire des Stickstoffkreislaufs",
    layout="wide"
)

# =====================================================
# STYLING
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #dbeafe 0%, #f8fafc 40%, #ffffff 100%);
        color: #0f172a;
    }

    h1, h2, h3 {
        color: #0f172a;
        text-align: center;
    }

    .info-box, .highlight-card, .process-card {
        color: #0f172a;
    }

    .info-box {
        background: rgba(255,255,255,0.96);
        padding: 22px;
        border-radius: 24px;
        border: 1px solid rgba(15, 23, 42, 0.12);
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
        margin-bottom: 24px;
    }

    .highlight-card {
        background: rgba(255,255,255,0.96);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        margin-top: 20px;
        text-align: center;
    }

    .process-card {
        background: rgba(255,255,255,0.96);
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        margin-top: 18px;
    }

    .process-card h3 {
        margin: 0 0 8px 0;
        color: #1e3a8a;
    }

    .process-card p {
        margin: 0;
        font-size: 14px;
        line-height: 1.6;
    }

    .stSidebar {
        background: #0f172a;
    }

    .stSidebar * {
        color: #f8fafc !important;
    }

    .stSidebar [data-baseweb="base-input"] {
        background: #1e293b !important;
    }

    .stSidebar .stSlider > div > div > div {
        background: rgba(59, 130, 246, 0.2);
    }

    .sidebar-text {
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.5;
    }

    select, [role="option"] {
        background: #1e293b !important;
        color: #f8fafc !important;
    }

    option {
        background: #334155 !important;
        color: #f8fafc !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔬 Stickstoffkreislauf über die Zeit")

st.markdown(
    """
    <div class="info-box">
    Bewege den Schieber, um die Entwicklung des Stickstoffkreislaufs über die Jahrzehnte zu verfolgen.
    Links: Natürliche Entwicklung (ohne menschliche Einflüsse). Rechts: Mit anthropogenem Einfluss.
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Zeitstahl-Steuerung")

year = st.sidebar.slider(
    "Jahr auswählen",
    min_value=1900,
    max_value=2050,
    value=2025,
    step=1,
)

current_atmosphaere = 780
current_land = 120
current_ozean = 250

# =====================================================
# PROJEKTIONSLOGIK (VEREINFACHT)
# =====================================================

# Zwei Szenarien: Natural-only vs. With Anthropogenic
relative_year = (year - 2025) / 125

# Szenario 1: Natürlich (minimal, stabil)
natural_params = {"Atmosphäre": 0.01, "Land": -0.005, "Ozean": 0.008}
baseline_atmosphaere = int(current_atmosphaere * max(0.1, 1 + natural_params["Atmosphäre"] * relative_year))
baseline_land = int(current_land * max(0.1, 1 + natural_params["Land"] * relative_year))
baseline_ozean = int(current_ozean * max(0.1, 1 + natural_params["Ozean"] * relative_year))

# Szenario 2: Mit anthropogenem Einfluss (dramatische Veränderung)
anthropogenic_params = {"Atmosphäre": 0.65, "Land": -0.35, "Ozean": 0.40}
projected_atmosphaere = int(current_atmosphaere * max(0.1, 1 + anthropogenic_params["Atmosphäre"] * relative_year))
projected_land = int(current_land * max(0.1, 1 + anthropogenic_params["Land"] * relative_year))
projected_ozean = int(current_ozean * max(0.1, 1 + anthropogenic_params["Ozean"] * relative_year))

today_total = current_atmosphaere + current_land + current_ozean

# =====================================================
# HILFSFUNKTIONEN UND KONSTANTEN FÜR VISUALISIERUNG
# =====================================================

min_circle_size = 50
max_circle_size = 120

# Feste Dreieckspunkte: Die Reservoir-Kreise bleiben in denselben Ecken
atm_center_x = 230
atm_center_y = 120
land_center_x = 120
land_center_y = 400
ocean_center_x = 340
ocean_center_y = 400

def connect_on_border(x1, y1, r1, x2, y2, r2):
    """Berechne Linienendpunkte, die an den Kreisrändern enden."""
    dx = x2 - x1
    dy = y2 - y1
    dist = (dx ** 2 + dy ** 2) ** 0.5
    if dist == 0:
        return x1, y1, x2, y2
    ux = dx / dist
    uy = dy / dist
    return (
        x1 + ux * r1,
        y1 + uy * r1,
        x2 - ux * r2,
        y2 - uy * r2,
    )

# =====================================================
# ZWEI-SPALTEN-VISUALISIERUNG
# =====================================================

col1, col2 = st.columns(2)

# Spalte 1: NATÜRLICH (ohne anthropogenen Einfluss)
with col1:
    st.subheader("🌿 Ohne anthropogenen Einfluss")
    
    # Berechne Größen für natürliches Szenario
    max_value_natural = max(baseline_atmosphaere, baseline_land, baseline_ozean, 1)
    atm_size_nat = min(max_circle_size, max(min_circle_size, int(min_circle_size + (baseline_atmosphaere / max_value_natural) * (max_circle_size - min_circle_size))))
    land_size_nat = min(max_circle_size, max(min_circle_size, int(min_circle_size + (baseline_land / max_value_natural) * (max_circle_size - min_circle_size))))
    ocean_size_nat = min(max_circle_size, max(min_circle_size, int(min_circle_size + (baseline_ozean / max_value_natural) * (max_circle_size - min_circle_size))))
    
    atm_radius_nat = atm_size_nat / 2
    land_radius_nat = land_size_nat / 2
    ocean_radius_nat = ocean_size_nat / 2
    
    atm_land_x1_nat, atm_land_y1_nat, atm_land_x2_nat, atm_land_y2_nat = connect_on_border(
        atm_center_x, atm_center_y, atm_radius_nat,
        land_center_x, land_center_y, land_radius_nat,
    )
    atm_ocean_x1_nat, atm_ocean_y1_nat, atm_ocean_x2_nat, atm_ocean_y2_nat = connect_on_border(
        atm_center_x, atm_center_y, atm_radius_nat,
        ocean_center_x, ocean_center_y, ocean_radius_nat,
    )
    land_ocean_x1_nat, land_ocean_y1_nat, land_ocean_x2_nat, land_ocean_y2_nat = connect_on_border(
        land_center_x, land_center_y, land_radius_nat,
        ocean_center_x, ocean_center_y, ocean_radius_nat,
    )
    
    natural_baseline_total = baseline_atmosphaere + baseline_land + baseline_ozean
    
    triangle_natural_html = f"""
    <div style="width:100%; background: rgba(255,255,255,0.98); padding:15px; border-radius:16px; box-shadow:0 12px 28px rgba(15,23,42,0.08);">
        <p style="text-align:center; color:#334155; margin:0 0 12px 0; font-size:13px;">Natürliche Entwicklung (stabiler Zustand)</p>
        <div style="position:relative; width:100%; height:380px;">
            <svg width="100%" height="100%" viewBox="0 0 460 520" preserveAspectRatio="xMidYMid meet" style="position:absolute; top:0; left:0;">
                <defs>
                    <marker id="arrow-end-nat" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="strokeWidth">
                        <path d="M0,0 L8,4 L0,8 Z" fill="#0f172a" />
                    </marker>
                    <marker id="arrow-start-nat" markerWidth="8" markerHeight="8" refX="0" refY="4" orient="auto" markerUnits="strokeWidth">
                        <path d="M8,0 L0,4 L8,8 Z" fill="#0f172a" />
                    </marker>
                </defs>
                <polygon points="{atm_center_x},{atm_center_y} {land_center_x},{land_center_y} {ocean_center_x},{ocean_center_y}" fill="rgba(59,130,246,0.08)" stroke="#0f172a" stroke-width="2" />
                <line x1="{atm_land_x1_nat}" y1="{atm_land_y1_nat}" x2="{atm_land_x2_nat}" y2="{atm_land_y2_nat}" stroke="#0f172a" stroke-width="3" marker-start="url(#arrow-start-nat)" marker-end="url(#arrow-end-nat)" />
                <line x1="{atm_ocean_x1_nat}" y1="{atm_ocean_y1_nat}" x2="{atm_ocean_x2_nat}" y2="{atm_ocean_y2_nat}" stroke="#0f172a" stroke-width="3" marker-start="url(#arrow-start-nat)" marker-end="url(#arrow-end-nat)" />
                <line x1="{land_ocean_x1_nat}" y1="{land_ocean_y1_nat}" x2="{land_ocean_x2_nat}" y2="{land_ocean_y2_nat}" stroke="#0f172a" stroke-width="3" marker-start="url(#arrow-start-nat)" marker-end="url(#arrow-end-nat)" />
                <circle cx="{atm_center_x}" cy="{atm_center_y}" r="{atm_radius_nat}" fill="#9ca3af" stroke="#4b5563" stroke-width="3" />
                <circle cx="{land_center_x}" cy="{land_center_y}" r="{land_radius_nat}" fill="#a3b9a1" stroke="#5c6f5b" stroke-width="3" />
                <circle cx="{ocean_center_x}" cy="{ocean_center_y}" r="{ocean_radius_nat}" fill="#8ba8c9" stroke="#4b6b95" stroke-width="3" />
                <text x="{atm_center_x}" y="{atm_center_y - 8}" text-anchor="middle" fill="white" font-size="11" font-weight="700">Atm.</text>
                <text x="{land_center_x}" y="{land_center_y - 8}" text-anchor="middle" fill="white" font-size="11" font-weight="700">Land</text>
                <text x="{ocean_center_x}" y="{ocean_center_y - 8}" text-anchor="middle" fill="white" font-size="11" font-weight="700">Ozean</text>
                <text x="{atm_center_x}" y="{atm_center_y + 20}" text-anchor="middle" fill="white" font-size="11" font-weight="600">{baseline_atmosphaere} Gt</text>
                <text x="{land_center_x}" y="{land_center_y + 20}" text-anchor="middle" fill="white" font-size="11" font-weight="600">{baseline_land} Gt</text>
                <text x="{ocean_center_x}" y="{ocean_center_y + 20}" text-anchor="middle" fill="white" font-size="11" font-weight="600">{baseline_ozean} Gt</text>
            </svg>
        </div>
        <div style="margin-top:10px; padding:8px; background:#f0f9ff; border-radius:8px; font-size:12px; color:#1e3a8a; text-align:center;">
            Gesamtstickstoff: <strong>{natural_baseline_total} Gt N</strong>
        </div>
    </div>
    """
    
    components.html(triangle_natural_html, height=450)

# Spalte 2: MIT ANTHROPOGENEM EINFLUSS
with col2:
    st.subheader("⚡ Mit anthropogenem Einfluss")
    
    # Berechne Größen für anthropogenes Szenario
    max_value_anthro = max(projected_atmosphaere, projected_land, projected_ozean, 1)
    atm_size_anth = min(max_circle_size, max(min_circle_size, int(min_circle_size + (projected_atmosphaere / max_value_anthro) * (max_circle_size - min_circle_size))))
    land_size_anth = min(max_circle_size, max(min_circle_size, int(min_circle_size + (projected_land / max_value_anthro) * (max_circle_size - min_circle_size))))
    ocean_size_anth = min(max_circle_size, max(min_circle_size, int(min_circle_size + (projected_ozean / max_value_anthro) * (max_circle_size - min_circle_size))))
    
    atm_radius_anth = atm_size_anth / 2
    land_radius_anth = land_size_anth / 2
    ocean_radius_anth = ocean_size_anth / 2
    
    atm_land_x1_anth, atm_land_y1_anth, atm_land_x2_anth, atm_land_y2_anth = connect_on_border(
        atm_center_x, atm_center_y, atm_radius_anth,
        land_center_x, land_center_y, land_radius_anth,
    )
    atm_ocean_x1_anth, atm_ocean_y1_anth, atm_ocean_x2_anth, atm_ocean_y2_anth = connect_on_border(
        atm_center_x, atm_center_y, atm_radius_anth,
        ocean_center_x, ocean_center_y, ocean_radius_anth,
    )
    land_ocean_x1_anth, land_ocean_y1_anth, land_ocean_x2_anth, land_ocean_y2_anth = connect_on_border(
        land_center_x, land_center_y, land_radius_anth,
        ocean_center_x, ocean_center_y, ocean_radius_anth,
    )
    
    projected_total = projected_atmosphaere + projected_land + projected_ozean
    
    triangle_anthro_html = f"""
    <div style="width:100%; background: rgba(255,255,255,0.98); padding:15px; border-radius:16px; box-shadow:0 12px 28px rgba(15,23,42,0.08);">
        <p style="text-align:center; color:#334155; margin:0 0 12px 0; font-size:13px;">Mit anthropogenem Einfluss – Jahr {year}</p>
        <div style="position:relative; width:100%; height:380px;">
            <svg width="100%" height="100%" viewBox="0 0 460 520" preserveAspectRatio="xMidYMid meet" style="position:absolute; top:0; left:0;">
                <defs>
                    <marker id="arrow-end-anth" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="strokeWidth">
                        <path d="M0,0 L8,4 L0,8 Z" fill="#0f172a" />
                    </marker>
                    <marker id="arrow-start-anth" markerWidth="8" markerHeight="8" refX="0" refY="4" orient="auto" markerUnits="strokeWidth">
                        <path d="M8,0 L0,4 L8,8 Z" fill="#0f172a" />
                    </marker>
                </defs>
                <polygon points="{atm_center_x},{atm_center_y} {land_center_x},{land_center_y} {ocean_center_x},{ocean_center_y}" fill="rgba(239,68,68,0.08)" stroke="#0f172a" stroke-width="2" />
                <line x1="{atm_land_x1_anth}" y1="{atm_land_y1_anth}" x2="{atm_land_x2_anth}" y2="{atm_land_y2_anth}" stroke="#0f172a" stroke-width="3" marker-start="url(#arrow-start-anth)" marker-end="url(#arrow-end-anth)" />
                <line x1="{atm_ocean_x1_anth}" y1="{atm_ocean_y1_anth}" x2="{atm_ocean_x2_anth}" y2="{atm_ocean_y2_anth}" stroke="#0f172a" stroke-width="3" marker-start="url(#arrow-start-anth)" marker-end="url(#arrow-end-anth)" />
                <line x1="{land_ocean_x1_anth}" y1="{land_ocean_y1_anth}" x2="{land_ocean_x2_anth}" y2="{land_ocean_y2_anth}" stroke="#0f172a" stroke-width="3" marker-start="url(#arrow-start-anth)" marker-end="url(#arrow-end-anth)" />
                <circle cx="{atm_center_x}" cy="{atm_center_y}" r="{atm_radius_anth}" fill="#ef4444" stroke="#991b1b" stroke-width="3" />
                <circle cx="{land_center_x}" cy="{land_center_y}" r="{land_radius_anth}" fill="#f87171" stroke="#b91c1c" stroke-width="3" />
                <circle cx="{ocean_center_x}" cy="{ocean_center_y}" r="{ocean_radius_anth}" fill="#fca5a5" stroke="#dc2626" stroke-width="3" />
                <text x="{atm_center_x}" y="{atm_center_y - 8}" text-anchor="middle" fill="white" font-size="11" font-weight="700">Atm.</text>
                <text x="{land_center_x}" y="{land_center_y - 8}" text-anchor="middle" fill="white" font-size="11" font-weight="700">Land</text>
                <text x="{ocean_center_x}" y="{ocean_center_y - 8}" text-anchor="middle" fill="white" font-size="11" font-weight="700">Ozean</text>
                <text x="{atm_center_x}" y="{atm_center_y + 20}" text-anchor="middle" fill="white" font-size="11" font-weight="600">{projected_atmosphaere} Gt</text>
                <text x="{land_center_x}" y="{land_center_y + 20}" text-anchor="middle" fill="white" font-size="11" font-weight="600">{projected_land} Gt</text>
                <text x="{ocean_center_x}" y="{ocean_center_y + 20}" text-anchor="middle" fill="white" font-size="11" font-weight="600">{projected_ozean} Gt</text>
            </svg>
        </div>
        <div style="margin-top:10px; padding:8px; background:#fee2e2; border-radius:8px; font-size:12px; color:#991b1b; text-align:center;">
            Gesamtstickstoff: <strong>{projected_total} Gt N</strong>
        </div>
    </div>
    """
    
    components.html(triangle_anthro_html, height=450)

st.markdown("---")

st.markdown("""
### 📊 Zeitvergleich: Natürliche Stabilität vs. Anthropogene Veränderung

Beobachte, wie sich der Stickstoffkreislauf über die Jahrzehnte entwickelt:
- **Links**: Ohne menschliche Einflüsse bleibt die Verteilung weitgehend stabil
- **Rechts**: Mit anthropogenen Aktivitäten (Industrie, Landwirtschaft) verändert sich der Kreislauf dramatisch

**Verschiebe den Jahr-Schieber in der Seitenleiste**, um zu sehen, wie sich beide Szenarien parallel entwickeln.
""")
