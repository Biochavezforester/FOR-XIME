import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import os
from pathlib import Path
from datetime import datetime
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram, linkage

# ==========================================
# 0. CONFIGURACIÓN DE DIRECTORIOS PORTABLES
# ==========================================
# Obtener el directorio base de la aplicación
BASE_DIR = Path(__file__).parent.absolute()

# Crear estructura de carpetas portables
OUTPUTS_DIR = BASE_DIR / "outputs"
EXAMPLES_DIR = BASE_DIR / "examples"
TEMP_DIR = BASE_DIR / "temp"

# Crear directorios si no existen
OUTPUTS_DIR.mkdir(exist_ok=True)
EXAMPLES_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="FORXIME", 
    layout="wide", 
    page_icon="🌿"
)

# Estilos CSS para personalizar la apariencia
st.markdown("""
    <style>
    /* Fondo general */
    .main { background-color: #f1f8e9; }
    
    /* Títulos y encabezados */
    h1 { color: #1b5e20; text-align: center; font-family: 'Helvetica', sans-serif;}
    h2, h3 { color: #2e7d32; }
    
    /* Botones */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        font-weight: bold; 
        color: white; 
        background-color: #43a047; 
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #2e7d32;
        color: white;
    }

    /* Caja de donación */
    .donation-box {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        border-left: 6px solid #fdd835;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .credit-box {
        padding: 15px;
        background-color: #e8f5e9;
        border-radius: 10px;
        border: 1px solid #c8e6c9;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNCIONES DE CÁLCULO (CIENCIA DE DATOS)
# ==========================================

def calcular_shannon(x):
    """Calcula el índice de Shannon-Wiener (H')"""
    total = x.sum()
    if total == 0: return 0
    p = x / total
    p = p[p > 0] # Eliminar ceros para evitar error matemático en log
    return -np.sum(p * np.log(p))

def calcular_simpson_d(x):
    """Calcula el índice de Simpson (D)"""
    total = x.sum()
    if total == 0: return 0
    p = x / total
    return np.sum(p**2)

def calcular_bray_curtis(df):
    """Calcula la matriz de distancia de Bray-Curtis entre sitios"""
    # Transponer para que filas sean sitios y columnas sean especies
    df_t = df.T
    # Calcular distancia Bray-Curtis
    distancias = pdist(df_t, metric='braycurtis')
    # Convertir a matriz cuadrada
    matriz_dist = squareform(distancias)
    return matriz_dist, distancias

def generar_dendrograma(df, ax):
    """Genera un dendrograma basado en distancia Bray-Curtis"""
    matriz_dist, distancias = calcular_bray_curtis(df)
    # Realizar clustering jerárquico (UPGMA)
    Z = linkage(distancias, method='average')
    # Generar dendrograma
    dendrogram(Z, labels=df.columns.tolist(), ax=ax, orientation='right')
    ax.set_xlabel('Distancia de Bray-Curtis')
    ax.set_title('Dendrograma de Similitud entre Sitios\n(Método UPGMA - Bray-Curtis)')
    return Z

def interpretar_resultados(resultados):
    """Genera interpretación automática de los resultados estadísticos"""
    interpretacion = []
    
    # Análisis de Riqueza
    sitio_max_riqueza = resultados['Riqueza (S)'].idxmax()
    sitio_min_riqueza = resultados['Riqueza (S)'].idxmin()
    max_riqueza = resultados['Riqueza (S)'].max()
    min_riqueza = resultados['Riqueza (S)'].min()
    
    interpretacion.append(f"**📊 Riqueza de Especies:**")
    interpretacion.append(f"- El sitio **{sitio_max_riqueza}** presenta la mayor riqueza con **{int(max_riqueza)} especies**.")
    interpretacion.append(f"- El sitio **{sitio_min_riqueza}** presenta la menor riqueza con **{int(min_riqueza)} especies**.")
    
    if max_riqueza > min_riqueza * 1.5:
        interpretacion.append(f"- Existe una **diferencia considerable** en riqueza entre sitios.")
    else:
        interpretacion.append(f"- La riqueza es **relativamente homogénea** entre sitios.")
    
    interpretacion.append("")
    
    # Análisis de Shannon
    sitio_max_shannon = resultados['Shannon (H\')'].idxmax()
    sitio_min_shannon = resultados['Shannon (H\')'].idxmin()
    max_shannon = resultados['Shannon (H\')'].max()
    min_shannon = resultados['Shannon (H\')'].min()
    
    interpretacion.append(f"**🌈 Índice de Shannon (Diversidad):**")
    interpretacion.append(f"- El sitio **{sitio_max_shannon}** tiene la mayor diversidad (H' = {max_shannon:.3f}).")
    interpretacion.append(f"- El sitio **{sitio_min_shannon}** tiene la menor diversidad (H' = {min_shannon:.3f}).")
    
    # Interpretación del valor de Shannon
    promedio_shannon = resultados['Shannon (H\')'].mean()
    if promedio_shannon > 2.5:
        interpretacion.append(f"- En general, los sitios presentan **alta diversidad** (promedio H' = {promedio_shannon:.3f}).")
    elif promedio_shannon > 1.5:
        interpretacion.append(f"- En general, los sitios presentan **diversidad moderada** (promedio H' = {promedio_shannon:.3f}).")
    else:
        interpretacion.append(f"- En general, los sitios presentan **baja diversidad** (promedio H' = {promedio_shannon:.3f}).")
    
    interpretacion.append("")
    
    # Análisis de Simpson
    sitio_min_simpson = resultados['Simpson (1-D)'].idxmax()  # Mayor 1-D = menor dominancia
    sitio_max_simpson = resultados['Simpson (1-D)'].idxmin()  # Menor 1-D = mayor dominancia
    
    interpretacion.append(f"**👑 Índice de Simpson (Dominancia):**")
    interpretacion.append(f"- El sitio **{sitio_min_simpson}** tiene la **menor dominancia** (mayor equitatividad).")
    interpretacion.append(f"- El sitio **{sitio_max_simpson}** tiene la **mayor dominancia** (pocas especies dominan).")
    
    interpretacion.append("")
    interpretacion.append("**💡 Recomendaciones:**")
    interpretacion.append(f"- Los sitios con alta diversidad (como **{sitio_max_shannon}**) son importantes para la conservación.")
    interpretacion.append(f"- Considerar acciones de manejo en sitios con baja diversidad (como **{sitio_min_shannon}**).")
    
    return "\n".join(interpretacion)

# ==========================================
# 3. INTERFAZ DE USUARIO PRINCIPAL
# ==========================================

def main():
    # --- MENÚ LATERAL ---
    st.sidebar.title("Menú Principal")
    opcion = st.sidebar.radio("Navegación:", 
                              ["Bienvenida", "EJEMPLOS", "OBTENER ESTADISTICOS", "GENERAR EVENTOS INDEPENDIENTES"])

    # Mostrar información de directorios en el sidebar
    with st.sidebar.expander("📁 Carpetas de la Aplicación"):
        st.write(f"**Carpeta principal:**")
        st.code(str(BASE_DIR), language="")
        st.write(f"**Salidas guardadas en:**")
        st.code(str(OUTPUTS_DIR), language="")
        st.write(f"**Ejemplos en:**")
        st.code(str(EXAMPLES_DIR), language="")

    # ----------------------------------------------------------------------
    # SECCIÓN: BIENVENIDA
    # ----------------------------------------------------------------------
    if opcion == "Bienvenida":
        st.title("🌿 FORXIME")
        st.subheader("Plataforma de Análisis de Biodiversidad de Cámaras Trampa")
        st.markdown("**Simplifica el análisis estadístico de datos de fototrampeo con sitios simples y pareados**")
        
        st.markdown("---")
        
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("### 👋 Acerca de la plataforma")
            st.write("""
            Esta herramienta está pensada para **simplificar el análisis estadístico de datos obtenidos 
            a partir de muestreo por fototrampeo**, contemplando tanto **sitios simples como pareados**.
            
            **Funciones principales:**
            * 📊 Cálculo de índices de biodiversidad (Riqueza, Shannon, Simpson)
            * 📈 Generación automática de gráficas profesionales
            * 🔄 Estandarización de eventos independientes (promedio de duplicados)
            * 📁 Procesamiento de datos de sitios simples y pareados
            """)
            
            st.markdown('<div class="credit-box">', unsafe_allow_html=True)
            st.markdown("#### 👨‍🔬 Desarrollada por:")
            st.markdown("### **Biólogo Erick Elio Chavez Gurrola**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Información sobre portabilidad
            st.info("""
            💼 **Aplicación Portable**: Todos los archivos generados se guardan en la carpeta 
            `outputs/` dentro del directorio de la aplicación. Puedes mover toda la carpeta 
            a cualquier computadora sin perder tus datos.
            """)

        with col_right:
            st.markdown('<div class="donation-box">', unsafe_allow_html=True)
            st.markdown("### 🤝 Apoya el Proyecto")
            st.write("Si esta herramienta te es útil, considera hacer un donativo para su mantenimiento:")
            st.markdown("---")
            st.markdown("🏦 **Banco:** BBVA")
            st.markdown("💳 **Tarjeta:** `4152 3144 0105 9541`")
            st.markdown("👤 **Beneficiario:** Erick Elio Chavez Gurrola")
            st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------------------------
    # SECCIÓN: EJEMPLOS
    # ----------------------------------------------------------------------
    elif opcion == "EJEMPLOS":
        st.title("📚 Ejemplos de Formato de Archivos")
        st.write("A continuación se muestran ejemplos de cómo deben estar estructurados los archivos para cada tipo de análisis.")
        
        st.markdown("---")
        
        # EJEMPLO 1: MAMIFEROS
        st.header("1️⃣ Formato MAMIFEROS (Para Estadísticos)")
        st.info("📊 Este formato se usa en la sección **OBTENER ESTADISTICOS**")
        
        st.markdown("### Estructura del archivo:")
        st.write("""
        - **Primera columna**: Nombre de la especie
        - **Columnas siguientes**: Cada columna representa un sitio de muestreo
        - **Última columna (opcional)**: Total de eventos independientes
        - **Valores**: Número de registros de cada especie en cada sitio
        """)
        
        # Mostrar ejemplo visual
        ejemplo_mamiferos = pd.DataFrame({
            'Especie': ['Jaguar', 'Puma', 'Ocelote', 'Tapir', 'Pecarí', 'Venado'],
            'Sitio_1': [5, 3, 8, 2, 12, 7],
            'Sitio_2': [3, 4, 6, 1, 10, 5],
            'Sitio_3': [7, 2, 5, 3, 15, 9],
            'Sitio_4': [4, 5, 7, 2, 8, 6],
            'EVENTO INDEPENDIENTE': [19, 14, 26, 8, 45, 27]
        })
        
        st.markdown("### Vista previa del formato:")
        st.dataframe(ejemplo_mamiferos, use_container_width=True)
        
        # Botón de descarga
        ejemplo_path = EXAMPLES_DIR / "ejemplo_mamiferos.xlsx"
        try:
            with open(ejemplo_path, 'rb') as f:
                st.download_button(
                    label="📥 Descargar Archivo de Ejemplo (MAMIFEROS)",
                    data=f,
                    file_name="ejemplo_mamiferos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except FileNotFoundError:
            st.warning(f"⚠️ Archivo de ejemplo no encontrado en: {ejemplo_path}")
            st.info("💡 Ejecuta `python create_examples.py` para generar los archivos de ejemplo.")
        
        st.markdown("---")
        
        # EJEMPLO 2: EVENTOS
        st.header("2️⃣ Formato EVENTOS (Para Generar Eventos Independientes)")
        st.info("🔄 Este formato se usa en la sección **GENERAR EVENTOS INDEPENDIENTES**")
        
        st.markdown("### Estructura del archivo:")
        st.write("""
        - **Columna 'sitio'**: Identificador del sitio de muestreo (número o texto)
        - **Columna 'especie'**: Nombre de la especie registrada
        - **Columna 'eventos_independientes'**: Número de eventos independientes registrados
        - **Nota**: Si hay duplicados (misma especie en el mismo sitio), se calculará el promedio automáticamente
        """)
        
        # Mostrar ejemplo visual
        ejemplo_eventos = pd.DataFrame({
            'sitio': [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 1, 2],
            'especie': ['JAGUAR', 'PUMA', 'OCELOTE', 'JAGUAR', 'JAGUAR', 'PUMA', 'TAPIR', 
                       'JAGUAR', 'OCELOTE', 'VENADO', 'PUMA', 'PUMA', 'JAGUAR'],
            'eventos_independientes': [5, 3, 8, 6, 3, 4, 1, 7, 5, 9, 2, 4, 2]
        })
        
        st.markdown("### Vista previa del formato:")
        st.dataframe(ejemplo_eventos, use_container_width=True)
        
        st.warning("""
        ⚠️ **Nota sobre duplicados**: En este ejemplo, hay registros duplicados:
        - Sitio 1 + JAGUAR aparece 2 veces (5 y 6 eventos) → Se promediará a 5.5
        - Sitio 1 + PUMA aparece 2 veces (3 y 4 eventos) → Se promediará a 3.5
        - Sitio 2 + JAGUAR aparece 2 veces (3 y 2 eventos) → Se promediará a 2.5
        """)
        
        # Botón de descarga
        ejemplo_path = EXAMPLES_DIR / "ejemplo_eventos.xlsx"
        try:
            with open(ejemplo_path, 'rb') as f:
                st.download_button(
                    label="📥 Descargar Archivo de Ejemplo (EVENTOS)",
                    data=f,
                    file_name="ejemplo_eventos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except FileNotFoundError:
            st.warning(f"⚠️ Archivo de ejemplo no encontrado en: {ejemplo_path}")
            st.info("💡 Ejecuta `python create_examples.py` para generar los archivos de ejemplo.")
        
        st.markdown("---")
        
        # Consejos adicionales
        st.header("💡 Consejos Importantes")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ✅ Buenas Prácticas:
            - Usa nombres de especies consistentes
            - Evita espacios al inicio/final de los nombres
            - Usa números enteros para los conteos
            - Verifica que no haya celdas vacías
            - Guarda en formato .xlsx o .csv
            """)
        
        with col2:
            st.markdown("""
            ### ❌ Errores Comunes:
            - Nombres de especies con errores tipográficos
            - Mezclar mayúsculas y minúsculas inconsistentemente
            - Dejar celdas vacías en lugar de poner 0
            - Usar caracteres especiales en nombres de columnas
            - Formato de archivo incorrecto
            """)


    # ----------------------------------------------------------------------
    # SECCIÓN: OBTENER ESTADÍSTICOS
    # ----------------------------------------------------------------------
    elif opcion == "OBTENER ESTADISTICOS":
        st.header("📊 Estadísticos de Biodiversidad")
        st.info("ℹ️ Sube tu archivo con formato 'MAMIFEROS' (Tabla de Especie x Sitio). Compatible con sitios simples y pareados.")

        archivo_stats = st.file_uploader("Cargar Archivo (Excel .xlsx o CSV)", type=['xlsx', 'csv'], key="stats")

        if archivo_stats is not None:
            if st.button("PROCESAR DATOS"):
                try:
                    # 1. Cargar Datos
                    if archivo_stats.name.endswith('.csv'):
                        df = pd.read_csv(archivo_stats)
                    else:
                        df = pd.read_excel(archivo_stats)

                    # 2. Limpieza
                    # Asumimos que la primera columna es la Especie (Índice)
                    df = df.set_index(df.columns[0])
                    
                    # Filtramos columnas numéricas (Sitios) excluyendo la columna de resumen si existe
                    cols_sitios = [c for c in df.columns if "EVENTO" not in str(c).upper()]
                    df_clean = df[cols_sitios].apply(pd.to_numeric, errors='coerce').fillna(0)

                    st.success("✅ Archivo cargado correctamente.")

                    # 3. Cálculos
                    resultados = pd.DataFrame(index=df_clean.columns)
                    resultados.index.name = 'Sitio'
                    
                    resultados['Riqueza (S)'] = df_clean.apply(lambda x: (x > 0).sum())
                    resultados['Abundancia (N)'] = df_clean.sum()
                    resultados['Shannon (H\')'] = df_clean.apply(calcular_shannon)
                    resultados['Simpson (D)'] = df_clean.apply(calcular_simpson_d)
                    resultados['Simpson (1-D)'] = 1 - resultados['Simpson (D)']

                    # 4. Mostrar Resultados Numéricos
                    st.subheader("📋 Tabla de Resultados")
                    st.dataframe(resultados.style.highlight_max(axis=0, color='lightgreen'))

                    # 5. Guardar en carpeta outputs con timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"FORXIME_Estadisticos_{timestamp}.xlsx"
                    output_path = OUTPUTS_DIR / output_filename
                    
                    # Descarga Excel
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        resultados.to_excel(writer, sheet_name='Resultados')
                    
                    # Guardar también en disco
                    with open(output_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    
                    st.download_button(
                        label="📥 Descargar Resultados (Excel)",
                        data=buffer.getvalue(),
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    st.success(f"💾 Archivo también guardado en: `outputs/{output_filename}`")

                    # 5.5. Interpretación Automática de Resultados
                    st.markdown("---")
                    st.subheader("📝 Interpretación de Resultados")
                    interpretacion_texto = interpretar_resultados(resultados)
                    st.info(interpretacion_texto)

                    # 6. Generar Gráficas
                    st.subheader("📈 Gráficas Generadas")
                    col1, col2 = st.columns(2)

                    # Gráfica Riqueza
                    fig1, ax1 = plt.subplots(figsize=(6,4))
                    resultados['Riqueza (S)'].plot(kind='bar', ax=ax1, color='#66bb6a', edgecolor='black')
                    ax1.set_title("Riqueza (S) por Sitio")
                    ax1.set_ylabel("Especies")
                    plt.tight_layout()
                    col1.pyplot(fig1)
                    
                    # Guardar gráfica
                    fig1_path = OUTPUTS_DIR / f"Grafica_Riqueza_{timestamp}.png"
                    fig1.savefig(fig1_path, dpi=300, bbox_inches='tight')

                    # Gráfica Shannon
                    fig2, ax2 = plt.subplots(figsize=(6,4))
                    resultados['Shannon (H\')'].plot(kind='bar', ax=ax2, color='#ffa726', edgecolor='black')
                    ax2.set_title("Índice de Shannon (H')")
                    plt.tight_layout()
                    col2.pyplot(fig2)
                    
                    # Guardar gráfica
                    fig2_path = OUTPUTS_DIR / f"Grafica_Shannon_{timestamp}.png"
                    fig2.savefig(fig2_path, dpi=300, bbox_inches='tight')

                    # Gráfica Abundancia
                    fig3, ax3 = plt.subplots(figsize=(10,4))
                    resultados['Abundancia (N)'].plot(kind='bar', ax=ax3, color='#42a5f5', edgecolor='black')
                    ax3.set_title("Abundancia Total (N)")
                    plt.tight_layout()
                    st.pyplot(fig3)
                    
                    # Guardar gráfica
                    fig3_path = OUTPUTS_DIR / f"Grafica_Abundancia_{timestamp}.png"
                    fig3.savefig(fig3_path, dpi=300, bbox_inches='tight')
                    
                    # Dendrograma de Bray-Curtis
                    st.markdown("---")
                    st.subheader("🌳 Dendrograma de Similitud (Bray-Curtis)")
                    st.write("""
                    El dendrograma muestra la similitud entre sitios basándose en su composición de especies.
                    Sitios más cercanos en el dendrograma tienen comunidades más similares.
                    """)
                    
                    # Verificar que haya al menos 2 sitios para el dendrograma
                    if len(df_clean.columns) >= 2:
                        fig4, ax4 = plt.subplots(figsize=(10, 6))
                        try:
                            generar_dendrograma(df_clean, ax4)
                            plt.tight_layout()
                            st.pyplot(fig4)
                            
                            # Guardar dendrograma
                            fig4_path = OUTPUTS_DIR / f"Dendrograma_BrayCurtis_{timestamp}.png"
                            fig4.savefig(fig4_path, dpi=300, bbox_inches='tight')
                            
                            st.success("✅ Dendrograma generado. Sitios agrupados indican comunidades similares.")
                        except Exception as e:
                            st.warning(f"⚠️ No se pudo generar el dendrograma: {e}")
                    else:
                        st.warning("⚠️ Se necesitan al menos 2 sitios para generar el dendrograma.")
                    
                    st.info(f"📊 Todas las gráficas guardadas en la carpeta `outputs/`")

                except Exception as e:
                    st.error(f"Error al procesar: {e}")

    # ----------------------------------------------------------------------
    # SECCIÓN: GENERAR EVENTOS INDEPENDIENTES
    # ----------------------------------------------------------------------
    elif opcion == "GENERAR EVENTOS INDEPENDIENTES":
        st.header("🔄 Procesamiento de Eventos Independientes")
        st.write("Sube tu archivo con formato 'EVENTOS' (Base de datos cruda).")
        st.warning("⚠️ Esta función detectará duplicados de (Sitio + Especie) y calculará su **PROMEDIO**.")

        archivo_eventos = st.file_uploader("Cargar Archivo (Excel .xlsx o CSV)", type=['xlsx', 'csv'], key="ev")

        if archivo_eventos is not None:
            if st.button("PROCESAR Y PROMEDIAR"):
                try:
                    # 1. Cargar
                    if archivo_eventos.name.endswith('.csv'):
                        df_ev = pd.read_csv(archivo_eventos)
                    else:
                        df_ev = pd.read_excel(archivo_eventos)

                    # 2. Normalizar columnas (minúsculas y sin espacios)
                    df_ev.columns = [str(c).strip().lower() for c in df_ev.columns]

                    # Validar columnas necesarias
                    if 'sitio' not in df_ev.columns or 'especie' not in df_ev.columns:
                        st.error("❌ El archivo debe contener las columnas: 'sitio' y 'especie'.")
                    else:
                        # Buscar la columna de conteo (eventos)
                        cols_posibles = [c for c in df_ev.columns if 'evento' in c or 'independiente' in c]
                        
                        if not cols_posibles:
                            st.error("❌ No se encontró una columna de 'Eventos Independientes' (numérica).")
                        else:
                            col_target = cols_posibles[0]
                            
                            # Limpieza de texto en Especie
                            df_ev['especie'] = df_ev['especie'].astype(str).str.strip().str.upper()

                            st.write("🔄 Procesando duplicados...")

                            # 3. LÓGICA PRINCIPAL: Agrupar y Promediar
                            # Si existe sitio=1, especie=JAGUAR dos veces, se saca el promedio de sus eventos.
                            df_promedio = df_ev.groupby(['sitio', 'especie'])[col_target].mean().reset_index()

                            # 4. Transformar a Matriz (Pivot Table)
                            # Filas = Especie, Columnas = Sitio
                            df_final = df_promedio.pivot(index='especie', columns='sitio', values=col_target)
                            
                            # Rellenar vacíos con 0
                            df_final = df_final.fillna(0)
                            
                            # 5. Agregar Columna de Total (Formato MAMIFEROS)
                            df_final['EVENTO INDEPENDIENTE'] = df_final.sum(axis=1)

                            st.success("✅ Matriz generada exitosamente con promedios aplicados.")
                            
                            st.write("Vista previa:")
                            st.dataframe(df_final.head())

                            # 6. Guardar y Descargar
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            output_filename = f"MAMIFEROS_Generado_{timestamp}.xlsx"
                            output_path = OUTPUTS_DIR / output_filename
                            
                            buffer_fin = io.BytesIO()
                            with pd.ExcelWriter(buffer_fin, engine='openpyxl') as writer:
                                df_final.to_excel(writer, sheet_name='Matriz_Procesada')
                            
                            # Guardar también en disco
                            with open(output_path, 'wb') as f:
                                f.write(buffer_fin.getvalue())
                            
                            st.download_button(
                                label="📥 Descargar Archivo Generado (Excel)",
                                data=buffer_fin.getvalue(),
                                file_name=output_filename,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            
                            st.success(f"💾 Archivo también guardado en: `outputs/{output_filename}`")

                except Exception as e:
                    st.error(f"Error inesperado: {e}")

# Ejecutar la app
if __name__ == '__main__':
    main()
