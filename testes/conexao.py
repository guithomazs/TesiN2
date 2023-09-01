import sqlite3
from sqlite3 import Error
def conecta():
    try:
        con = sqlite3.connect('banco.db')
        print('Conexão estabelecida com sucesso!')
        return con
    except Error as er:
        print('Erro durante a conexão.')

sql_criar_tabela = '''CREATE TABLE if not exists cliente(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome VARCHAR(100) NOT NULL,
cpf VARCHAR(11) NOT NULL,
email VARCHAR(60) NOT NULL
);'''
def criar_tabela(sql):
    con = conecta()
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()

sql_mostra_cliente = 'SELECT * FROM cliente;'
'Estabelecer a conexão com o banco de dados'
def mostrar_tabela(sql):
    con = conecta()
    cursor = con.cursor() #Objeto que permite executar SQL
    resultado = cursor.execute(sql)
    for i in resultado:
        print(i)
    con.close()

sql_inserir_cliente = "INSERT INTO cliente VALUES (NULL, 'Teste', '123', 'teste@teste');"
'Passos: conexão, usar a conexão, executar a instrução, fechar a conexão'
def inserir(sql):
    con = conecta()
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()

sql_atualizar = 'UPDATE cliente SET nome="Teste Alterado", email="teste@alterado" WHERE id=5;'
def atualizar(sql):
    con = conecta()
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()

sql_remover = f'DELETE FROM cliente WHERE id=4;'
def remover(sql):
    con = conecta()
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()

criar_tabela(sql_criar_tabela)
inserir(sql_inserir_cliente)
atualizar(sql_atualizar)
remover(sql_remover)
mostrar_tabela(sql_mostra_cliente)