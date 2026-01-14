from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database
from model import Libro, LibroBase, Utente, UtenteBase, Prenotazione, PrenotazioneCreate, PrenotazioneUpdate
from repository import LibroRepository, UtenteRepository, PrenotazioneRepository

database.init_db()
app = FastAPI(title="Gestione Biblioteca")

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

repo_libri = LibroRepository()
repo_utenti = UtenteRepository()
repo_prenotazioni = PrenotazioneRepository()

@app.post("/libri/", response_model=Libro, tags=["Libri"])
def crea_libro(libro: LibroBase, db: Session = Depends(get_db)):
    return repo_libri.crea(db, libro)

@app.get("/libri/", response_model=List[Libro], tags=["Libri"])
def leggi_libri(db: Session = Depends(get_db)):
    return repo_libri.leggi_tutti(db)

@app.post("/utenti/", response_model=Utente, tags=["Utenti"])
def crea_utente(utente: UtenteBase, db: Session = Depends(get_db)):
    return repo_utenti.crea(db, utente)

@app.get("/utenti/", response_model=List[Utente], tags=["Utenti"])
def leggi_utenti(db: Session = Depends(get_db)):
    return repo_utenti.leggi_tutti(db)

@app.post("/prenotazioni/", response_model=Prenotazione, tags=["Prenotazioni"])
def crea_prenotazione(pren: PrenotazioneCreate, db: Session = Depends(get_db)):
    if not repo_libri.leggi_uno(db, pren.libro_id): raise HTTPException(404, "Libro non trovato")
    if not repo_utenti.leggi_uno(db, pren.utente_id): raise HTTPException(404, "Utente non trovato")
    return repo_prenotazioni.crea(db, pren)

@app.put("/prenotazioni/{id}/termina", response_model=Prenotazione, tags=["Prenotazioni"])
def termina_prenotazione(id: int, db: Session = Depends(get_db)):
    res = repo_prenotazioni.termina(db, id)
    if not res: raise HTTPException(404, "Prenotazione non trovata")
    return res

@app.patch("/prenotazioni/{id}", response_model=Prenotazione, tags=["Prenotazioni"])
def aggiorna_prenotazione(id: int, payload: PrenotazioneUpdate, db: Session = Depends(get_db)):
    res = repo_prenotazioni.aggiorna(db, id, payload)
    if not res: raise HTTPException(404, "Prenotazione non trovata")
    return res