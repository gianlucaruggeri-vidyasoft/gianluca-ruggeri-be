from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- ENTITÀ DATABASE ---
class LibroDB(Base):
    __tablename__ = "libri"
    id = Column(Integer, primary_key=True, index=True)
    titolo = Column(String, index=True)
    autore = Column(String)
    copie_totali = Column(Integer, default=1)
    prenotazioni = relationship("PrenotazioneDB", back_populates="libro")

class UtenteDB(Base):
    __tablename__ = "utenti"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    prenotazioni = relationship("PrenotazioneDB", back_populates="utente")

class PrenotazioneDB(Base):
    __tablename__ = "prenotazioni"
    id = Column(Integer, primary_key=True, index=True)
    data_inizio = Column(DateTime, default=datetime.now)
    data_fine = Column(DateTime, nullable=True)
    attiva = Column(Boolean, default=True)
    libro_id = Column(Integer, ForeignKey("libri.id"))
    utente_id = Column(Integer, ForeignKey("utenti.id"))
    libro = relationship("LibroDB", back_populates="prenotazioni")
    utente = relationship("UtenteDB", back_populates="prenotazioni")

# --- DTO (Pydantic) ---
class LibroBase(BaseModel):
    titolo: str
    autore: str
    copie_totali: int
class Libro(LibroBase):
    id: int
    class Config: orm_mode = True

class UtenteBase(BaseModel):
    nome: str
    email: str
class Utente(UtenteBase):
    id: int
    class Config: orm_mode = True

class PrenotazioneCreate(BaseModel):
    libro_id: int
    utente_id: int
class Prenotazione(BaseModel):
    id: int
    data_inizio: datetime
    data_fine: Optional[datetime]
    attiva: bool
    libro_id: int
    utente_id: int
    class Config: orm_mode = True