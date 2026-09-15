# Como o código funciona (N-rainhas)

Explicação complementar da lógica implementada em `src/n_queens_aigym.py`.

## A ideia central: como o tabuleiro é guardado

Não guardamos uma matriz NxN. Guardamos só uma lista chamada `rainhas`, onde:

- a **posição** na lista é a **linha**
- o **valor** guardado é a **coluna** onde a rainha daquela linha está

Exemplo: `rainhas = [2, 0]` quer dizer "rainha da linha 0 está na coluna 2, rainha da linha 1 está na coluna 0". Ainda faltam as linhas 2 e 3 num tabuleiro 4x4.

Como a lista só tem **uma rainha por linha** (nunca duas), duas rainhas nunca vão estar na mesma linha — isso já elimina um tipo de ataque de graça, sem precisar checar nada.

## O que cada função faz

### `_coluna_segura(coluna)`

Pergunta: "se eu colocar uma rainha nesta coluna, na próxima linha vazia, alguma rainha que já está no tabuleiro consegue atacar ela?"

Compara a coluna candidata contra **todas** as rainhas já colocadas (não só a última), uma por uma:

- **mesma coluna?** → ataque vertical
- **mesma diagonal?** → duas casas estão na mesma diagonal quando a diferença entre as linhas é igual à diferença entre as colunas. É por isso que a função usa `abs()` (valor absoluto — tira o sinal do número): a "distância" entre colunas não tem sinal, então `abs(coluna_ocupada - coluna)` dá sempre um número positivo, não importa qual das duas é maior.

Se achar mesma coluna OU mesma diagonal com qualquer rainha anterior, a posição não é segura.

### `successors()`

Pergunta: "a partir deste tabuleiro, quais são os próximos tabuleiros possíveis?"

Testa cada coluna (0 até N-1) pra próxima linha vazia. Pra cada coluna segura (`_coluna_segura` devolveu `True`), cria um **novo** `QueensState` com essa rainha a mais — sem alterar o estado atual, só criando uma cópia da lista com um item novo no fim.

Cada um desses novos estados é um "filho" do estado atual. É esse método que a busca (`BuscaProfundidade`) usa pra saber pra onde ir.

### `is_goal()`

Pergunta: "terminei?" → sim, quando já tem uma rainha em cada uma das N linhas.

### `cost()`, `env()`, `description()`

Esses três não têm lógica nenhuma nossa — são exigidos pela classe `State` da biblioteca `aigyminsper` (é uma interface: toda subclasse é obrigada a implementar esses métodos, senão nem consegue criar o objeto). Só o `env()` é realmente usado (identifica o estado); `cost()` sempre devolve `1` porque toda jogada "vale o mesmo"; `description()` não é chamado em lugar nenhum do fluxo.

### `solve_all(n)` e `visitar(estado)`

Isso é extra, feito por nós pra alimentar a visualização em pygame — a APS não pede isso. A biblioteca (`BuscaProfundidade`) só acha a **primeira** solução; aqui a gente quis achar **todas**, pra poder navegar entre elas com as setas do teclado.

`visitar(estado)` faz uma busca por **backtracking**: tenta uma coluna, segue em frente como se essa escolha estivesse certa (chamando `visitar()` de novo no filho), e se travar (nenhuma coluna segura sobrar), essa chamada simplesmente termina sem fazer nada de especial.

Não tem nenhum código de "desfazer a jogada": como cada estado filho é uma cópia nova (a lista de rainhas do estado anterior nunca é alterada), quando uma chamada de `visitar()` termina, o `for` de um nível acima simplesmente segue pro próximo filho da lista. Essa continuação do `for` É o "voltar" do backtracking — não precisa de nenhuma lógica extra pra isso.

Exemplo rápido de um galho sem solução (N=4, `rainhas = [1, 3, 0]`, faltando a linha 3):
1. `is_goal()` → `False` (só tem 3 rainhas)
2. `successors()` testa as 4 colunas da linha 3, nenhuma é segura → devolve lista vazia
3. o `for filho in successors()` não roda nenhuma vez
4. `visitar()` termina ali, sem ter achado solução
5. quem chamou essa `visitar()` estava no meio de um `for`, um nível acima (testando os filhos de `[1, 3]`) — esse `for` simplesmente segue pro próximo filho

### `imprimir_tabuleiro(rainhas)`

Desenha o tabuleiro em texto: para cada linha, para cada coluna, imprime `Q` se `rainhas[linha] == coluna` (é ali que a rainha daquela linha está), senão imprime `.`.

## A sequência de execução (o que roda quando você dá `python src/n_queens_aigym.py`)

1. `main()` roda um loop pra N = 4, 5, 6, 7, 8.
2. Pra cada N, cria um `QueensState(n)` vazio (tabuleiro sem nenhuma rainha) e chama `BuscaProfundidade().search(estado_inicial, m=n)`.
   - `m=n` é o limite de profundidade da busca — faz sentido ser N porque a solução completa tem exatamente N rainhas.
3. **A busca em si (DFS) não é código nosso** — é da biblioteca `aigyminsper`. Por baixo dos panos, ela usa uma pilha: tira o último estado que colocou, checa `is_goal()`, se não for, empilha os `successors()` dele, e repete. Isso é uma busca em profundidade porque sempre desce até o fim de um galho antes de tentar outro (é uma pilha, não uma fila).
4. A busca devolve um `Node` (não um `QueensState` puro) chamado `resultado`. O tabuleiro final está em `resultado.state.rainhas`.
5. `resultado.show_path()` (método do `Node`, também da biblioteca) monta o "caminho" percorrido: sobe a cadeia de nós-pai até a raiz, concatenando o `operator` de cada um (a string tipo `"linha 0 -> coluna 2"` que a gente monta em `successors()`).
6. `imprimir_tabuleiro()` desenha o resultado.

## Resumo de quem faz o quê

| Parte | Responsável |
|---|---|
| Representar o tabuleiro, checar segurança, gerar filhos | Nosso código (`QueensState`) |
| Algoritmo de busca em si (pilha, DFS) | Biblioteca `aigyminsper` (`BuscaProfundidade`) |
| Achar **todas** as soluções, pra visualização | Nosso código (`solve_all`), extra — não é exigido pela APS |
| Desenhar o tabuleiro em texto/pygame | Nosso código |
