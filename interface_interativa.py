"""
Interface Interativa - Sistema de Otimização de Rotas
======================================================
Interface gráfica para o sistema de cálculo de rotas.
Permite:
- Visualizar cidades predefinidas sem grafo
- Escolher origem e destino para gerar o grafo
- Quebrar estradas e recalcular automaticamente
"""

import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Patch
import copy
from otimizacao_rotas import RedeDistribuicao


class InterfaceRotas:
    """Interface gráfica para o sistema de rotas."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Otimização de Rotas")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Estado da aplicação
        self.rede = None
        self.grafo_gerado = False
        self.estradas_quebradas = []  # Lista de estradas quebradas
        self.grafo_backup = None  # Backup do grafo original
        
        # Cidades predefinidas (sem grafo ainda)
        self.cidades_predefinidas = {
            'armazem': "São Paulo",
            'intermediarias': ["Campinas", "Ribeirão Preto", "Sorocaba"],
            'clientes': ["Rio de Janeiro", "Belo Horizonte", "Curitiba"]
        }
        
        # Estradas predefinidas (para quando gerar o grafo)
        self.estradas_predefinidas = [
            ("São Paulo", "Campinas", 100),
            ("São Paulo", "Sorocaba", 90),
            ("São Paulo", "Ribeirão Preto", 310),
            ("Campinas", "Rio de Janeiro", 350),
            ("Campinas", "Belo Horizonte", 580),
            ("Campinas", "Sorocaba", 120),
            ("Sorocaba", "Curitiba", 280),
            ("Sorocaba", "Campinas", 120),
            ("Ribeirão Preto", "Belo Horizonte", 520),
            ("Ribeirão Preto", "Campinas", 220),
            ("São Paulo", "Rio de Janeiro", 430),
            ("São Paulo", "Curitiba", 410),
            ("Rio de Janeiro", "Belo Horizonte", 440),
            ("Belo Horizonte", "Curitiba", 980),
        ]
        
        self.criar_interface()
        self.atualizar_visualizacao()
    
    def criar_interface(self):
        """Cria os componentes da interface."""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame esquerdo - Controles
        left_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_frame.config(width=350)
        
        # Título
        title_label = tk.Label(left_frame, text="SISTEMA DE ROTAS", 
                               font=('Arial', 16, 'bold'), 
                               bg='#2a2a2a', fg='white')
        title_label.pack(pady=15)
        
        # Seção 1: Cidades Predefinidas
        sec1_frame = tk.LabelFrame(left_frame, text="Cidades Predefinidas", 
                                   font=('Arial', 11, 'bold'),
                                   bg='#2a2a2a', fg='white', 
                                   relief=tk.RAISED, bd=2)
        sec1_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(sec1_frame, text="Armazém:", 
                bg='#2a2a2a', fg='#ff3333', font=('Arial', 9, 'bold')).pack(anchor='w', padx=5, pady=2)
        tk.Label(sec1_frame, text=f"  • {self.cidades_predefinidas['armazem']}", 
                bg='#2a2a2a', fg='white', font=('Arial', 9)).pack(anchor='w', padx=10)
        
        tk.Label(sec1_frame, text="Intermediárias:", 
                bg='#2a2a2a', fg='#66ccff', font=('Arial', 9, 'bold')).pack(anchor='w', padx=5, pady=(5,2))
        for cidade in self.cidades_predefinidas['intermediarias']:
            tk.Label(sec1_frame, text=f"  • {cidade}", 
                    bg='#2a2a2a', fg='white', font=('Arial', 9)).pack(anchor='w', padx=10)
        
        tk.Label(sec1_frame, text="Clientes:", 
                bg='#2a2a2a', fg='#3399ff', font=('Arial', 9, 'bold')).pack(anchor='w', padx=5, pady=(5,2))
        for cidade in self.cidades_predefinidas['clientes']:
            tk.Label(sec1_frame, text=f"  • {cidade}", 
                    bg='#2a2a2a', fg='white', font=('Arial', 9)).pack(anchor='w', padx=10)
        
        # Seção 2: Gerar Grafo
        sec2_frame = tk.LabelFrame(left_frame, text="Gerar Grafo", 
                                   font=('Arial', 11, 'bold'),
                                   bg='#2a2a2a', fg='white', 
                                   relief=tk.RAISED, bd=2)
        sec2_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(sec2_frame, text="Origem:", 
                bg='#2a2a2a', fg='white', font=('Arial', 9)).pack(anchor='w', padx=5, pady=5)
        
        todas_cidades = ([self.cidades_predefinidas['armazem']] + 
                        self.cidades_predefinidas['intermediarias'] + 
                        self.cidades_predefinidas['clientes'])
        
        self.origem_var = tk.StringVar(value=self.cidades_predefinidas['armazem'])
        origem_combo = ttk.Combobox(sec2_frame, textvariable=self.origem_var, 
                                   values=todas_cidades, state='readonly', width=25)
        origem_combo.pack(padx=5, pady=2)
        
        tk.Label(sec2_frame, text="Destino:", 
                bg='#2a2a2a', fg='white', font=('Arial', 9)).pack(anchor='w', padx=5, pady=(10,5))
        
        self.destino_var = tk.StringVar(value=self.cidades_predefinidas['clientes'][0])
        destino_combo = ttk.Combobox(sec2_frame, textvariable=self.destino_var, 
                                    values=todas_cidades, state='readonly', width=25)
        destino_combo.pack(padx=5, pady=2)
        
        btn_gerar = tk.Button(sec2_frame, text="Gerar Grafo", 
                              command=self.gerar_grafo,
                              bg='#00aa00', fg='white', 
                              font=('Arial', 10, 'bold'),
                              relief=tk.RAISED, bd=3, cursor='hand2')
        btn_gerar.pack(pady=15, padx=5, fill=tk.X)
        
        # Status do grafo
        self.status_label = tk.Label(sec2_frame, text="Grafo: NÃO GERADO", 
                                     bg='#2a2a2a', fg='#ff4444', 
                                     font=('Arial', 9, 'bold'))
        self.status_label.pack(pady=5)
        
        # Seção 3: Informações da Rota
        sec3_frame = tk.LabelFrame(left_frame, text="Rota Atual", 
                                   font=('Arial', 11, 'bold'),
                                   bg='#2a2a2a', fg='white', 
                                   relief=tk.RAISED, bd=2)
        sec3_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.rota_label = tk.Label(sec3_frame, text="Nenhuma rota calculada", 
                                  bg='#2a2a2a', fg='#888888', 
                                  font=('Arial', 9), wraplength=300, justify='left')
        self.rota_label.pack(padx=5, pady=5)
        
        self.custo_label = tk.Label(sec3_frame, text="", 
                                    bg='#2a2a2a', fg='#00ff00', 
                                    font=('Arial', 10, 'bold'))
        self.custo_label.pack(padx=5, pady=2)
        
        # Seção 4: Quebrar Estrada
        sec4_frame = tk.LabelFrame(left_frame, text="Quebrar Estrada", 
                                  font=('Arial', 11, 'bold'),
                                  bg='#2a2a2a', fg='white', 
                                  relief=tk.RAISED, bd=2)
        sec4_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(sec4_frame, text="Origem:", 
                bg='#2a2a2a', fg='white', font=('Arial', 9)).pack(anchor='w', padx=5, pady=5)
        
        self.quebrar_origem_var = tk.StringVar()
        quebrar_origem_combo = ttk.Combobox(sec4_frame, textvariable=self.quebrar_origem_var, 
                                            values=[], state='readonly', width=25)
        quebrar_origem_combo.pack(padx=5, pady=2)
        self.quebrar_origem_combo = quebrar_origem_combo
        
        tk.Label(sec4_frame, text="Destino:", 
                bg='#2a2a2a', fg='white', font=('Arial', 9)).pack(anchor='w', padx=5, pady=(10,5))
        
        self.quebrar_destino_var = tk.StringVar()
        quebrar_destino_combo = ttk.Combobox(sec4_frame, textvariable=self.quebrar_destino_var, 
                                             values=[], state='readonly', width=25)
        quebrar_destino_combo.pack(padx=5, pady=2)
        self.quebrar_destino_combo = quebrar_destino_combo
        
        btn_quebrar = tk.Button(sec4_frame, text="Quebrar Estrada", 
                                command=self.quebrar_estrada,
                                bg='#ff4444', fg='white', 
                                font=('Arial', 10, 'bold'),
                                relief=tk.RAISED, bd=3, cursor='hand2')
        btn_quebrar.pack(pady=15, padx=5, fill=tk.X)
        
        btn_restaurar = tk.Button(sec4_frame, text="Restaurar Todas Estradas", 
                                 command=self.restaurar_todas_estradas,
                                 bg='#ff8800', fg='white', 
                                 font=('Arial', 9, 'bold'),
                                 relief=tk.RAISED, bd=2, cursor='hand2')
        btn_restaurar.pack(pady=5, padx=5, fill=tk.X)
        
        # Lista de estradas quebradas
        tk.Label(sec4_frame, text="Estradas Quebradas:", 
                bg='#2a2a2a', fg='white', font=('Arial', 9, 'bold')).pack(anchor='w', padx=5, pady=(10,5))
        
        self.estradas_quebradas_listbox = tk.Listbox(sec4_frame, height=4, 
                                                     bg='#1a1a1a', fg='#ff4444',
                                                     font=('Arial', 8))
        self.estradas_quebradas_listbox.pack(padx=5, pady=2, fill=tk.X)
        
        # Frame direito - Visualização
        right_frame = tk.Frame(main_frame, bg='#1a1a1a')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas para matplotlib
        self.fig = plt.Figure(figsize=(10, 8), facecolor='#1a1a1a')
        self.ax = self.fig.add_subplot(111, facecolor='#1a1a1a')
        self.canvas = FigureCanvasTkAgg(self.fig, right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def gerar_grafo(self):
        """Gera o grafo completo com todas as estradas predefinidas."""
        origem = self.origem_var.get()
        destino = self.destino_var.get()
        
        if origem == destino:
            messagebox.showwarning("Aviso", "Origem e destino devem ser diferentes!")
            return
        
        # Criar rede
        self.rede = RedeDistribuicao()
        
        # Adicionar todas as cidades
        self.rede.adicionar_cidade(self.cidades_predefinidas['armazem'], tipo='armazem')
        for cidade in self.cidades_predefinidas['intermediarias']:
            self.rede.adicionar_cidade(cidade, tipo='intermediaria')
        for cidade in self.cidades_predefinidas['clientes']:
            self.rede.adicionar_cidade(cidade, tipo='cliente')
        
        # Adicionar todas as estradas predefinidas
        for origem_est, destino_est, custo in self.estradas_predefinidas:
            self.rede.adicionar_estrada(origem_est, destino_est, custo)
        
        # Fazer backup do grafo original
        self.grafo_backup = copy.deepcopy(self.rede.grafo)
        
        self.grafo_gerado = True
        self.estradas_quebradas = []
        
        # Atualizar interface
        self.status_label.config(text="Grafo: GERADO", fg='#00ff00')
        
        # Atualizar combos de quebrar estrada
        todas_cidades = list(self.rede.grafo.nodes())
        self.quebrar_origem_combo['values'] = todas_cidades
        self.quebrar_destino_combo['values'] = todas_cidades
        
        # Calcular rota inicial
        self.calcular_rota()
        self.atualizar_visualizacao()
        
        messagebox.showinfo("Sucesso", "Grafo gerado com sucesso!\nTodas as estradas foram criadas.")
    
    def calcular_rota(self):
        """Calcula a rota entre origem e destino."""
        if not self.grafo_gerado or not self.rede:
            return
        
        origem = self.origem_var.get()
        destino = self.destino_var.get()
        
        caminho, custo = self.rede.calcular_caminho_minimo_manual(origem, destino)
        
        if caminho:
            rota_texto = " → ".join(caminho)
            self.rota_label.config(text=f"Rota: {rota_texto}", fg='white')
            self.custo_label.config(text=f"Custo: {custo:.0f} unidades")
        else:
            self.rota_label.config(text="ERRO: Nenhuma rota encontrada!", fg='#ff4444')
            self.custo_label.config(text="")
    
    def quebrar_estrada(self):
        """Quebra uma estrada e recalcula a rota."""
        if not self.grafo_gerado or not self.rede:
            messagebox.showwarning("Aviso", "Gere o grafo primeiro!")
            return
        
        origem = self.quebrar_origem_var.get()
        destino = self.quebrar_destino_var.get()
        
        if not origem or not destino:
            messagebox.showwarning("Aviso", "Selecione origem e destino da estrada!")
            return
        
        if origem == destino:
            messagebox.showwarning("Aviso", "Origem e destino devem ser diferentes!")
            return
        
        if not self.rede.grafo.has_edge(origem, destino):
            messagebox.showwarning("Aviso", f"A estrada {origem} → {destino} não existe!")
            return
        
        # Verificar se já está quebrada
        if (origem, destino) in self.estradas_quebradas:
            messagebox.showinfo("Info", "Esta estrada já está quebrada!")
            return
        
        # Quebrar estrada
        self.rede.grafo.remove_edge(origem, destino)
        self.estradas_quebradas.append((origem, destino))
        
        # Atualizar lista
        self.estradas_quebradas_listbox.insert(tk.END, f"{origem} → {destino}")
        
        # Recalcular rota automaticamente
        self.calcular_rota()
        self.atualizar_visualizacao()
        
        messagebox.showinfo("Estrada Quebrada", 
                           f"Estrada {origem} → {destino} foi quebrada!\n"
                           f"A rota foi recalculada automaticamente.")
    
    def restaurar_todas_estradas(self):
        """Restaura todas as estradas quebradas."""
        if not self.grafo_gerado or not self.rede:
            return
        
        if not self.estradas_quebradas:
            messagebox.showinfo("Info", "Nenhuma estrada quebrada para restaurar!")
            return
        
        # Restaurar grafo do backup
        self.rede.grafo = copy.deepcopy(self.grafo_backup)
        self.estradas_quebradas = []
        self.estradas_quebradas_listbox.delete(0, tk.END)
        
        # Recalcular rota
        self.calcular_rota()
        self.atualizar_visualizacao()
        
        messagebox.showinfo("Sucesso", "Todas as estradas foram restauradas!")
    
    def atualizar_visualizacao(self):
        """Atualiza a visualização do grafo."""
        self.ax.clear()
        self.ax.set_facecolor('#1a1a1a')
        
        if not self.grafo_gerado or not self.rede:
            # Mostrar apenas cidades sem grafo
            self.ax.text(0.5, 0.5, 
                        'Cidades Predefinidas\n\n'
                        'Gere o grafo selecionando\n'
                        'origem e destino acima',
                        ha='center', va='center',
                        fontsize=16, color='white',
                        transform=self.ax.transAxes,
                        bbox=dict(boxstyle='round', facecolor='#2a2a2a', 
                                edgecolor='white', linewidth=2))
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        # Visualizar grafo
        G = self.rede.grafo
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        # Calcular rota atual para destacar
        origem = self.origem_var.get()
        destino = self.destino_var.get()
        caminho, custo = self.rede.calcular_caminho_minimo_manual(origem, destino)
        arestas_caminho = []
        if caminho and len(caminho) > 1:
            arestas_caminho = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
        
        # Desenhar todas as arestas em cinza
        arestas_normais = [(u, v) for u, v in G.edges() 
                          if (u, v) not in arestas_caminho and 
                          (u, v) not in self.estradas_quebradas]
        nx.draw_networkx_edges(G, pos, edgelist=arestas_normais, ax=self.ax,
                              edge_color='#888888', width=2, alpha=0.5, 
                              arrows=True, arrowsize=20, arrowstyle='->')
        
        # Destacar caminho mínimo
        if arestas_caminho:
            nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho, ax=self.ax,
                                  edge_color='#00ff00', width=4, alpha=0.9,
                                  arrows=True, arrowsize=25, arrowstyle='->',
                                  style='dashed')
        
        # Destacar estradas quebradas (se ainda existirem no grafo - não deveriam)
        # Mas vamos mostrar visualmente quais foram quebradas
        for origem_q, destino_q in self.estradas_quebradas:
            if origem_q in pos and destino_q in pos:
                # Desenhar linha tracejada vermelha para indicar estrada quebrada
                x1, y1 = pos[origem_q]
                x2, y2 = pos[destino_q]
                self.ax.plot([x1, x2], [y1, y2], 'r--', linewidth=2, 
                           alpha=0.5, label='Estrada Quebrada' if origem_q == self.estradas_quebradas[0][0] else '')
        
        # Desenhar nós
        nos_armazem = [n for n in G.nodes() if G.nodes[n].get('tipo') == 'armazem']
        nos_clientes = [n for n in G.nodes() if G.nodes[n].get('tipo') == 'cliente']
        nos_outros = [n for n in G.nodes() 
                     if G.nodes[n].get('tipo') not in ['armazem', 'cliente']]
        
        if nos_armazem:
            nx.draw_networkx_nodes(G, pos, nodelist=nos_armazem, ax=self.ax,
                                  node_color='#ff3333', node_size=2000, 
                                  node_shape='s', alpha=1.0, 
                                  edgecolors='white', linewidths=3)
        if nos_clientes:
            nx.draw_networkx_nodes(G, pos, nodelist=nos_clientes, ax=self.ax,
                                  node_color='#3399ff', node_size=1500, 
                                  node_shape='o', alpha=1.0,
                                  edgecolors='white', linewidths=3)
        if nos_outros:
            nx.draw_networkx_nodes(G, pos, nodelist=nos_outros, ax=self.ax,
                                  node_color='#66ccff', node_size=1200, 
                                  node_shape='o', alpha=0.9,
                                  edgecolors='white', linewidths=2)
        
        # Labels dos nós
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=10, 
                               font_weight='bold', font_color='white')
        
        # Labels das arestas (custos)
        labels_arestas = {}
        for u, v in G.edges():
            if (u, v) not in self.estradas_quebradas:
                custo = G[u][v]['custo']
                labels_arestas[(u, v)] = f'{custo}'
        
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_arestas, ax=self.ax,
                                    font_size=8, font_color='white',
                                    bbox=dict(boxstyle='round,pad=0.3', 
                                            facecolor='#2a2a2a', alpha=0.8, 
                                            edgecolor='white', linewidth=1))
        
        # Legenda
        from matplotlib.patches import Patch
        legenda = [
            Patch(color='#ff3333', label='Armazém'),
            Patch(color='#3399ff', label='Cliente'),
            Patch(color='#66ccff', label='Intermediária'),
            Patch(color='#00ff00', label='Rota Mínima'),
        ]
        if self.estradas_quebradas:
            legenda.append(Patch(color='red', label='Estrada Quebrada', linestyle='--'))
        
        self.ax.legend(handles=legenda, loc='upper left', 
                      facecolor='#2a2a2a', edgecolor='white', 
                      labelcolor='white', framealpha=0.9)
        
        # Título
        titulo = "Rede de Distribuição"
        if caminho:
            titulo += f"\nRota: {' → '.join(caminho)} (Custo: {custo:.0f})"
        if self.estradas_quebradas:
            titulo += f"\nEstradas Quebradas: {len(self.estradas_quebradas)}"
        
        self.ax.set_title(titulo, fontsize=12, fontweight='bold', 
                         color='white', pad=10)
        self.ax.axis('off')
        
        self.canvas.draw()
    
    def on_origem_destino_change(self, event=None):
        """Callback quando origem ou destino mudam."""
        if self.grafo_gerado:
            self.calcular_rota()
            self.atualizar_visualizacao()


def main():
    """Função principal."""
    root = tk.Tk()
    app = InterfaceRotas(root)
    
    # Atualizar quando origem/destino mudarem
    app.origem_var.trace('w', lambda *args: app.on_origem_destino_change())
    app.destino_var.trace('w', lambda *args: app.on_origem_destino_change())
    
    root.mainloop()


if __name__ == "__main__":
    main()

