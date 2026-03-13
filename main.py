from fastapi import FastAPI
from fastapi.responses import Response

#Инициализация FastAPI
app = FastAPI


@app.get('/health')
def health_check():
    return Response(status_code=200)