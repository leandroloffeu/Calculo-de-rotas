# Instruções de Uso - Interface Interativa

## Como Usar a Interface

### 1. Iniciar o Sistema

Execute o arquivo `interface_interativa.py`:

```bash
python interface_interativa.py
```

A interface será aberta mostrando:
- **Cidades Predefinidas**: Lista de todas as cidades disponíveis (armazém, intermediárias e clientes)
- **Painel de Controle**: Para gerar o grafo e quebrar estradas
- **Visualização**: Área onde o grafo será exibido

### 2. Estado Inicial (Sem Grafo)

Quando o sistema inicia, você verá:
- Lista de cidades predefinidas:
  - **Armazém**: São Paulo
  - **Intermediárias**: Campinas, Ribeirão Preto, Sorocaba
  - **Clientes**: Rio de Janeiro, Belo Horizonte, Curitiba
- Status: "Grafo: NÃO GERADO"
- Visualização mostra apenas uma mensagem informativa

### 3. Gerar o Grafo

Para gerar o grafo completo:

1. **Selecione a Origem**: Escolha a cidade de origem no dropdown (padrão: São Paulo)
2. **Selecione o Destino**: Escolha a cidade de destino no dropdown (padrão: Rio de Janeiro)
3. **Clique em "Gerar Grafo"**

O sistema irá:
- Criar todas as cidades predefinidas
- Criar todas as 14 estradas predefinidas com seus custos
- Calcular automaticamente a melhor rota entre origem e destino
- Exibir o grafo completo na visualização
- Atualizar o status para "Grafo: GERADO"

### 4. Visualizar a Rota

Após gerar o grafo, você verá:
- **Rota Atual**: Mostra o caminho completo (ex: "São Paulo → Rio de Janeiro")
- **Custo**: Mostra o custo total da rota em unidades
- **Visualização Gráfica**: 
  - Cidades em diferentes cores (vermelho=armazém, azul=clientes, ciano=intermediárias)
  - Rota mínima destacada em verde
  - Custos das estradas exibidos nas arestas

### 5. Quebrar uma Estrada

Para simular a quebra de uma estrada:

1. **Selecione a Origem da Estrada**: Escolha a cidade de origem da estrada a quebrar
2. **Selecione o Destino da Estrada**: Escolha a cidade de destino da estrada a quebrar
3. **Clique em "Quebrar Estrada"**

O sistema irá:
- Remover a estrada do grafo
- **Recalcular automaticamente** a melhor rota entre origem e destino
- Atualizar a visualização mostrando a nova rota
- Adicionar a estrada à lista de "Estradas Quebradas"
- Mostrar a estrada quebrada em vermelho tracejado (se ainda visível)

### 6. Restaurar Estradas

Para restaurar todas as estradas quebradas:

- **Clique em "Restaurar Todas Estradas"**

O sistema irá:
- Restaurar o grafo ao estado original
- Recalcular a rota com todas as estradas disponíveis
- Limpar a lista de estradas quebradas

### 7. Alterar Origem/Destino

Você pode alterar a origem ou destino a qualquer momento:

1. **Altere a seleção** nos dropdowns de "Origem" e "Destino"
2. A rota será **recalculada automaticamente**
3. A visualização será atualizada mostrando a nova rota

## Funcionalidades Principais

### ✅ Cidades Predefinidas
- Sistema inicia com cidades já definidas
- Não é necessário criar cidades manualmente

### ✅ Geração de Grafo
- Grafo completo é gerado apenas quando você clica em "Gerar Grafo"
- Todas as 14 estradas são criadas automaticamente

### ✅ Cálculo Automático de Rotas
- Rota mínima é calculada automaticamente após gerar o grafo
- Recalcula automaticamente quando você:
  - Quebra uma estrada
  - Altera origem ou destino
  - Restaura estradas

### ✅ Visualização Interativa
- Grafo visual com cores diferentes para cada tipo de cidade
- Rota mínima destacada em verde
- Estradas quebradas indicadas visualmente
- Custos exibidos nas arestas

## Exemplo de Uso

1. **Iniciar**: Execute `python interface_interativa.py`
2. **Gerar Grafo**: Selecione "São Paulo" (origem) e "Rio de Janeiro" (destino), clique em "Gerar Grafo"
3. **Ver Rota**: Observe a rota "São Paulo → Rio de Janeiro" com custo 430
4. **Quebrar Estrada**: Quebre a estrada "São Paulo → Rio de Janeiro"
5. **Ver Nova Rota**: O sistema recalcula automaticamente mostrando "São Paulo → Campinas → Rio de Janeiro" com custo 450
6. **Restaurar**: Clique em "Restaurar Todas Estradas" para voltar ao estado original

## Notas Importantes

- O grafo só é gerado quando você clica em "Gerar Grafo"
- A rota é sempre recalculada automaticamente após qualquer mudança
- Você pode quebrar múltiplas estradas
- Todas as estradas podem ser restauradas de uma vez
- A origem e destino podem ser alteradas a qualquer momento

## Requisitos

- Python 3.7+
- tkinter (geralmente incluído com Python)
- matplotlib
- networkx

Instale as dependências com:
```bash
pip install -r requirements.txt
```

