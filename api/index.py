# api/index.py
from qquiz_app.asgi import application  # adjust if your project name is different

# Vercel ASGI expects a variable named `app`
app = application
