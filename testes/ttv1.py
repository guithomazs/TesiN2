import tkinter as tk
from tkinter import ttk

janela = tk.Tk()

tvw = ttk.Treeview(janela)
tvw.pack()
professores = tvw.insert('', 'end', text='Professores')
tvw.insert(professores, 'end', text='Fulano')
tvw.insert(professores, 0, text='Beltrano')
alunos = tvw.insert('', 'end', text='Alunos')
tvw.insert(alunos, 'end', text='Ciclano')


janela.mainloop()