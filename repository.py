from sqlalchemy.orm import Session
from model import LibroDB, UtenteDB, PrenotazioneDB, LibroBase, UtenteBase, PrenotazioneCreate, PrenotazioneUpdate
from datetime import datetime

class LibroRepository:
    def crea(self, db: Session, libro: LibroBase):
        db_libro = LibroDB(**libro.model_dump())
        db.add(db_libro)
        db.commit()
        db.refresh(db_libro)
        return db_libro

    def leggi_tutti(self, db: Session):
        return db.query(LibroDB).all()

    def leggi_uno(self, db: Session, id: int):
        return db.query(LibroDB).filter(LibroDB.id == id).first()

    def aggiorna(self, db: Session, id: int, dati: LibroBase):
        obj = db.query(LibroDB).filter(LibroDB.id == id).first()
        if obj:
            obj.titolo = dati.titolo
            obj.autore = dati.autore
            obj.copie_totali = dati.copie_totali
            db.commit()
            db.refresh(obj)
            return obj
        return None

    def elimina(self, db: Session, id: int):
        obj = db.query(LibroDB).filter(LibroDB.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

class UtenteRepository:
    def crea(self, db: Session, utente: UtenteBase):
        db_utente = UtenteDB(**utente.model_dump())
        db.add(db_utente)
        db.commit()
        db.refresh(db_utente)
        return db_utente

    def leggi_tutti(self, db: Session):
        return db.query(UtenteDB).all()

    def leggi_uno(self, db: Session, id: int):
        return db.query(UtenteDB).filter(UtenteDB.id == id).first()

    def aggiorna(self, db: Session, id: int, dati: UtenteBase):
        obj = db.query(UtenteDB).filter(UtenteDB.id == id).first()
        if obj:
            obj.nome = dati.nome
            obj.email = dati.email
            db.commit()
            db.refresh(obj)
            return obj
        return None

    def elimina(self, db: Session, id: int):
        obj = db.query(UtenteDB).filter(UtenteDB.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

class PrenotazioneRepository:
    def crea(self, db: Session, dati: PrenotazioneCreate):
        nuova = PrenotazioneDB(libro_id=dati.libro_id, utente_id=dati.utente_id)
        db.add(nuova)
        db.commit()
        db.refresh(nuova)
        return nuova

    def trova_tutte(self, db: Session):
        return db.query(PrenotazioneDB).all()
    
    def leggi_tutti(self, db: Session):
        return db.query(PrenotazioneDB).all()

    def termina(self, db: Session, id: int):
        p = db.query(PrenotazioneDB).filter(PrenotazioneDB.id == id).first()
        if p and p.attiva:
            p.attiva = False
            p.data_fine = datetime.now()
            db.commit()
            db.refresh(p)
            return p
        return None

    def aggiorna(self, db: Session, id: int, dati: PrenotazioneUpdate):
        db_pren = db.query(PrenotazioneDB).filter(PrenotazioneDB.id == id).first()
        if not db_pren:
            return None
        
        update_data = dati.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_pren, key, value)

        db.commit()
        db.refresh(db_pren)
        return db_pren