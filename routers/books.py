from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
# Importiamo le classi Repository
from repositories import LibroRepository, PrenotazioneRepository
from schemas import Libro, LibroBase, Prenotazione, PrenotazioneCreate
# Nota: Assicurati di importare PrenotazioneDB o gestire l'errore 404 nel service, 
# ma per ora va bene così.

router = APIRouter(prefix="/books", tags=["libri"])

# Istanziamo i repository
libro_repo = LibroRepository()
prenotazione_repo = PrenotazioneRepository()

@router.get("/", response_model=List[Libro])
def get_books(db: Session = Depends(get_db)):
    # Guarda quanto è pulito ora!
    return libro_repo.leggi_tutti(db)

@router.post("/", response_model=Libro)
def create_book(libro: LibroBase, db: Session = Depends(get_db)):
    return libro_repo.crea(db, libro)

# --- Endpoint Prenotazione ---
@router.post("/{book_id}/reserve/v1", response_model=Prenotazione)
def reserve_book(book_id: int, prenotazione_in: PrenotazioneCreate, db: Session = Depends(get_db)):
    
    # 1. Controlliamo se il libro esiste usando il repo
    libro = libro_repo.leggi_uno(db, book_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro non trovato")

    # 2. Prepariamo i dati per la prenotazione
    # Poiché il repo si aspetta un oggetto con libro_id, dobbiamo assicurarci
    # che sia quello dell'URL
    prenotazione_in.libro_id = book_id 
    
    # 3. Creiamo
    return prenotazione_repo.crea(db, prenotazione_in)