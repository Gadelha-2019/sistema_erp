import pymysql.cursors

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
autentico = False

def logarCadastrar():
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = 2

    if decisao == 1:
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False
        if not autenticado:
            print('Email ou Senha Inváldos')

    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1

        if usuarioExistente == 1:
            print('Usuário já cadastrado tente um nome ou senha diferentes')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros(nome, senha, nivel) values (%s, %s, %s)', (nome, senha, 1))
                    conexao.commit()
                print('Usuário cadastrado com sucesso')
            except:
                print('Erro ao inserir os dados no banco')

    return autenticado, usuarioMaster

def cadastrarProdutos():
    nome = input('Digite o nome do produto: ')
    ingredientes = input('Digite os ingredientes do produto: ')
    grupo = input('Digite o grupo pertencente a esse produto: ')
    preco = float(input('Digite o preço do produto:R$ '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos(nome, ingredientes, grupo, preco) values (%s, %s, %s, %s)', (nome, ingredientes, grupo, preco))
            conexao.commit()
            print('Produto cadastrado com sucesso')
    except:
        print('Erro ao inserir os produtos no banco de dados')

def listarProdutos():
    produtos = []

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()
    except:
        print('Erro ao conectar ao banco de dados')
    for i in produtosCadastrados:
        produtos.append(i)
    if len(produtos) != 0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('Nenhum produto cadastrado!')

def excluirProduto():
    idDeletar = int(input('Digite o id referente ao produto que deseja excluir: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('delete from produtos where id = {}'.format(idDeletar))
    except:
        print('Erro ao tentar excluir o produto')


while not autentico:
    decisao = int(input('Digite [1] - Logar [2] - Cadastrar'))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()
    except:
        print('Erro ao conectar no banco de dados')

    autentico, usuarioSupremo = logarCadastrar()


if autentico:
    print('Usuário autenticado com sucesso')

    if usuarioSupremo == True:
        decisaoUsuario = 1

        while decisaoUsuario != 0:
            decisaoUsuario = int(input('Digite [0] - Sair [1] - Cadastrar produtos [2] - Listar produtos cadastrados: '))

            if decisaoUsuario == 1:
                cadastrarProdutos()
            elif decisaoUsuario == 2:
                listarProdutos()

                delete = int(input('Digite [1] - Excluir produto [2] - Sair'))

                if delete == 1:
                    excluirProduto()


