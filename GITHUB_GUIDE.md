# 📤 Guía para Publicar FORXIME en GitHub

Esta guía te llevará paso a paso para publicar tu aplicación FORXIME en GitHub.

## 📋 Requisitos Previos

Antes de comenzar, necesitas:

1. ✅ Una cuenta de GitHub (gratuita)
2. ✅ Git instalado en tu computadora
3. ✅ Los archivos de FORXIME listos

## 🔧 Paso 1: Instalar Git (Si no lo tienes)

### Windows

1. Descarga Git desde: <https://git-scm.com/download/win>
2. Ejecuta el instalador
3. Usa las opciones predeterminadas
4. Reinicia tu terminal/PowerShell

### Verificar instalación

Abre una terminal y ejecuta:

```bash
git --version
```

Deberías ver algo como: `git version 2.x.x`

## 🌐 Paso 2: Crear Cuenta en GitHub (Si no tienes)

1. Ve a <https://github.com>
2. Haz clic en "Sign up"
3. Completa el registro con tu email
4. Verifica tu email
5. Inicia sesión

## 📁 Paso 3: Crear un Nuevo Repositorio en GitHub

### Opción A: Desde la Web (Recomendado para principiantes)

1. **Inicia sesión en GitHub**
2. **Haz clic en el botón "+" en la esquina superior derecha**
3. **Selecciona "New repository"**
4. **Completa el formulario**:
   - **Repository name**: `forxime` (o el nombre que prefieras)
   - **Description**: `Plataforma de Análisis de Biodiversidad de Cámaras Trampa`
   - **Public** ✅ (para que sea público)
   - **NO marques** "Initialize this repository with a README" (ya tenemos uno)
   - **NO agregues** .gitignore ni license (ya los tenemos)
5. **Haz clic en "Create repository"**

GitHub te mostrará una página con instrucciones. **Guarda esta página abierta**.

## 💻 Paso 4: Configurar Git en tu Computadora

Abre PowerShell o Terminal en la carpeta `nabna_rubi` y ejecuta:

```bash
# Configura tu nombre (usa tu nombre real)
git config --global user.name "Erick Elio Chavez Gurrola"

# Configura tu email (usa el email de tu cuenta de GitHub)
git config --global user.email "tu_email@ejemplo.com"
```

## 📦 Paso 5: Inicializar el Repositorio Local

En la carpeta `nabna_rubi`, ejecuta estos comandos **uno por uno**:

```bash
# 1. Inicializar Git
git init

# 2. Agregar todos los archivos
git add .

# 3. Hacer el primer commit
git commit -m "Initial commit: FORXIME v1.0 - Portable biodiversity analysis platform"

# 4. Renombrar la rama a 'main'
git branch -M main
```

## 🔗 Paso 6: Conectar con GitHub

Copia el comando que GitHub te mostró (debería verse así):

```bash
git remote add origin https://github.com/TU_USUARIO/forxime.git
```

**Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub**.

Ejemplo:

```bash
git remote add origin https://github.com/erickelio/forxime.git
```

## 🚀 Paso 7: Subir el Código a GitHub

```bash
git push -u origin main
```

**Importante**: La primera vez que hagas push, Git te pedirá autenticación:

### Autenticación

GitHub ya no acepta contraseñas. Necesitas usar un **Personal Access Token**:

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Haz clic en "Generate new token (classic)"
3. Dale un nombre: "FORXIME Upload"
4. Selecciona el scope: `repo` (marca toda la sección)
5. Haz clic en "Generate token"
6. **COPIA EL TOKEN** (solo se muestra una vez)
7. Cuando Git pida contraseña, **pega el token** (no tu contraseña de GitHub)

## ✅ Paso 8: Verificar que Funcionó

1. Ve a tu repositorio en GitHub: `https://github.com/TU_USUARIO/forxime`
2. Deberías ver todos tus archivos
3. El README.md se mostrará automáticamente en la página principal

## 🎨 Paso 9: Personalizar el README (Opcional)

Edita el archivo `README.md` y reemplaza:

- `TU_USUARIO` con tu nombre de usuario real de GitHub
- Agrega capturas de pantalla en la carpeta `docs/screenshots/`

Para agregar capturas:

```bash
# Crear carpeta para screenshots
mkdir -p docs/screenshots

# Copia tus capturas de pantalla ahí
# Luego actualiza el README con las rutas correctas
```

## 📸 Paso 10: Agregar Capturas de Pantalla

1. Toma capturas de pantalla de tu aplicación
2. Guárdalas en `docs/screenshots/`
3. Nómbralas:
   - `welcome.png` - Página de bienvenida
   - `examples.png` - Sección de ejemplos
   - `results.png` - Resultados estadísticos

4. Actualiza y sube los cambios:

```bash
git add docs/screenshots/
git commit -m "Add screenshots"
git push
```

## 🔄 Actualizaciones Futuras

Cuando hagas cambios a tu código:

```bash
# 1. Agregar cambios
git add .

# 2. Hacer commit con mensaje descriptivo
git commit -m "Descripción de los cambios"

# 3. Subir a GitHub
git push
```

## 🏷️ Crear una Release (Versión)

Para crear versiones oficiales:

1. Ve a tu repositorio en GitHub
2. Haz clic en "Releases" (lado derecho)
3. Haz clic en "Create a new release"
4. Tag version: `v1.0.0`
5. Release title: `FORXIME v1.0.0 - Primera Versión Pública`
6. Describe los cambios
7. Haz clic en "Publish release"

## 📊 Agregar Badges (Insignias)

Los badges ya están en el README. Para personalizarlos:

- Reemplaza `TU_USUARIO` con tu usuario de GitHub
- Los badges se actualizarán automáticamente

## 🌟 Promover tu Proyecto

1. **Comparte el enlace** con colegas
2. **Agrega topics** en GitHub:
   - biodiversity
   - camera-trap
   - ecology
   - conservation
   - streamlit
   - python

Para agregar topics:

- Ve a tu repositorio
- Haz clic en el ⚙️ junto a "About"
- Agrega los topics

## 🐛 Solución de Problemas

### Error: "fatal: not a git repository"

```bash
# Asegúrate de estar en la carpeta correcta
cd C:\Users\erick\.gemini\antigravity\scratch\nabna_rubi
git init
```

### Error: "remote origin already exists"

```bash
# Elimina el remote existente y agrégalo de nuevo
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/forxime.git
```

### Error: "failed to push some refs"

```bash
# Si el repositorio remoto tiene cambios
git pull origin main --rebase
git push origin main
```

### Error de autenticación

- Asegúrate de usar un **Personal Access Token**, no tu contraseña
- Verifica que el token tenga permisos de `repo`

## 📞 Ayuda Adicional

- **Documentación de Git**: <https://git-scm.com/doc>
- **GitHub Guides**: <https://guides.github.com/>
- **Markdown Guide**: <https://www.markdownguide.org/>

## ✅ Checklist Final

Antes de publicar, verifica:

- [ ] Git está instalado
- [ ] Cuenta de GitHub creada
- [ ] Repositorio creado en GitHub
- [ ] Git configurado con nombre y email
- [ ] Archivos agregados y commit realizado
- [ ] Remote configurado correctamente
- [ ] Push exitoso
- [ ] README personalizado
- [ ] Capturas de pantalla agregadas (opcional)
- [ ] License incluida
- [ ] .gitignore configurado

---

## 🎉 ¡Listo

Tu proyecto FORXIME ahora es público en GitHub y cualquiera puede:

- Ver el código
- Descargar la aplicación
- Contribuir con mejoras
- Reportar problemas
- Dar estrellas ⭐

**URL de tu proyecto**: `https://github.com/TU_USUARIO/forxime`

¡Comparte este enlace con la comunidad científica!

---

**Desarrollado por**: Biólogo Erick Elio Chavez Gurrola  
**Fecha**: Enero 2026
