from fastapi import FastAPI, Depends
from database import SessionLocal, Base, engine
from schemas import Libro, LibroBase
from model import LibroDB
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app = FastAPI() 

@app.post("/libros/", response_model=Libro)
async def crear_libro(libro: LibroBase, db: Session = Depends(get_db)):
    db_libro = LibroDB(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro