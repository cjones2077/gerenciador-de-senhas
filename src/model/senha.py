from datetime import datetime
from pathlib import Path


class ModeloBase:
    # define o diretório base do projeto
    BASE_DIR = Path("../../../gerenciador-de-senhas")

    # define o diretório onde os atributos serão salvos
    DB_DIR = BASE_DIR / "db"

    def save(self):  # salva os todos os atributos criados e seus respectivos valores
        diretorio = self.DB_DIR / f'{self.__class__.__name__}.txt'
        tabela_dir = Path(diretorio)

        if not tabela_dir.exists():
            tabela_dir.touch()

        with open(tabela_dir, "a") as arq:
            arq.write("|".join(list(map(str, self.__dict__.values()))))
            arq.write("\n")

    @classmethod
    def get(cls):  # retorna todas os atributos salvos
        diretorio = cls.DB_DIR / f'{cls.__name__}.txt'
        tabela_dir = Path(diretorio)

        if not tabela_dir.exists():
            tabela_dir.touch()

        with open(tabela_dir, "r") as arq:
            linhas = arq.readlines()

        atributos = vars(cls())  # atributos da classe
        resultados = []

        for linha in linhas:
            linha_split = linha.split('|')
            dict_ = dict(zip(atributos, linha_split))  # salva os atributos e valores como um dicionário
            resultados.append(dict_)
        return resultados


class Senha(ModeloBase):
    def __init__(self, dominio=None, senha=None, ):
        self.dominio = dominio
        self.senha = senha
        self.data_criacao = datetime.now().isoformat()
