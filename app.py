"""
Dashboard IRC · Análise de Atendimento
Adaptado para Base_de_Dados.xlsx
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─────────────────────────────────────────────
#  CONFIGURAÇÃO GERAL
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard IRC · Atendimento",
    page_icon="📊",
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
        # backgrounds
        "bg":          "#0f1117",
        "sidebar_bg":  "#161b27",
        "sidebar_bdr": "#1e2535",
        "card_bg":     "linear-gradient(135deg,#1a2035 0%,#1e2840 100%)",
        "card_bdr":    "#2a3650",
        "tabs_bg":     "#161b27",
        "tab_sel_bg":  "#1e2840",
        # texto
        "text":        "#e8eaf0",
        "text_label":  "#7c8db5",
        "text_sub":    "#4a6fa5",
        "text_val":    "#f0f4ff",
        "tab_color":   "#7c8db5",
        "tab_sel":     "#60a5fa",
        # plotly
        "pt_font":     "#9ab0d0",
        "pt_grid":     "#1e2535",
        "pt_line":     "#2a3650",
        "pt_text_out": "#9ab0d0",
        # gauge
        "gauge_bg":    "#1a2035",
        "gauge_step":  ["#0d2b1d","#1a2d3d","#3b2a0a","#3b1414"],
        "gauge_num":   "#f0f4ff",
        # scrollbar
        "scroll_track":"#0f1117",
        "scroll_thumb":"#2a3650",
        # seção title border
        "sec_bdr":     "#1e2535",
        # scatter marker border
        "dot_bdr":     "#0f1117",
        # quadrant lines
        "quad_line":   "rgba(255, 255, 255, 0.5)",
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
        "gauge_bg":    "#f1f5f9",
        "gauge_step":  ["#d1fae5","#dbeafe","#fef3c7","#fee2e2"],
        "gauge_num":   "#0f172a",
        "scroll_track":"#f1f5f9",
        "scroll_thumb":"#cbd5e1",
        "sec_bdr":     "#e2e8f0",
        "dot_bdr":     "#f5f6fa",
        "quad_line":   "#d511be",
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
  .kpi-card.ciano::before   {{ background: linear-gradient(90deg,#06b6d4,#67e8f9); }}

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

  /* Ajustes modo claro para widgets nativos */
  {'[data-testid="stMetric"] { background: white; border-radius:8px; padding:8px; }' if st.session_state.tema == "claro" else ''}
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
COR_RISCO = {"Low":"#10b981","Medium":"#3b82f6","High":"#f59e0b","Critical":"#ef4444"}
COR_SENT  = {"Positive":"#10b981","Neutral":"#3b82f6","Negative":"#ef4444"}

def kpi(label, value, sub="", cor="azul"):
    st.markdown(f"""<div class="kpi-card {cor}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def sec(txt):
    st.markdown(f'<div class="section-title">{txt}</div>', unsafe_allow_html=True)

def pct(v): return f"{v:.1%}"
def fmt_n(v): return f"{int(v):,}".replace(",",".")

@st.cache_data(show_spinner="Carregando dados...")
def carregar(raw_bytes, nome):
    if nome.endswith(".csv"):
        df = pd.read_csv(raw_bytes, parse_dates=["dt_criacao"])
    else:
        df = pd.read_excel(raw_bytes, parse_dates=["dt_criacao"])

    if "ds_nivel_conformidade" in df.columns:
        df["ds_nivel_conformidade"] = df["ds_nivel_conformidade"].str.strip().replace({"Nao Conforme":"Não Conforme"})

    df["resolvido"] = df["ds_status_resolucao"] == "resolved"
    df["conforme"]  = df["ds_nivel_conformidade"] == "Conforme com Oportunidades"

    def simplifica(s):
        if pd.isna(s): return "Neutro"
        mapa = {
            "Frustrated":"Negativo","Angry":"Negativo","Disappointed":"Negativo",
            "Confused":"Neutro","Indifferent":"Neutro","Curious":"Neutro",
            "Satisfied":"Positivo","Grateful":"Positivo","Interested":"Positivo","Positive":"Positivo",
        }
        return mapa.get(str(s).split(",")[0].strip(), "Neutro")

    df["sent_ini_s"] = df["ds_sentimento_cliente_inicial"].apply(simplifica)
    df["sent_fim_s"] = df["ds_sentimento_cliente_final"].apply(simplifica)
    df["tema_p"]     = df["ds_tema"].fillna("Não informado").str.split(",").str[0].str.strip()
    df["dt_criacao"] = pd.to_datetime(df["dt_criacao"]).dt.normalize()
    return df

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # ── Header + toggle de tema ──
    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        st.markdown(f"""<div style='padding:8px 0 20px'>
          <div style='font-size:20px;font-weight:700;color:{T["text_val"]}'>📊 IRC Dashboard</div>
          <div style='font-size:11px;color:{T["text_sub"]};margin-top:4px'>ANÁLISE DE ATENDIMENTO · RN623</div>
        </div>""", unsafe_allow_html=True)
    with col_toggle:
        st.markdown("<div style='padding-top:12px'>", unsafe_allow_html=True)
        eh_escuro = st.session_state.tema == "escuro"
        label_btn = "☀️" if eh_escuro else "🌙"
        if st.button(label_btn, help="Alternar tema claro/escuro", use_container_width=True):
            st.session_state.tema = "claro" if eh_escuro else "escuro"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    sec("Fonte de Dados")
    arquivo = st.file_uploader("Carregar Base_de_Dados.xlsx", type=["xlsx","xls","csv"])

    if arquivo is None:
        st.info("⬆️ Faça upload do arquivo **Base_de_Dados.xlsx** para começar.")
        st.stop()

    df_raw = carregar(arquivo.read(), arquivo.name)
    st.success(f"✓ {fmt_n(len(df_raw))} atendimentos")

    st.markdown("<br>", unsafe_allow_html=True)
    sec("Filtros")

    datas = df_raw["dt_criacao"].dt.date
    c1, c2 = st.columns(2)
    with c1: d_ini = st.date_input("De",  value=datas.min(), min_value=datas.min(), max_value=datas.max())
    with c2: d_fim = st.date_input("Até", value=datas.max(), min_value=datas.min(), max_value=datas.max())

    agentes_sel = st.multiselect("Agente",  sorted(df_raw["nm_agente"].dropna().unique()), placeholder="Todos")
    grupos_sel  = st.multiselect("Grupo",   sorted(df_raw["ds_grupo"].dropna().unique()),   placeholder="Todos")
    riscos_sel  = st.multiselect("Risco IRC", ["Low","Medium","High","Critical"],            placeholder="Todos")

    mask = (df_raw["dt_criacao"].dt.date >= d_ini) & (df_raw["dt_criacao"].dt.date <= d_fim)
    if agentes_sel: mask &= df_raw["nm_agente"].isin(agentes_sel)
    if grupos_sel:  mask &= df_raw["ds_grupo"].isin(grupos_sel)
    if riscos_sel:  mask &= df_raw["ds_irc_classificacao"].isin(riscos_sel)
    df = df_raw[mask].copy()

    st.markdown(f'<div style="font-size:11px;color:#4a6fa5;margin-top:8px">{fmt_n(len(df))} registros no período</div>', unsafe_allow_html=True)
    csv_bytes = df.drop(columns=["ds_dialogo","ds_dialogo_resumo"], errors="ignore").to_csv(index=False).encode()
    st.download_button("⬇ Exportar CSV filtrado", csv_bytes, "irc_filtrado.csv", "text/csv")

if len(df) == 0:
    st.warning("Nenhum dado para o filtro selecionado.")
    st.stop()

# KPIs globais
total        = len(df)
taxa_res     = df["resolvido"].mean()
taxa_risco   = df["ds_irc_classificacao"].isin(["High","Critical"]).mean()
irc_medio    = df["vl_irc_score"].mean()
conf_rn623   = df["conforme"].mean()
neg_ini      = df[df["sent_ini_s"]=="Negativo"]
reversao     = neg_ini["sent_fim_s"].isin(["Positivo","Neutro"]).mean() if len(neg_ini) else 0
ordem_s      = {"Positivo":2,"Neutro":1,"Negativo":0}
escalada     = df.apply(lambda r: ordem_s.get(r["sent_fim_s"],1)<ordem_s.get(r["sent_ini_s"],1), axis=1).mean()

# ─────────────────────────────────────────────
#  ABAS
# ─────────────────────────────────────────────
tabs = st.tabs(["🏠 Visão Geral","😊 Experiência","⚠️ Risco","🛡️ RN623","🔍 Investigação"])

# ══ PÁG 1 ═══════════════════════════════════
with tabs[0]:
    sec("Indicadores-chave")
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    with k1: kpi("Volume Total",        fmt_n(total),         f"{d_ini} → {d_fim}",             "azul")
    with k2: kpi("Taxa Resolução",      pct(taxa_res),        f"{fmt_n(df['resolvido'].sum())} resolvidos", "verde")
    with k3: kpi("Risco Alto/Crítico",  pct(taxa_risco),      f"{fmt_n(df['ds_irc_classificacao'].isin(['High','Critical']).sum())} atend.", "vermelho")
    with k4: kpi("IRC Médio",           f"{irc_medio:.1f}",   "escala 0–100",                   "laranja")
    with k5: kpi("Reversão Sentimento", pct(reversao),        "negativos que melhoraram",        "roxo")
    with k6: kpi("Conf. RN623",         pct(conf_rn623),      "atend. conformes",               "ciano")

    st.markdown("<br>", unsafe_allow_html=True)

    cg, cp = st.columns([1,2])
    with cg:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=irc_medio,
            number={"font":{"size":44,"color":T["gauge_num"],"family":"DM Mono"},"valueformat":".1f"},
            gauge=dict(
                axis=dict(range=[0,100], tickfont=dict(color=T["text_label"],size=10)),
                bar=dict(color="#3b82f6", thickness=0.25),
                bgcolor=T["gauge_bg"], borderwidth=0,
                steps=[dict(range=[0,30],color=T["gauge_step"][0]),dict(range=[30,60],color=T["gauge_step"][1]),
                       dict(range=[60,80],color=T["gauge_step"][2]),dict(range=[80,100],color=T["gauge_step"][3])],
                threshold=dict(line=dict(color="#ef4444",width=2),thickness=0.75,value=80),
            ),
            title={"text":"IRC Médio Geral","font":{"size":13,"color":T["text_label"]}},
        ))
        fig_g.update_layout(paper_bgcolor="rgba(0,0,0,0)",height=230,margin=dict(t=40,b=10,l=20,r=20))
        st.plotly_chart(fig_g, use_container_width=True)

    with cp:
        sec("Decomposição por Pilar IRC")
        pilares = {
            "Pilar 1 · Conteúdo":   df["vl_irc_score_pilar_1"].mean(),
            "Pilar 2 · Sentimento": df["vl_irc_score_pilar_2"].mean(),
            "Pilar 3 · Processo":   df["vl_irc_score_pilar_3"].mean(),
            "Pilar 4 · Gatilhos":   df["vl_irc_score_pilar_4"].mean(),
        }
        mx = max(pilares.values()) or 1
        fig_p = go.Figure(go.Bar(
            y=list(pilares.keys()), x=list(pilares.values()), orientation="h",
            marker=dict(color=list(pilares.values()),
                        colorscale=[[0,"#1e3a5f"],[0.5,"#3b82f6"],[1,"#ef4444"]],showscale=False),
            text=[f"{v:.2f}" for v in pilares.values()],
            textposition="outside", textfont=dict(color=T["pt_text_out"]),
        ))
        fig_p.update_layout(title="Score médio por Pilar",xaxis_range=[0,mx*1.35],height=220,**PT)
        st.plotly_chart(fig_p, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("Evolução Temporal")
    ec1, ec2 = st.columns(2)

    with ec1:
        di = df.groupby("dt_criacao")["vl_irc_score"].mean().reset_index().sort_values("dt_criacao")
        mu, sig = di["vl_irc_score"].mean(), di["vl_irc_score"].std()
        fc = go.Figure()
        fc.add_trace(go.Scatter(x=di["dt_criacao"],y=[mu+2*sig]*len(di),mode="lines",line=dict(color="#ef4444",dash="dot",width=1),name="LSC +2σ"))
        fc.add_trace(go.Scatter(x=di["dt_criacao"],y=[mu-2*sig]*len(di),mode="lines",line=dict(color="#3b82f6",dash="dot",width=1),fill="tonexty",fillcolor="rgba(59,130,246,0.06)",name="LIC -2σ"))
        fc.add_trace(go.Scatter(x=di["dt_criacao"],y=[mu]*len(di),mode="lines",line=dict(color="#7c8db5",dash="dash",width=1),name="Média"))
        fc.add_trace(go.Scatter(x=di["dt_criacao"],y=di["vl_irc_score"],mode="lines+markers",line=dict(color="#3b82f6",width=2.5),marker=dict(size=5,color="#60a5fa"),name="IRC Médio Diário"))
        fora = di[(di["vl_irc_score"]>mu+2*sig)|(di["vl_irc_score"]<mu-2*sig)]
        if len(fora): fc.add_trace(go.Scatter(x=fora["dt_criacao"],y=fora["vl_irc_score"],mode="markers",marker=dict(size=10,color="#ef4444",symbol="circle-open",line=dict(color="#ef4444",width=2)),name="Fora de controle"))
        fc.update_layout(title="Gráfico de Controle · IRC Médio Diário",legend=dict(orientation="h",y=-0.2,font=dict(size=10)),**PT)
        st.plotly_chart(fc, use_container_width=True)

    with ec2:
        dv = df.groupby("dt_criacao").size().reset_index(name="n").sort_values("dt_criacao")
        dv["ma7"] = dv["n"].rolling(7,min_periods=1).mean()
        fv = go.Figure()
        fv.add_trace(go.Bar(x=dv["dt_criacao"],y=dv["n"],name="Volume",marker_color="#1e3a5f",marker_line_color="#3b82f6",marker_line_width=0.5))
        fv.add_trace(go.Scatter(x=dv["dt_criacao"],y=dv["ma7"],mode="lines",name="Média 7d",line=dict(color="#f59e0b",width=2)))
        fv.update_layout(title="Volume de Atendimentos por Dia",legend=dict(orientation="h",y=-0.2,font=dict(size=10)),**PT)
        st.plotly_chart(fv, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("Distribuições")
    d1,d2,d3 = st.columns(3)

    with d1:
        cs = df["ds_sentimento_cliente_geral"].value_counts().reset_index()
        cs.columns=["s","n"]
        fig_s = go.Figure(go.Pie(labels=cs["s"],values=cs["n"],hole=0.6,
            marker_colors=[COR_SENT.get(s,"#7c8db5") for s in cs["s"]],
            textinfo="label+percent",textfont=dict(size=11)))
        fig_s.update_layout(title="Sentimento Geral",showlegend=False,**PT)
        st.plotly_chart(fig_s, use_container_width=True)

    with d2:
        orr = ["Low","Medium","High","Critical"]
        cr = df["ds_irc_classificacao"].value_counts().reindex(orr,fill_value=0).reset_index()
        cr.columns=["r","n"]
        fig_r = go.Figure(go.Bar(x=cr["r"],y=cr["n"],marker_color=[COR_RISCO[r] for r in cr["r"]],
            text=cr["n"],textposition="outside",textfont=dict(color=T["pt_text_out"])))
        fig_r.update_layout(title="Distribuição de Risco (IRC)",showlegend=False,**PT)
        st.plotly_chart(fig_r, use_container_width=True)

    with d3:
        orrs = ["resolved","pending","unresolved","callback","escalated"]
        lbls = {"resolved":"Resolvido","pending":"Pendente","unresolved":"Não resolvido","callback":"Callback","escalated":"Escalado"}
        cs2 = df["ds_status_resolucao"].value_counts().reindex(orrs,fill_value=0).reset_index()
        cs2.columns=["s","n"]
        cs2["l"] = cs2["s"].map(lbls)
        fig_st = go.Figure(go.Bar(x=cs2["l"],y=cs2["n"],
            marker_color=["#10b981","#f59e0b","#ef4444","#3b82f6","#8b5cf6"],
            text=cs2["n"],textposition="outside",textfont=dict(color=T["pt_text_out"])))
        fig_st.update_layout(title="Status de Resolução",showlegend=False,**PT)
        st.plotly_chart(fig_st, use_container_width=True)

# ══ PÁG 2 ═══════════════════════════════════


# ══ PÁG 3 ═══════════════════════════════════
with tabs[1]:
    sec("Experiência do Atendimento")
    e1,e2 = st.columns(2)

    with e1:
        labels = ["Neg. Inicial","Neutro Inicial","Pos. Inicial","Neg. Final","Neutro Final","Pos. Final"]
        li = {"Negativo":0,"Neutro":1,"Positivo":2}
        lf = {"Negativo":3,"Neutro":4,"Positivo":5}
        flows = df.groupby(["sent_ini_s","sent_fim_s"]).size().reset_index(name="n")
        src,tgt,val=[],[],[]
        for _,row in flows.iterrows():
            if row["sent_ini_s"] in li and row["sent_fim_s"] in lf:
                src.append(li[row["sent_ini_s"]]); tgt.append(lf[row["sent_fim_s"]]); val.append(int(row["n"]))
        cn = ["#ef4444","#3b82f6","#10b981","#ef4444","#3b82f6","#10b981"]
        fsan = go.Figure(go.Sankey(
            node=dict(label=labels,color=cn,pad=20,thickness=20,line=dict(color="#0f1117",width=0.5)),
            link=dict(source=src,target=tgt,value=val,color="rgba(59,130,246,0.15)")))
        fsan.update_layout(title="Fluxo Sentimento · Inicial → Final",height=380,**PT)
        st.plotly_chart(fsan, use_container_width=True)

    with e2:
        top8 = df["tema_p"].value_counts().head(8).index.tolist()
        dfb  = df[df["tema_p"].isin(top8)]
        cbx  = px.colors.qualitative.Set2
        fbox = go.Figure()
        for i,tema in enumerate(top8):
            sub = dfb[dfb["tema_p"]==tema]["vl_tempo_duracao"]
            fbox.add_trace(go.Box(y=sub,name=tema[:20],marker_color=cbx[i%len(cbx)],boxmean=True,line=dict(width=1.5)))
        fbox.update_layout(title="Boxplot Duração (s) por Tema",height=380,showlegend=False,**PT)
        st.plotly_chart(fbox, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("Métricas de Experiência")
    m1,m2,m3,m4 = st.columns(4)
    with m1: kpi("Reversão Sentimento", pct(reversao),                    "negativos que melhoraram","verde")
    with m2: kpi("Escalada de Conflito", pct(escalada),                   "atend. que pioraram",      "vermelho")
    with m3: kpi("Duração Mediana",     f"{df['vl_tempo_duracao'].median():.0f}s", f"≈{df['vl_tempo_duracao'].median()/60:.1f} min","azul")
    with m4: kpi("Silêncio Mediano",    f"{df['vl_tempo_silencio'].median():.0f}s","por atendimento",        "laranja")

    st.markdown("<br>", unsafe_allow_html=True)
    fsil = go.Figure(go.Scatter(x=df["vl_tempo_silencio"],y=df["vl_irc_score"],mode="markers",
        marker=dict(size=4,opacity=0.4,color=df["vl_irc_score"],
            colorscale=[[0,"#10b981"],[0.5,"#f59e0b"],[1,"#ef4444"]],
            showscale=True,colorbar=dict(title="IRC",thickness=12)),
        hovertemplate="Silêncio: %{x:.0f}s<br>IRC: %{y}<extra></extra>"))
    fsil.update_layout(title="Scatter Silêncio × IRC Score",xaxis_title="Silêncio (s)",yaxis_title="IRC Score",height=300,**PT)
    st.plotly_chart(fsil, use_container_width=True)

# ══ PÁG 4 ═══════════════════════════════════
with tabs[3]:
    sec("Análise de Risco de Conflito")
    r1,r2 = st.columns(2)

    with r1:
        orr2=["Low","Medium","High","Critical"]
        cr2 = df["ds_irc_classificacao"].value_counts().reindex(orr2,fill_value=0).reset_index()
        cr2.columns=["c","n"]
        cr2["pct"]=cr2["n"]/cr2["n"].sum()*100
        fr = go.Figure(go.Bar(x=cr2["c"],y=cr2["n"],marker_color=[COR_RISCO[r] for r in cr2["c"]],
            text=[f"{p:.1f}%" for p in cr2["pct"]],textposition="outside",textfont=dict(color=T["pt_text_out"])))
        fr.update_layout(title="Volume por Classificação IRC",showlegend=False,**PT)
        st.plotly_chart(fr, use_container_width=True)

    with r2:
        rt = df.groupby("tema_p").agg(vol=("tema_p","count"),irc=("vl_irc_score","mean")).reset_index()
        
        # Calculando as médias
        media_vol = rt["vol"].mean()
        media_irc = rt["irc"].mean()
        
        # --- MÁGICA PARA CENTRALIZAR A CRUZ ---
        # 1. Descobrimos a maior distância entre a média e as bolinhas extremas
        max_dist_vol = max(media_vol - rt["vol"].min(), rt["vol"].max() - media_vol)
        max_dist_irc = max(media_irc - rt["irc"].min(), rt["irc"].max() - media_irc)
        
        # 2. Adicionamos 10% de folga para as bolinhas não grudarem na borda
        margem_vol = max_dist_vol * 1.2 if max_dist_vol > 0 else 10
        margem_irc = max_dist_irc * 1.2 if max_dist_irc > 0 else 10
        
        fm = go.Figure(go.Scatter(
            x=rt["vol"],
            y=rt["irc"],
            mode="markers+text",
            text=rt["tema_p"],
            textposition="top center",
            textfont=dict(size=8),
            # Bolinhas do mesmo tamanho (14)
            marker=dict(size=14, color=rt["irc"],
                colorscale=[[0,"#10b981"],[0.5,"#f59e0b"],[1,"#ef4444"]],
                showscale=True, colorbar=dict(title="IRC Médio", thickness=15),
                line=dict(color=T["dot_bdr"], width=1), opacity=0.85),
            hovertemplate="<b>%{text}</b><br>Vol: %{x}<br>IRC: %{y:.1f}<extra></extra>"
        ))
        
        # Desenhando a cruz com as médias
        fm.add_hline(y=media_irc, line=dict(color=T["quad_line"], dash="dot", width=0.8))
        fm.add_vline(x=media_vol, line=dict(color=T["quad_line"], dash="dot", width=0.8))
        
        fm.add_annotation(x=rt["vol"].max(), y=rt["irc"].max(), text="⚠ Prioridade Máxima", showarrow=False, font=dict(color="#ef4444", size=11))
        
        fm.update_layout(
            title="Matriz de Risco · Volume × IRC",
            xaxis_title="Volume",
            yaxis_title="IRC Médio",
            height=480,
            # Removendo grade de fundo E a linha do zero
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_zeroline=False,
            # Forçando a cruz a ficar no centro exato da tela
            xaxis_range=[media_vol - margem_vol, media_vol + margem_vol],
            yaxis_range=[media_irc - margem_irc, media_irc + margem_irc],
            **PT
        )
        st.plotly_chart(fm, use_container_width=True)

# ══ PÁG 5 ═══════════════════════════════════
with tabs[2]:
    sec("Conformidade RN623")
    n1,n2,n3 = st.columns(3)
    conf_pct = df["vl_score_conformidade_rn623"].mean()
    n_nc = df["ds_nivel_conformidade"].value_counts().get("Não Conforme",0)
    n_co = df["ds_nivel_conformidade"].value_counts().get("Conforme com Oportunidades",0)
    with n1: kpi("Score Médio RN623",        f"{conf_pct:.1f}%",   "média geral",                  "roxo")
    with n2: kpi("Não Conformes",            fmt_n(n_nc),          pct(n_nc/total)+" do total",    "vermelho")
    with n3: kpi("Conf. c/ Oportunidades",   fmt_n(n_co),          pct(n_co/total)+" do total",    "verde")

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        cr3 = df["ds_criterios_rn623"].dropna().str.split(",").explode().str.strip().value_counts().head(12).reset_index()
        cr3.columns=["criterio","n"]
        fc3 = go.Figure(go.Bar(y=cr3["criterio"],x=cr3["n"],orientation="h",
            marker_color="#8b5cf6",opacity=0.85,
            text=cr3["n"],textposition="outside",textfont=dict(color=T["pt_text_out"])))
        fc3.update_layout(title="Critérios RN623 mais presentes",height=400,**PT)
        st.plotly_chart(fc3, use_container_width=True)

    with c2:
        ac = df.groupby("nm_agente")["vl_score_conformidade_rn623"].mean().sort_values().tail(20).reset_index()
        ac.columns=["agente","score"]
        fac = go.Figure(go.Bar(y=ac["agente"],x=ac["score"],orientation="h",
            marker=dict(color=ac["score"],colorscale=[[0,"#ef4444"],[0.5,"#f59e0b"],[1,"#10b981"]],
                showscale=True,colorbar=dict(title="Score %",thickness=12)),
            text=[f"{v:.1f}%" for v in ac["score"]],textposition="outside",textfont=dict(color=T["pt_text_out"])))
        fac.update_layout(title="Score RN623 por Agente",height=400,**PT)
        st.plotly_chart(fac, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ev = df.groupby("dt_criacao")["vl_score_conformidade_rn623"].mean().reset_index().sort_values("dt_criacao")
    fev = go.Figure(go.Scatter(x=ev["dt_criacao"],y=ev["vl_score_conformidade_rn623"],
        mode="lines+markers",line=dict(color="#8b5cf6",width=2.5),marker=dict(size=5,color="#a78bfa"),
        fill="tozeroy",fillcolor="rgba(139,92,246,0.08)"))
    fev.update_layout(title="Evolução do Score de Conformidade RN623",yaxis_title="Score médio (%)",**PT)
    st.plotly_chart(fev, use_container_width=True)

# ══ PÁG 6 ═══════════════════════════════════  
with tabs[4]:
    sec("Investigação de Casos")
    fi1,fi2,fi3,fi4 = st.columns(4)
    with fi1: risco_inv  = st.selectbox("Risco IRC",     ["Todos","Low","Medium","High","Critical"])
    with fi2: sent_inv   = st.selectbox("Sentimento",    ["Todos","Positive","Neutral","Negative"])
    with fi3: status_inv = st.selectbox("Status",        ["Todos","resolved","pending","unresolved","callback","escalated"])
    with fi4: agente_inv = st.selectbox("Agente",        ["Todos"]+sorted(df["nm_agente"].dropna().unique()))

    dfi = df.copy()
    if risco_inv  != "Todos": dfi = dfi[dfi["ds_irc_classificacao"]==risco_inv]
    if sent_inv   != "Todos": dfi = dfi[dfi["ds_sentimento_cliente_geral"]==sent_inv]
    if status_inv != "Todos": dfi = dfi[dfi["ds_status_resolucao"]==status_inv]
    if agente_inv != "Todos": dfi = dfi[dfi["nm_agente"]==agente_inv]

    cols_show = ["dt_criacao","nr_protocolo","nm_agente","ds_tema","nm_cliente",
                 "ds_sentimento_cliente_inicial","ds_sentimento_cliente_final",
                 "vl_irc_score","ds_irc_classificacao","ds_status_resolucao",
                 "vl_score_conformidade_rn623","ds_nivel_conformidade",
                 "vl_tempo_duracao","ds_dialogo_resumo"]
    df_show = dfi[cols_show].sort_values("vl_irc_score",ascending=False).head(300)

    st.dataframe(df_show, hide_index=True, use_container_width=True, column_config={
        "dt_criacao":                    st.column_config.DateColumn("Data"),
        "nr_protocolo":                  st.column_config.TextColumn("Protocolo"),
        "nm_agente":                     st.column_config.TextColumn("Agente"),
        "ds_tema":                       st.column_config.TextColumn("Tema"),
        "nm_cliente":                    st.column_config.TextColumn("Cliente"),
        "ds_sentimento_cliente_inicial": st.column_config.TextColumn("Sent. Inicial"),
        "ds_sentimento_cliente_final":   st.column_config.TextColumn("Sent. Final"),
        "vl_irc_score":                  st.column_config.NumberColumn("IRC Score", format="%d"),
        "ds_irc_classificacao":          st.column_config.TextColumn("Risco"),
        "ds_status_resolucao":           st.column_config.TextColumn("Status"),
        "vl_score_conformidade_rn623":   st.column_config.NumberColumn("Conf. RN623 %", format="%.1f%%"),
        "ds_nivel_conformidade":         st.column_config.TextColumn("Nível Conf."),
        "vl_tempo_duracao":              st.column_config.NumberColumn("Duração (s)", format="%.0f"),
        "ds_dialogo_resumo":             st.column_config.TextColumn("Resumo", width="large"),
    })
    st.caption(f"Exibindo até 300 · {len(dfi):,} encontrados")

    st.markdown("<br>", unsafe_allow_html=True)
    sec("Detalhe do Diálogo")
    protos = dfi["nr_protocolo"].dropna().unique()[:100]
    proto_sel = st.selectbox("Selecionar protocolo", ["—"]+list(protos))
    
    if proto_sel != "—":
        filtro = dfi[dfi["nr_protocolo"]==proto_sel]
        if not filtro.empty:
            row = filtro.iloc[0]
            ci, cd = st.columns([1,2])
            with ci:
                st.markdown(f"""
**Protocolo:** {row['nr_protocolo']}  
**Data:** {row['dt_criacao'].date()}  
**Agente:** {row['nm_agente']}  
**Cliente:** {row['nm_cliente']}  
**Tema:** {row['ds_tema']}  
**IRC Score:** {row['vl_irc_score']} ({row['ds_irc_classificacao']})  
**Status:** {row['ds_status_resolucao']}  
**Sent. Inicial:** {row['ds_sentimento_cliente_inicial']}  
**Sent. Final:** {row['ds_sentimento_cliente_final']}  
**Score RN623:** {row['vl_score_conformidade_rn623']:.1f}%  
**Nível Conf.:** {row['ds_nivel_conformidade']}
""")
                st.markdown("**Resumo:**")
                st.info(str(row["ds_dialogo_resumo"]))
            with cd:
                st.markdown("**Diálogo Completo:**")
                st.text_area("", value=str(row.get("ds_dialogo","Não disponível")), height=400, disabled=True, label_visibility="collapsed")