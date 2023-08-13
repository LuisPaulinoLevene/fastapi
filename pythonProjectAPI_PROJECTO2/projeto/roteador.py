from fastapi import APIRouter
from pydantic import BaseModel
import json


roteador = APIRouter()
nome_de_arquivo = 'database.json'

tarefa = None
class Projeto(BaseModel):
    id: int
    nome: str
    descricao: str
    tarefas: list



def transformar_em_dict(projeto: Projeto) -> dict:
    return {
        'id': projeto.id,
        'nome': projeto.nome,
        'descricao': projeto.descricao,
        'tarefas': projeto.tarefas
    }


def carregar_dados():
    try:
        with open(nome_de_arquivo, 'r') as db:
            return json.load(db)
    except FileNotFoundError:
        return {"projetos": []}

def mandar_dados(dict_em_db: dict):
    with open(nome_de_arquivo, 'w') as db:
        json.dump(dict_em_db, db)


dict_db = carregar_dados()

'''=============================================================================================='''

@roteador.post('/')
def crir_projeto(projeto: Projeto):
    convertido = transformar_em_dict(projeto)
    dict_db['projetos'].append(convertido)
    mandar_dados(dict_db)


@roteador.get('/')
def ver_projetos():
    return dict_db['projetos']

@roteador.get('/{id}')
def ver_um_projeto(id: int):
    filtro = filter(lambda projeto: projeto['id']==id, dict_db['projetos'])
    projeto = list(filtro)[0]
    return projeto

@roteador.put('/{id}')
def actualizar_um_projeto(projeto: Projeto, id: int):
    filtro = filter(lambda projeto: projeto['id'] == id, dict_db['projetos'])
    antigo_projeto = list(filtro)[0]
    antigo_projeto['marca'] = projeto.nome
    antigo_projeto['descricao'] = projeto.descricao
    antigo_projeto['tarefas'] = projeto.tarefas
    mandar_dados(dict_db)
    return {'mensagem': 'Dados actualizado.'}

@roteador.delete('/{id}')
def apagar_projeto(id: int):
    filtro = filter(lambda projeto: projeto['id'] == id, dict_db['projetos'])
    projeto = list(filtro)[0]
    dict_db['projetos'].remove(projeto)
    return {'mensagem': 'projeto apagado.'}