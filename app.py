from fastapi import FastAPI, Response
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

class Contato(BaseModel):
    nome: str
    email: Optional[str] = None
    idade: int
    habilitado: Optional[bool] = True


contatos = [
    {'id':1, 'nome': 'Joao', 'email': 'joao@email.com','idade': 50, 'habilitado': True},
    {'id':2,'nome': 'Jose', 'email': 'jose@email.com','idade': 40, 'habilitado': False},
    {'id':3,'nome': 'Maria', 'email': 'maria@email.com','idade': 16, 'habilitado': True}
]

@app.get('/')
def home():
    return Response('<h1>Exemplo com FastAPI</h1>')

@app.get('/contatos', tags=['contatos'])
def listar_contatos():
    return {'Agenda': contatos}

@app.get('/contatos/habilitados', tags=['contatos'])
def contatos_habilitados() -> list:
    contatos_habilitados = []
    for conta in contatos:
        if conta['habilitado']:
            contatos_habilitados.append(conta)
    return contatos_habilitados

@app.get('/contatos/{id_contato}', tags=['contatos'])
def obter_contato(id_contato: int) -> dict:
    for contato in contatos:
        if contato['id'] == id_contato:
            return contato
    return {}

@app.post('/contatos', tags=['contatos'])
def criar_contato(contato: Contato) -> dict:
    contato = dict(contato)
    contato['id'] = len(contatos) + 1
    contatos.append(contato)
    return contato

@app.put('/contatos/{id_contato}', tags=['contatos'])
def atualizar_contato(id_contato: int, contato: Contato) -> dict:
    contato = dict(contato)
    contato['id'] = id_contato
    for index, conta in enumerate(contatos):
        if conta['id'] == id_contato:
            contatos[index] = contato
            return {'message': f'Contato {conta['nome']} atualizado com sucesso'}
    return {'message':'Contato não encontrado para atualizar'}

@app.delete('/contatos/{id_contato}', tags=['contatos'])
def apagar_contato(id_contato:int) -> dict:
    for index, conta in enumerate(contatos):
        if conta['id']==id_contato:
            contatos.pop(index)
            return{'message': 'Contato removido com sucesso'}
    return {'message': 'Contato não encontrado'}
