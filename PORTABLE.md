# 💼 FORXIME - Versión Portable

## ¿Qué es una aplicación portable?

Esta versión de FORXIME es **completamente portable**, lo que significa que:

✅ **No requiere instalación** - Solo necesitas Python instalado  
✅ **Todos los archivos en un solo lugar** - Datos, resultados y configuración en una carpeta  
✅ **Fácil de mover** - Copia la carpeta completa a cualquier computadora  
✅ **Sin dependencias del sistema** - No modifica el registro ni carpetas del sistema  
✅ **Múltiples instancias** - Puedes tener varias copias para diferentes proyectos  

## 📁 Estructura de Carpetas

```
nabna_rubi/
├── app.py                      # Aplicación principal
├── requirements.txt            # Dependencias de Python
├── create_examples.py          # Script para generar ejemplos
├── README.md                   # Documentación general
├── PORTABLE.md                 # Este archivo
│
├── examples/                   # Archivos de ejemplo
│   ├── ejemplo_mamiferos.xlsx
│   └── ejemplo_eventos.xlsx
│
├── outputs/                    # TODOS tus resultados se guardan aquí
│   ├── FORXIME_Estadisticos_20260111_203045.xlsx
│   ├── Grafica_Riqueza_20260111_203045.png
│   ├── Grafica_Shannon_20260111_203045.png
│   ├── Grafica_Abundancia_20260111_203045.png
│   └── MAMIFEROS_Generado_20260111_203512.xlsx
│
└── temp/                       # Archivos temporales (se puede limpiar)
```

## 🚀 Uso Portable

### Primera Vez

1. **Copia la carpeta completa** `nabna_rubi` a donde quieras (USB, disco duro, red)
2. **Abre una terminal** en esa carpeta
3. **Instala dependencias** (solo la primera vez):

   ```bash
   python -m pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación**:

   ```bash
   python -m streamlit run app.py
   ```

### Usos Posteriores

Solo necesitas ejecutar:

```bash
python -m streamlit run app.py
```

## 💾 Dónde se Guardan los Archivos

### Resultados de Estadísticos

Cuando procesas datos en **OBTENER ESTADISTICOS**, se generan:

- `outputs/FORXIME_Estadisticos_[FECHA]_[HORA].xlsx` - Tabla de resultados
- `outputs/Grafica_Riqueza_[FECHA]_[HORA].png` - Gráfica de riqueza
- `outputs/Grafica_Shannon_[FECHA]_[HORA].png` - Gráfica de Shannon
- `outputs/Grafica_Abundancia_[FECHA]_[HORA].png` - Gráfica de abundancia

### Resultados de Eventos

Cuando procesas datos en **GENERAR EVENTOS INDEPENDIENTES**, se genera:

- `outputs/MAMIFEROS_Generado_[FECHA]_[HORA].xlsx` - Matriz procesada

### Nomenclatura con Timestamp

Todos los archivos incluyen fecha y hora para evitar sobrescribir resultados anteriores:

- Formato: `YYYYMMDD_HHMMSS`
- Ejemplo: `20260111_203045` = 11 de enero 2026, 20:30:45

## 🔄 Mover a Otra Computadora

### Opción 1: Copiar Todo

1. Cierra la aplicación si está corriendo
2. Copia la carpeta completa `nabna_rubi`
3. Pégala en la nueva computadora
4. Ejecuta `python -m streamlit run app.py`

### Opción 2: Solo Resultados

Si solo quieres los resultados:

1. Copia la carpeta `outputs/`
2. Todos tus análisis están ahí

### Opción 3: USB/Disco Externo

1. Copia `nabna_rubi` a tu USB
2. Ejecuta directamente desde el USB
3. Todos los resultados se guardan en el USB

## 🧹 Mantenimiento

### Limpiar Archivos Temporales

```bash
# Windows
rmdir /s /q temp
mkdir temp

# Linux/Mac
rm -rf temp/*
```

### Organizar Resultados

Puedes crear subcarpetas dentro de `outputs/`:

```
outputs/
├── proyecto_1/
├── proyecto_2/
└── analisis_2026/
```

Solo mueve los archivos manualmente a las subcarpetas que necesites.

### Backup

Para hacer respaldo de todo tu trabajo:

```bash
# Copia toda la carpeta nabna_rubi a tu ubicación de backup
```

## 📊 Ventajas de la Versión Portable

| Característica | Versión Portable | Instalación Normal |
|----------------|------------------|-------------------|
| Instalación | ❌ No requiere | ✅ Requiere |
| Archivos centralizados | ✅ Sí | ❌ Dispersos |
| Fácil de mover | ✅ Sí | ❌ No |
| Múltiples versiones | ✅ Sí | ⚠️ Complicado |
| Backup simple | ✅ Copiar carpeta | ⚠️ Varios pasos |
| Uso en USB | ✅ Sí | ❌ No |

## 🔍 Verificar Ubicación de Archivos

La aplicación muestra en el **menú lateral** (sidebar) las rutas exactas donde se guardan los archivos:

1. Abre la aplicación
2. Mira el sidebar izquierdo
3. Expande "📁 Carpetas de la Aplicación"
4. Verás las rutas completas

## ⚠️ Importante

- **No renombres** `app.py` - La aplicación lo necesita para encontrar las carpetas
- **No elimines** las carpetas `outputs/`, `examples/`, `temp/` mientras la app esté corriendo
- **Mantén** `requirements.txt` en la misma carpeta que `app.py`

## 🆘 Solución de Problemas

### "No se encuentra la carpeta outputs"

La aplicación la crea automáticamente al iniciar. Si no existe, verifica que `app.py` esté en la carpeta correcta.

### "Los archivos no se guardan"

Verifica que tengas permisos de escritura en la carpeta. Si está en una ubicación protegida (ej. Archivos de Programa), muévela a Documentos o Escritorio.

### "Error al mover la carpeta"

Cierra la aplicación antes de mover la carpeta. Streamlit mantiene archivos abiertos mientras corre.

## 📞 Soporte

Para preguntas sobre la versión portable, contacta al desarrollador:
**Biólogo Erick Elio Chavez Gurrola**

---

**Versión Portable**: 2.0  
**Última actualización**: Enero 2026
