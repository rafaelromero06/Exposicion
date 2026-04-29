import dash
import os
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Big Data — Presentación Completa"

BG="#0A0A0F"; SFC="#12121A"; CARD="#1A1A26"
A="#6EE7F7"; A2="#A78BFA"; A3="#34D399"; A4="#F59E0B"; A5="#F472B6"
T="#E2E8F0"; ST="#94A3B8"; BD="#2D2D42"
FD="'Syne',sans-serif"; FB="'DM Sans',sans-serif"

SLIDES = [
    "portada","agenda","que-es","historia","datos-info",
    "las-5v","estructura","tipos-arch","pipeline","almacen",
    "nosql","tecnologias","mapreduce","batch-stream","ml-bd",
    "cloud","casos","escala","profesiones","retos","cierre"
]
TITLES = [
    "Inicio","Agenda","¿Qué es?","Historia","Datos vs Info",
    "Las 5 V's","Estructura","Arquitecturas","Pipeline","Almacenamiento",
    "NoSQL","Tecnologías","MapReduce","Batch vs Stream","Big Data + ML",
    "Cloud","Casos de Uso","Escala Global","Profesiones","Retos","Cierre"
]

GFONTS = html.Link(rel="stylesheet",
    href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap")

# ─── UI Helpers ──────────────────────────────────────────────────────────────
def C(ch, ex=None):
    s={"background":CARD,"borderRadius":"14px","border":f"1px solid {BD}",
       "padding":"20px","boxShadow":"0 4px 24px rgba(0,0,0,.35)"}
    if ex: s.update(ex)
    return html.Div(ch, style=s)

def pill(txt, col=A):
    return html.Span(txt, style={
        "background":f"{col}18","color":col,"border":f"1px solid {col}44",
        "borderRadius":"999px","padding":"4px 14px","fontSize":"12px",
        "fontWeight":"500","fontFamily":FB,"letterSpacing":".05em","textTransform":"uppercase"})

def H(t): return html.H2(t,style={"fontFamily":FD,"fontSize":"32px","color":T,"marginBottom":"6px"})
def S(t): return html.P(t,style={"color":ST,"fontFamily":FB,"marginBottom":"22px","fontSize":"15px"})

def stat(num, lab, col=A):
    return html.Div([
        html.Div(num,style={"fontSize":"32px","fontWeight":"800","fontFamily":FD,"color":col,"lineHeight":"1"}),
        html.Div(lab,style={"fontSize":"11px","color":ST,"fontFamily":FB,"marginTop":"4px","lineHeight":"1.3"})
    ],style={"textAlign":"center","padding":"12px"})

def icard(icon, title, desc, col=A, extra=None):
    s={"background":CARD,"borderRadius":"12px","border":f"1px solid {BD}","padding":"16px"}
    if extra: s.update(extra)
    return html.Div([
        html.Div(icon,style={"fontSize":"26px","marginBottom":"8px"}),
        html.Div(title,style={"fontFamily":FD,"fontWeight":"700","fontSize":"15px","color":col,"marginBottom":"6px"}),
        html.P(desc,style={"color":ST,"fontFamily":FB,"fontSize":"13px","lineHeight":"1.5","margin":"0"})
    ],style=s)

def timeline_row(year, title, desc, col=A):
    return html.Div([
        html.Div([
            html.Div(year,style={"fontFamily":FD,"fontWeight":"800","fontSize":"14px","color":col}),
            html.Div(style={"width":"1px","background":BD,"flex":"1","margin":"4px 0","minHeight":"16px"})
        ],style={"display":"flex","flexDirection":"column","alignItems":"center","width":"60px","flexShrink":"0"}),
        html.Div([
            html.Div(title,style={"fontFamily":FD,"fontWeight":"700","fontSize":"14px","color":T,"marginBottom":"3px"}),
            html.Div(desc,style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4"})
        ],style={"background":CARD,"borderRadius":"8px","border":f"1px solid {BD}",
                  "padding":"10px 14px","flex":"1","marginBottom":"8px"})
    ],style={"display":"flex","gap":"12px","alignItems":"flex-start"})

def sw(sid, ch):
    return html.Div(ch,id=f"slide-{sid}",style={"display":"none","animation":"fadeSlide .45s ease forwards"})

# ─── Charts ───────────────────────────────────────────────────────────────────
def _layout(fig, h=None, extra=None):
    kw={"paper_bgcolor":"rgba(0,0,0,0)","plot_bgcolor":"rgba(0,0,0,0)",
        "margin":dict(l=0,r=0,t=10,b=0),"font":dict(family=FB,color=ST)}
    if extra: kw.update(extra)
    fig.update_layout(**kw)
    return fig

def ch_radar():
    cats=["Volumen","Velocidad","Variedad","Veracidad","Valor"]
    fig=go.Figure(go.Scatterpolar(
        r=[95,88,82,72,90,95],theta=cats+[cats[0]],
        fill="toself",fillcolor="rgba(110,231,247,.12)",
        line=dict(color=A,width=2.5),marker=dict(color=A,size=7)))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",showlegend=False,
        margin=dict(l=40,r=40,t=20,b=20),
        polar=dict(bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True,range=[0,100],gridcolor=BD,linecolor=BD,
                            tickfont=dict(color=ST,size=9,family=FB)),
            angularaxis=dict(gridcolor=BD,linecolor=BD,tickfont=dict(color=T,size=12,family=FB))))
    return fig

def ch_donut():
    labels=["Texto/Docs","Imágenes","Video/Audio","Logs/Sensores","Transacciones","Social"]
    values=[28,18,22,16,8,8]
    colors=[A,A2,A3,A4,A5,"#60A5FA"]
    fig=go.Figure(go.Pie(labels=labels,values=values,hole=0.62,
        marker=dict(colors=colors,line=dict(color=BG,width=3)),
        textfont=dict(family=FB,size=11,color=T),
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>"))
    fig.add_annotation(text="Tipos<br>de Datos",x=.5,y=.5,showarrow=False,
                       font=dict(size=13,color=T,family=FD))
    return _layout(fig, extra={"legend":dict(font=dict(color=ST,family=FB,size=11),bgcolor="rgba(0,0,0,0)")})

def ch_growth():
    years=list(range(2010,2027))
    zb=[2,5,10,20,35,55,80,120,160,210,275,350,440,550,680,820,1000]
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=years,y=zb,mode="lines+markers",
        line=dict(color=A,width=3,shape="spline"),fill="tozeroy",
        fillcolor="rgba(110,231,247,.1)",
        marker=dict(color=A2,size=6,line=dict(color=A,width=2))))
    fig.add_annotation(x=2026,y=1000,text="~1,000 ZB",showarrow=True,
        arrowhead=2,arrowcolor=A3,font=dict(color=A3,size=11,family=FB),
        bgcolor=CARD,bordercolor=A3,borderwidth=1)
    return _layout(fig,extra={
        "xaxis":dict(gridcolor=BD,color=ST,tickfont=dict(family=FB)),
        "yaxis":dict(gridcolor=BD,color=ST,tickfont=dict(family=FB),
                     title=dict(text="Zettabytes",font=dict(color=ST,family=FB)))})

def ch_techs():
    techs=["Apache Spark","Hadoop","Kafka","Cassandra","Flink","HBase"]
    vals=[91,82,75,60,55,48]
    cols=[A if i%2==0 else A2 for i in range(len(techs))]
    fig=go.Figure(go.Bar(x=vals,y=techs,orientation="h",marker=dict(color=cols),
        text=[f"{v}%" for v in vals],textposition="outside",
        textfont=dict(color=T,family=FB,size=12)))
    return _layout(fig,extra={
        "xaxis":dict(range=[0,112],showgrid=False,showticklabels=False),
        "yaxis":dict(gridcolor=BD,color=T,tickfont=dict(family=FB,size=13)),"bargap":.35})

def ch_sectors():
    s=["Salud","Finanzas","Retail","Logística","Gobierno","Entretenim.","Industria","Educación"]
    v=[87,92,78,83,65,94,76,60]
    fig=go.Figure(go.Bar(x=s,y=v,marker=dict(color=v,colorscale=[[0,A2],[.5,A],[1,A3]]),
        text=[f"{x}%" for x in v],textposition="outside",textfont=dict(color=T,family=FB,size=11)))
    return _layout(fig,extra={
        "xaxis":dict(gridcolor=BD,color=T,tickfont=dict(family=FB,size=11)),
        "yaxis":dict(range=[0,110],gridcolor=BD,color=ST,tickfont=dict(family=FB),
                     title=dict(text="Adopción %",font=dict(color=ST,family=FB))),"bargap":.3})

def ch_lambda():
    fig=go.Figure()
    # Nodos como scatter
    nodes_x=[0,2,2,4,4,6]
    nodes_y=[2,3,1,3,1,2]
    labels=["Fuente<br>de datos","Batch<br>Layer","Speed<br>Layer","Serving<br>Layer (Batch)","Serving<br>Layer (Speed)","Vista<br>Final"]
    colors_n=[A,A2,A3,A4,A5,A]
    for i in range(len(nodes_x)):
        fig.add_trace(go.Scatter(
            x=[nodes_x[i]],y=[nodes_y[i]],mode="markers+text",
            marker=dict(color=colors_n[i],size=36,line=dict(color=BG,width=2)),
            text=[labels[i]],textposition="middle center",
            textfont=dict(color=BG,size=9,family=FB),showlegend=False,
            hoverinfo="text",hovertext=labels[i]))
    # Edges
    edges=[(0,1),(0,2),(1,3),(2,4),(3,5),(4,5)]
    for a,b in edges:
        fig.add_shape(type="line",x0=nodes_x[a],y0=nodes_y[a],x1=nodes_x[b],y1=nodes_y[b],
                      line=dict(color=BD,width=2))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-0.5,6.5]),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[0,4]),
        margin=dict(l=10,r=10,t=10,b=10),height=220)
    return fig

def ch_nosql():
    cats=["Escalabilidad","Velocidad escritura","Flexibilidad schema",
          "Consultas complejas","Consistencia","Soporte comunidad"]
    relacional=[40,50,30,95,95,90]
    nosql=[95,90,95,60,65,80]
    fig=go.Figure()
    fig.add_trace(go.Scatterpolar(r=relacional+[relacional[0]],theta=cats+[cats[0]],
        name="Relacional",fill="toself",fillcolor="rgba(167,139,250,.15)",
        line=dict(color=A2,width=2),marker=dict(color=A2,size=6)))
    fig.add_trace(go.Scatterpolar(r=nosql+[nosql[0]],theta=cats+[cats[0]],
        name="NoSQL",fill="toself",fillcolor="rgba(52,211,153,.15)",
        line=dict(color=A3,width=2),marker=dict(color=A3,size=6)))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",showlegend=True,
        margin=dict(l=50,r=50,t=20,b=20),
        polar=dict(bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True,range=[0,100],gridcolor=BD,linecolor=BD,
                            tickfont=dict(color=ST,size=8,family=FB)),
            angularaxis=dict(gridcolor=BD,linecolor=BD,tickfont=dict(color=T,size=10,family=FB))),
        legend=dict(font=dict(color=T,family=FB,size=12),bgcolor="rgba(0,0,0,0)",
                    orientation="h",y=-0.1))
    return fig

def ch_ml_data():
    sizes=[1,5,20,100,500]
    acc_classic=[55,68,72,75,76]
    acc_dl=[30,52,65,78,91]
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=sizes,y=acc_classic,mode="lines+markers",name="ML Clásico",
        line=dict(color=A2,width=2.5,dash="dash"),marker=dict(color=A2,size=8)))
    fig.add_trace(go.Scatter(x=sizes,y=acc_dl,mode="lines+markers",name="Deep Learning",
        line=dict(color=A3,width=2.5),marker=dict(color=A3,size=8)))
    fig.add_annotation(x=500,y=91,text="Big Data aquí",showarrow=True,arrowhead=2,
        arrowcolor=A,font=dict(color=A,size=11,family=FB),bgcolor=CARD,bordercolor=A,borderwidth=1)
    return _layout(fig,extra={
        "xaxis":dict(type="log",gridcolor=BD,color=ST,tickfont=dict(family=FB),
                     title=dict(text="Tamaño del dataset (millones de registros)",font=dict(color=ST,family=FB))),
        "yaxis":dict(gridcolor=BD,color=ST,tickfont=dict(family=FB),range=[20,100],
                     title=dict(text="Precisión del modelo %",font=dict(color=ST,family=FB))),
        "legend":dict(font=dict(color=T,family=FB),bgcolor="rgba(0,0,0,0)")})

def ch_mapreduce():
    cats=["Entrada","Map","Shuffle","Reduce","Salida"]
    vals=[100,400,400,100,100]
    colors_mr=[A,A2,A3,A4,A5]
    fig=go.Figure(go.Funnel(y=cats,x=vals,
        marker=dict(color=colors_mr,line=dict(color=BG,width=2)),
        textfont=dict(family=FB,size=13,color=BG),
        textinfo="label+percent initial"))
    return _layout(fig,extra={"showlegend":False})

def ch_cloud_share():
    labels=["AWS","Azure","Google Cloud","Alibaba","Otros"]
    values=[32,22,11,9,26]
    colors_c=[A4,"#0078D4","#4285F4","#FF6A00",BD]
    fig=go.Figure(go.Pie(labels=labels,values=values,hole=0.5,
        marker=dict(colors=colors_c,line=dict(color=BG,width=2)),
        textfont=dict(family=FB,size=12,color=T),
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>"))
    fig.add_annotation(text="Cloud<br>Market",x=.5,y=.5,showarrow=False,
                       font=dict(size=12,color=T,family=FD))
    return _layout(fig,extra={"legend":dict(font=dict(color=ST,family=FB,size=11),bgcolor="rgba(0,0,0,0)")})

def ch_salaries():
    roles=["Data Analyst","Data Engineer","ML Engineer","Data Scientist","Data Architect","CDO"]
    salarios=[55,85,105,110,130,180]
    colors_s=[A,A2,A3,A4,A5,"#60A5FA"]
    fig=go.Figure(go.Bar(x=salarios,y=roles,orientation="h",
        marker=dict(color=colors_s),
        text=[f"~${s}k" for s in salarios],textposition="outside",
        textfont=dict(color=T,family=FB,size=12)))
    return _layout(fig,extra={
        "xaxis":dict(range=[0,220],showgrid=False,showticklabels=False),
        "yaxis":dict(gridcolor=BD,color=T,tickfont=dict(family=FB,size=12)),"bargap":.3})

# ─── SLIDES ───────────────────────────────────────────────────────────────────

def sl_portada():
    return sw("portada",[
        html.Div([
            html.Div(style={"position":"absolute","inset":"0",
                "background":f"radial-gradient(ellipse 80% 60% at 50% 40%, {A}14, transparent 70%)",
                "pointerEvents":"none"}),
            html.Div([
                pill("Exposición — 40 minutos",A3),
                html.Br(),html.Br(),
                html.H1("Big Data",style={"fontSize":"clamp(60px,9vw,96px)","fontFamily":FD,
                    "fontWeight":"800","color":T,"letterSpacing":"-2px","lineHeight":"1","margin":"0"}),
                html.Div("La era de los datos masivos",style={"fontSize":"clamp(16px,3vw,24px)",
                    "color":A,"fontFamily":FB,"fontWeight":"300","marginTop":"10px"}),
                html.P("Arquitecturas, tecnologías, estructuras de datos, inteligencia artificial y "
                       "el impacto real del Big Data en el mundo moderno.",
                    style={"color":ST,"fontFamily":FB,"maxWidth":"520px","lineHeight":"1.7",
                           "marginTop":"18px","fontSize":"15px"}),
                html.Div([
                    stat("2.5 QB","generados cada día",A),
                    stat("328 M","correos/minuto",A2),
                    stat("500 M","tweets diarios",A3),
                    stat("5 M","búsquedas/minuto",A4),
                ],style={"display":"flex","gap":"6px","marginTop":"32px","flexWrap":"wrap"}),
                html.Div([
                    html.Div("21 temas",style={"color":ST,"fontFamily":FB,"fontSize":"13px"}),
                    html.Div(style={"width":"1px","height":"16px","background":BD}),
                    html.Div("40 minutos",style={"color":ST,"fontFamily":FB,"fontSize":"13px"}),
                    html.Div(style={"width":"1px","height":"16px","background":BD}),
                    html.Div("Nivel introductorio → intermedio",style={"color":ST,"fontFamily":FB,"fontSize":"13px"}),
                ],style={"display":"flex","gap":"14px","alignItems":"center","marginTop":"20px"})
            ],style={"position":"relative","zIndex":"1","padding":"52px 44px"})
        ],style={"minHeight":"520px","position":"relative",
                 "background":f"linear-gradient(135deg,{BG},{SFC})",
                 "borderRadius":"20px","overflow":"hidden","border":f"1px solid {BD}"})
    ])

def sl_agenda():
    items = [
        ("01","¿Qué es Big Data?","Definición, contexto y por qué importa",A),
        ("02","Historia","Evolución desde los años 60 hasta hoy",A2),
        ("03","Datos vs Información","La diferencia fundamental",A3),
        ("04","Las 5 V's","Volumen, Velocidad, Variedad, Veracidad, Valor",A4),
        ("05","Estructura de datos","Estructurado, semi y no estructurado",A5),
        ("06","Arquitecturas","Lambda, Kappa y Data Mesh",A),
        ("07","Pipeline de datos","Del origen al insight",A2),
        ("08","Almacenamiento","Data Warehouse, Data Lake, Lakehouse",A3),
        ("09","NoSQL","Tipos y comparativa con SQL",A4),
        ("10","Tecnologías clave","Hadoop, Spark, Kafka y más",A5),
        ("11","MapReduce","El algoritmo que lo cambió todo",A),
        ("12","Batch vs Streaming","Dos paradigmas de procesamiento",A2),
        ("13","Big Data + ML","Por qué más datos = mejores modelos",A3),
        ("14","Cloud Computing","AWS, GCP, Azure y Big Data",A4),
        ("15","Casos de uso","Salud, finanzas, retail y más",A5),
        ("16","Escala global","Números que impresionan",A),
        ("17","Profesiones","Roles y salarios en el ecosistema",A2),
        ("18","Retos","Privacidad, energía y talento",A3),
        ("19","El futuro","Tendencias que vienen",A4),
        ("20","Cierre","Resumen y conclusiones",A5),
    ]
    rows1 = items[:10]; rows2 = items[10:]
    def row(n,t,d,c):
        return html.Div([
            html.Div(n,style={"fontFamily":FD,"fontWeight":"800","fontSize":"13px",
                               "color":c,"width":"28px","flexShrink":"0"}),
            html.Div([
                html.Div(t,style={"fontFamily":FD,"fontWeight":"700","fontSize":"13px","color":T}),
                html.Div(d,style={"color":ST,"fontFamily":FB,"fontSize":"11px","marginTop":"1px"})
            ])
        ],style={"display":"flex","gap":"10px","padding":"8px 12px",
                 "borderRadius":"8px","border":f"1px solid {BD}","marginBottom":"6px",
                 "background":CARD})
    return sw("agenda",[
        H("Agenda de la Exposición"),S("20 temas · 40 minutos — aproximadamente 2 minutos por tema"),
        html.Div([
            html.Div([row(*r) for r in rows1]),
            html.Div([row(*r) for r in rows2]),
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"12px"})
    ])

def sl_que_es():
    return sw("que-es",[
        H("¿Qué es el Big Data?"),S("Una explicación desde cero, sin tecnicismos."),
        html.Div([
            html.Div([
                icard("📡","El Problema",
                    "Cada segundo, millones de personas generan datos: búsquedas, compras, mensajes, "
                    "sensores IoT, cámaras, GPS. El volumen supera lo que cualquier base de datos "
                    "convencional puede capturar o procesar.",A),
                icard("💡","La Definición",
                    "Big Data es el conjunto de tecnologías, metodologías y herramientas diseñadas "
                    "para capturar, almacenar, procesar y analizar colecciones de datos tan masivas, "
                    "variadas o veloces que desbordan el software tradicional.",A2),
                icard("🎯","El Objetivo",
                    "Descubrir patrones ocultos, correlaciones y tendencias que permitan tomar "
                    "decisiones más inteligentes, predecir comportamientos y crear nuevas "
                    "fuentes de valor económico o social.",A3),
            ],style={"display":"flex","flexDirection":"column","gap":"12px"}),
            html.Div([
                C([
                    html.Div("¿Cuándo un dataset es 'Big Data'?",style={
                        "fontFamily":FD,"fontWeight":"700","fontSize":"16px","color":T,"marginBottom":"14px"}),
                    *[html.Div([
                        html.Div(style={"width":"8px","height":"8px","borderRadius":"50%",
                                         "background":c,"flexShrink":"0","marginTop":"5px"}),
                        html.Div([
                            html.Div(t,style={"color":c,"fontFamily":FD,"fontWeight":"700","fontSize":"13px"}),
                            html.Div(d,style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4"})
                        ])
                    ],style={"display":"flex","gap":"10px","marginBottom":"12px"})
                    for c,t,d in [
                        (A,"No cabe en una sola máquina","Requiere distribución en múltiples servidores."),
                        (A2,"No se puede procesar en tiempo razonable","Un script de Python tomaría semanas o años."),
                        (A3,"No tiene esquema fijo","Los datos llegan en formatos heterogéneos."),
                        (A4,"La velocidad supera la escritura a disco","Streaming en tiempo real continuo."),
                        (A5,"Genera valor económico real","Decisiones basadas en millones de registros."),
                    ]],
                    html.Div(["💡 ",
                        html.Span("Analogía: ",style={"color":A,"fontWeight":"700","fontFamily":FD}),
                        html.Span("Big Data es como el océano. No lo puedes beber de golpe, "
                                  "pero con las herramientas correctas extraes agua pura (conocimiento).",
                                  style={"color":ST,"fontFamily":FB,"fontSize":"13px"})
                    ],style={"marginTop":"14px","padding":"12px 14px","background":f"{A}10",
                              "borderRadius":"8px","border":f"1px solid {A}30","fontSize":"13px"})
                ])
            ])
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_historia():
    events=[
        ("1960s","Primeros DBs","IBM crea IMS, el primer sistema de gestión de bases de datos para la NASA.",A),
        ("1970","Modelo relacional","Edgar Codd publica el modelo relacional y nace SQL.",A2),
        ("1989","Data Warehousing","Bill Inmon acuña el concepto de Data Warehouse empresarial.",A3),
        ("1997","Primera mención","Roger Magoulas usa por primera vez el término 'Big Data' en O'Reilly.",A4),
        ("2003","Google File System","Google publica el paper de GFS. Base de Hadoop.",A5),
        ("2004","MapReduce","Google publica MapReduce. La computación distribuida se democratiza.",A),
        ("2006","Hadoop","Doug Cutting y Mike Cafarella crean Hadoop en Yahoo!, open source.",A2),
        ("2008","NoSQL movement","Johan Oskarsson lanza el movimiento NoSQL en Twitter.",A3),
        ("2011","Spark","AMPLab de UC Berkeley lanza Apache Spark, 100× más rápido que Hadoop.",A4),
        ("2016","Data Lakes","Confluencia de Kafka, Spark y Flink define la arquitectura moderna.",A5),
        ("2023","LLMs + Big Data","Los modelos de lenguaje como GPT-4 requieren petabytes de datos.",A),
    ]
    col1=events[:6]; col2=events[5:]
    return sw("historia",[
        H("Historia del Big Data"),S("De los primeros discos magnéticos a los zettabytes actuales."),
        html.Div([
            html.Div([timeline_row(*e) for e in col1]),
            html.Div([timeline_row(*e) for e in col2]),
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_datos_info():
    return sw("datos-info",[
        H("Datos vs Información vs Conocimiento"),S("La jerarquía fundamental que todo analista debe entender."),
        html.Div([
            C([
                html.Div("🔢",style={"fontSize":"40px","marginBottom":"10px"}),
                html.Div("Dato",style={"fontFamily":FD,"fontWeight":"800","fontSize":"22px","color":A,"marginBottom":"8px"}),
                html.P("Un hecho crudo sin contexto. Solo existe, no significa nada por sí solo.",
                    style={"color":ST,"fontFamily":FB,"fontSize":"14px","lineHeight":"1.6","marginBottom":"12px"}),
                html.Div([
                    html.Div("Ej:",style={"color":A,"fontFamily":FD,"fontWeight":"700","fontSize":"13px"}),
                    html.Div('37, "Colombia", 08:32:14, 0.82',
                        style={"fontFamily":"'Courier New',monospace","color":A3,"fontSize":"13px",
                               "background":f"{BG}","padding":"8px","borderRadius":"6px","marginTop":"6px"})
                ])
            ],{"textAlign":"center"}),
            html.Div([
                html.Div("▼",style={"textAlign":"center","color":BD,"fontSize":"24px","margin":"auto"}),
            ],style={"display":"flex","alignItems":"center","justifyContent":"center"}),
            C([
                html.Div("📊",style={"fontSize":"40px","marginBottom":"10px"}),
                html.Div("Información",style={"fontFamily":FD,"fontWeight":"800","fontSize":"22px","color":A2,"marginBottom":"8px"}),
                html.P("Datos con contexto y estructura. Ya responden una pregunta básica.",
                    style={"color":ST,"fontFamily":FB,"fontSize":"14px","lineHeight":"1.6","marginBottom":"12px"}),
                html.Div([
                    html.Div("Ej:",style={"color":A2,"fontFamily":FD,"fontWeight":"700","fontSize":"13px"}),
                    html.Div('"Usuario de 37 años en Colombia compró a las 8am con prob. fraude 82%"',
                        style={"color":A3,"fontFamily":FB,"fontSize":"13px","lineHeight":"1.4",
                               "background":f"{BG}","padding":"8px","borderRadius":"6px","marginTop":"6px"})
                ])
            ],{"textAlign":"center"}),
            html.Div([
                html.Div("▼",style={"textAlign":"center","color":BD,"fontSize":"24px","margin":"auto"}),
            ],style={"display":"flex","alignItems":"center","justifyContent":"center"}),
            C([
                html.Div("💡",style={"fontSize":"40px","marginBottom":"10px"}),
                html.Div("Conocimiento",style={"fontFamily":FD,"fontWeight":"800","fontSize":"22px","color":A3,"marginBottom":"8px"}),
                html.P("Información interpretada que permite tomar decisiones y predecir el futuro.",
                    style={"color":ST,"fontFamily":FB,"fontSize":"14px","lineHeight":"1.6","marginBottom":"12px"}),
                html.Div([
                    html.Div("Ej:",style={"color":A3,"fontFamily":FD,"fontWeight":"700","fontSize":"13px"}),
                    html.Div('"Bloquear transacción, notificar usuario, reforzar modelo con nuevo caso positivo"',
                        style={"color":A3,"fontFamily":FB,"fontSize":"13px","lineHeight":"1.4",
                               "background":f"{BG}","padding":"8px","borderRadius":"6px","marginTop":"6px"})
                ])
            ],{"textAlign":"center"}),
        ],style={"display":"grid","gridTemplateColumns":"1fr auto 1fr auto 1fr","gap":"8px","alignItems":"start"}),
        html.Div([
            html.Div("El ROI del Big Data está en subir de datos crudos → conocimiento accionable lo más rápido posible.",
                style={"color":ST,"fontFamily":FB,"fontSize":"14px","lineHeight":"1.6"}),
        ],style={"marginTop":"16px","padding":"14px 18px","background":f"{A}10",
                  "borderRadius":"10px","border":f"1px solid {A}30"})
    ])

def sl_5v():
    vs=[
        {"e":"📦","t":"Volumen","c":A,"sub":"Terabytes → Petabytes → Zettabytes",
         "d":"La cantidad de datos es tan masiva que no cabe en servidores convencionales. Un solo avión Boeing 737 genera 240 TB de datos por vuelo."},
        {"e":"⚡","t":"Velocidad","c":A2,"sub":"Tiempo real o casi real",
         "d":"Los datos llegan en streams continuos. Twitter procesa 500M tweets/día; Visa evalúa 65,000 transacciones/segundo."},
        {"e":"🎨","t":"Variedad","c":A3,"sub":"Estructurado · Semi · No estructurado",
         "d":"Textos, imágenes, videos, logs, JSON, CSV, audio… El 80% de los datos del mundo no tienen formato definido."},
        {"e":"✅","t":"Veracidad","c":A4,"sub":"Calidad y confiabilidad",
         "d":"'Garbage in, garbage out'. IBM estima que datos de mala calidad cuestan ~$3.1 trillones anuales a la economía de EE.UU."},
        {"e":"💰","t":"Valor","c":A5,"sub":"Conocimiento accionable",
         "d":"El dato crudo vale poco. El insight que permite tomar una decisión puede valer millones. El valor es el fin último."},
    ]
    rows=[html.Div([
        html.Div([
            html.Div(v["e"],style={"fontSize":"26px","marginRight":"10px","flexShrink":"0"}),
            html.Div([
                html.Div(v["t"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"17px","color":v["c"]}),
                html.Div(v["sub"],style={"color":T,"fontFamily":FB,"fontSize":"12px","marginTop":"1px"}),
                html.P(v["d"],style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.5","margin":"4px 0 0"})
            ])
        ],style={"display":"flex","padding":"12px 14px","background":CARD,
                  "borderRadius":"10px","border":f"1px solid {BD}","marginBottom":"8px"})
    ]) for v in vs]
    return sw("las-5v",[
        H("Las 5 V's del Big Data"),S("Los cinco pilares que definen y caracterizan cualquier sistema de Big Data."),
        html.Div([
            html.Div(rows),
            C([html.Div("Intensidad relativa de cada V",style={"fontFamily":FD,"fontWeight":"700",
                         "fontSize":"14px","color":T,"marginBottom":"4px"}),
               dcc.Graph(figure=ch_radar(),config={"displayModeBar":False},style={"height":"340px"})])
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_estructura():
    tipos=[
        {"tag":"Estructurado","c":A,"icon":"📋",
         "d":"Organizados en filas y columnas con esquema rígido predefinido. Son los más fáciles de analizar.",
         "ex":"Bases de datos relacionales (MySQL, PostgreSQL), hojas de cálculo, archivos CSV",
         "pct":"20%"},
        {"tag":"Semi-estructurado","c":A2,"icon":"🗂️",
         "d":"Tienen marcadores o etiquetas que definen cierta estructura, pero no siguen un esquema estricto.",
         "ex":"JSON, XML, HTML, correos electrónicos, logs con formato",
         "pct":"~5-10%"},
        {"tag":"No estructurado","c":A3,"icon":"🌊",
         "d":"Sin formato ni esquema predefinido. Son el tipo de dato más abundante del mundo.",
         "ex":"Imágenes, videos, audio, texto libre, redes sociales, documentos PDF",
         "pct":"~80%"},
    ]
    tcards=[C([
        html.Div([pill(t["tag"],t["c"]),
                  html.Span(f"  {t['pct']} de datos",style={"color":ST,"fontFamily":FB,"fontSize":"11px","marginLeft":"8px"})]),
        html.Div(t["icon"]+" "+t["tag"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"17px",
                                                 "color":T,"marginTop":"10px","marginBottom":"8px"}),
        html.P(t["d"],style={"color":ST,"fontFamily":FB,"fontSize":"13px","lineHeight":"1.6","margin":"0"}),
        html.Div(t["ex"],style={"marginTop":"8px","fontFamily":FB,"fontSize":"12px","color":t["c"],
                                  "padding":"8px","background":f"{t['c']}10","borderRadius":"6px"})
    ]) for t in tipos]
    return sw("estructura",[
        H("Estructura de los Datos"),S("El tipo de dato determina cómo se almacena, procesa y analiza."),
        html.Div([
            html.Div(tcards,style={"display":"flex","flexDirection":"column","gap":"12px"}),
            C([html.Div("Distribución global por tipo",style={"fontFamily":FD,"fontWeight":"700",
                         "fontSize":"14px","color":T,"marginBottom":"4px"}),
               dcc.Graph(figure=ch_donut(),config={"displayModeBar":False},style={"height":"360px"})])
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_arquitecturas():
    archs=[
        {"icon":"λ","name":"Arquitectura Lambda","c":A,
         "d":"Combina procesamiento batch y en tiempo real en paralelo. Propuesta por Nathan Marz en 2011.",
         "pros":"Alta tolerancia a fallos, puede reprocesar histórico",
         "cons":"Compleja de mantener, código duplicado"},
        {"icon":"κ","name":"Arquitectura Kappa","c":A2,
         "d":"Solo procesamiento en streaming. Simplifica Lambda al eliminar la capa batch.",
         "pros":"Código unificado, más simple de operar",
         "cons":"Reprocesar histórico es costoso"},
        {"icon":"⬡","name":"Data Mesh","c":A3,
         "d":"Descentraliza la propiedad de los datos. Cada dominio de negocio es dueño de sus datos.",
         "pros":"Escalable en organizaciones grandes, autonomía de equipos",
         "cons":"Requiere cultura de datos madura"},
    ]
    acards=[C([
        html.Div(a["icon"],style={"fontSize":"36px","fontFamily":FD,"fontWeight":"800","color":a["c"]}),
        html.Div(a["name"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"17px","color":T,"marginTop":"6px","marginBottom":"8px"}),
        html.P(a["d"],style={"color":ST,"fontFamily":FB,"fontSize":"13px","lineHeight":"1.5","marginBottom":"10px"}),
        html.Div([
            html.Div([html.Span("✓ ",style={"color":A3}),a["pros"]],
                style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginBottom":"4px"}),
            html.Div([html.Span("✗ ",style={"color":A5}),a["cons"]],
                style={"color":ST,"fontFamily":FB,"fontSize":"12px"})
        ],style={"padding":"8px","background":f"{BG}","borderRadius":"6px"})
    ]) for a in archs]
    return sw("tipos-arch",[
        H("Arquitecturas de Big Data"),S("Los tres modelos arquitectónicos más importantes del ecosistema."),
        html.Div([
            html.Div(acards,style={"display":"flex","flexDirection":"column","gap":"12px"}),
            C([
                html.Div("Arquitectura Lambda — Diagrama",style={"fontFamily":FD,"fontWeight":"700",
                           "fontSize":"14px","color":T,"marginBottom":"4px"}),
                dcc.Graph(figure=ch_lambda(),config={"displayModeBar":False},style={"height":"230px"}),
                html.Div([
                    html.Div([pill("Batch Layer",A)," Procesa histórico completo"],
                        style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginTop":"8px","marginBottom":"4px"}),
                    html.Div([pill("Speed Layer",A2)," Procesa datos recientes en RT"],
                        style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginBottom":"4px"}),
                    html.Div([pill("Serving Layer",A3)," Une ambas vistas para consultas"],
                        style={"color":ST,"fontFamily":FB,"fontSize":"12px"}),
                ])
            ])
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_pipeline():
    steps=[
        {"n":"01","t":"Ingesta","i":"📥","c":A,
         "d":"Captura de datos desde múltiples fuentes: APIs, sensores IoT, bases de datos, logs, archivos."},
        {"n":"02","t":"Almacenamiento","i":"🗄️","c":A2,
         "d":"Persistencia en Data Lakes (raw) o Data Warehouses (procesado). S3, HDFS, BigQuery."},
        {"n":"03","t":"Procesamiento","i":"⚙️","c":A3,
         "d":"Limpieza, transformación y enriquecimiento (ETL/ELT). Spark, Flink, dbt."},
        {"n":"04","t":"Análisis","i":"📊","c":A4,
         "d":"Exploración estadística, machine learning, consultas SQL. Jupyter, Databricks."},
        {"n":"05","t":"Visualización","i":"📈","c":A5,
         "d":"Dashboards, reportes y alertas en tiempo real. Tableau, Power BI, Grafana."},
        {"n":"06","t":"Acción","i":"🎯","c":A,
         "d":"Decisiones automatizadas o asistidas por humanos. El ciclo se retroalimenta."},
    ]
    scards=[html.Div([
        html.Div([
            html.Div(s["n"],style={"fontFamily":FD,"fontWeight":"800","fontSize":"11px","color":s["c"]}),
            html.Div(s["i"],style={"fontSize":"24px","margin":"4px 0"}),
            html.Div(s["t"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"14px","color":T}),
        ],style={"textAlign":"center","marginBottom":"8px"}),
        html.P(s["d"],style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4","margin":"0","textAlign":"center"})
    ],style={"background":CARD,"borderRadius":"12px","border":f"1px solid {s['c']}44",
              "padding":"14px","position":"relative"}) for s in steps]
    return sw("pipeline",[
        H("Pipeline de Datos"),S("El viaje de un dato: desde que nace hasta que genera valor."),
        html.Div(scards,style={"display":"grid","gridTemplateColumns":"repeat(3,1fr)","gap":"12px"}),
        C([
            html.Div("Conceptos clave del pipeline",style={"fontFamily":FD,"fontWeight":"700",
                       "fontSize":"15px","color":T,"marginBottom":"12px"}),
            html.Div([
                html.Div([
                    html.Div([pill("ETL",A)],style={"marginBottom":"4px"}),
                    html.P("Extract, Transform, Load — Transformar antes de cargar al destino.",
                        style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4","margin":"0"})
                ]),
                html.Div([
                    html.Div([pill("ELT",A2)],style={"marginBottom":"4px"}),
                    html.P("Extract, Load, Transform — Cargar primero, transformar en destino (enfoque moderno).",
                        style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4","margin":"0"})
                ]),
                html.Div([
                    html.Div([pill("Data Quality",A3)],style={"marginBottom":"4px"}),
                    html.P("Validación, limpieza y enriquecimiento continuo a lo largo de todo el pipeline.",
                        style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4","margin":"0"})
                ]),
                html.Div([
                    html.Div([pill("Observability",A4)],style={"marginBottom":"4px"}),
                    html.P("Monitoreo de latencia, errores y calidad del dato en cada etapa.",
                        style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4","margin":"0"})
                ]),
            ],style={"display":"grid","gridTemplateColumns":"repeat(4,1fr)","gap":"12px","marginTop":"0"})
        ],{"marginTop":"14px"})
    ])

def sl_almacen():
    opts=[
        {"icon":"🏛️","name":"Data Warehouse","c":A,
         "desc":"Almacén estructurado para datos históricos limpios y analizados. Óptimo para BI y reportes.",
         "pros":["Alta performance en consultas analíticas","Schema definido, fácil de usar","Datos limpios y confiables"],
         "cons":["Caro de escalar","Solo datos estructurados","No apto para ML en crudo"]},
        {"icon":"🏞️","name":"Data Lake","c":A2,
         "desc":"Repositorio de datos crudos en cualquier formato. Almacena todo, procesa después.",
         "pros":["Almacena cualquier tipo de dato","Muy barato (S3, GCS)","Ideal para ML y data science"],
         "cons":["Puede convertirse en 'data swamp'","Consultas más lentas","Gobernanza compleja"]},
        {"icon":"🏠","name":"Data Lakehouse","c":A3,
         "desc":"Lo mejor de ambos mundos: flexibilidad del Lake + performance del Warehouse.",
         "pros":["ACID transactions sobre datos crudos","Soporte para ML y BI","Delta Lake, Apache Iceberg"],
         "cons":["Tecnología más nueva","Requiere expertise","Tooling en evolución"]},
    ]
    def build(o):
        pros=[html.Div([html.Span("✓ ",style={"color":A3,"fontWeight":"700"}),p],
            style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginBottom":"3px"}) for p in o["pros"]]
        cons=[html.Div([html.Span("✗ ",style={"color":A5,"fontWeight":"700"}),c],
            style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginBottom":"3px"}) for c in o["cons"]]
        return C([
            html.Div(o["icon"],style={"fontSize":"30px","marginBottom":"8px"}),
            html.Div(o["name"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"17px","color":o["c"],"marginBottom":"6px"}),
            html.P(o["desc"],style={"color":ST,"fontFamily":FB,"fontSize":"13px","lineHeight":"1.5","marginBottom":"12px"}),
            html.Div([
                html.Div("Ventajas",style={"color":A3,"fontFamily":FD,"fontWeight":"700","fontSize":"12px","marginBottom":"4px"}),
                *pros,
                html.Div("Limitaciones",style={"color":A5,"fontFamily":FD,"fontWeight":"700","fontSize":"12px",
                                                 "marginBottom":"4px","marginTop":"8px"}),
                *cons
            ],style={"background":f"{BG}","borderRadius":"6px","padding":"10px"})
        ])
    return sw("almacen",[
        H("Almacenamiento: Warehouse, Lake y Lakehouse"),
        S("Tres paradigmas que evolucionaron para responder a los retos del Big Data."),
        html.Div([build(o) for o in opts],
                 style={"display":"grid","gridTemplateColumns":"repeat(3,1fr)","gap":"14px"}),
        html.Div([
            html.Div("💡 Tendencia actual: ",style={"color":A,"fontFamily":FD,"fontWeight":"700","fontSize":"14px"}),
            html.Span("Las empresas migran hacia el Lakehouse (Databricks, Snowflake, BigQuery) porque "
                      "unifica el stack para BI, ML y data engineering en una sola plataforma.",
                      style={"color":ST,"fontFamily":FB,"fontSize":"13px"})
        ],style={"marginTop":"14px","padding":"14px 18px","background":f"{A}10",
                  "borderRadius":"10px","border":f"1px solid {A}30"})
    ])

def sl_nosql():
    tipos=[
        {"icon":"📄","name":"Documentos","c":A,
         "ej":"MongoDB, CouchDB","d":"Almacena datos como documentos JSON/BSON. Ideal para catálogos, perfiles."},
        {"icon":"🔑","name":"Clave-Valor","c":A2,
         "ej":"Redis, DynamoDB","d":"Acceso O(1) por clave. Perfecto para cachés y sesiones de usuarios."},
        {"icon":"📊","name":"Columnar","c":A3,
         "ej":"Cassandra, HBase","d":"Optimizado para escrituras masivas y lectura por columnas. Para IoT y logs."},
        {"icon":"🕸️","name":"Grafos","c":A4,
         "ej":"Neo4j, Amazon Neptune","d":"Relaciones entre entidades. Redes sociales, recomendaciones, fraude."},
    ]
    ncards=[C([
        html.Div(nt["icon"],style={"fontSize":"28px","marginBottom":"8px"}),
        html.Div(nt["name"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"16px","color":nt["c"],"marginBottom":"4px"}),
        pill(nt["ej"],nt["c"]),
        html.P(nt["d"],style={"color":ST,"fontFamily":FB,"fontSize":"13px","lineHeight":"1.5","margin":"8px 0 0"})
    ]) for nt in tipos]
    return sw("nosql",[
        H("Bases de Datos NoSQL"),S("4 familias diseñadas para escalar horizontalmente sin límite."),
        html.Div([
            html.Div([
                html.Div(ncards[:2],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"10px","marginBottom":"10px"}),
                html.Div(ncards[2:],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"10px"}),
            ]),
            C([
                html.Div("SQL vs NoSQL — Comparativa",style={"fontFamily":FD,"fontWeight":"700","fontSize":"14px","color":T,"marginBottom":"4px"}),
                dcc.Graph(figure=ch_nosql(),config={"displayModeBar":False},style={"height":"330px"}),
                html.P("NoSQL no reemplaza SQL — los complementa. La elección depende del caso de uso.",
                    style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginTop":"8px","textAlign":"center"})
            ])
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_tecnologias():
    techs=[
        {"i":"🐘","n":"Hadoop HDFS","c":A,"r":"Sistema de archivos distribuido",
         "d":"Divide archivos en bloques de 128MB replicados en múltiples nodos. Tolerante a fallos."},
        {"i":"⚡","n":"Apache Spark","c":A2,"r":"Motor de cómputo en memoria",
         "d":"100× más rápido que Hadoop MapReduce. Soporta SQL, ML, streaming y grafos."},
        {"i":"📨","n":"Apache Kafka","c":A3,"r":"Bus de mensajes distribuido",
         "d":"Maneja millones de eventos/segundo. Usado por LinkedIn, Netflix, Uber."},
        {"i":"🗄️","n":"Apache Cassandra","c":A4,"r":"Base de datos NoSQL columnar",
         "d":"Escala horizontal sin límite, sin punto único de fallo. Netflix almacena 30 PB en ella."},
        {"i":"🌊","n":"Apache Flink","c":A5,"r":"Streaming en tiempo real",
         "d":"Procesamiento de eventos con latencia de milisegundos. Stateful computations."},
        {"i":"🐝","n":"Apache Hive","c":A,"r":"SQL sobre Hadoop",
         "d":"Permite consultar HDFS con sintaxis SQL. El puente entre analistas y Big Data."},
    ]
    tcards=[C([
        html.Div(t["i"],style={"fontSize":"22px"}),
        html.Div(t["n"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"15px","color":t["c"],"marginTop":"5px"}),
        html.Div(t["r"],style={"color":T,"fontFamily":FB,"fontSize":"12px","fontWeight":"500"}),
        html.P(t["d"],style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.5","margin":"6px 0 0"})
    ],{"padding":"14px"}) for t in techs]
    return sw("tecnologias",[
        H("Tecnologías Clave del Ecosistema"),S("El stack que hace posible capturar, procesar y analizar a escala."),
        html.Div([
            html.Div(tcards,style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"10px"}),
            C([html.Div("Adopción en la industria (2024)",style={"fontFamily":FD,"fontWeight":"700",
                         "fontSize":"14px","color":T,"marginBottom":"4px"}),
               dcc.Graph(figure=ch_techs(),config={"displayModeBar":False},style={"height":"320px"})])
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_mapreduce():
    return sw("mapreduce",[
        H("MapReduce — El Algoritmo que lo Cambió Todo"),
        S("El paradigma de programación que permitió procesar petabytes en clusters de computadoras baratas."),
        html.Div([
            C([
                html.Div("¿Cómo funciona?",style={"fontFamily":FD,"fontWeight":"700","fontSize":"16px","color":T,"marginBottom":"14px"}),
                *[html.Div([
                    html.Div(step["n"],style={"fontFamily":FD,"fontWeight":"800","fontSize":"14px","color":step["c"],"width":"28px"}),
                    html.Div([
                        html.Div(step["t"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"15px","color":step["c"]}),
                        html.Div(step["d"],style={"color":ST,"fontFamily":FB,"fontSize":"13px","lineHeight":"1.4","marginTop":"3px"})
                    ])
                ],style={"display":"flex","gap":"10px","marginBottom":"14px","padding":"10px 12px",
                          "background":f"{BG}","borderRadius":"8px"})
                for step in [
                    {"n":"1","c":A,"t":"Input — División del problema",
                     "d":"El dataset gigante se divide en chunks independientes distribuidos en el cluster."},
                    {"n":"2","c":A2,"t":"Map — Transformación en paralelo",
                     "d":"Cada nodo aplica una función map() a su chunk. Ej: contar palabras en un documento."},
                    {"n":"3","c":A3,"t":"Shuffle — Agrupación por clave",
                     "d":"El sistema agrupa automáticamente todos los resultados con la misma clave en el mismo nodo."},
                    {"n":"4","c":A4,"t":"Reduce — Aggregación final",
                     "d":"Cada nodo aplica reduce() a su grupo. Ej: sumar los conteos de la misma palabra."},
                    {"n":"5","c":A5,"t":"Output — Resultado unificado",
                     "d":"Los resultados se consolidan y escriben. El problema se resolvió en paralelo."},
                ]],
                html.Div([
                    html.Div("Ejemplo clásico:",style={"color":A,"fontFamily":FD,"fontWeight":"700","fontSize":"13px"}),
                    html.Div('Contar palabras en 10 TB de texto → Map emite ("palabra", 1) → Shuffle agrupa → Reduce suma',
                        style={"fontFamily":"'Courier New',monospace","color":A3,"fontSize":"12px",
                               "background":BG,"padding":"8px","borderRadius":"6px","marginTop":"6px"})
                ],style={"marginTop":"8px"})
            ]),
            html.Div([
                C([html.Div("Flujo de reducción",style={"fontFamily":FD,"fontWeight":"700","fontSize":"14px","color":T,"marginBottom":"4px"}),
                   dcc.Graph(figure=ch_mapreduce(),config={"displayModeBar":False},style={"height":"280px"})]),
                html.Div(style={"height":"10px"}),
                C([
                    html.Div("Ventajas clave",style={"fontFamily":FD,"fontWeight":"700","fontSize":"14px","color":T,"marginBottom":"10px"}),
                    *[html.Div([html.Span("→ ",style={"color":v["c"]}),
                                html.Span(v["t"],style={"color":T,"fontFamily":FD,"fontWeight":"700","fontSize":"13px"}),
                                html.Span(f" — {v['d']}",style={"color":ST,"fontFamily":FB,"fontSize":"12px"})],
                               style={"marginBottom":"8px"})
                      for v in [
                          {"c":A,"t":"Tolerancia a fallos","d":"Si un nodo falla, el trabajo se reasigna automáticamente."},
                          {"c":A2,"t":"Escalabilidad lineal","d":"Añadir más nodos reduce el tiempo proporcionalmente."},
                          {"c":A3,"t":"Localidad de datos","d":"El cómputo va donde están los datos, no al revés."},
                      ]]
                ])
            ])
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_batch_stream():
    return sw("batch-stream",[
        H("Batch vs Streaming"),S("Dos paradigmas de procesamiento para necesidades distintas."),
        html.Div([
            C([
                html.Div("🗂️ Procesamiento Batch",style={"fontFamily":FD,"fontWeight":"700","fontSize":"18px","color":A,"marginBottom":"12px"}),
                html.P("Procesa grandes volúmenes de datos acumulados en intervalos definidos. "
                       "Óptimo cuando la latencia no es crítica.",
                    style={"color":ST,"fontFamily":FB,"fontSize":"14px","lineHeight":"1.6","marginBottom":"14px"}),
                *[html.Div([html.Span(t+" ",style={"color":A,"fontWeight":"700"}),
                             html.Span(d,style={"color":ST,"fontFamily":FB,"fontSize":"13px"})],
                            style={"marginBottom":"8px"})
                  for t,d in [
                      ("Latencia:","Minutos → Horas → Días"),
                      ("Ejemplo:","Generar reporte de ventas mensual"),
                      ("Herramientas:","Hadoop MapReduce, Spark Batch, Hive"),
                      ("Casos:","Nóminas, facturación, reportes BI, ML training"),
                  ]],
                html.Div([
                    html.Div("Ventajas",style={"color":A3,"fontFamily":FD,"fontWeight":"700","fontSize":"13px","marginBottom":"6px"}),
                    html.Div("✓ Muy eficiente para grandes volúmenes",style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginBottom":"3px"}),
                    html.Div("✓ Más fácil de implementar y depurar",style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginBottom":"3px"}),
                    html.Div("✓ Óptimo en uso de recursos",style={"color":ST,"fontFamily":FB,"fontSize":"12px"}),
                ],style={"background":BG,"borderRadius":"6px","padding":"10px","marginTop":"12px"})
            ]),
            html.Div([
                html.Div("VS",style={"fontFamily":FD,"fontWeight":"800","fontSize":"24px",
                                      "color":BD,"textAlign":"center","margin":"auto"})
            ],style={"display":"flex","alignItems":"center","justifyContent":"center"}),
            C([
                html.Div("🌊 Procesamiento Streaming",style={"fontFamily":FD,"fontWeight":"700","fontSize":"18px","color":A2,"marginBottom":"12px"}),
                html.P("Procesa cada evento en el instante en que llega. Indispensable cuando "
                       "cada milisegundo cuenta.",
                    style={"color":ST,"fontFamily":FB,"fontSize":"14px","lineHeight":"1.6","marginBottom":"14px"}),
                *[html.Div([html.Span(t+" ",style={"color":A2,"fontWeight":"700"}),
                             html.Span(d,style={"color":ST,"fontFamily":FB,"fontSize":"13px"})],
                            style={"marginBottom":"8px"})
                  for t,d in [
                      ("Latencia:","Milisegundos → Segundos"),
                      ("Ejemplo:","Detectar fraude en transacción bancaria"),
                      ("Herramientas:","Kafka Streams, Apache Flink, Spark Streaming"),
                      ("Casos:","Monitoreo IoT, trading HFT, alertas en tiempo real"),
                  ]],
                html.Div([
                    html.Div("Ventajas",style={"color":A3,"fontFamily":FD,"fontWeight":"700","fontSize":"13px","marginBottom":"6px"}),
                    html.Div("✓ Respuesta inmediata a eventos",style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginBottom":"3px"}),
                    html.Div("✓ Siempre actualizado",style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginBottom":"3px"}),
                    html.Div("✓ Detecta anomalías al instante",style={"color":ST,"fontFamily":FB,"fontSize":"12px"}),
                ],style={"background":BG,"borderRadius":"6px","padding":"10px","marginTop":"12px"})
            ]),
        ],style={"display":"grid","gridTemplateColumns":"1fr auto 1fr","gap":"10px","alignItems":"start"}),
        html.Div([
            html.Div("🔑 Regla práctica: ",style={"color":A4,"fontFamily":FD,"fontWeight":"700","fontSize":"14px"}),
            html.Span("¿Necesitas actuar en menos de 1 segundo? → Streaming. ¿En minutos o más? → Batch. "
                      "Las arquitecturas modernas (Lambda/Kappa) combinan ambos según el caso.",
                      style={"color":ST,"fontFamily":FB,"fontSize":"14px"})
        ],style={"marginTop":"14px","padding":"14px 18px","background":f"{A4}10",
                  "borderRadius":"10px","border":f"1px solid {A4}30"})
    ])

def sl_ml_bd():
    return sw("ml-bd",[
        H("Big Data + Machine Learning"),S("Por qué más datos no solo ayuda, sino que es el factor diferenciador."),
        html.Div([
            html.Div([
                C([
                    html.Div("La ley de los datos",style={"fontFamily":FD,"fontWeight":"700","fontSize":"16px","color":T,"marginBottom":"4px"}),
                    dcc.Graph(figure=ch_ml_data(),config={"displayModeBar":False},style={"height":"270px"}),
                    html.P("Los algoritmos de Deep Learning siguen mejorando con más datos, mientras que el ML "
                           "clásico llega a un techo. Big Data rompe ese techo.",
                        style={"color":ST,"fontFamily":FB,"fontSize":"12px","marginTop":"8px","textAlign":"center"})
                ]),
            ]),
            html.Div([
                *[icard(it["i"],it["t"],it["d"],it["c"]) for it in [
                    {"i":"🧠","t":"Entrenamiento de LLMs","c":A,
                     "d":"GPT-4 fue entrenado con ~45 TB de texto. Sin Big Data, los LLMs no existen."},
                    {"i":"🎯","t":"Sistemas de Recomendación","c":A2,
                     "d":"Netflix y Spotify procesan billones de interacciones para personalizar cada usuario."},
                    {"i":"🔍","t":"Detección de Anomalías","c":A3,
                     "d":"Los bancos analizan millones de transacciones para encontrar el 0.01% fraudulento."},
                    {"i":"🚗","t":"Vehículos Autónomos","c":A4,
                     "d":"Tesla Fleet Learning: millones de kilómetros reales mejoran el modelo continuamente."},
                ]],
            ],style={"display":"flex","flexDirection":"column","gap":"10px"})
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_cloud():
    providers=[
        {"logo":"☁️","name":"Amazon Web Services","short":"AWS","c":A4,
         "services":["S3 (Data Lake)","Redshift (DW)","EMR (Spark)","Kinesis (Streaming)","SageMaker (ML)"]},
        {"logo":"🔵","name":"Microsoft Azure","short":"Azure","c":"#0078D4",
         "services":["Azure Data Lake","Synapse Analytics","HDInsight","Event Hubs","Azure ML"]},
        {"logo":"🟡","name":"Google Cloud Platform","short":"GCP","c":"#4285F4",
         "services":["BigQuery","Dataflow","Dataproc","Pub/Sub","Vertex AI"]},
    ]
    pcards=[C([
        html.Div([html.Span(p["logo"],style={"fontSize":"22px","marginRight":"8px"}),
                  html.Span(p["name"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"15px","color":p["c"]})]),
        html.Div([html.Div([html.Span("• ",style={"color":p["c"]}),
                             html.Span(s,style={"color":ST,"fontFamily":FB,"fontSize":"12px"})])
                  for s in p["services"]],style={"marginTop":"10px"})
    ]) for p in providers]
    return sw("cloud",[
        H("Big Data en la Nube"),S("La nube democratizó el Big Data: ya no necesitas un datacenter propio."),
        html.Div([
            html.Div([
                html.Div(pcards,style={"display":"flex","flexDirection":"column","gap":"10px"}),
                html.Div([
                    html.Div("💡 Beneficio clave: ",style={"color":A,"fontFamily":FD,"fontWeight":"700","fontSize":"14px"}),
                    html.Span("Paga solo por lo que usas. Una startup puede procesar petabytes "
                              "sin comprar hardware.",
                              style={"color":ST,"fontFamily":FB,"fontSize":"13px"})
                ],style={"marginTop":"10px","padding":"12px 14px","background":f"{A}10",
                          "borderRadius":"8px","border":f"1px solid {A}30"})
            ]),
            C([
                html.Div("Cuota de mercado cloud (2024)",style={"fontFamily":FD,"fontWeight":"700","fontSize":"14px","color":T,"marginBottom":"4px"}),
                dcc.Graph(figure=ch_cloud_share(),config={"displayModeBar":False},style={"height":"270px"}),
                html.Div([
                    *[html.Div([
                        html.Div([pill(t,c)],style={"marginBottom":"4px"}),
                        html.P(d,style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4","margin":"0"})
                    ],style={"marginBottom":"10px"})
                    for t,c,d in [
                        ("Serverless",A,"Lambda, Cloud Functions — ejecuta código sin gestionar servidores."),
                        ("Data Mesh",A2,"Arquitectura que descentraliza la propiedad de los datos por dominio."),
                        ("MLOps",A3,"Automatización del ciclo de vida de los modelos ML en producción."),
                    ]]
                ])
            ])
        ],style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"14px"})
    ])

def sl_casos():
    casos=[
        {"i":"🎬","co":"Netflix","c":A,
         "d":"Analiza 250M de perfiles para personalizar. El motor de recomendaciones genera el 80% del contenido consumido.",
         "kpi":"$1B/año ahorrado en churn gracias a recomendaciones"},
        {"i":"🏥","co":"Mayo Clinic","c":A2,
         "d":"Cruza historial de millones de pacientes para diagnóstico predictivo con 94% de precisión en ciertas enfermedades.",
         "kpi":"Detección temprana de sepsis: reducción 20% mortalidad"},
        {"i":"🛍️","co":"Amazon","c":A3,
         "d":"Sistema de recomendación procesa billones de clicks. Anticipatory shipping: envía antes de que compres.",
         "kpi":"35% de ingresos provienen de recomendaciones"},
        {"i":"🚗","co":"Tesla","c":A4,
         "d":"Fleet Learning: cada auto envía datos de conducción. El modelo mejora para todos simultáneamente.",
         "kpi":"4M de millas de datos reales procesados por día"},
        {"i":"🌦️","co":"The Weather Company","c":A5,
         "d":"Procesa 400TB de datos meteorológicos diarios para predicciones hiperlocales.",
         "kpi":"25B de predicciones meteorológicas diarias"},
        {"i":"🏦","co":"JPMorgan Chase","c":A,
         "d":"Analiza millones de transacciones en tiempo real para detectar fraude con ML.",
         "kpi":"Fraude reducido un 50% con ML + Big Data"},
    ]
    ccards=[C([
        html.Div(ca["i"]+" "+ca["co"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"16px","color":ca["c"],"marginBottom":"8px"}),
        html.P(ca["d"],style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.5","marginBottom":"8px"}),
        html.Div([html.Span("📈 ",),ca["kpi"]],
            style={"color":ca["c"],"fontFamily":FB,"fontSize":"11px","fontStyle":"italic",
                   "background":f"{ca['c']}10","padding":"6px 8px","borderRadius":"6px"})
    ],{"padding":"14px"}) for ca in casos]
    return sw("casos",[
        H("Casos de Uso Reales"),S("Cómo las empresas más grandes del mundo usan Big Data hoy."),
        html.Div([
            html.Div(ccards,style={"display":"grid","gridTemplateColumns":"1fr 1fr 1fr","gap":"10px"}),
            html.Div([
                html.Br(),
                C([html.Div("Tasa de adopción por sector",
                             style={"fontFamily":FD,"fontWeight":"700","fontSize":"14px","color":T,"marginBottom":"4px"}),
                   dcc.Graph(figure=ch_sectors(),config={"displayModeBar":False},style={"height":"240px"})])
            ])
        ],style={"display":"flex","flexDirection":"column","gap":"12px"})
    ])

def sl_escala():
    return sw("escala",[
        H("La Escala Global"),S("Números que ponen en perspectiva el tamaño del universo de datos."),
        C([html.Div("Datos generados globalmente (Zettabytes)",style={"fontFamily":FD,"fontWeight":"700","fontSize":"15px","color":T,"marginBottom":"4px"}),
           dcc.Graph(figure=ch_growth(),config={"displayModeBar":False},style={"height":"270px"})]),
        html.Div([
            stat("90%","de los datos del mundo se crearon en los últimos 2 años",A),
            stat("44 ZB","volumen del datasphere en 2023",A2),
            stat("175 ZB","proyección para 2025",A3),
            stat("3.5 B","búsquedas Google/día",A4),
            stat("5 B","videos vistos en YouTube/día",A5),
            stat("65K","transacciones Visa/segundo",A),
        ],style={"display":"grid","gridTemplateColumns":"repeat(6,1fr)","gap":"8px","marginTop":"14px"}),
        html.Div([
            html.Div("Para visualizar 1 Zettabyte:",style={"color":A,"fontFamily":FD,"fontWeight":"700","fontSize":"14px","marginBottom":"8px"}),
            html.Div([
                html.Div("Si cada byte fuera un grano de arena, llenarías 250 planetas Tierra.",
                    style={"color":ST,"fontFamily":FB,"fontSize":"13px","marginBottom":"4px"}),
                html.Div("Si grabases 1 ZB en DVDs estándar, la pila llegaría a 2/3 partes del camino a la Luna.",
                    style={"color":ST,"fontFamily":FB,"fontSize":"13px"}),
            ])
        ],style={"marginTop":"14px","padding":"14px 18px","background":f"{A}10",
                  "borderRadius":"10px","border":f"1px solid {A}30"})
    ])

def sl_profesiones():
    roles=[
        {"i":"🔍","r":"Data Analyst","c":A,"sal":"~$55k",
         "d":"Explora y visualiza datos para responder preguntas de negocio. SQL, Excel, Tableau."},
        {"i":"🏗️","r":"Data Engineer","c":A2,"sal":"~$85k",
         "d":"Construye y mantiene los pipelines de datos. Python, Spark, Kafka, SQL."},
        {"i":"🤖","r":"ML Engineer","c":A3,"sal":"~$105k",
         "d":"Lleva modelos de ML a producción y los escala. Python, Docker, Kubernetes, MLflow."},
        {"i":"🧪","r":"Data Scientist","c":A4,"sal":"~$110k",
         "d":"Crea modelos predictivos y encuentra insights profundos. Python, R, estadística, ML."},
        {"i":"🏛️","r":"Data Architect","c":A5,"sal":"~$130k",
         "d":"Diseña la arquitectura de datos de la organización. Cloud, data modeling, gobernanza."},
        {"i":"👑","r":"Chief Data Officer","c":A,"sal":"~$180k",
         "d":"Dirige la estrategia de datos de toda la empresa. Liderazgo, estrategia, política."},
    ]
    rcards=[C([
        html.Div(r["i"],style={"fontSize":"24px","marginBottom":"6px"}),
        html.Div(r["r"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"15px","color":r["c"],"marginBottom":"2px"}),
        html.Div(r["sal"]+" / año (EE.UU. promedio)",style={"color":A4,"fontFamily":FB,"fontSize":"12px","marginBottom":"6px"}),
        html.P(r["d"],style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4","margin":"0"})
    ],{"padding":"14px"}) for r in roles]
    return sw("profesiones",[
        H("Profesiones en el Ecosistema Big Data"),S("Roles, responsabilidades y salarios promedio en el mercado global."),
        html.Div([
            html.Div(rcards,style={"display":"grid","gridTemplateColumns":"1fr 1fr 1fr","gap":"10px"}),
            C([html.Div("Salario promedio anual (USD, EE.UU.)",style={"fontFamily":FD,"fontWeight":"700","fontSize":"14px","color":T,"marginBottom":"4px"}),
               dcc.Graph(figure=ch_salaries(),config={"displayModeBar":False},style={"height":"270px"}),
               html.P("Fuente: Bureau of Labor Statistics, LinkedIn Salary, Glassdoor 2024. "
                      "En Latinoamérica los rangos son 30-50% menores, pero la demanda crece al mismo ritmo.",
                   style={"color":ST,"fontFamily":FB,"fontSize":"11px","marginTop":"8px"})
            ],{"marginTop":"12px"})
        ],style={"display":"flex","flexDirection":"column","gap":"12px"})
    ])

def sl_retos():
    retos=[
        {"i":"🔒","t":"Privacidad y Regulación","c":A,
         "d":"GDPR (Europa) y CCPA (California) obligan a anonimizar datos, obtener consentimiento y garantizar el 'derecho al olvido'."},
        {"i":"🧹","t":"Calidad del Dato","c":A2,
         "d":"'Garbage in, garbage out'. IBM estima que datos de mala calidad cuestan $3.1T/año. La limpieza consume el 80% del tiempo."},
        {"i":"⚡","t":"Consumo Energético","c":A3,
         "d":"Los centros de datos consumen ~1-2% de la electricidad global. Un entrenamiento de GPT-3 = 500 toneladas de CO₂."},
        {"i":"🧠","t":"Escasez de Talento","c":A4,
         "d":"Hay más ofertas de Data Scientist que personas calificadas. El déficit global supera los 250,000 profesionales."},
        {"i":"🕵️","t":"Seguridad y Brechas","c":A5,
         "d":"A mayor concentración de datos, mayor el blanco para ataques. La brecha de Facebook (2019) expuso 533M de registros."},
        {"i":"⚖️","t":"Sesgo Algorítmico","c":A,
         "d":"Los modelos entrenados con datos sesgados producen decisiones sesgadas. Discriminación racial, de género o socioeconómica."},
    ]
    rcards=[C([
        html.Div(r["i"]+" "+r["t"],style={"fontFamily":FD,"fontWeight":"700","fontSize":"14px","color":r["c"],"marginBottom":"8px"}),
        html.P(r["d"],style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.5","margin":"0"})
    ]) for r in retos]
    futuro=[
        (A,"Edge Computing","Procesamiento en el dispositivo (IoT), latencia cero, no depende de la red."),
        (A2,"IA + Big Data","Ciclo virtuoso: más datos → mejores modelos → más valor → más datos."),
        (A3,"Computación Cuántica","Podría resolver en segundos problemas que hoy toman meses."),
        (A4,"Synthetic Data","Generar datos artificiales para entrenar modelos sin violar privacidad."),
        (A5,"Data as a Product","Cada dataset tratado como producto con dueño, SLA y usuarios."),
    ]
    frows=[html.Div([
        html.Div(style={"width":"7px","height":"7px","borderRadius":"50%","background":c,
                         "flexShrink":"0","marginTop":"5px"}),
        html.Div([
            html.Span(t+" — ",style={"color":c,"fontFamily":FD,"fontWeight":"700","fontSize":"13px"}),
            html.Span(d,style={"color":ST,"fontFamily":FB,"fontSize":"12px","lineHeight":"1.4"})
        ])
    ],style={"display":"flex","gap":"10px","marginBottom":"10px"}) for c,t,d in futuro]
    return sw("retos",[
        H("Retos Actuales y el Futuro"),S("Los desafíos que enfrenta el ecosistema Big Data en 2024-2025."),
        html.Div([
            html.Div(rcards,style={"display":"grid","gridTemplateColumns":"1fr 1fr 1fr","gap":"10px"}),
            C([
                html.Div("🚀 Tendencias que vienen",style={"fontFamily":FD,"fontWeight":"800","fontSize":"18px","color":A,"marginBottom":"16px"}),
                html.Div(frows)
            ],{"marginTop":"12px"})
        ],style={"display":"flex","flexDirection":"column","gap":"12px"})
    ])

def sl_cierre():
    puntos=[
        ("Big Data","es el conjunto de tecnologías para capturar, procesar y analizar datos a escala masiva.",A),
        ("Las 5 V's","definen cualquier sistema de Big Data: Volumen, Velocidad, Variedad, Veracidad y Valor.",A2),
        ("Estructura","Los datos pueden ser estructurados (SQL), semi-estructurados (JSON) o no estructurados (texto, imagen).",A3),
        ("Pipeline","Todo dato sigue un pipeline: ingesta → almacenamiento → procesamiento → análisis → acción.",A4),
        ("Tecnologías","Hadoop, Spark, Kafka, Cassandra y la nube (AWS/GCP/Azure) son el stack moderno.",A5),
        ("ML + Big Data","Más datos = mejores modelos. El Big Data y la IA son inseparables.",A),
        ("Oportunidad","Es un campo en déficit de talento. Hay carrera profesional enorme por delante.",A2),
    ]
    rows=[html.Div([
        html.Div(style={"width":"6px","height":"6px","borderRadius":"50%","background":c,
                         "flexShrink":"0","marginTop":"6px"}),
        html.Div([
            html.Span(t+" — ",style={"color":c,"fontFamily":FD,"fontWeight":"700","fontSize":"14px"}),
            html.Span(d,style={"color":ST,"fontFamily":FB,"fontSize":"14px","lineHeight":"1.4"})
        ])
    ],style={"display":"flex","gap":"10px","marginBottom":"10px"}) for t,d,c in puntos]
    return sw("cierre",[
        html.Div([
            html.Div(style={"position":"absolute","inset":"0",
                "background":f"radial-gradient(ellipse 60% 50% at 50% 30%, {A3}12, transparent 70%)",
                "pointerEvents":"none"}),
            html.Div([
                pill("Resumen Final",A3),
                html.Br(),html.Br(),
                html.H2("Puntos Clave de la Exposición",style={"fontFamily":FD,"fontSize":"28px","color":T,"marginBottom":"16px"}),
                html.Div(rows),
                html.Div([
                    html.Div("🎯",style={"fontSize":"28px","marginBottom":"8px"}),
                    html.Div('"El objetivo del Big Data no es tener más datos.',style={"color":A,"fontFamily":FD,"fontWeight":"700","fontSize":"16px"}),
                    html.Div('Es tomar mejores decisiones más rápido."',style={"color":A,"fontFamily":FD,"fontWeight":"700","fontSize":"16px"}),
                    html.Div("— Filosofía central del campo",style={"color":ST,"fontFamily":FB,"fontSize":"13px","marginTop":"6px"})
                ],style={"marginTop":"20px","padding":"16px 20px","background":f"{A}10",
                          "borderRadius":"10px","border":f"1px solid {A}30","textAlign":"center"}),
                html.Div([
                    stat("40 min","de exposición completados",A),
                    stat("21","temas cubiertos",A2),
                    stat("∞","posibilidades en este campo",A3),
                ],style={"display":"flex","gap":"6px","marginTop":"24px","justifyContent":"center"})
            ],style={"position":"relative","zIndex":"1","padding":"48px 44px"})
        ],style={"minHeight":"480px","position":"relative",
                 "background":f"linear-gradient(135deg,{BG},{SFC})",
                 "borderRadius":"20px","overflow":"hidden","border":f"1px solid {BD}"})
    ])

# ─── Layout ───────────────────────────────────────────────────────────────────
dots=[html.Div(id=f"dot-{i}",style={
    "width":"7px","height":"7px","borderRadius":"50%",
    "background":A if i==0 else BD,"display":"inline-block","cursor":"pointer","title":TITLES[i]
}) for i in range(len(SLIDES))]

app.layout=html.Div([
    GFONTS,
    html.Div([
        # Header
        html.Div([
            html.Div([
                html.Span("●",style={"color":A,"fontSize":"10px","animation":"pulse 2s infinite"}),
                html.Span(" Big Data",style={"fontFamily":FD,"fontWeight":"800","fontSize":"16px","color":T,"marginLeft":"6px"})
            ],style={"display":"flex","alignItems":"center"}),
            html.Div(id="counter",style={"fontFamily":FB,"fontSize":"13px","color":ST})
        ],style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                  "padding":"14px 28px","borderBottom":f"1px solid {BD}",
                  "background":f"{SFC}cc","backdropFilter":"blur(10px)",
                  "position":"sticky","top":"0","zIndex":"100"}),
        # Progress
        html.Div(html.Div(id="prog",style={"height":"2px","background":f"linear-gradient(90deg,{A},{A2})",
            "width":"0%","transition":"width .4s ease","borderRadius":"2px"}),
            style={"background":BD,"height":"2px"}),
        # Slides
        html.Div([
            sl_portada(),sl_agenda(),sl_que_es(),sl_historia(),sl_datos_info(),
            sl_5v(),sl_estructura(),sl_arquitecturas(),sl_pipeline(),sl_almacen(),
            sl_nosql(),sl_tecnologias(),sl_mapreduce(),sl_batch_stream(),sl_ml_bd(),
            sl_cloud(),sl_casos(),sl_escala(),sl_profesiones(),sl_retos(),sl_cierre(),
        ],style={"padding":"24px","minHeight":"calc(100vh - 120px)"}),
        # Footer
        html.Div([
            html.Button("← Anterior",id="btn-prev",n_clicks=0,className="nav-btn"),
            html.Div(dots,style={"display":"flex","gap":"6px","alignItems":"center","flexWrap":"wrap","maxWidth":"300px","justifyContent":"center"}),
            html.Button("Siguiente →",id="btn-next",n_clicks=0,className="nav-btn"),
        ],style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                  "padding":"14px 28px","borderTop":f"1px solid {BD}","background":f"{SFC}cc"}),
    ],style={"maxWidth":"1100px","margin":"0 auto","minHeight":"100vh","display":"flex","flexDirection":"column"}),
    dcc.Store(id="slide-idx",data=0),
],style={"background":BG,"minHeight":"100vh"})

# ─── Callbacks ────────────────────────────────────────────────────────────────
@app.callback(Output("slide-idx","data"),
    Input("btn-prev","n_clicks"),Input("btn-next","n_clicks"),
    dash.dependencies.State("slide-idx","data"),prevent_initial_call=True)
def nav(p,n,cur):
    btn=dash.callback_context.triggered[0]["prop_id"]
    return min(cur+1,len(SLIDES)-1) if "next" in btn else max(cur-1,0)

@app.callback(
    [Output(f"slide-{s}","style") for s in SLIDES]+
    [Output(f"dot-{i}","style") for i in range(len(SLIDES))]+
    [Output("counter","children"),Output("prog","style")],
    Input("slide-idx","data"))
def update(idx):
    ss=[{"display":"block","animation":"fadeSlide .45s ease forwards"} if i==idx
        else {"display":"none"} for i in range(len(SLIDES))]
    ds=[{"width":"10px" if i==idx else "7px","height":"10px" if i==idx else "7px",
         "borderRadius":"50%","background":A if i==idx else BD,"display":"inline-block",
         "transition":"all .25s ease","boxShadow":f"0 0 8px {A}88" if i==idx else "none","cursor":"pointer"}
        for i in range(len(SLIDES))]
    pct=round((idx/(len(SLIDES)-1))*100)
    prog={"height":"2px","background":f"linear-gradient(90deg,{A},{A2})",
          "width":f"{pct}%","transition":"width .4s ease","borderRadius":"2px"}
    return ss+ds+[f"{TITLES[idx]}  ·  {idx+1} / {len(SLIDES)}",prog]
server = app.server
if __name__=="__main__":
    app.run(debug=True,port=8050)