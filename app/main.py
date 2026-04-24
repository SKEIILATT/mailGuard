from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, emails

app = FastAPI(title='MailGuard API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(emails.router, prefix='/emails', tags=['emails'])

@app.get('/')
def root():
    return {'status': 'MailGuard API corriendo'}