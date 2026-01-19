from fastapi import FastAPI

from pkg.config.database import init_db
from pkg.routers.libri import router as libri_router
from pkg.routers.prenotazioni import router as prenotazioni_router
from pkg.routers.utenti import router as utenti_router


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(title="Gestione Biblioteca")
    app.include_router(libri_router)
    app.include_router(utenti_router)
    app.include_router(prenotazioni_router)
    return app


app = create_app()
