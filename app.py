# -*- coding: utf-8 -*-
import os
import base64
from pathlib import Path
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# ============================================================
# NOVAFLUX INDUSTRIE — Dashboard de fabrication & logistique
# ============================================================

APP_NAME = "NOVAFLUX"
APP_SUBTITLE = "Pilotage industriel & logistique"
DATA_FILE = Path(__file__).with_name("dataset.csv")

# Identifiants de démonstration — à modifier avant une utilisation réelle.
USERS = {
    "admin": "Nova@2026",
    "manager": "Manager@2026",
}


# ------------------------- Configuration --------------------
st.set_page_config(
    page_title=f"{APP_NAME} | {APP_SUBTITLE}",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

sns.set_theme(style="whitegrid")


# ---------------------------- Logo ---------------------------
LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 150">
  <defs>
    <linearGradient id="g" x1="0" x2="1">
      <stop offset="0" stop-color="#0f766e"/>
      <stop offset="1" stop-color="#14b8a6"/>
    </linearGradient>
  </defs>
  <rect width="520" height="150" rx="30" fill="#f8fafc"/>
  <circle cx="82" cy="75" r="48" fill="url(#g)"/>
  <path d="M58 88 L82 43 L106 88" fill="none" stroke="white" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M69 76 H95" stroke="white" stroke-width="8" stroke-linecap="round"/>
  <text x="145" y="72" font-family="Arial, sans-serif" font-size="42" font-weight="700" fill="#0f172a">NOVAFLUX</text>
  <text x="147" y="104" font-family="Arial, sans-serif" font-size="18" fill="#475569">INDUSTRIE • DATA • PERFORMANCE</text>
</svg>
"""

ICON_SVGS = {
    "dashboard": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="8" y="8" width="20" height="20" rx="4" fill="#0f766e"/><rect x="36" y="8" width="20" height="20" rx="4" fill="#14b8a6"/><rect x="8" y="36" width="20" height="20" rx="4" fill="#14b8a6"/><rect x="36" y="36" width="20" height="20" rx="4" fill="#0f766e"/></svg>""",
    "analyse": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path d="M10 52h44" stroke="#0f172a" stroke-width="5"/><rect x="14" y="32" width="8" height="18" rx="2" fill="#0f766e"/><rect x="28" y="23" width="8" height="27" rx="2" fill="#14b8a6"/><rect x="42" y="14" width="8" height="36" rx="2" fill="#0f766e"/><path d="M13 25l12-9 9 6 17-14" fill="none" stroke="#334155" stroke-width="4" stroke-linecap="round"/></svg>""",
    "performance": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path d="M12 46a20 20 0 1140 0" fill="none" stroke="#0f766e" stroke-width="7"/><path d="M32 46l12-18" stroke="#14b8a6" stroke-width="7" stroke-linecap="round"/><circle cx="32" cy="46" r="5" fill="#0f172a"/></svg>""",
    "data": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><ellipse cx="32" cy="15" rx="20" ry="8" fill="#0f766e"/><path d="M12 15v18c0 5 9 8 20 8s20-3 20-8V15" fill="#14b8a6"/><path d="M12 33v16c0 5 9 8 20 8s20-3 20-8V33" fill="#0f766e"/><ellipse cx="32" cy="33" rx="20" ry="8" fill="#14b8a6"/></svg>""",
}

def svg_data(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


def logo_html(height=92):
    return f'<img src="{svg_data(LOGO_SVG)}" style="width:100%;height:{height}px;object-fit:contain;">'


# ------------------------------ CSS --------------------------
st.markdown("""
<style>
    .stApp {
        background: #f4f7f9;
    }
    [data-testid="stSidebar"] {
        background: #0f172a;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #134e4a 100%);
        padding: 30px 34px;
        border-radius: 22px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(15,23,42,.10);
    }
    .hero h1 {
        margin: 0;
        font-size: 34px;
        letter-spacing: -.5px;
    }
    .hero p {
        margin: 8px 0 0 0;
        color: #ccfbf1;
        font-size: 16px;
    }
    .metric-top {
        display: flex;
        align-items: center;
        gap: 11px;
    }
    .metric-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: #ecfdf5;
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 0 0 40px;
    }
    .metric-icon img {
        width: 25px;
        height: 25px;
    }
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 18px 20px;
        min-height: 118px;
        box-shadow: 0 6px 18px rgba(15,23,42,.05);
    }
    .metric-label {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .4px;
    }
    .metric-value {
        color: #0f172a;
        font-size: 29px;
        font-weight: 750;
        margin-top: 8px;
    }
    .metric-note {
        color: #0f766e;
        font-size: 12px;
        margin-top: 4px;
    }
    .section-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 5px 16px rgba(15,23,42,.04);
    }
    .login-shell {
        max-width: 560px;
        margin: 4vh auto;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 28px;
        padding: 18px 30px 30px 30px;
        box-shadow: 0 20px 60px rgba(15,23,42,.13);
    }
    .welcome {
        text-align: center;
        padding: 5px 0 16px;
    }
    .welcome h1 {
        color: #0f172a;
        font-size: 29px;
        margin-bottom: 5px;
    }
    .welcome p {
        color: #64748b;
        margin-top: 0;
    }
    .small-footer {
        text-align:center;
        color:#94a3b8;
        font-size:12px;
        padding-top:16px;
    }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 12px;
        border-radius: 15px;
    }
    .stButton > button {
        border-radius: 12px;
        font-weight: 650;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------- Données -------------------------
def load_data():
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=[
            "Date", "Ordre_Fabrication", "Produit", "Machine", "Ligne",
            "Operateur", "Equipe", "Quantite_Prevue", "Quantite_Produite",
            "Quantite_Defectueuse", "Taux_Defaut_%", "Statut"
        ])
    data = pd.read_csv(DATA_FILE, sep=";")
    return clean_data(data)


def clean_data(data):
    data = data.copy()

    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    numeric_cols = [
        "Quantite_Prevue", "Quantite_Produite",
        "Quantite_Defectueuse", "Taux_Defaut_%"
    ]
    for col in numeric_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    for col in ["Quantite_Prevue", "Quantite_Produite", "Quantite_Defectueuse"]:
        if col in data.columns:
            data[col] = data[col].fillna(0).clip(lower=0)

    if {"Quantite_Defectueuse", "Quantite_Produite"}.issubset(data.columns):
        denom = data["Quantite_Produite"].replace(0, pd.NA)
        data["Taux_Defaut_%"] = (
            data["Quantite_Defectueuse"] / denom * 100
        ).fillna(0).round(2)

    data = data.drop_duplicates().reset_index(drop=True)
    return data


def save_data(data):
    out = data.copy()
    if "Date" in out.columns:
        out["Date"] = pd.to_datetime(out["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
    out.to_csv(DATA_FILE, sep=";", index=False, encoding="utf-8-sig")


def icon_data(name):
    svg_file = Path(__file__).with_name(f"icon_{name}.svg")
    if svg_file.exists():
        return "data:image/svg+xml;base64," + base64.b64encode(
            svg_file.read_bytes()
        ).decode("ascii")
    return ""

def metric_card(label, value, note="", icon="production"):
    src = icon_data(icon)
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-icon">
                    <img src="{src}" alt="">
                </div>
                <div class="metric-label">{label}</div>
            </div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpis(data):
    production = data["Quantite_Produite"].sum()
    planned = data["Quantite_Prevue"].sum()
    defects = data["Quantite_Defectueuse"].sum()

    realization = (production / planned * 100) if planned else 0
    defect_rate = (defects / production * 100) if production else 0
    orders = data["Ordre_Fabrication"].nunique() if "Ordre_Fabrication" in data else 0

    return production, planned, defects, realization, defect_rate, orders


# ----------------------------- Login -------------------------
def login_screen():
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    st.markdown(logo_html(155), unsafe_allow_html=True)
    st.markdown(
        """
        <div class="welcome">
            <h1>Bienvenue chez NOVAFLUX</h1>
            <p>Votre espace de pilotage industriel et logistique</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        username = st.text_input("Identifiant", placeholder="Votre identifiant")
        password = st.text_input("Mot de passe", type="password", placeholder="Votre mot de passe")
        submit = st.form_submit_button("Se connecter", use_container_width=True)

    if submit:
        if username in USERS and USERS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Identifiant ou mot de passe incorrect.")

    st.markdown(
        '<div class="small-footer">Accès sécurisé • NOVAFLUX Industrie</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_screen()
    st.stop()


# --------------------------- Application ---------------------
df = load_data()

with st.sidebar:
    st.markdown(logo_html(95), unsafe_allow_html=True)
    st.markdown("---")
    st.caption(f"Connecté : {st.session_state.get('username', '')}")

    st.markdown(
        '<div style="font-size:12px;font-weight:700;letter-spacing:.08em;color:#94a3b8;margin-bottom:6px;">NAVIGATION</div>',
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Navigation",
        ["Dashboard", "Analyse", "Performance", "Saisie des données", "Nettoyage", "Données"],
        index=0,
    )

    st.markdown("---")
    if st.button("Se déconnecter", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()


# ----------------------------- Filtres -----------------------
st.sidebar.markdown(
        f'<div style="display:flex;align-items:center;gap:9px;margin:8px 0 10px;">'
        f'<img src="{icon_data("filter")}" style="width:24px;height:24px;">'
        f'<span style="font-size:18px;font-weight:700;">Filtres</span></div>',
        unsafe_allow_html=True,
    )

filter_df = df.copy()

if not df.empty:
    machines = sorted(df["Machine"].dropna().astype(str).unique())
    lignes = sorted(df["Ligne"].dropna().astype(str).unique())
    produits = sorted(df["Produit"].dropna().astype(str).unique())
    statuts = sorted(df["Statut"].dropna().astype(str).unique())

    selected_machines = st.sidebar.multiselect("Machine", machines)
    selected_lignes = st.sidebar.multiselect("Ligne", lignes)
    selected_produits = st.sidebar.multiselect("Produit", produits)
    selected_statuts = st.sidebar.multiselect("Statut", statuts)

    if selected_machines:
        filter_df = filter_df[filter_df["Machine"].isin(selected_machines)]
    if selected_lignes:
        filter_df = filter_df[filter_df["Ligne"].isin(selected_lignes)]
    if selected_produits:
        filter_df = filter_df[filter_df["Produit"].isin(selected_produits)]
    if selected_statuts:
        filter_df = filter_df[filter_df["Statut"].isin(selected_statuts)]

    dates = pd.to_datetime(df["Date"], errors="coerce").dropna()
    if not dates.empty:
        date_min, date_max = dates.min().date(), dates.max().date()
        date_range = st.sidebar.date_input(
            "Période",
            value=(date_min, date_max),
            min_value=date_min,
            max_value=date_max,
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start, end = date_range
            filter_df = filter_df[
                (filter_df["Date"].dt.date >= start)
                & (filter_df["Date"].dt.date <= end)
            ]

if filter_df.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")


# ---------------------------- Header -------------------------
st.markdown(
    f"""
    <div class="hero">
        <h1>{APP_NAME} — {page}</h1>
        <p>Suivi de fabrication, qualité et performance logistique • Interface de pilotage en français</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------- Dashboard -----------------------
if page == "Dashboard":
    production, planned, defects, realization, defect_rate, orders = kpis(filter_df)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Production", f"{production:,.0f}", "unités produites", "production")
    with c2:
        metric_card("Prévision", f"{planned:,.0f}", "unités planifiées", "target")
    with c3:
        metric_card("Réalisation", f"{realization:.1f} %", "production / prévision", "trend")
    with c4:
        metric_card("Taux de défaut", f"{defect_rate:.2f} %", "défectueux / produit", "quality")
    with c5:
        metric_card("Ordres", f"{orders:,}", "ordres de fabrication", "orders")

    st.markdown("### Vue opérationnelle")

    if not filter_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="section-card"><b>Production par machine</b></div>', unsafe_allow_html=True)
            machine_prod = filter_df.groupby("Machine")["Quantite_Produite"].sum().sort_values()
            fig, ax = plt.subplots(figsize=(8, 4.5))
            machine_prod.plot(kind="barh", ax=ax)
            ax.set_xlabel("Quantité produite")
            ax.set_ylabel("")
            ax.set_title("Production cumulée par machine")
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)

        with col2:
            st.markdown('<div class="section-card"><b>Production par ligne</b></div>', unsafe_allow_html=True)
            line_prod = filter_df.groupby("Ligne")["Quantite_Produite"].sum().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 4.5))
            sns.barplot(x=line_prod.values, y=line_prod.index, ax=ax)
            ax.set_xlabel("Quantité produite")
            ax.set_ylabel("")
            ax.set_title("Production cumulée par ligne")
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)

        daily = filter_df.groupby("Date", as_index=False)["Quantite_Produite"].sum()
        if not daily.empty:
            fig, ax = plt.subplots(figsize=(12, 4.5))
            ax.plot(daily["Date"], daily["Quantite_Produite"], marker="o")
            ax.set_title("Évolution de la production")
            ax.set_xlabel("Date")
            ax.set_ylabel("Quantité produite")
            plt.xticks(rotation=35)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)


# ----------------------------- Analyse ------------------------
elif page == "Analyse":
    st.subheader("Analyse des données")
    if not filter_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            summary = filter_df.groupby("Produit").agg(
                Production=("Quantite_Produite", "sum"),
                Defauts=("Quantite_Defectueuse", "sum"),
            ).sort_values("Production", ascending=False)
            summary["Taux_defaut_%"] = (
                summary["Defauts"] / summary["Production"].replace(0, pd.NA) * 100
            ).fillna(0).round(2)
            st.dataframe(summary, use_container_width=True)

        with col2:
            defect_machine = filter_df.groupby("Machine")["Quantite_Defectueuse"].sum().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 4.5))
            sns.barplot(x=defect_machine.values, y=defect_machine.index, ax=ax)
            ax.set_title("Défauts par machine")
            ax.set_xlabel("Quantité défectueuse")
            ax.set_ylabel("")
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)

        st.download_button(
            "Télécharger les données filtrées",
            filter_df.to_csv(index=False, sep=";").encode("utf-8-sig"),
            "donnees_filtrees.csv",
            "text/csv",
        )


# -------------------------- Performance ----------------------
elif page == "Performance":
    st.subheader("Performance industrielle")
    if not filter_df.empty:
        perf = filter_df.groupby("Machine").agg(
            Prevue=("Quantite_Prevue", "sum"),
            Produite=("Quantite_Produite", "sum"),
            Defauts=("Quantite_Defectueuse", "sum"),
        )
        perf["Taux_Realisation_%"] = (perf["Produite"] / perf["Prevue"].replace(0, pd.NA) * 100).fillna(0)
        perf["Taux_Defaut_%"] = (perf["Defauts"] / perf["Produite"].replace(0, pd.NA) * 100).fillna(0)
        perf = perf.round(2)

        st.dataframe(perf.sort_values("Taux_Realisation_%", ascending=False), use_container_width=True)

        fig, ax = plt.subplots(figsize=(11, 4.8))
        sns.barplot(
            data=perf.reset_index(),
            x="Machine",
            y="Taux_Realisation_%",
            ax=ax
        )
        ax.axhline(100, linestyle="--", linewidth=1.5)
        ax.set_ylim(bottom=0)
        ax.set_title("Taux de réalisation par machine")
        ax.set_xlabel("")
        ax.set_ylabel("Taux de réalisation (%)")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)


# ------------------------ Saisie de données ------------------
elif page == "Saisie des données":
    st.subheader("Ajouter un nouvel enregistrement")
    st.info("Après validation, le fichier dataset.csv est mis à jour et les KPI/graphiques sont recalculés automatiquement.")

    with st.form("add_data_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            new_date = st.date_input("Date", value=date.today())
            new_of = st.text_input("Ordre de fabrication", placeholder="OF016")
            new_product = st.text_input("Produit", placeholder="Produit A")
            new_machine = st.text_input("Machine", placeholder="Machine CNC")
        with c2:
            new_line = st.text_input("Ligne", placeholder="Ligne A")
            new_operator = st.text_input("Opérateur", placeholder="Nom")
            new_team = st.text_input("Équipe", placeholder="Équipe matin")
            new_status = st.selectbox("Statut", ["Terminé", "En cours", "En attente", "Annulé"])
        with c3:
            new_planned = st.number_input("Quantité prévue", min_value=0, step=1)
            new_produced = st.number_input("Quantité produite", min_value=0, step=1)
            new_defects = st.number_input("Quantité défectueuse", min_value=0, step=1)

        submitted = st.form_submit_button("Ajouter les données", use_container_width=True)

    if submitted:
        if not new_of or not new_product or not new_machine or not new_line:
            st.error("Veuillez renseigner au minimum l'OF, le produit, la machine et la ligne.")
        else:
            new_rate = (new_defects / new_produced * 100) if new_produced else 0
            new_row = pd.DataFrame([{
                "Date": pd.to_datetime(new_date),
                "Ordre_Fabrication": new_of,
                "Produit": new_product,
                "Machine": new_machine,
                "Ligne": new_line,
                "Operateur": new_operator,
                "Equipe": new_team,
                "Quantite_Prevue": new_planned,
                "Quantite_Produite": new_produced,
                "Quantite_Defectueuse": new_defects,
                "Taux_Defaut_%": round(new_rate, 2),
                "Statut": new_status,
            }])
            updated = pd.concat([df, new_row], ignore_index=True)
            updated = clean_data(updated)
            save_data(updated)
            st.success("Enregistrement ajouté. Les données, KPI et graphiques ont été actualisés.")
            st.rerun()


# ---------------------------- Nettoyage ----------------------
elif page == "Nettoyage":
    st.subheader("Nettoyage et contrôle qualité des données")
    before = len(df)
    missing_before = int(df.isna().sum().sum())
    duplicates_before = int(df.duplicated().sum())

    cleaned = clean_data(df)
    missing_after = int(cleaned.isna().sum().sum())
    duplicates_after = int(cleaned.duplicated().sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Lignes initiales", before)
    c2.metric("Cellules manquantes initiales", missing_before)
    c3.metric("Doublons initiaux", duplicates_before)

    st.markdown("### Résultat du contrôle")
    st.write({
        "Lignes après nettoyage": len(cleaned),
        "Cellules manquantes après nettoyage": missing_after,
        "Doublons après nettoyage": duplicates_after,
    })

    if st.button("Enregistrer la version nettoyée", type="primary"):
        save_data(cleaned)
        st.success("Version nettoyée enregistrée dans dataset.csv.")
        st.rerun()

    st.dataframe(cleaned, use_container_width=True)


# ----------------------------- Données -----------------------
elif page == "Données":
    st.subheader("Base de données")
    st.dataframe(filter_df, use_container_width=True, height=560)

    st.download_button(
        "Exporter la vue actuelle en CSV",
        filter_df.to_csv(index=False, sep=";").encode("utf-8-sig"),
        "novaflux_export.csv",
        "text/csv",
    )
