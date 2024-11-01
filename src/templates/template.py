from src.model.senha import Senha
from src.view.senhas_view import FernetHasher


def salvar_senha():
    if len(Senha.get()) == 0:
        chave, diretorio = FernetHasher.create_key(archive=True)
        print("Chave criada com Sucesso! Guarde-a com cuidado.")
        print(f'{chave.decode("utf-8")}\n')
        if diretorio:
            print("Chave salva com sucesso!")
            print(f'{diretorio}\n')
    else:
        chave = input("Digite sua chave usada para criptografia: ")
    try:
        user_fernet = FernetHasher(chave)
        dominio = input("Digite o domínio: ")
        senha = input("Digite a senha: ")
        senha_encriptada = user_fernet.encrypt(senha).decode("utf-8")
        s = Senha(dominio=dominio, senha=senha_encriptada)
        s.save()
        print("Senha salva com Sucesso!\n")
    except ValueError as e:
        print("Chave de crpitografia Inválida!\n")


def ver_senha():
    chave = input("Digite sua chave usada para criptografia: ")
    senha = None
    try:
        user_fernet = FernetHasher(chave)
        dominio = input("Digite o domínio: ")
        dados = Senha.get()

        for linha in dados:
            if dominio in linha["dominio"]:
                senha = user_fernet.decrypt(linha["senha"])

        if senha is not None:
            print(f'Senha de {dominio}: {senha}')
        else:
            print("Nenhuma senha encontrada para o domínio!\n")
    except ValueError as e:
        print("Chave de crpitografia Inválida!\n")


if __name__ == '__main__':
    while 1:
        print("Menu")
        print("1: Salvar nova senha\n2: Ver uma senha salva\n3: Encerrar\n")
        escolha = input('Escolha: ')
        match escolha:
            case '1':
                salvar_senha()
            case '2':
                ver_senha()
            case '3':
                break
            case _:
                print("Opção inválida!\n")
