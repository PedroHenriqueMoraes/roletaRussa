from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Conectar ao banco de dados SQLite
DATABASE_URL = "sqlite:///players.db"  # Para MySQL ou PostgreSQL, substitua por sua URL
engine = create_engine(DATABASE_URL, echo=True)  # echo=True para logs de SQL


Base = declarative_base()

class Jogadores(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key= True, autoincrement= True )
    usuario = Column(String, nullable=False)  # 'user'
    vida = Column(Integer, nullable=False)
    lista = Column(JSON, nullable= False)

    


Base.metadata.create_all(engine)

    
