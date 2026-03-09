import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ─────────────────────────────────────────────
#  CONFIGURAÇÃO GERAL
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Carteira e Custo",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  TEMA: escuro / claro
# ─────────────────────────────────────────────
if "tema" not in st.session_state:
    st.session_state.tema = "escuro"

TEMAS = {
    "escuro": {
        "bg":          "#0f1117",
        "sidebar_bg":  "#161b27",
        "sidebar_bdr": "#1e2535",
        "card_bg":     "linear-gradient(135deg,#1a2035 0%,#1e2840 100%)",
        "card_bdr":    "#2a3650",
        "tabs_bg":     "#161b27",
        "tab_sel_bg":  "#1e2840",
        "text":        "#e8eaf0",
        "text_label":  "#7c8db5",
        "text_sub":    "#4a6fa5",
        "text_val":    "#f0f4ff",
        "tab_color":   "#7c8db5",
        "tab_sel":     "#60a5fa",
        "pt_font":     "#9ab0d0",
        "pt_grid":     "#1e2535",
        "pt_line":     "#2a3650",
        "pt_text_out": "#9ab0d0",
        "scroll_track":"#0f1117",
        "scroll_thumb":"#2a3650",
        "sec_bdr":     "#1e2535",
    },
    "claro": {
        "bg":          "#f5f6fa",
        "sidebar_bg":  "#ffffff",
        "sidebar_bdr": "#e2e8f0",
        "card_bg":     "linear-gradient(135deg,#ffffff 0%,#f0f4ff 100%)",
        "card_bdr":    "#dde3f0",
        "tabs_bg":     "#eef1f8",
        "tab_sel_bg":  "#ffffff",
        "text":        "#1e2a3a",
        "text_label":  "#64748b",
        "text_sub":    "#94a3b8",
        "text_val":    "#0f172a",
        "tab_color":   "#64748b",
        "tab_sel":     "#2563eb",
        "pt_font":     "#475569",
        "pt_grid":     "#e2e8f0",
        "pt_line":     "#cbd5e1",
        "pt_text_out": "#475569",
        "scroll_track":"#f1f5f9",
        "scroll_thumb":"#cbd5e1",
        "sec_bdr":     "#e2e8f0",
    },
}

T = TEMAS[st.session_state.tema]

def aplicar_tema():
    T = TEMAS[st.session_state.tema]
    st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
  html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
  .stApp {{ background: {T['bg']}; color: {T['text']}; }}
  [data-testid="stSidebar"] {{ background: {T['sidebar_bg']}; border-right: 1px solid {T['sidebar_bdr']}; }}

  .kpi-card {{
    background: {T['card_bg']};
    border: 1px solid {T['card_bdr']}; border-radius: 12px;
    padding: 18px 22px; position: relative; overflow: hidden; height: 110px;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
  }}
  .kpi-card::before {{ content:''; position:absolute; top:0; left:0; right:0; height:3px; }}
  .kpi-card.azul::before    {{ background: linear-gradient(90deg,#3b82f6,#60a5fa); }}
  .kpi-card.verde::before   {{ background: linear-gradient(90deg,#10b981,#34d399); }}
  .kpi-card.laranja::before {{ background: linear-gradient(90deg,#f59e0b,#fbbf24); }}
  .kpi-card.vermelho::before{{ background: linear-gradient(90deg,#ef4444,#f87171); }}
  .kpi-card.roxo::before    {{ background: linear-gradient(90deg,#8b5cf6,#a78bfa); }}

  .kpi-label {{ font-size:11px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:{T['text_label']}; margin-bottom:6px; }}
  .kpi-value {{ font-size:28px; font-weight:700; color:{T['text_val']}; line-height:1.1; font-family:'DM Mono',monospace; }}
  .kpi-sub   {{ font-size:11px; color:{T['text_sub']}; margin-top:4px; }}

  .section-title {{ font-size:12px; font-weight:600; letter-spacing:.1em; text-transform:uppercase;
    color:{T['text_label']}; padding-bottom:8px; border-bottom:1px solid {T['sec_bdr']}; margin-bottom:14px; }}

  .stTabs [data-baseweb="tab-list"] {{ background:{T['tabs_bg']}; border-radius:8px; padding:4px; gap:4px; }}
  .stTabs [data-baseweb="tab"] {{ border-radius:6px; color:{T['tab_color']}; font-weight:500; }}
  .stTabs [aria-selected="true"] {{ background:{T['tab_sel_bg']} !important; color:{T['tab_sel']} !important; }}

  ::-webkit-scrollbar {{ width:6px; }}
  ::-webkit-scrollbar-track {{ background:{T['scroll_track']}; }}
  ::-webkit-scrollbar-thumb {{ background:{T['scroll_thumb']}; border-radius:3px; }}
</style>
""", unsafe_allow_html=True)

aplicar_tema()
T = TEMAS[st.session_state.tema]

PT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=T["pt_font"], size=12),
    xaxis=dict(gridcolor=T["pt_grid"], linecolor=T["pt_line"]),
    yaxis=dict(gridcolor=T["pt_grid"], linecolor=T["pt_line"]),
    margin=dict(l=16, r=16, t=40, b=16),
)

def kpi(label, value, sub="", cor="azul"):
    st.markdown(f"""<div class="kpi-card {cor}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def sec(txt):
    st.markdown(f'<div class="section-title">{txt}</div>', unsafe_allow_html=True)

def fmt_n(v): return f"{int(v):,}".replace(",",".")
def fmt_m(v): return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@st.cache_data(show_spinner="Carregando dados...")
def carregar(raw_bytes, nome):
    if nome.endswith(".csv"):
        df = pd.read_csv(raw_bytes)
    else:
        df = pd.read_excel(raw_bytes)
    df["Data"] = pd.to_datetime(df["Data"]).dt.normalize()
    return df

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    col_title, col_toggle = st.columns([3, 1]) #Dashboard 2.0
    with col_title:
        st.markdown(f"""<div style='padding:8px 0 20px'>
          <div style='font-size:20px;font-weight:700;color:{T["text_val"]}'> CARTEIRA E CUSTO ASSISTENCIAL</div> 
          <div style='font-size:11px;color:{T["text_sub"]};margin-top:4px'>Dashboard 2.0</div>
        </div>""", unsafe_allow_html=True)
    with col_toggle:
        eh_escuro = st.session_state.tema == "escuro"
        label_btn = "☀️" if eh_escuro else "🌙"
        if st.button(label_btn, help="Alternar tema claro/escuro", use_container_width=True):
            st.session_state.tema = "claro" if eh_escuro else "escuro"
            st.rerun()

    sec("Fonte de Dados")
    arquivo = st.file_uploader("Carregar Base_Teste_Carteira_Custo.xlsx", type=["xlsx","xls","csv"])

    if arquivo is None:
        st.info("⬆️ Faça upload do arquivo de base para começar.")
        st.stop()

    df_raw = carregar(arquivo.read(), arquivo.name)
    st.success(f"✓ {fmt_n(len(df_raw))} registros")

    sec("Filtros Principais")
    datas = df_raw["Data"].dt.date
    c1, c2 = st.columns(2)
    with c1: d_ini = st.date_input("De",  value=datas.min())
    with c2: d_fim = st.date_input("Até", value=datas.max())

    estados_sel = st.multiselect("Estado", sorted(df_raw["Estado"].dropna().unique()), placeholder="Todos")
    planos_sel  = st.multiselect("Plano", sorted(df_raw["Plano"].dropna().unique()), placeholder="Todos")
    
    with st.expander("Filtros de Detalhamento"):
        cidades_sel = st.multiselect("Cidade", sorted(df_raw["Cidade"].dropna().unique()), placeholder="Todas")
        bairros_sel = st.multiselect("Bairro", sorted(df_raw["Bairro"].dropna().unique()), placeholder="Todos")
        sexo_sel    = st.multiselect("Sexo", ["M", "F"], placeholder="Ambos")

    mask = (df_raw["Data"].dt.date >= d_ini) & (df_raw["Data"].dt.date <= d_fim)
    if estados_sel: mask &= df_raw["Estado"].isin(estados_sel)
    if planos_sel:  mask &= df_raw["Plano"].isin(planos_sel)
    if cidades_sel: mask &= df_raw["Cidade"].isin(cidades_sel)
    if bairros_sel: mask &= df_raw["Bairro"].isin(bairros_sel)
    if sexo_sel:    mask &= df_raw["Sexo"].isin(sexo_sel)
    df = df_raw[mask].copy()

# ─────────────────────────────────────────────
#  LAYOUT PRINCIPAL
# ─────────────────────────────────────────────
tabs = st.tabs(["📊 Visão Geral", "👥 Carteira", "💰 Custo Assistencial", "🔍 Investigação"])

# --- TAB 1: VISÃO GERAL ---
with tabs[0]:
    sec("Indicadores Principais")
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi("Total Beneficiários", fmt_n(len(df)), "base filtrada", "azul")
    with k2: kpi("Custo Total", fmt_m(df["Custo_Assistencial"].sum()), "no período", "vermelho")
    with k3: kpi("Custo Médio/Benef.", fmt_m(df["Custo_Assistencial"].mean()), "média simples", "laranja")
    with k4: kpi("Idade Média", f"{df['Idade'].mean():.1f} anos", "perfil demográfico", "roxo")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        ev_custo = df.groupby("Data")["Custo_Assistencial"].sum().reset_index()
        fig_ev = px.line(ev_custo, x="Data", y="Custo_Assistencial", title="Evolução do Custo Assistencial")
        fig_ev.update_layout(**PT)
        st.plotly_chart(fig_ev, use_container_width=True)
    with c2:
        dist_plano = df["Plano"].value_counts().reset_index()
        fig_plano = px.pie(dist_plano, names="Plano", values="count", title="Distribuição por Plano", hole=0.4)
        fig_plano.update_layout(**PT)
        st.plotly_chart(fig_plano, use_container_width=True)

# --- TAB 2: CARTEIRA ---
with tabs[1]:
    sec("Análise Demográfica")
    c1, c2 = st.columns([1, 1])
    with c1:
        # Pirâmide Etária
        df_m = df[df["Sexo"] == "M"].copy()
        df_f = df[df["Sexo"] == "F"].copy()
        bins = [0, 18, 23, 28, 33, 38, 43, 48, 53, 58, 100]
        labels = ["0-18", "19-23", "24-28", "29-33", "34-38", "39-43", "44-48", "49-53", "54-58", "59+"]
        df_m["Faixa"] = pd.cut(df_m["Idade"], bins=bins, labels=labels)
        df_f["Faixa"] = pd.cut(df_f["Idade"], bins=bins, labels=labels)
        
        m_counts = df_m["Faixa"].value_counts().sort_index()
        f_counts = df_f["Faixa"].value_counts().sort_index()
        
        fig_pir = go.Figure()
        fig_pir.add_trace(go.Bar(y=labels, x=m_counts.values, name="Masc", orientation='h', marker_color='#3b82f6'))
        fig_pir.add_trace(go.Bar(y=labels, x=-f_counts.values, name="Fem", orientation='h', marker_color='#ef4444'))
        fig_pir.update_layout(title="Pirâmide Etária", barmode='overlay', **PT)
        st.plotly_chart(fig_pir, use_container_width=True)
    
    with c2:
        # Drill-down Geográfico (Simulado com Treemap)
        fig_geo = px.treemap(df, path=['Estado', 'Cidade', 'Bairro'], values='Idade', title="Hierarquia Geográfica (Drill-down)")
        fig_geo.update_layout(**PT)
        st.plotly_chart(fig_geo, use_container_width=True)

# --- TAB 3: CUSTO ASSISTENCIAL ---
with tabs[2]:
    sec("Análise de Custos e Prestadores")
    c1, c2 = st.columns(2)
    with c1:
        # Curva ABC de Materiais
        abc = df.groupby("Material_Medicamento")["Custo_Assistencial"].sum().sort_values(ascending=False).reset_index()
        abc["% Acumulada"] = abc["Custo_Assistencial"].cumsum() / abc["Custo_Assistencial"].sum() * 100
        abc["Categoria"] = abc["% Acumulada"].apply(lambda x: "A" if x <= 80 else ("B" if x <= 95 else "C"))
        
        fig_abc = px.bar(abc.head(15), x="Material_Medicamento", y="Custo_Assistencial", color="Categoria", 
                         title="Curva ABC: Top 15 Materiais/Medicamentos", color_discrete_map={"A":"#ef4444", "B":"#f59e0b", "C":"#10b981"})
        fig_abc.update_layout(**PT)
        st.plotly_chart(fig_abc, use_container_width=True)
        
    with c2:
        # Custo por Procedimento
        proc = df.groupby("Procedimento")["Custo_Assistencial"].sum().sort_values().reset_index()
        fig_proc = px.bar(proc, y="Procedimento", x="Custo_Assistencial", orientation='h', title="Custo por Tipo de Procedimento")
        fig_proc.update_layout(**PT)
        st.plotly_chart(fig_proc, use_container_width=True)

# --- TAB 4: INVESTIGAÇÃO ---
with tabs[3]:
    sec("Investigação de Casos e Status")
    
    # Lógica de Status (Simulada para o exemplo)
    df_inv = df.copy()
    # Definir um "Risco" baseado no custo e idade
    df_inv["Score_Risco"] = (df_inv["Custo_Assistencial"] / df_inv["Custo_Assistencial"].max() * 70) + (df_inv["Idade"] / 100 * 30)
    
    def get_status(score):
        if score > 60: return "🔴 Crítico"
        if score > 40: return "🟡 Atenção"
        return "🟢 Normal"
    
    df_inv["Status"] = df_inv["Score_Risco"].apply(get_status)
    
    # Filtros de Investigação
    fi1, fi2, fi3 = st.columns(3)
    with fi1: status_f = st.selectbox("Filtrar Status", ["Todos", "🔴 Crítico", "🟡 Atenção", "🟢 Normal"])
    with fi2: prestador_f = st.selectbox("Filtrar Prestador", ["Todos"] + sorted(df["Prestador"].unique().tolist()))
    with fi3: busca = st.text_input("Busca por ID Beneficiário")
    
    if status_f != "Todos": df_inv = df_inv[df_inv["Status"] == status_f]
    if prestador_f != "Todos": df_inv = df_inv[df_inv["Prestador"] == prestador_f]
    if busca: df_inv = df_inv[df_inv["Beneficiário_ID"].str.contains(busca, case=False)]
    
    cols_show = ["Status", "Beneficiário_ID", "Idade", "Sexo", "Plano", "Prestador", "Procedimento", "Custo_Assistencial"]
    st.dataframe(df_inv[cols_show].sort_values("Custo_Assistencial", ascending=False), 
                 use_container_width=True, hide_index=True,
                 column_config={
                     "Custo_Assistencial": st.column_config.NumberColumn("Custo", format="R$ %.2f"),
                     "Status": st.column_config.TextColumn("Status", width="small")
                 })
    
    st.markdown("<br>", unsafe_allow_html=True)
    sec("Detalhes do Beneficiário")
    ben_sel = st.selectbox("Selecionar Beneficiário para Detalhes", ["—"] + df_inv["Beneficiário_ID"].tolist())
    
    if ben_sel != "—":
        detalhe = df_inv[df_inv["Beneficiário_ID"] == ben_sel].iloc[0]
        d1, d2 = st.columns([1, 2])
        with d1:
            st.markdown(f"""
            **ID:** {detalhe['Beneficiário_ID']}  
            **Idade:** {detalhe['Idade']} anos  
            **Sexo:** {detalhe['Sexo']}  
            **Plano:** {detalhe['Plano']}  
            **Local:** {detalhe['Bairro']}, {detalhe['Cidade']} - {detalhe['Estado']}
            """)
        with d2:
            st.markdown(f"**Análise de Risco:** {detalhe['Status']}")
            if detalhe['Status'] == "🔴 Crítico":
                st.error(f"Este beneficiário apresenta um custo assistencial elevado ({fmt_m(detalhe['Custo_Assistencial'])}) associado ao perfil etário. Recomenda-se auditoria no prestador {detalhe['Prestador']}.")
            elif detalhe['Status'] == "🟡 Atenção":
                st.warning(f"Beneficiário com utilização acima da média. Monitorar recorrência de {detalhe['Procedimento']}.")
            else:
                st.success("Utilização dentro dos parâmetros esperados para o perfil.")
