from fastapi import FastAPI
from projeto import roteador as roteador_projeto
from tarefa import roteador as roteador_tarefa

app = FastAPI()
app.include_router(roteador_projeto.roteador,
                   prefix='/projeto',
                   tags=['projeto']
                )

app.include_router(roteador_tarefa.roteador,
                   prefix='/tarefa',
                   tags=['tarefa']
                )