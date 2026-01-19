from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pkg.config.database import get_db
from pkg.repositories.libri import LibroRepository
from pkg.repositories.prenotazioni import PrenotazioneRepository
from pkg.repositories.utenti import UtenteRepository
from pkg.schemas.prenotazione import Prenotazione, PrenotazioneCreate, PrenotazioneUpdate
from pkg.services.reservations import PrenotazioneService

router = APIRouter(prefix="/prenotazioni", tags=["Prenotazioni"])

libri_repo = LibroRepository()
utenti_repo = UtenteRepository()
prenotazioni_repo = PrenotazioneRepository()
prenotazione_service = PrenotazioneService(libri_repo, utenti_repo, prenotazioni_repo)


@router.post("/", response_model=Prenotazione)
def crea_prenotazione(pren: PrenotazioneCreate, db: Session = Depends(get_db)):
    try:
        return prenotazione_service.crea(db, pren)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.put("/{prenotazione_id}/termina", response_model=Prenotazione)
def termina_prenotazione(prenotazione_id: int, db: Session = Depends(get_db)):
    result = prenotazione_service.termina(db, prenotazione_id)
    if not result:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return result


@router.patch("/{prenotazione_id}", response_model=Prenotazione)
def aggiorna_prenotazione(
    prenotazione_id: int,
    payload: PrenotazioneUpdate,
    db: Session = Depends(get_db),
):
    result = prenotazione_service.aggiorna(db, prenotazione_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    return result
