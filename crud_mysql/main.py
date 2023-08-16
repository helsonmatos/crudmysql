from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import models
from secrets import token_hex

app = FastAPI()


def conectaBanco():
    engine = create_engine(models.CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


@app.post('/cadastro')
def cadastro(nome:str, user: str, senha: str):
    
    session = conectaBanco()
    usuario = session.query(models.Pessoa).filter_by(usuario=user, senha=senha).all()
    
    if len(usuario) == 0:
        x = models.Pessoa(nome=nome, usuario=user, senha=senha)
        session.add(x)
        session.commit()
        return {'status':'sucess'}

    elif len(usuario) > 0:
        return {'status': 'Usuário já cadastrado.'}

@app.post('/login')
def login(usuario: str, senha: str):
    session = conectaBanco()
    user = session.query(models.Pessoa).filter_by(usuario=usuario, senha= senha). all()

    if len(user) == 0:
        return {'status': 'usuario inexistente'}
    
    #elif user[0].senha == int(senha):
    #   return {'status': 'senha incorreta'}
    
    while True:
        token = token_hex(50)
        token_existe = session.query(models.Tokens).filter_by(token=token).all()
        if len(token_existe) == 0:
            pessoa_existe = session.query(models.Tokens).filter_by(id_pessoa=user[0].id).all()
            if len(pessoa_existe) == 0:
                novo_token = models.Tokens(id_pessoa=user[0].id, token=token)
                session.add(novo_token)
            elif len(pessoa_existe) > 0:
                pessoa_existe[0].tokens = token

            session.commit()
            break
    return token