# ============================================================================
# DASHBOARD MATRIZ ENERGÉTICA COLOMBIA
# Proyecto Curso Talento Tech - Análisis de Datos
# Autor: Michely Muñoz
# ============================================================================

import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Matriz Energética Colombia | Talento Tech",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================================
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 2rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# CONEXIÓN A BASE DE DATOS
# ============================================================================
@st.cache_resource
def init_connection():
    """Inicializa la conexión a MySQL"""
    try:
        conn = mysql.connector.connect(
            host=st.secrets.get("DB_HOST", "localhost"),
            user=st.secrets.get("DB_USER", "root"),
            password=st.secrets.get("DB_PASSWORD", ""),
            database=st.secrets.get("DB_NAME", "bd_matriz_energetica_colombia"),
            port=st.secrets.get("DB_PORT", 3306)
        )
        return conn
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

@st.cache_data
def run_query(query, params=None):
    """Ejecuta consultas SQL y retorna DataFrame"""
    conn = init_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=params)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error en consulta: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# ============================================================================
# PÁGINA DE INICIO (LANDING PAGE)
# ============================================================================
def landing_page():
    """Muestra la página de aterrizaje del proyecto"""
    
    # Header principal
    st.markdown('<h1 class="main-header">⚡ Matriz Energética Colombia</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Dashboard de Análisis de Datos - Curso Talento Tech</p>', unsafe_allow_html=True)
    
    # Columnas de información
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image("https://img.icons8.com/color/200/000000/electricity.png", width=150)
        
        st.markdown("""
        ### 📊 Sobre este Proyecto
        
        Este dashboard presenta un análisis completo de la matriz energética de Colombia, 
        permitiendo visualizar métricas clave de generación, demanda, costos e impacto ambiental.
        
        **Objetivos del Análisis:**
        - 📈 Monitorear la generación de energía por tipo
        - 💰 Analizar costos e inversiones del sector
        - 🌱 Evaluar impacto ambiental (emisiones CO2)
        - 📅 Identificar tendencias históricas
        
        **Tecnologías Utilizadas:**
        - Python + Streamlit
        - MySQL Database
        - Plotly para visualizaciones
        - Pandas para análisis de datos
        """)
        
        # Botón de navegación
        if st.button("🚀 Ir al Dashboard", type="primary", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()
    
    # Footer con información del autor
    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.markdown("""
        <div style="text-align: center;">
            <p><strong>Elaborado por:</strong> Michely Muñoz</p>
            <p><strong>Curso:</strong> Talento Tech - Análisis de Datos</p>
            <p><strong>Fecha:</strong> """ + datetime.now().strftime("%Y") + """</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD PRINCIPAL
# ============================================================================
def dashboard_page():
    """Muestra el dashboard de análisis"""
    
    # Sidebar de navegación
    st.sidebar.image("https://img.icons8.com/color/96/000000/electricity.png", width=80)
    st.sidebar.title("📊 Navegación")
    
    # Selección de página
    page = st.sidebar.radio(
        "Ir a:",
        ["🏠 Inicio", "📈 Resumen General", "⚡ Tipos de Energía", "📅 Análisis Temporal", "🌱 Impacto Ambiental", "📊 Datos Crudos"],
        index=1
    )
    
    # Botón para volver al inicio
    if st.sidebar.button("🏠 Volver al Inicio"):
        st.session_state['page'] = 'landing'
        st.rerun()
    
    # Información del autor en sidebar
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Autor:** Michely Muñoz  
    **Curso:** Talento Tech  
    **Proyecto:** Análisis de Datos
    """)
    
    # ========================================================================
    # PÁGINA: RESUMEN GENERAL
    # ========================================================================
    if page == "📈 Resumen General":
        st.title("📈 Resumen General - Matriz Energética")
        st.markdown("Vista panorámica de los indicadores clave del sistema energético")
        
        # Cargar datos de KPIs
        query_kpi = """
        SELECT 
            COUNT(DISTINCT e.id_estadistica) as total_registros,
            ROUND(SUM(e.generacion_gwh), 2) as total_generacion_gwh,
            ROUND(SUM(e.demanda_gwh), 2) as total_demanda_gwh,
            ROUND(AVG(e.porcentaje_cobertura), 2) as cobertura_promedio,
            ROUND(SUM(e.inversion_usd_millones), 2) as inversion_total,
            ROUND(SUM(e.emisiones_co2_toneladas), 2) as emisiones_totales
        FROM estadisticas_energia e
        """
        df_kpi = run_query(query_kpi)
        
        if not df_kpi.empty:
            # KPIs en columnas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="⚡ Generación Total (GWh)",
                    value=f"{df_kpi['total_generacion_gwh'][0]:,.2f}" if df_kpi['total_generacion_gwh'][0] else "0.00",
                    delta="Acumulado histórico"
                )
            
            with col2:
                st.metric(
                    label="📊 Demanda Total (GWh)",
                    value=f"{df_kpi['total_demanda_gwh'][0]:,.2f}" if df_kpi['total_demanda_gwh'][0] else "0.00",
                    delta="Acumulado histórico"
                )
            
            with col3:
                st.metric(
                    label="🎯 Cobertura Promedio (%)",
                    value=f"{df_kpi['cobertura_promedio'][0]:.2f}" if df_kpi['cobertura_promedio'][0] else "0.00",
                    delta="Sistema nacional"
                )
            
            with col4:
                st.metric(
                    label="💰 Inversión Total (USD M)",
                    value=f"${df_kpi['inversion_total'][0]:,.2f}" if df_kpi['inversion_total'][0] else "0.00",
                    delta="Millones de dólares"
                )
            
            st.markdown("---")
            
            # Gráfico de generación vs demanda
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                query_gen_dem = """
                SELECT 
                    p.anio,
                    ROUND(SUM(e.generacion_gwh), 2) as generacion,
                    ROUND(SUM(e.demanda_gwh), 2) as demanda
                FROM estadisticas_energia e
                JOIN periodo p ON e.id_periodo = p.id_periodo
                GROUP BY p.anio
                ORDER BY p.anio
                """
                df_gen_dem = run_query(query_gen_dem)
                
                if not df_gen_dem.empty:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=df_gen_dem['anio'],
                        y=df_gen_dem['generacion'],
                        name='Generación (GWh)',
                        marker_color='#1f77b4'
                    ))
                    fig.add_trace(go.Bar(
                        x=df_gen_dem['anio'],
                        y=df_gen_dem['demanda'],
                        name='Demanda (GWh)',
                        marker_color='#ff7f0e'
                    ))
                    fig.update_layout(
                        title="📊 Generación vs Demanda por Año",
                        xaxis_title="Año",
                        yaxis_title="GWh",
                        barmode='group',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col_g2:
                query_cobertura = """
                SELECT 
                    te.nombre as tipo_energia,
                    ROUND(AVG(e.porcentaje_cobertura), 2) as cobertura_promedio
                FROM estadisticas_energia e
                JOIN tipo_energia te ON e.id_tipo_energia = te.id_tipo_energia
                GROUP BY te.id_tipo_energia, te.nombre
                ORDER BY cobertura_promedio DESC
                """
                df_cobertura = run_query(query_cobertura)
                
                if not df_cobertura.empty:
                    fig = px.pie(
                        df_cobertura,
                        values='cobertura_promedio',
                        names='tipo_energia',
                        title='🎯 Cobertura por Tipo de Energía',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.warning("⚠️ No hay datos disponibles en la base de datos")
    
    # ========================================================================
    # PÁGINA: TIPOS DE ENERGÍA
    # ========================================================================
    elif page == "⚡ Tipos de Energía":
        st.title("⚡ Análisis por Tipo de Energía")
        st.markdown("Desglose detallado de cada fuente energética")
        
        # Selector de tipo de energía
        query_tipos = "SELECT DISTINCT nombre FROM tipo_energia ORDER BY nombre"
        df_tipos = run_query(query_tipos)
        
        if not df_tipos.empty:
            tipo_seleccionado = st.sidebar.selectbox(
                "Seleccionar Tipo de Energía:",
                df_tipos['nombre'].tolist()
            )
            
            # Datos del tipo seleccionado
            query_detalle = """
            SELECT 
                te.nombre,
                te.descripcion,
                p.anio,
                e.generacion_gwh,
                e.oferta_gwh,
                e.demanda_gwh,
                e.costo_mwh,
                e.porcentaje_cobertura,
                e.inversion_usd_millones,
                e.emisiones_co2_toneladas
            FROM estadisticas_energia e
            JOIN tipo_energia te ON e.id_tipo_energia = te.id_tipo_energia
            JOIN periodo p ON e.id_periodo = p.id_periodo
            WHERE te.nombre = %s
            ORDER BY p.anio
            """
            df_detalle = run_query(query_detalle, params=(tipo_seleccionado,))
            
            if not df_detalle.empty:
                # Información del tipo
                st.info(f"**Descripción:** {df_detalle['descripcion'][0] if df_detalle['descripcion'][0] else 'Sin descripción'}")
                
                # Métricas del tipo seleccionado
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Generación Promedio (GWh)",
                        f"{df_detalle['generacion_gwh'].mean():,.2f}"
                    )
                
                with col2:
                    st.metric(
                        "Costo Promedio (USD/MWh)",
                        f"${df_detalle['costo_mwh'].mean():,.2f}"
                    )
                
                with col3:
                    st.metric(
                        "Inversión Total (USD M)",
                        f"${df_detalle['inversion_usd_millones'].sum():,.2f}"
                    )
                
                # Gráfico de tendencia
                fig_trend = px.line(
                    df_detalle,
                    x='anio',
                    y='generacion_gwh',
                    title=f'📈 Tendencia de Generación - {tipo_seleccionado}',
                    markers=True,
                    line_shape='spline'
                )
                fig_trend.update_layout(height=400)
                st.plotly_chart(fig_trend, use_container_width=True)
                
                # Tabla de datos
                with st.expander("📋 Ver Datos Detallados"):
                    st.dataframe(df_detalle, use_container_width=True)
            else:
                st.warning("No hay datos para este tipo de energía")
        else:
            st.warning("No hay tipos de energía registrados")
    
    # ========================================================================
    # PÁGINA: ANÁLISIS TEMPORAL
    # ========================================================================
    elif page == "📅 Análisis Temporal":
        st.title("📅 Análisis Temporal")
        st.markdown("Evolución histórica de los indicadores energéticos")
        
        # Selector de año
        query_anios = "SELECT DISTINCT anio FROM periodo ORDER BY anio"
        df_anios = run_query(query_anios)
        
        if not df_anios.empty:
            anio_seleccionado = st.sidebar.slider(
                "Seleccionar Año:",
                int(df_anios['anio'].min()),
                int(df_anios['anio'].max()),
                int(df_anios['anio'].max())
            )
            
            # Datos del año seleccionado
            query_anio = """
            SELECT 
                te.nombre as tipo_energia,
                e.generacion_gwh,
                e.demanda_gwh,
                e.costo_mwh,
                e.porcentaje_cobertura
            FROM estadisticas_energia e
            JOIN tipo_energia te ON e.id_tipo_energia = te.id_tipo_energia
            JOIN periodo p ON e.id_periodo = p.id_periodo
            WHERE p.anio = %s
            ORDER BY e.generacion_gwh DESC
            """
            df_anio = run_query(query_anio, params=(anio_seleccionado,))
            
            if not df_anio.empty:
                # Gráfico de barras
                fig = px.bar(
                    df_anio,
                    x='tipo_energia',
                    y='generacion_gwh',
                    title=f'⚡ Generación por Tipo de Energía - {anio_seleccionado}',
                    color='generacion_gwh',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla comparativa
                st.subheader("📋 Comparativa por Tipo de Energía")
                st.dataframe(df_anio, use_container_width=True)
            else:
                st.warning("No hay datos para el año seleccionado")
        else:
            st.warning("No hay datos temporales disponibles")
    
    # ========================================================================
    # PÁGINA: IMPACTO AMBIENTAL
    # ========================================================================
    elif page == "🌱 Impacto Ambiental":
        st.title("🌱 Impacto Ambiental - Emisiones CO2")
        st.markdown("Análisis de emisiones de carbono por tipo de energía")
        
        # Query de emisiones
        query_emisiones = """
        SELECT 
            te.nombre as tipo_energia,
            ROUND(SUM(e.emisiones_co2_toneladas), 2) as emisiones_totales,
            ROUND(AVG(e.emisiones_co2_toneladas), 2) as emisiones_promedio,
            ROUND(SUM(e.generacion_gwh), 2) as generacion_total
        FROM estadisticas_energia e
        JOIN tipo_energia te ON e.id_tipo_energia = te.id_tipo_energia
        GROUP BY te.id_tipo_energia, te.nombre
        ORDER BY emisiones_totales DESC
        """
        df_emisiones = run_query(query_emisiones)
        
        if not df_emisiones.empty:
            # Calcular intensidad de emisiones
            df_emisiones['intensidad_co2'] = round(
                df_emisiones['emisiones_totales'] / df_emisiones['generacion_total'].replace(0, 1), 2
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.bar(
                    df_emisiones,
                    x='tipo_energia',
                    y='emisiones_totales',
                    title='🏭 Emisiones Totales de CO2 por Tipo de Energía',
                    color='emisiones_totales',
                    color_continuous_scale='Reds'
                )
                fig1.update_layout(height=400)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.bar(
                    df_emisiones,
                    x='tipo_energia',
                    y='intensidad_co2',
                    title='📊 Intensidad de Emisiones (CO2/GWh)',
                    color='intensidad_co2',
                    color_continuous_scale='YlOrRd'
                )
                fig2.update_layout(height=400)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Tabla de resumen
            st.subheader("📋 Resumen de Emisiones")
            st.dataframe(df_emisiones, use_container_width=True)
        else:
            st.warning("No hay datos de emisiones disponibles")
    
    # ========================================================================
    # PÁGINA: DATOS CRUDOS
    # ========================================================================
    elif page == "📊 Datos Crudos":
        st.title("📊 Explorador de Datos")
        st.markdown("Visualiza y exporta los datos completos de la base de datos")
        
        # Selector de tabla
        tabla_seleccionada = st.sidebar.selectbox(
            "Seleccionar Tabla:",
            ["estadisticas_energia", "tipo_energia", "periodo"]
        )
        
        query_tabla = f"SELECT * FROM {tabla_seleccionada} LIMIT 100"
        df_tabla = run_query(query_tabla)
        
        if not df_tabla.empty:
            st.subheader(f"📋 Tabla: {tabla_seleccionada}")
            st.dataframe(df_tabla, use_container_width=True)
            
            # Botón de descarga
            csv = df_tabla.to_csv(index=False, encoding='utf-8')
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=f'{tabla_seleccionada}.csv',
                mime='text/csv'
            )
        else:
            st.warning("No hay datos disponibles")

# ============================================================================
# CONTROL DE NAVEGACIÓN
# ============================================================================
if 'page' not in st.session_state:
    st.session_state['page'] = 'landing'

if st.session_state['page'] == 'landing':
    landing_page()
else:
    dashboard_page()

# ============================================================================
# FOOTER GLOBAL
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>Proyecto Curso Talento Tech - Análisis de Datos</strong></p>
    <p>Elaborado por: <strong>Michely Muñoz</strong> | """ + datetime.now().strftime("%Y") + """</p>
</div>
""", unsafe_allow_html=True)
