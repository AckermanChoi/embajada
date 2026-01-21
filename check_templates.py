from fastapi.templating import Jinja2Templates

# Carpeta de templates que estás usando en main.py
templates = Jinja2Templates(directory="app/templates")

# Lista de archivos que Jinja2 puede cargar
try:
    template = templates.get_template("pages/nuevo_residente.html")
    print("✅ Template encontrado: pages/nuevo_residente.html")
except Exception as e:
    print("❌ No se encontró el template.")
    print(e)
