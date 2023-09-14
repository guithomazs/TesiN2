import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Tela():
    def __init__(self, master):
        self.janela = master
        colunas = ('nome', 'telefone', 'email')
        self.tvw = ttk.Treeview(self.janela, columns=colunas, height=5, show='headings')
        self.tvw.grid()
        #Cabeçalho
        self.tvw.heading('nome', text='Nome')
        self.tvw.heading('telefone', text='Telefone')
        self.tvw.heading('email', text='E-mail')
        #Colunas
        self.tvw.column('nome', minwidth=200, width=200)
        self.tvw.column('telefone', minwidth=100, width=100)
        self.tvw.column('email', minwidth=300, width=300)
        #Linhas
        self.tvw.insert('', 'end', values=['Limeira', '99999', 'limeira@ufac'])
        self.tvw.insert('', 'end', values=['Fulano', '99999', 'fulano@ufac'])
        self.tvw.insert('', 'end', values=['Beltrano', '99999', 'beltrano@ufac'])
        self.tvw.insert('', 'end', values=['Ciclano', '99999', 'ciclano@ufac'])
        self.tvw.insert('', 'end', values=['Pek', '99999', 'pek@ufac'])
        self.tvw.insert('', 'end', values=['Segovinha', '99999', 'pek@ufac'])
        self.tvw.insert('', 'end', values=['Orelhano', '99999', 'pek@ufac'])
        self.tvw.insert('', 'end', values=['Pedro Raul', '99999', 'pek@ufac'])
        #Barra de rolagem
        scb = tk.Scrollbar(self.janela, orient=tk.VERTICAL,command=self.tvw.yview)
        scb.grid(row=0, column=1, sticky='ns')
        self.tvw.config(yscrollcommand=scb.set)
        #Botões
        frm_botoes = tk.Frame(self.janela)
        frm_botoes.grid(row=1, column=0)
        btn_cadastrar = tk.Button(frm_botoes, text='Cadastrar',
                                  command=self.cadastrar)
        btn_cadastrar.grid(row=0, column=0)
        btn_excluir = tk.Button(frm_botoes,
                                  text='Excluir',
                                  command=self.excluir)
        btn_excluir.grid(row=0, column=1)
        btn_editar = tk.Button(frm_botoes, text='Editar',
                               command=self.editar)
        btn_editar.grid(row=0, column=2)

    def editar(self):
        item = self.tvw.selection()
        if len(item) != 1:
            messagebox.showwarning('Aviso', 'Selecione apenas um item')
        else:
            valores = self.tvw.item(item, 'values')
            self.top_editar = tk.Toplevel()
            self.top_editar.grab_set()
            lbl_nome = tk.Label(self.top_editar, text='Nome:')
            lbl_nome.grid(row=0, column=0)
            lbl_telefone = tk.Label(self.top_editar, text='Telefone:')
            lbl_telefone.grid(row=1, column=0)
            lbl_email = tk.Label(self.top_editar, text='E-mail:')
            lbl_email.grid(row=2, column=0)
            self.ent_nome = tk.Entry(self.top_editar)
            self.ent_nome.grid(row=0, column=1)
            self.ent_nome.insert('end', valores[0])
            self.ent_telefone = tk.Entry(self.top_editar)
            self.ent_telefone.grid(row=1, column=1)
            self.ent_telefone.insert('end', valores[1])
            self.ent_email = tk.Entry(self.top_editar)
            self.ent_email.grid(row=2, column=1)
            self.ent_email.insert('end', valores[2])
            btn_confirmar = tk.Button(self.top_editar,
                                      text='Confirmar',
                                      command=self.confirmar_edicao)
            btn_confirmar.grid(row=3, column=0)

    def confirmar_edicao(self):
        nome = self.ent_nome.get()
        telefone = self.ent_telefone.get()
        email = self.ent_email.get()
        selecionado = self.tvw.selection()
        if nome == '' or telefone == '' or email == '':
            messagebox.showinfo('Aviso', 'Por favor, todos os campos são obrigatórios.', parent=self.top_cadastrar)
        else:
            self.tvw.item(selecionado, values=(nome, telefone, email))
            self.top_editar.destroy()

    def excluir(self):
        tupla = self.tvw.selection()
        # if len(tupla) == 1:
        #     self.tvw.delete(tupla)
        # elif len(tupla) > 1:
        #     for item in tupla:
        #         self.tvw.delete(item)
        for item in tupla:
            self.tvw.delete(item)


    def cadastrar(self):
        self.top_cadastrar = tk.Toplevel()
        self.top_cadastrar.grab_set()
        lbl_nome = tk.Label(self.top_cadastrar, text='Nome:')
        lbl_nome.grid(row=0, column=0)
        lbl_telefone = tk.Label(self.top_cadastrar, text='Telefone:')
        lbl_telefone.grid(row=1, column=0)
        lbl_email = tk.Label(self.top_cadastrar, text='E-mail:')
        lbl_email.grid(row=2, column=0)
        self.ent_nome = tk.Entry(self.top_cadastrar)
        self.ent_nome.grid(row=0, column=1)
        self.ent_telefone = tk.Entry(self.top_cadastrar)
        self.ent_telefone.grid(row=1, column=1)
        self.ent_email = tk.Entry(self.top_cadastrar)
        self.ent_email.grid(row=2, column=1)
        btn_confirmar = tk.Button(self.top_cadastrar,
                                  text='Confirmar',
                                  command=self.confirmar_cadastro)
        btn_confirmar.grid(row=3, column=0)


    def confirmar_cadastro(self):
        nome = self.ent_nome.get()
        telefone = self.ent_telefone.get()
        email = self.ent_email.get()
        if nome == '' or telefone == '' or email == '':
            messagebox.showinfo('Aviso', 'Por favor, todos os campos são obrigatórios.', parent=self.top_cadastrar)
        else:
            self.tvw.insert('','end', values=(nome, telefone, email))
            self.top_cadastrar.destroy()

app = tk.Tk()
Tela(app)
app.mainloop()