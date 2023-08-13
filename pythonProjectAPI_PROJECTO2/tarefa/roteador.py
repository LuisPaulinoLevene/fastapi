from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

roteador = APIRouter()
nome_de_arquivo = 'database.json'


class Tarefa(BaseModel):
    id: int
    nome: str
    descricao: str
    feito: bool
    projetoID: int


def transformar_em_dict(tarefa: Tarefa) -> dict:
    return {
        'id': tarefa.id,
        'nome': tarefa.nome,
        'descricao': tarefa.descricao,
        'projetoID': tarefa.projetoID
    }


def carregar_dados():
    try:
        with open(nome_de_arquivo, 'r') as db:
            return json.load(db)
    except FileNotFoundError:
        return {"tarefa": []}


def mandar_dados(dict_em_db: dict):
    with open(nome_de_arquivo, 'w') as db:
        json.dump(dict_em_db, db)


dict_db = carregar_dados()
'''========================================================================================'''

@roteador.post('/{id}')
def crir_tarefa(tarefa: Tarefa):
    convertido = transformar_em_dict(tarefa)
    dict_db['tarefas'].append(convertido)
    mandar_dados(dict_db)


@roteador.get('/')
def ver_tarefa():
    return dict_db['tarefa']

@roteador.get('/{id}')
def ver_uma_tarefa(id: int):
    filtro = filter(lambda tarefa: tarefa['id']==id, dict_db['tarefas'])
    tarefa = list(filtro)[0]
    return tarefa


@roteador.put('/{id}')
def actualizar_um_tarefa(tarefa: Tarefa, id: int):
    filtro = filter(lambda tarefa: tarefa['id'] == id, dict_db['tarefas'])
    antiga_tarefa = list(filtro)[0]
    antiga_tarefa['nome'] = tarefa.nome
    antiga_tarefa['descricao'] = tarefa.descricao
    antiga_tarefa['feito'] = tarefa.feito
    antiga_tarefa['projetoID'] = tarefa.projetoID
    mandar_dados(dict_db)
    return {'mensagem': 'Dados actualizado.'}

@roteador.delete('/{id}')
def apagar_tarefa(id: int):
    filtro = filter(lambda tarefa: tarefa['id'] == id, dict_db['projetos'])
    tarefa= list(filtro)[0]
    dict_db['projetos'].remove(tarefa)
    return {'mensagem': 'tarefa apagado.'}