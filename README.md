# OrphanTLCleaner

**OrphanTLCleaner** es una herramienta gráfica para limpiar bloques de traducción huérfanos en proyectos **Ren'Py**.

Cuando ejecutas el linter de Ren'Py (`lint`), este genera un archivo `lint.txt` que contiene identificadores de traducciones que apuntan a cadenas fuente que ya no existen. Este programa lee ese `lint.txt`, escanea todos los archivos `.rpy` y `.rpym` de tu proyecto, y **elimina o comenta** esos bloques de traducción huérfanos.

## Características

-   Interfaz gráfica nativa con HTML/CSS/JS (vía pywebview + Qt)
-   Soporte para 7 idiomas: español, inglés, francés, portugués (BR), japonés, ruso y chino tradicional
-   Modo oscuro
-   Opción para **eliminar** bloques huérfanos o **comentarlos** (`#`)
-   Persistencia de configuración (idioma, tema, modo)
-   Compatible con empaquetado PyInstaller

## Requisitos

-   Python 3.9+
-   WebView2 Runtime (Windows) o Qt (incluido vía PyQt5)
-   Dependencias listadas en `requirements.txt`

## Instalación

```bash
# Clonar o copiar el proyecto
cd OrphanTLCleaner

# Crear y activar entorno virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

1.  Ejecuta la aplicación:
    ```bash
    python main.py
    ```

2.  En la ventana:
    -   Selecciona el **directorio** donde están tus archivos `.rpy` y `.rpym`
    -   Selecciona el archivo **`lint.txt`** generado por el linter de Ren'Py
    -   Ingresa el **idioma** de las traducciones a limpiar (p. ej. `english`, `spanish`)
    -   Opcionalmente marca **"Comentar bloques en lugar de borrarlos"**
    -   Haz clic en **Ejecutar**

3.  Los resultados se muestran en el área de texto, listando los archivos modificados.

## Estructura del proyecto

```
_OrphanTLCleaner_/
├── main.py                        # Punto de entrada
├── orphan_tl_cleaner/             # Paquete principal
│   ├── __init__.py
│   ├── i18n.py                    # Traducciones de la interfaz
│   ├── settings.py                # Persistencia de configuración
│   ├── api.py                     # Lógica de negocio
│   └── gui.py                     # Interfaz gráfica (HTML + puente JS)
├── requirements.txt               # Dependencias
├── languages/                     # Archivos de traducción (legado Qt)
├── icon.ico                       # Icono de la aplicación
└── README.md
```

## Cómo funciona

1.  **Carga de identificadores**: Lee el `lint.txt` y extrae los IDs de traducción huérfanos usando el patrón `(id <identificador>)`.
2.  **Escaneo de archivos**: Recorre recursivamente el directorio seleccionado buscando archivos `.rpy` y `.rpym`.
3.  **Procesamiento**: Para cada identificador huérfano, busca bloques `translate <idioma> <id>:` y los elimina o comenta según la opción elegida.
4.  **Resultado**: Lista los archivos que fueron modificados.

## Licencia

MIT
