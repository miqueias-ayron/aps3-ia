# APS 3
## Integrantes
- Brenda de Oliveira Lima
- Miqueias Ayron Mamedes Ferreira

## Problema das N rainhas
Dado um tabuleiro *NxN* é possível encontrar uma configuração onde 
rainhas no tabuleiro não conseguem atacar nenhuma das outras rainhas no mesmo tabuleiro?



<img width="372" height="372" alt="image" src="https://github.com/user-attachments/assets/2d873e37-af62-42c0-9f17-8a0c2403a177" />



Implementar o problema das N damas para tabuleiros de dimensões: 4, 5, 6, 7, 8 usando um algoritmo de **Busca em Largura** ou **Busca em Profundidade**

## Solução

Implementação em Python usando **Busca em Profundidade** (`BuscaProfundidade`) da biblioteca [`aigyminsper`](https://pypi.org/project/aigyminsper/) do Insper.

### Estrutura

```
src/
  n_queens_aigym.py   # QueensState (interface State da aigyminsper) + BuscaProfundidade
  n_queens_pygame.py  # visualização gráfica das soluções (pygame)
```

O estado do tabuleiro (`QueensState`) implementa a interface `State` da lib (`successors`, `is_goal`, `cost`, `env`, `description`); a poda de rainhas que se atacam já acontece dentro de `successors()`, então a busca em profundidade encontra a primeira solução completa em profundidade N. `n_queens_pygame.py` reaproveita esse mesmo `QueensState` para enumerar todas as soluções e navegar entre elas.

### Executar

```bash
pip install -r requirements.txt
python src/n_queens_aigym.py
```

Imprime, para cada tabuleiro (4, 5, 6, 7 e 8), o caminho encontrado por `BuscaProfundidade` e o tabuleiro resultante.

### Visualização (pygame)

```bash
pip install -r requirements.txt
python src/n_queens_pygame.py
```

Controles:
- `→` / `Espaço`: próxima solução
- `←`: solução anterior
- `N`: próximo tamanho de tabuleiro (4, 5, 6, 7, 8)
- `ESC`: sair

### Resultados esperados

| N | Soluções |
|---|----------|
| 4 | 2        |
| 5 | 10       |
| 6 | 4        |
| 7 | 40       |
| 8 | 92       |
