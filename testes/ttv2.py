import tkinter as tk
from tkinter import ttk

janela = tk.Tk()
colunas = ('nome', 'telefone', 'email')
tvw = ttk.Treeview(janela, columns=colunas, height=5, show='headings')
tvw.grid()
#Cabeçalho
tvw.heading('nome', text='Nome')
tvw.heading('telefone', text='Telefone')
tvw.heading('email', text='E-mail')
#Colunas
tvw.column('nome', minwidth=200, width=200)
tvw.column('telefone', minwidth=100, width=100)
tvw.column('email', minwidth=300, width=300)
#Linhas
tvw.insert('', 'end', values=['Limeira', '99999', 'limeira@ufac'])
tvw.insert('', 'end', values=['Fulano', '99999', 'fulano@ufac'])
tvw.insert('', 'end', values=['Beltrano', '99999', 'beltrano@ufac'])
tvw.insert('', 'end', values=['Ciclano', '99999', 'ciclano@ufac'])
tvw.insert('', 'end', values=['Pek', '99999', 'pek@ufac'])
tvw.insert('', 'end', values=['Segovinha', '99999', 'pek@ufac'])
tvw.insert('', 'end', values=['Orelhano', '99999', 'pek@ufac'])
tvw.insert('', 'end', values=['Pedro Raul', '99999', 'pek@ufac'])
#Barra de rolagem
scb = tk.Scrollbar(janela, orient=tk.VERTICAL,command=tvw.yview)
scb.grid(row=0, column=1, sticky='ns')
tvw.config(yscrollcommand=scb.set)

janela.mainloop()