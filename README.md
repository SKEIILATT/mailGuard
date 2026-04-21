# MailGuard

MailGuard es una app de filtrado inteligente de correos que se conecta a tu Gmail y organiza tu bandeja de entrada automáticamente usando un motor de reglas. Sin más spam, newsletters ni correos no deseados llenando tu correo.

> 🚧 Este proyecto está actualmente en desarrollo activo.

---

## Qué hace

- Se conecta a tu Gmail mediante Google OAuth (sin guardar contraseñas)
- Lee los correos entrantes y los evalúa contra tus reglas personalizadas
- Archiva, etiqueta, mueve o elimina correos automáticamente según tus preferencias
- Corre en segundo plano para que tu bandeja de entrada se mantenga limpia

---

## Stack tecnológico

- **Backend**: Python + FastAPI
- **Correo**: Gmail API (Google)
- **Autenticación**: Google OAuth 2.0
- **Base de datos**: PostgreSQL + SQLAlchemy
- **Frontend**: Next.js (TypeScript)

---

## Estructura del proyecto

```
mailguard/
├── mailguard-backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── auth/
│   │   ├── gmail/
│   │   ├── rules/
│   │   ├── models/
│   │   └── db/
│   ├── requirements.txt
│   └── .env.example
└── mailguard-frontend/        (próximamente)
```

---

## Cómo empezar

### Requisitos previos

- Python 3.12+
- Un proyecto en Google Cloud con Gmail API habilitada
- Credenciales OAuth 2.0 (`credentials.json`)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/mailguard.git
cd mailguard/mailguard-backend

# Crear y activar entorno virtual
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt
```

### Configuración de Google Cloud

1. Ve a [console.cloud.google.com](https://console.cloud.google.com)
2. Crea un nuevo proyecto llamado `mailguard`
3. Habilita la Gmail API
4. Configura la pantalla de consentimiento OAuth (Externo)
5. Crea credenciales OAuth (Aplicación de escritorio) y descarga el `credentials.json`
6. Coloca el `credentials.json` dentro de la carpeta `mailguard-backend/`

### Ejecutar el script de correos

```bash
python fetch_emails.py
```

La primera vez se abrirá una ventana del navegador pidiendo que autorices el acceso a Gmail. Después verás tus últimos 20 correos impresos en la terminal.

---

## Seguridad y privacidad

- Tus correos nunca se almacenan en ningún servidor
- Solo se guarda el resultado de la clasificación (etiqueta), nunca el contenido del correo
- Los tokens de OAuth se guardan localmente y nunca se comparten
- `credentials.json` y `token.json` están excluidos del control de versiones

---

## Roadmap

- [x] Conexión con Gmail API
- [x] Motor de reglas básico (remitente, asunto, dominio)
- [ ] Backend con FastAPI y endpoints REST
- [ ] Google OAuth para múltiples usuarios
- [ ] Polling automático cada hora
- [ ] Dashboard en Next.js
- [ ] Constructor visual de reglas
- [ ] Clasificación inteligente con IA (premium)
- [ ] Pagos con Stripe

---

