import tkinter as tk
from tkinter import ttk
from lexador_logic import AnalisadorLexico

class LexadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador Léxico Didático - Case 3")
        
        largura = 1100
        altura = 650
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        self.root.geometry(f"{largura}x{altura}+{(largura_tela-largura)//2}+{(altura_tela-altura)//2}")
        self.root.configure(bg="#2c3e50")

        self.logic = AnalisadorLexico()
        self.criar_widgets()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self.root, text="ANALISADOR LÉXICO (COMPILADORES)", font=("Arial", 20, "bold"), bg="#2c3e50", fg="white")
        lbl_titulo.pack(pady=15)

        frame_main = tk.Frame(self.root, bg="#2c3e50")
        frame_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Esquerda: Entrada
        frame_esq = tk.Frame(frame_main, bg="#2c3e50")
        frame_esq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(frame_esq, text="Código Fonte:", bg="#2c3e50", fg="white", font=("Arial", 12, "bold")).pack(anchor="w")
        self.text_entrada = tk.Text(frame_esq, font=("Consolas", 12), bg="#ecf0f1", height=15)
        self.text_entrada.pack(fill=tk.BOTH, expand=True, pady=5)
        self.text_entrada.insert(tk.END, "int contador = 10;\nfloat nota = 9.5;\n\n// Loop de teste\nif (contador > 5) {\n    print(nota);\n}")

        self.btn_analisar = tk.Button(frame_esq, text="▶ EXECUTAR ANÁLISE LÉXICA", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), command=self.iniciar_analise)
        self.btn_analisar.pack(fill=tk.X, pady=15)

        # Direita: Tabelas
        frame_dir = tk.Frame(frame_main, bg="#2c3e50")
        frame_dir.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Treeview Tokens
        tk.Label(frame_dir, text="Tokens Identificados:", bg="#2c3e50", fg="white", font=("Arial", 11, "bold")).pack(anchor="w")
        self.tree_tokens = ttk.Treeview(frame_dir, columns=("Tipo", "Lexema", "Linha"), show="headings", height=8)
        for col in ("Tipo", "Lexema", "Linha"):
            self.tree_tokens.heading(col, text=col)
            self.tree_tokens.column(col, width=100, anchor=tk.CENTER)
        self.tree_tokens.pack(fill=tk.BOTH, expand=True, pady=5)

        # Treeview Símbolos (Aqui entra sua pesquisa!)
        tk.Label(frame_dir, text="Tabela de Símbolos (Memória):", bg="#2c3e50", fg="white", font=("Arial", 11, "bold")).pack(anchor="w", pady=(15, 0))
        colunas_simb = ("ID", "Tipo Dado", "Escopo", "Endereço")
        self.tree_simbolos = ttk.Treeview(frame_dir, columns=colunas_simb, show="headings", height=6)
        for col in colunas_simb:
            self.tree_simbolos.heading(col, text=col)
            self.tree_simbolos.column(col, width=90, anchor=tk.CENTER)
        self.tree_simbolos.pack(fill=tk.BOTH, expand=True, pady=5)

    def iniciar_analise(self):
        for item in self.tree_tokens.get_children(): self.tree_tokens.delete(item)
        for item in self.tree_simbolos.get_children(): self.tree_simbolos.delete(item)

        codigo = self.text_entrada.get("1.0", tk.END)
        tokens, tabela_simbolos = self.logic.analisar(codigo)

        # Preenche a Tabela de Símbolos
        for lexema, info in tabela_simbolos.items():
            self.tree_simbolos.insert("", tk.END, values=(lexema, info["tipo"], info["escopo"], info["endereco"]))

        self.animar_tokens(tokens, 0)

    def animar_tokens(self, tokens, index):
        if index < len(tokens):
            tipo, lexema, linha = tokens[index]
            tag = "erro" if tipo == "ERRO_LEXICO" else ""
            self.tree_tokens.insert("", tk.END, values=(tipo, repr(lexema), linha), tags=(tag,))
            self.tree_tokens.tag_configure("erro", background="#e74c3c", foreground="white")
            self.tree_tokens.see(self.tree_tokens.get_children()[-1])
            self.root.after(100, self.animar_tokens, tokens, index + 1)