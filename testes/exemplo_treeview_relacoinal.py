import tkinter as tk

import ttkbootstrap
from ttkbootstrap import ttk
from tkinter import messagebox
import conexao as bd
from ttkbootstrap.constants import *

class Tela():
    def __init__(self, master):
        self.janela = master
        colunas = ('id', 'numero', 'saldo', 'nome')
        self.tvw = ttk.Treeview(self.janela, columns=colunas, height=5, show='headings', bootstyle=DARK)
        self.tvw.grid()
        #Cabeçalho
        self.tvw.heading('id', text='ID')
        self.tvw.heading('numero', text='Número')
        self.tvw.heading('saldo', text='Saldo')
        self.tvw.heading('nome', text='Nome')
        #Colunas
        self.tvw.column('id', minwidth=30, width=30)
        self.tvw.column('numero', minwidth=100, width=100)
        self.tvw.column('saldo', minwidth=100, width=100)
        self.tvw.column('nome', minwidth=200, width=200)
        #Linhas
        self.atualizar_treeview()
        #Barra de rolagem
        scb = ttk.Scrollbar(self.janela, orient=tk.VERTICAL,command=self.tvw.yview)
        scb.grid(row=0, column=1, sticky='ns')
        self.tvw.config(yscrollcommand=scb.set)
        #Botões
        frm_botoes = tk.Frame(self.janela)
        frm_botoes.grid(row=1, column=0)
        btn_cadastrar = ttk.Button(frm_botoes, text='Cadastrar',
                                   command=self.cadastrar)
        btn_cadastrar.grid(row=0, column=0, padx=5, pady=5)
        btn_excluir = ttk.Button(frm_botoes,
                                  text='Excluir',
                                  command=self.excluir)
        btn_excluir.grid(row=0, column=1, padx=5, pady=5)

    def atualizar_treeview(self):
        items = self.tvw.get_children() #limpando o componente treeview antes de preencher com o conteúdo do BD
        for i in items:
            self.tvw.delete(i)
        sql_listar_contas = ''
        dados = bd.listar(sql_listar_contas)
        for linha in dados:
            self.tvw.insert('', tk.END, values=linha)

    def excluir(self):
        tupla = self.tvw.selection()
        if len(tupla) != 1:
            messagebox.showwarning('Aviso', 'Selecione somente um item')
        else:
            id = self.tvw.item(tupla, 'values')[0]
            nome = self.tvw.item(tupla, 'values')[1]
            f'SELECT nome FROM conta WHERE id={id};'
            confirma = messagebox.askyesno('Aviso', f'Confirma a exclusão do cliente: {nome}?')
            if confirma:
                bd.remover(f'DELETE FROM conta WHERE id={id}')
                for item in tupla:
                    self.tvw.delete(item)

    def cadastrar(self):
        self.top_cadastrar = ttkbootstrap.Toplevel()
        self.top_cadastrar.grab_set()
        lbl_numero = tk.Label(self.top_cadastrar, text='Número:')
        lbl_numero.grid(row=0, column=0, pady=2, stick='w')
        lbl_nome = tk.Label(self.top_cadastrar, text='Nome:')
        lbl_nome.grid(row=1, column=0, pady=2, stick='w')
        self.ent_num_conta = tk.Entry(self.top_cadastrar)
        self.ent_num_conta.grid(row=0, column=1, pady=2)
        self.ent_nome_cliente = tk.Entry(self.top_cadastrar)
        self.ent_nome_cliente.grid(row=1, column=1, pady=2)
        self.btn_pesquisar = tk.Button(self.top_cadastrar, text='Pesquisar Cliente', command=self.pesquisar)
        self.btn_pesquisar.grid(row=2, column=0)

        btn_confirmar = tk.Button(self.top_cadastrar,
                                  text='Confirmar',
                                  command=self.confirmar_cadastro)
        btn_confirmar.grid(row=2, column=1, padx=5, pady=5)

    def pesquisar(self):
        # Janela para pesquisar clientes (semelhante a de listagem) com um botão de pesquisar e ourto para selecionar
        pass
    def selecionar(self):
        # Função para selecionar um cliente, guardar nome + id nos campos de entrada e destruir a TopLevel
        pass
    def pesquisar_cliente(self):
        # Função para limpar o treeview, usar o nome digitado para buscar no BD o cliente com o operador like "%{nome}%" e preencher o treeview
        pass
    def confirmar_cadastro(self):
        # Função para inserir os dados da conta no BD, atalizar o treeview e destruir a TopLevel
        pass

app = ttkbootstrap.Window(themename='litera')
Tela(app)
app.mainloop()