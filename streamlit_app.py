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
    }

    .process-card {
        background: linear-gradient(135deg, rgba(236, 253, 245, 0.95), rgba(224, 242, 254, 0.95));
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(59, 130, 246, 0.16);
        margin-top: 24px;
    }

    .process-card h3 {
        margin-top: 0;
        color: #1e3a8a;
    }

    .stSidebar {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.98), rgba(15, 23, 42, 0.92));
        color: #f8fafc !important;
    }

    .stSidebar *,
    .sidebar-text,
    .stSidebar label,
    .stSidebar span,
    .stSidebar p,
    .stSidebar div,
    .stSidebar .stMarkdown,
    .stSidebar .css-1d391kg,
    .stSidebar .css-1udyy4t,
    .stSidebar .css-1v0mbdj,
    .stSidebar .css-1gkcyyc {
        color: #f8fafc !important;
    }

    .stSidebar .css-1xhj18k {
        border-color: rgba(255,255,255,0.18) !important;
    }

    .stSidebar select,
    .stSidebar option,
    .stSidebar [role="option"],
    .stSidebar [role="listbox"] {
        color: #f8fafc !important;
    }

    select,
    option,
    [role="option"],
    [role="listbox"],
    [data-baseweb="option"],
    [data-baseweb="select"] {
        color: #f8fafc !important;
    }

    .stSidebar .stButton>button {
        background-color: #2563eb;
        color: white;
    }

    body, p, span, li, strong {
        color: #0f172a !important;
    }

    a {
        color: #1d4ed8 !important;
    }

    .st-bdg, .st-bdg span {
        color: #0f172a !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# APP-TITEL
# =====================================================

st.title("🔬 Interaktiver Stickstoffkreislauf")

st.markdown(
    """
    <div class="info-box">
    Diese App zeigt die drei wichtigsten Stickstoff-Reservoire und wie sie sich durch unterschiedliche soziale und ökologische Einflüsse über die Jahre verändern.
    Wähle einen Zeitraum und einen menschlichen Einfluss, um die Entwicklung sichtbar zu machen.
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Reservoir-Steuerung")

current_atmosphaere = st.sidebar.slider(
    "Aktuelle Atmosphäre (Gt N)",
    min_value=100,
    max_value=1000,
    value=780,
    step=10,
)

current_land = st.sidebar.slider(
    "Aktuelles Land/Biosphäre (Gt N)",
    min_value=10,
    max_value=500,
    value=120,
    step=5,
)

current_ozean = st.sidebar.slider(
    "Aktueller Ozean (Gt N)",
    min_value=10,
    max_value=500,
    value=250,
    step=5,
)

year = st.sidebar.slider(
    "Jahr",
    min_value=1900,
    max_value=2050,
    value=2025,
    step=5,
)

influence = st.sidebar.selectbox(
    "Anthropogener Einfluss",
    ["Sehr niedrig", "Niedrig", "Mittel", "Hoch", "Sehr hoch"],
)

natural_influence_enabled = st.sidebar.checkbox("Natürlichen Einfluss aktivieren", value=False)

if natural_influence_enabled:
    natural_influence = st.sidebar.selectbox(
        "Natürlicher Einfluss",
        ["Sehr niedrig", "Niedrig", "Mittel", "Hoch", "Sehr hoch"],
    )
else:
    natural_influence = "Mittel"

reservoir_focus = st.sidebar.selectbox(
    "Reservoir-Fokus",
    ["Gleichmäßig", "Atmosphäre stärker", "Land stärker", "Ozean stärker"],
)

scenario_template = st.sidebar.selectbox(
    "Szenario-Vorlage",
    ["Standard", "Stark wachsend", "Moderates Wachstum", "Abschwächung", "Stabil"],
)

show_connections = st.sidebar.checkbox("Verbindungen anzeigen", value=True)

selected_process = st.sidebar.selectbox(
    "Prozess wählen",
    [
        "Stickstofffixierung",
        "Nitrifikation",
        "Denitrifikation",
        "Pflanzenaufnahme",
        "Austausch Atmosphäre-Ozean",
    ],
)

st.sidebar.markdown(
    """
    <div class="sidebar-text">
    Wähle das Jahr, die Stärke des menschlichen Einflusses und einen Prozess, um den Stickstoffkreislauf interaktiv zu erkunden.
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# PROJEKTIONSLOGIK
# =====================================================

anthropogenic_params = {
    "Sehr niedrig": {"Atmosphäre": 0.08, "Land": -0.04, "Ozean": 0.05},
    "Niedrig": {"Atmosphäre": 0.12, "Land": -0.06, "Ozean": 0.08},
    "Mittel": {"Atmosphäre": 0.28, "Land": -0.16, "Ozean": 0.18},
    "Hoch": {"Atmosphäre": 0.55, "Land": -0.30, "Ozean": 0.36},
    "Sehr hoch": {"Atmosphäre": 0.75, "Land": -0.42, "Ozean": 0.50},
}

natural_influence_params = {
    "Sehr niedrig": {"Atmosphäre": 0.02, "Land": -0.01, "Ozean": 0.01},
    "Niedrig": {"Atmosphäre": 0.05, "Land": -0.02, "Ozean": 0.03},
    "Mittel": {"Atmosphäre": 0.08, "Land": -0.04, "Ozean": 0.05},
    "Hoch": {"Atmosphäre": 0.12, "Land": -0.06, "Ozean": 0.08},
    "Sehr hoch": {"Atmosphäre": 0.18, "Land": -0.10, "Ozean": 0.12},
}

reservoir_focus_adjust = {
    "Gleichmäßig": {"Atmosphäre": 0.0, "Land": 0.0, "Ozean": 0.0},
    "Atmosphäre stärker": {"Atmosphäre": 0.08, "Land": -0.04, "Ozean": 0.02},
    "Land stärker": {"Atmosphäre": 0.02, "Land": -0.10, "Ozean": 0.04},
    "Ozean stärker": {"Atmosphäre": 0.01, "Land": -0.03, "Ozean": 0.08},
}

scenario_template_adjust = {
    "Standard": {"Atmosphäre": 0.0, "Land": 0.0, "Ozean": 0.0},
    "Stark wachsend": {"Atmosphäre": 0.10, "Land": -0.05, "Ozean": 0.05},
    "Moderates Wachstum": {"Atmosphäre": 0.05, "Land": -0.03, "Ozean": 0.03},
    "Abschwächung": {"Atmosphäre": -0.03, "Land": 0.02, "Ozean": -0.01},
    "Stabil": {"Atmosphäre": 0.0, "Land": 0.0, "Ozean": 0.0},
}

process_adjust = {
    "Stickstofffixierung": {"Atmosphäre": -0.02, "Land": 0.05, "Ozean": 0.0},
    "Nitrifikation": {"Atmosphäre": 0.02, "Land": -0.01, "Ozean": 0.0},
    "Denitrifikation": {"Atmosphäre": 0.03, "Land": -0.02, "Ozean": 0.0},
    "Pflanzenaufnahme": {"Atmosphäre": -0.04, "Land": 0.06, "Ozean": -0.01},
    "Austausch Atmosphäre-Ozean": {"Atmosphäre": -0.02, "Land": 0.0, "Ozean": 0.03},
}

relative_year = (year - 2025) / 125
base_params = anthropogenic_params[influence]
extra_focus = reservoir_focus_adjust[reservoir_focus]
extra_template = scenario_template_adjust[scenario_template]
extra_process = process_adjust[selected_process]
params = {
    key: base_params[key] + extra_focus[key] + extra_template[key] + extra_process[key]
    for key in base_params
}

# Damit die Szenario-Auswahl auch bei Jahr 2025 sichtbar wird,
# wird ein kleiner Basis-Einfluss hinzugefügt.
scenario_offset = 0.20
effective_year_factor = relative_year + scenario_offset

projected_atmosphaere = int(current_atmosphaere * max(0.1, 1 + params["Atmosphäre"] * effective_year_factor))
projected_land = int(current_land * max(0.1, 1 + params["Land"] * effective_year_factor))
projected_ozean = int(current_ozean * max(0.1, 1 + params["Ozean"] * effective_year_factor))

today_total = current_atmosphaere + current_land + current_ozean
projected_total = projected_atmosphaere + projected_land + projected_ozean

if natural_influence_enabled:
    natural_params = natural_influence_params[natural_influence]
else:
    natural_params = {"Atmosphäre": 0.0, "Land": 0.0, "Ozean": 0.0}

baseline_atmosphaere = int(current_atmosphaere * max(0.1, 1 + natural_params["Atmosphäre"] * relative_year))
baseline_land = int(current_land * max(0.1, 1 + natural_params["Land"] * relative_year))
baseline_ozean = int(current_ozean * max(0.1, 1 + natural_params["Ozean"] * relative_year))

# =====================================================
# ZEITREIHEN
# =====================================================

years = list(range(1900, 2051, 10))
baseline_series = {
    "Atmosphäre": [],
    "Land": [],
    "Ozean": [],
}
anthropogenic_series = {
    "Atmosphäre": [],
    "Land": [],
    "Ozean": [],
}
for y in years:
    ry = (y - 2025) / 125
    baseline_series["Atmosphäre"].append(int(current_atmosphaere * max(0.1, 1 + natural_params["Atmosphäre"] * ry)))
    baseline_series["Land"].append(int(current_land * max(0.1, 1 + natural_params["Land"] * ry)))
    baseline_series["Ozean"].append(int(current_ozean * max(0.1, 1 + natural_params["Ozean"] * ry)))
    anthropogenic_series["Atmosphäre"].append(int(current_atmosphaere * max(0.1, 1 + params["Atmosphäre"] * ry)))
    anthropogenic_series["Land"].append(int(current_land * max(0.1, 1 + params["Land"] * ry)))
    anthropogenic_series["Ozean"].append(int(current_ozean * max(0.1, 1 + params["Ozean"] * ry)))

# =====================================================
# VISUALISIERUNG DER RESERVOIRS
# =====================================================

max_value = max(projected_atmosphaere, projected_land, projected_ozean, 1)

min_circle_size = 50
max_circle_size = 120
atm_size = min(max_circle_size, max(min_circle_size, int(min_circle_size + (projected_atmosphaere / max_value) * (max_circle_size - min_circle_size))))
land_size = min(max_circle_size, max(min_circle_size, int(min_circle_size + (projected_land / max_value) * (max_circle_size - min_circle_size))))
ocean_size = min(max_circle_size, max(min_circle_size, int(min_circle_size + (projected_ozean / max_value) * (max_circle_size - min_circle_size))))

# Feste Dreieckspunkte: Die Reservoir-Kreise bleiben in denselben Ecken,
# nur ihr Radius ändert sich mit dem Szenario.
# Die SVG-Maße und die Kreismittelpunkte sind so gesetzt, dass die Kreise immer sichtbar bleiben.
atm_center_x = 230
atm_center_y = 120
land_center_x = 120
land_center_y = 400
ocean_center_x = 340
ocean_center_y = 400

atm_radius = atm_size / 2
land_radius = land_size / 2
ocean_radius = ocean_size / 2

# Linien so anpassen, dass sie an den Kreisrändern enden

def connect_on_border(x1, y1, r1, x2, y2, r2):
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

atm_land_x1, atm_land_y1, atm_land_x2, atm_land_y2 = connect_on_border(
    atm_center_x, atm_center_y, atm_radius,
    land_center_x, land_center_y, land_radius,
)
atm_ocean_x1, atm_ocean_y1, atm_ocean_x2, atm_ocean_y2 = connect_on_border(
    atm_center_x, atm_center_y, atm_radius,
    ocean_center_x, ocean_center_y, ocean_radius,
)
land_ocean_x1, land_ocean_y1, land_ocean_x2, land_ocean_y2 = connect_on_border(
    land_center_x, land_center_y, land_radius,
    ocean_center_x, ocean_center_y, ocean_radius,
)

triangle_html = f"""
<div style="width:100%; max-width:1000px; margin:auto; background: rgba(255,255,255,0.98); padding:20px; border-radius:24px; box-shadow:0 18px 40px rgba(15,23,42,0.08);">
    <h3 style="text-align:center; color:#1e3a8a; margin-top:0;">Reservoir-Dreieck</h3>
    <p style="text-align:center; color:#334155; margin-bottom:18px;">Passe die Werte in der Sidebar an und sieh, wie sich Atmosphäre, Land und Ozean direkt an Dreiecksecken verändern.</p>
    <div style="position:relative; width:100%; height:520px;">
        <svg width="100%" height="100%" viewBox="0 0 460 520" preserveAspectRatio="xMidYMid meet" style="position:absolute; top:0; left:0;">
            <defs>
                <marker id="arrow-end" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="strokeWidth">
                    <path d="M0,0 L8,4 L0,8 Z" fill="#0f172a" />
                </marker>
                <marker id="arrow-start" markerWidth="8" markerHeight="8" refX="0" refY="4" orient="auto" markerUnits="strokeWidth">
                    <path d="M8,0 L0,4 L8,8 Z" fill="#0f172a" />
                </marker>
                <linearGradient id="atmGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#60a5fa" />
                    <stop offset="100%" stop-color="#2563eb" />
                </linearGradient>
                <linearGradient id="landGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#34d399" />
                    <stop offset="100%" stop-color="#059669" />
                </linearGradient>
                <linearGradient id="oceanGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#93c5fd" />
                    <stop offset="100%" stop-color="#1e40af" />
                </linearGradient>
            </defs>
            <polygon points="{atm_center_x},{atm_center_y} {land_center_x},{land_center_y} {ocean_center_x},{ocean_center_y}" fill="rgba(59,130,246,0.08)" stroke="#0f172a" stroke-width="2" />
            <line x1="{atm_land_x1}" y1="{atm_land_y1}" x2="{atm_land_x2}" y2="{atm_land_y2}" stroke="#0f172a" stroke-width="4" visibility="{'visible' if show_connections else 'hidden'}" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
            <line x1="{atm_ocean_x1}" y1="{atm_ocean_y1}" x2="{atm_ocean_x2}" y2="{atm_ocean_y2}" stroke="#0f172a" stroke-width="4" visibility="{'visible' if show_connections else 'hidden'}" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
            <line x1="{land_ocean_x1}" y1="{land_ocean_y1}" x2="{land_ocean_x2}" y2="{land_ocean_y2}" stroke="#0f172a" stroke-width="4" visibility="{'visible' if show_connections else 'hidden'}" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />
            <circle cx="{atm_center_x}" cy="{atm_center_y}" r="{atm_radius}" fill="#60a5fa" stroke="#1d4ed8" stroke-width="4" />
            <circle cx="{land_center_x}" cy="{land_center_y}" r="{land_radius}" fill="#34d399" stroke="#059669" stroke-width="4" />
            <circle cx="{ocean_center_x}" cy="{ocean_center_y}" r="{ocean_radius}" fill="#3b82f6" stroke="#1e40af" stroke-width="4" />
            <text x="{atm_center_x}" y="{atm_center_y + 6}" text-anchor="middle" fill="white" font-size="14" font-weight="700">Atmosphäre</text>
            <text x="{land_center_x}" y="{land_center_y + 6}" text-anchor="middle" fill="white" font-size="14" font-weight="700">Land</text>
            <text x="{ocean_center_x}" y="{ocean_center_y + 6}" text-anchor="middle" fill="white" font-size="14" font-weight="700">Ozean</text>
            <text x="{atm_center_x}" y="{atm_center_y + 28}" text-anchor="middle" fill="white" font-size="12">{projected_atmosphaere} Gt</text>
            <text x="{land_center_x}" y="{land_center_y + 28}" text-anchor="middle" fill="white" font-size="12">{projected_land} Gt</text>
            <text x="{ocean_center_x}" y="{ocean_center_y + 28}" text-anchor="middle" fill="white" font-size="12">{projected_ozean} Gt</text>
        </svg>
    </div>
</div>
"""

components.html(triangle_html, height=580)

# =====================================================
# AUSWERTUNG
# =====================================================

st.markdown("---")

st.subheader("Aktuelle Verteilung")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    st.metric("Atmosphäre", f"{current_atmosphaere} Gt N", f"{current_atmosphaere / today_total * 100:.1f}%")
with c2:
    st.metric("Land", f"{current_land} Gt N", f"{current_land / today_total * 100:.1f}%")
with c3:
    st.metric("Ozean", f"{current_ozean} Gt N", f"{current_ozean / today_total * 100:.1f}%")

st.markdown("---")

st.subheader("Projektierte Verteilung")

c4, c5, c6 = st.columns([1, 1, 1])
with c4:
    st.metric("Atmosphäre (proj.)", f"{projected_atmosphaere} Gt N", f"{projected_atmosphaere / projected_total * 100:.1f}%")
with c5:
    st.metric("Land (proj.)", f"{projected_land} Gt N", f"{projected_land / projected_total * 100:.1f}%")
with c6:
    st.metric("Ozean (proj.)", f"{projected_ozean} Gt N", f"{projected_ozean / projected_total * 100:.1f}%")

st.markdown(
    f"""
    <div class="highlight-card">
    Jahr: <strong>{year}</strong> · Szenario: <strong>{influence}</strong> · Gesamtmenge: <strong>{projected_total} Gt N</strong>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

st.subheader("Prognose der Reservoir-Veränderung")

st.markdown(
    f"""
    In diesem Szenario zeigen die Kreise, wie sich die Reservoirgrößen im Jahr {year} unter {influence.lower()}em menschlichen Einfluss verändern.
    """
)

baseline_df = pd.DataFrame(baseline_series, index=pd.Index(years, name="Jahr"))
anthro_df = pd.DataFrame({
    "Atmosphäre": anthropogenic_series["Atmosphäre"],
    "Land": anthropogenic_series["Land"],
    "Ozean": anthropogenic_series["Ozean"],
}, index=pd.Index(years, name="Jahr"))

col1, col2 = st.columns(2)
with col1:
    st.subheader("Ohne anthropogenen Einfluss")
    st.write("Natürliche Entwicklung der Reservoirgrößen, wenn menschlicher Druck gering bleibt.")
    st.line_chart(baseline_df)
with col2:
    st.subheader("Mit anthropogenem Einfluss")
    st.write(f"Prognose für das gewählte Szenario {influence} im Jahr {year}.")
    st.line_chart(anthro_df)

st.markdown("---")

st.subheader("Prozess-Guide")

process_info = {
    "Stickstofffixierung": "Stickstofffixierung macht atmogenen Stickstoff für Pflanzen verfügbar. Sie findet häufig in Böden, Wurzelsymbiosen und Algen statt.",
    "Nitrifikation": "Nitrifikation wandelt Ammonium in Nitrit und Nitrat um. Dadurch wird Stickstoff im Boden mobilisiert.",
    "Denitrifikation": "Denitrifikation gibt Stickstoff zurück in die Atmosphäre. Dadurch schließt sich der Kreislauf.",
    "Pflanzenaufnahme": "Pflanzen nehmen Stickstoff auf und speichern ihn in Biomasse. Das Land wird so zu einem aktiven Reservoir.",
    "Austausch Atmosphäre-Ozean": "Der Austausch zwischen Atmosphäre und Ozean reguliert die globale Stickstoffbilanz über Gaslösung und Austauschprozesse.",
}

st.markdown(
    f"""
    <div class="process-card">
        <h3>{selected_process}</h3>
        <p>{process_info[selected_process]}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

left, right = st.columns(2)
with left:
    st.markdown("""
    **Interaktive Schritte**

    1. Passe die aktuellen Reservoir-Werte an.
    2. Wähle das Jahr, um historische und zukünftige Entwicklungen zu sehen.
    3. Schau dir das Szenario an, um den anthropogenen Einfluss zu verstehen.
    """)
with right:
    st.markdown("""
    **Was du sehen solltest**

    - Die Kreise bleiben auf einer symmetrischen Dreieckslinie.
    - Größere Kreise bedeuten mehr gespeicherten Stickstoff.
    - Ein hoher anthropogener Einfluss verschiebt das Land-Reservoir nach unten.
    """)

st.markdown("---")

with st.expander("Mehr über den anthropogenen Einfluss"):
    st.write(
        """
        Menschliche Aktivitäten wie Landwirtschaft, Verbrennung fossiler Brennstoffe und Landnutzungsänderungen können den Stickstoffkreislauf stark verändern.
        In Zukunft können diese Prozesse die Atmosphäre und den Ozean stärker belasten, während Landvorräte sinken.
        """
    )
