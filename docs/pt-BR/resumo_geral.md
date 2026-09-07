# Especificação Técnica e Guia de Referência: I-NOC v1.4.5

A I-NOC é uma linguagem de programação criada para permitir que aplicações, dados, lógica e interfaces sejam descritos de forma direta, utilizando uma sintaxe compacta na qual a estrutura do programa é visualmente evidente.

A linguagem foi projetada para reduzir a distância entre a intenção do programador e a forma como essa intenção é expressa no código. Sua sintaxe utiliza símbolos para identificar estruturas fundamentais da linguagem e palavras para representar a semântica do programa, como nomes de variáveis, funções, dados e condições.

A I-NOC permite construir a lógica de uma aplicação, trabalhar com dados, utilizar funções e módulos e declarar interfaces de usuário dentro da própria linguagem. A interface e a lógica permanecem conceitualmente separadas: a interface declara os elementos que existem, enquanto a lógica consulta, modifica e reage ao estado desses elementos.

Uma característica fundamental da I-NOC é que a mesma aplicação pode utilizar diferentes renderizadores de interface. A escolha entre, por exemplo, Tk e Web é feita na própria declaração da aplicação, sem exigir uma segunda implementação da lógica do programa.

---

## Objetivos

### 1. Declarar a intenção
O código expressa de forma direta o que o programador deseja realizar, reduzindo a quantidade de detalhes necessários para representar uma intenção.

### 2. Ser simples, fácil de ler e escrever
A sintaxe é acessível e previsível, revelando a estrutura e o comportamento do código de forma natural.

### 3. Ser extremamente compacta
A I-NOC busca representar funcionalidades com o mínimo de código necessário, reduzindo a estrutura para expressar uma intenção.

### 4. Possuir lógica e UI nativas
A linguagem possui recursos próprios para construção da lógica da aplicação e declaração de interfaces de usuário, sem depender de frameworks externos para representar conceitos fundamentais da linguagem. A interface faz parte da própria linguagem, e não é apenas uma camada adicionada posteriormente por um framework.

### 5. Ser multiplataforma
A mesma lógica é utilizada em diferentes ambientes (Desktop/Tk e Navegador/Web) através de renderizadores especializados.

---

## 1. Introdução

A I-NOC atua como um mapa visual instantâneo do fluxo e da hierarquia da aplicação.

### Primeiro Programa
```inoc
/: OlaMundo #ui web
/+ Principal

¢ card # largura = 400, cor = "branco", arredondamento = 20, alinhamento = "centro"
    |#texto "Olá Mundo"|    ~~ UI: Elemento Visual
    |#botao "Sair"|         ~~ UI: Ponto de Evento

& verdadeiro
    @: e
    ? e == "Sair"
        ! "Até logo!"
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
| `#` | Propriedade | Configuração de elemento | `# cor = "azul"` |
| `?` | Condição | Inicia uma condição (Se) | `? ativo` |
| `£` | Senão | Inicia o bloco alternativo (Else) | `£` |
| `&` | Enquanto | Repetição condicional (While) | `& x < 10` |
| `&:` | Para Cada | Iteração sobre coleção (ForEach) | `&: item lista` |
| `!` | Saída | Exibe um valor no console | `! "Olá"` |
| `@` | Entrada/UI | Consulta o valor de um elemento da UI | `@ email` |
| `@:` | Evento | Captura um evento da interface | `@: evento` |
| `~~` | Comentário | Comentário de linha | `~~ comentário` |
| `=` | Atribuição | Atribui um valor a uma variável | `x = 10` |
| `==` | Igualdade | Compara igualdade entre valores | `? x == 10` |

---

## 3. Idiomas Suportados

A I-NOC permite escolher livremente entre **Português** e **Inglês**. As palavras são normalizadas internamente.

### Equivalências de UI e Propriedades
*   `entrada` / `input`
*   `botao` / `button`
*   `texto` / `text`
*   `cor` / `color`
*   `largura` / `width`
*   `altura` / `height`
*   `alinhamento` / `alignment`

---

## 4. Renderização Web Avançada (v1.4.5)

O motor Web agora suporta propriedades modernas de design:
*   **Estilo**: `fundo` (suporta linear-gradient), `sombra` (box-shadow), `arredondamento` (border-radius) e `padding`.
*   **Imagens**: Suporte para carregamento de imagens locais via conversão automática para Base64.
*   **Layout Dinâmico**: Centralização automática para cards e modo de expansão para telas cheias (`100vw/100vh`).
*   **Tipos**: Novo elemento `|#senha|` para campos protegidos.

---

## 5. Arquitetura e Ferramental

A I-NOC utiliza uma arquitetura baseada em LSP para o VS Code, oferecendo:
*   **Autocomplete Contextual**: Sugestões inteligentes baseadas na AST.
*   **Diagnósticos**: Identificação de erros sintáticos em tempo real.
*   **Integrated Runtime**: Execução via binário nativo incluído na extensão.

---
**I-NOC v1.4.5: Código nativo orientado a intenção.**
