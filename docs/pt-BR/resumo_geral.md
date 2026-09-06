# Especificação Técnica e Guia de Referência: I-NOC v1.4.1

A I-NOC é uma linguagem de programação criada para permitir que aplicações, dados, lógica e interfaces sejam descritos de forma direta, utilizando uma sintaxe compacta na qual a estrutura do programa é visualmente evidente.

A linguagem foi projetada para reduzir a distância entre a intenção do programador e a forma como essa intenção é expressa no código. Sua sintaxe utiliza símbolos para identificar estruturas fundamentais da linguagem e palavras para representar a semântica do programa, como nomes de variáveis, funções, dados e condições.

A I-NOC permite construir a lógica de uma aplicação, trabalhar com dados, utilizar funções e módulos e declarar interfaces de usuário dentro da própria linguagem. A interface e a lógica permanecem conceitualmente separadas: a interface declara os elementos que existem, enquanto a lógica consulta, modifica e reage ao estado desses elementos.

Uma característica fundamental da I-NOC é que a mesma aplicação pode utilizar diferentes renderizadores de interface. A escolha entre, por exemplo, Tk e Web é feita na própria declaração da aplicação, sem exigir uma segunda implementação da lógica do programa.

A linguagem busca, portanto, tornar a estrutura e a intenção do código reconhecíveis à primeira leitura, evitando que detalhes de implementação dominem a forma como o programa é escrito.

---

## Objetivos

A I-NOC foi projetada com os seguintes objetivos fundamentais:

### 1. Declarar a intenção
O código expressa de forma direta o que o programador deseja realizar, reduzindo a quantidade de detalhes necessários para representar uma intenção. A linguagem busca aproximar a escrita do programa do próprio conceito que está sendo implementado.

### 2. Ser simples, fácil de ler e escrever
A sintaxe é acessível e previsível, permitindo que o código seja compreendido sem exigir uma grande quantidade de elementos sintáticos. A leitura do código revela sua estrutura e seu comportamento de forma natural.

### 3. Ser extremamente compacta
A I-NOC busca representar funcionalidades com o mínimo de código necessário, sem sacrificar a clareza. Compactação, na I-NOC, não significa simplesmente escrever menos caracteres, mas reduzir a quantidade de estrutura necessária para expressar uma intenção.

### 4. Possuir lógica e UI nativas
A linguagem possui recursos próprios para construção da lógica da aplicação e declaração de interfaces de usuário, sem depender de frameworks externos para representar conceitos fundamentais da linguagem. A interface faz parte da própria linguagem, e não é apenas uma camada adicionada posteriormente por um framework.

### 5. Ser multiplataforma
A I-NOC permite que a mesma linguagem e a mesma lógica sejam utilizadas em diferentes ambientes por meio de seus renderizadores e da arquitetura de execução. Na v1.4.1, isso é representado principalmente pelos renderizadores Tk e Web. A existência de diferentes renderizadores permite separar a descrição da aplicação da tecnologia utilizada para apresentá-la.

### 6. Ter potencial para workflows multiagentes
A I-NOC também é projetada com potencial para utilização em workflows multiagentes, nos quais diferentes agentes de inteligência artificial podem analisar, gerar, modificar ou executar partes de um programa de maneira estruturada. Sua sintaxe compacta, estruturada e orientada à intenção pode favorecer a comunicação entre agentes e a geração programática de código.

*Nota: Esse objetivo representa uma direção de desenvolvimento da linguagem e não significa que a I-NOC v1.4.1 já possua um sistema próprio de agentes ou de execução multiagente.*

---

## 1. Introdução

A I-NOC foi desenvolvida para oferecer uma experienca de desenvolvimento onde a "margem esquerda" do código atua como um mapa visual instantâneo do fluxo e da hierarquia da aplicação.

### Primeiro Programa
```inoc
/: OlaMundo #ui tk      ~~ Estrutura: Declara o App
/+ Principal            ~~ Estrutura: Declara a Tela

|#texto "Olá Mundo"|    ~~ UI: Elemento Visual
|#botao "Sair"|         ~~ UI: Ponto de Evento

& true                  ~~ Lógica: Loop Infinito
    @: e                ~~ Lógica: Captura Evento
    ? e == "Sair"       ~~ Lógica: Condição
        ! "Até logo!"   ~~ IO: Saída de console
£                       ~~ Fim do Bloco
```

---

## 2. Tabela de Símbolos Fundamentais

| Símbolo | Nome | Significado Semântico | Exemplo |
| :--- | :--- | :--- | :--- |
| `/:` | Aplicação | Define a aplicação e o renderer | `/: App #ui web` |
| `/+` | Tela | Define uma nova tela/seção de UI | `/+ Principal` |
| `¢` | Container | Agrupa elementos e hierarquia visual | `¢ container` |
| `//` | Objeto | Estrutura de objeto/dicionário | `// usuario` |
| `§` | Módulo | Carrega módulo externo com namespace | `§ matematica` |
| `$` | Função | Declara uma função | `$ somar(a, b)` |
| `$: ` | Retorno | Retorna valor da função | `$: a + b` |
| `\|...\|` | UI | Declara um elemento de interface | `\|#botao "OK"\|` |
| `=>` | Navegação | Navegação entre telas (dentro de UI) | `\|Entrar\| => Home` |
| `#` | Propriedade | Configuração de elemento | `# cor = "azul"` |
| `?` | Condição | Inicia uma condição (Se) | `? ativo` |
| `£` | Senão | Inicia o bloco alternativo (Else) | `£` |
| `&` | Enquanto | Repetição condicional (While) | `& x < 10` |
| `&:` | Para Cada | Iteração sobre coleção (ForEach) | `&: item lista` |
| `!` | Saída | Exibe um valor no console | `! "Olá"` |
| `@` | Entrada/UI | Consulta o valor de um elemento da UI | `@ email` |
| `@:` | Evento | Captura um evento da interface | `@: evento` |
| `~~` | Comentário | Comentário de linha | `~~ comentário` |
| `.` | Ponto | Acesso a propriedade ou namespace | `usuario.nome` |
| `,` | Vírgula | Separador de coleções ou parâmetros | `[1, 2, 3]` |
| `( )` | Parênteses | Agrupamento e chamada de funções | `somar(2, 2)` |
| `[ ]` | Lista/Índice | Criação de listas e acesso por índice | `lista[0]` |
| `=` | Atribuição | Atribui um valor a uma variável | `x = 10` |
| `==` | Igualdade | Compara igualdade entre valores | `? x == 10` |

---

## 3. Anatomia de um Programa

Todo programa I-NOC inicia com a configuração da aplicação e suas telas.

*   `/:`: **Símbolo de Aplicação**. Define o nome do sistema e configurações globais.
*   `/+`: **Símbolo de Tela**. Define o nome de um contexto visual.
*   `#ui`: Propriedade obrigatória em `/:` para definir o motor gráfico (`tk` para desktop, `web` para navegador).
*   **Indentação**: A I-NOC utiliza indentação significativa (4 espaços) para definir blocos.

---

## 4. Léxico e Sintaxe

A I-NOC reconhece cinco categorias fundamentais de átomos léxicos:

1.  **Identificadores**: Nomes sem aspas (ex: `usuario`). Usados para variáveis e IDs de UI.
2.  **Números**: Literais decimais ou inteiros (ex: `3.14`).
3.  **Textos (Strings)**: Sempre entre aspas duplas (ex: `"azul"`).
4.  **Booleanos**: Literais `true` e `false`.
5.  **Símbolos**: Caracteres únicos ou duplos que definem a estrutura.

---

## 5. Idiomas Suportados

A I-NOC é uma linguagem multilíngue nativa, permitindo que o programador escolha livremente entre **Português** e **Inglês** como formas equivalentes de escrever o código. Não há diferença funcional entre os idiomas; as palavras são normalizadas internamente.

### Tabela de Equivalências

| Português | Inglês | Significado Semântico |
| :--- | :--- | :--- |
| `verdadeiro` | `true` | Valor booleano verdadeiro |
| `falso` | `false` | Valor booleano falso |
| `ou` | `or` | Operador lógico OU |
| `não` | `not` | Operador lógico NÃO |
| `se` | `if` | Início de bloco condicional |
| `senão` | `else` | Bloco condicional alternativo |
| `entrada` | `input` | Elemento de UI para entrada de texto |
| `botao` | `button` | Elemento de UI clicável |
| `texto` | `text` | Elemento de UI de rótulo / Função built-in |
| `janela` | `window` | Elemento de UI para configurações de tela |
| `cor` | `color` | Propriedade de cor de fundo |
| `cor_texto` | `text_color` | Propriedade de cor da fonte |
| `tamanho` | `size` | Propriedade de tamanho / Função built-in |
| `fonte` | `font` | Propriedade de família de fonte |
| `largura` | `width` | Propriedade de largura fixa |
| `altura` | `height` | Propriedade de altura fixa |
| `borda` | `border` | Propriedade de espessura de borda |
| `margem` | `margin` | Propriedade de espaçamento |
| `alinhamento`| `alignment` | Propriedade de alinhamento visual |
| `numero` | `number` | Função: Converte para número |
| `inserir` | `insert` | Função: Adiciona em lista |
| `remover` | `remove` | Função: Remove de lista |
| `tipo` | `type` | Função: Verifica tipo do dado |
| `subtexto` | `substring` | Função: Extrai pedaço de texto |
| `procurar` | `search` / `find` | Função: Busca termo em texto |
| `chaves` | `keys` | Função: Lista chaves de objeto |
| `arredondar` | `round` | Função: Arredonda número |
| `absoluto` | `absolute` / `abs` | Função: Valor absoluto |
| `definir` | `define` / `set` | Função: Altera elemento da UI |

### Exemplo em Inglês
```inoc
/: App #ui web
|#input "Name"| # id = user
& true
    @: e
    ? e == "Ok"
        ! "User: " + @ user
```

### Exemplo em Português
```inoc
/: App #ui web
|#entrada "Nome"| # id = usuario
& verdadeiro
    @: e
    ? e == "Ok"
        ! "Usuario: " + @ usuario
```

---

## 6. Variáveis e Atribuição

*   **Atribuição**: Realizada com o operador `=`.
    `idade = 25`
*   **Namespace**: As variáveis da lógica residem em um espaço de memória separado dos **IDs de UI**. Atribuir a `email` não altera o input com `id = email`.

---

## 7. Tipos de Dados

O interpretador I-NOC gerencia nativamente os seguintes tipos:

1.  **Número**: Valores numéricos de ponto flutuante.
2.  **Texto**: Cadeias de caracteres.
3.  **Booleano**: Valores `true` ou `false`.
4.  **Lista**: Coleção ordenada de valores heterogêneos.
5.  **Objeto**: Coleção de pares chave-valor.

---

## 8. Listas

Listas são coleções dinâmicas acessadas por índice numérico.

*   **Criação**: `lista = [10, "texto", true]`
*   **Indexação**: O índice começa em **zero**. Acesso via `lista[0]`.
*   **Alteração**: `lista[0] = 50`
*   **Iteração**:
```inoc
numeros = [1, 2, 3]
&: n numeros
    ! n
```

---

## 9. Objetos (`//`)

Objetos permitem organizar dados em pares chave-valor.

*   **Declaração**: `// usuario` (Inicializa no escopo global).
*   **Literal**: `obj = //` (Cria objeto vazio).
*   **Acesso**: Usa-se o ponto (`.`) para propriedades. `usuario.nome = "Jose"`.
*   **Nota**: `~~` é para comentários. `//` é para objetos.

---

## 10. Operadores e Precedência

Os operadores são avaliados na seguinte ordem de prioridade (da menor para a maior):

1.  **Lógico**: `or` → `and` → `not`.
2.  **Comparação**: `==`, `!=`, `<`, `>`, `<=`, `>=`.
3.  **Aritmética**: `+`, `-` → `*`, `/`.
4.  **Consulta de UI**: `@` (Operador unário).

---

## 11. Controle de Fluxo

### Condicional (`?` e `£`)
O bloco condicional inicia com `?` e pode conter cadeias de `else if`. O bloco final (senão) inicia com `£`.
```inoc
? saldo > 100
    ! "Rico"
else if saldo > 0
    ! "Estável"
£
    ! "Atenção"
```

### Repetições (`&` e `&:`)
*   **`&` (Enquanto)**: Executa enquanto a condição for verdadeira.
*   **`&:` (Para Cada)**: Itera sobre cada elemento de uma lista.

---

## 12. Funções (`$`)

Blocos de lógica reutilizáveis com parâmetros e retorno.

*   **Declaração**: `$ somar(a, b)`
*   **Retorno (`$:`)**: Interrompe a execução e devolve o valor.
```inoc
$ calcular(x)
    ? x > 10
        $: x * 2
    £
        $: x
```
*Nota: Se a função terminar sem `$:`, ela retorna um valor nulo (`nada`).*

---

## 13. Módulos (`§`)

Permite organizar o código em múltiplos arquivos.

*   **Importação**: `§ util` (Procura por `util.inoc`).
*   **Namespace**: O acesso é feito pelo nome do arquivo. `util.validar()`.
*   **Escopo**: Cada módulo possui suas próprias variáveis globais isoladas.

---

## 14. Funções Nativas (Built-ins)

| Função | Finalidade | Parâmetros | Retorno |
| :--- | :--- | :--- | :--- |
| `tamanho(v)` | Comprimento de lista ou texto | 1 (qualquer) | Número |
| `texto(v)` | Converte para string | 1 (qualquer) | Texto |
| `numero(v)` | Converte para número | 1 (texto) | Número |
| `tipo(v)` | Identifica o tipo do dado | 1 (qualquer) | Texto |
| `inserir(l, i)`| Adiciona item ao fim da lista | 2 (lista, item) | O item |
| `remover(l, x)`| Remove item por índice | 2 (lista, num) | Item removido |
| `subtexto(t,i,f)`| Extrai parte de um texto | 3 (texto, num, num) | Texto |
| `procurar(t,s)` | Busca termo no texto | 2 (texto, termo) | Posição ou -1 |
| `chaves(obj)` | Retorna lista de chaves | 1 (objeto) | Lista |
| `arredondar(n)` | Arredonda valor numérico | 1 (número) | Número |
| `absoluto(n)` | Valor positivo de um número | 1 (número) | Número |
| `definir(id, v)`| Altera elemento UI via ID | 2 (id, valor) | Valor |

---

## 15. Entrada e Saída (IO)

A I-NOC distingue claramente entre capturar ações e consultar estados.

*   **`!` (Saída)**: Exibe valores no console.
*   **`@ id` (Consulta)**: Operador de expressão que lê o valor atual de um elemento da UI.
    `valor = @ campo_input`
*   **`@: evento` (Captura)**: Comando que pausa a execução até que uma ação ocorra na UI.
    `@: e`

---

## 16. Interface Gráfica (UI)

A interface é declarada através da hierarquia de containers e elementos.

*   **`|...|`**: Elementos visuais (Botões, Inputs, Textos).
*   **`¢`**: Containers para agrupamento e layout.
*   **Hierarquia**: Definida rigidamente pela **indentação de 4 espaços**.

Exemplo de estrutura:
```inoc
¢ topo # margem = 10
    |#texto "Título"|
¢ corpo
    |#input ""| # id = entrada
    |#botao "OK"|
```

---

## 17. Propriedades de UI

As propriedades configuram a aparência e o comportamento dos elementos.

| Propriedade | Tk (Desktop) | Web (Navegador) | Valor esperado |
| :--- | :---: | :---: | :--- |
| `# id` | Sim | Sim | Identificador |
| `# cor` | Sim | Sim | Texto (ex: "verde") |
| `# tamanho` | Sim | Sim | Número (px) |
| `# fonte` | Sim | Não | Texto |
| `# largura` | Não | Sim | Número (px) |
| `# altura` | Não | Sim | Número (px) |
| `# borda` | Sim | Sim | Número (px) |
| `# margem` | Sim | Sim | Número (px) |
| `# alinhamento`| Sim | Sim | "centro", "direita" |

---

## 18. IDs de UI vs Variáveis

Distinção fundamental da v1.4.1 para garantir a separação UI/Lógica:
1.  **ID**: Etiqueta do elemento na UI (`id = login`). Não é uma variável.
2.  **Variável**: Espaço de memória na lógica (`u = @ login`).
*Nota: Mudar a ordem dos elementos na UI não quebra a lógica, desde que o ID permaneça o mesmo.*

---

## 19. Renderers

A I-NOC utiliza uma arquitetura multi-renderer:
*   **Tk Renderer**: Desktop nativo.
*   **Web Renderer**: Baseado em navegador. Utiliza comunicação otimizada entre o runtime e a interface web.

---

## 20. Exemplos Completos

### Login Interativo (v1.4.1)
```inoc
/: App #ui web
/+ Principal
|#input ""| # id = user
|#input ""| # id = pass
|#botao "Entrar"|
& true
    @: e
    ? e == "Entrar"
        u = @ user
        p = @ pass
        ? u == "admin" and p == "123"
            ! "Sucesso"
        £
            ! "Falha"
```

---

## 21. Arquitetura Interna e Ferramental

### Execução
`Lexer` (Tokens) → `Parser` (AST) → `Interpreter` (Ambiente/Namespace) → `UIRuntime` (Eventos) → `Renderers` (Visualização).

### Desenvolvimento (LSP)
Para suporte em IDEs como o VS Code, a I-NOC utiliza a seguinte cadeia:
`Language Client` → `JSON-RPC` → `Language Server` → `InocAnalyzer` → `AST/Símbolos`.
Esta arquitetura permite que o autocomplete e os diagnósticos sejam baseados na estrutura real da linguagem em tempo real.

---

## 22. Limitações e Futuro

*   **Renderers**: O Web Renderer ainda não mapeia todas as fontes do sistema operacional e possui limitações em layouts complexos.
*   **Mídia**: Não há suporte nativo para manipulação direta de áudio ou vídeo (deve ser feito via extensões de renderer).
*   **Extensão**: Suporte oficial v1.4.1 disponível com LSP real, autocomplete contextual, suporte bilingue no IntelliSense e diagnósticos instantâneos.

---
**I-NOC: Código nativo orientado a intenção.**
