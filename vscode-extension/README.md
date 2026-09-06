# ![I-NOC](./images/inoc-logo.png) I-NOC Language Support

Esta é a extensão oficial para a linguagem de programação **I-NOC** (v1.4.1).

## O que é I-NOC?

I-NOC é uma linguagem de programação estruturada sob o lema: **"Código nativo orientado a intenção"**.

Ela foi desenhada para permitir que o programador declare sua intenção de forma simples e direta, separando claramente a declaração de interfaces (UI) da lógica, utilizando uma "margem esquerda identitária" forte baseada em símbolos únicos.

## Funcionalidades

*   **Syntax Highlighting**: Realce de cores fiel à sintaxe v1.4.1.
*   **IntelliSense / Autocomplete**: Sugestões contextuais para elementos, propriedades e funções nativas.
*   **Suporte Multilíngue**: Escreva código em Português ou Inglês (ou misture ambos).
*   **Diagnósticos de Erro**: Identificação de erros de sintaxe em tempo real.
*   **Snippets**: Atalhos para `app`, `fun`, `if`, `while`, `foreach`, e elementos de UI.
*   **Comando Run**: Execute arquivos `.inoc` diretamente pelo VS Code usando o runtime oficial.

## Suporte Multilíngue (Aliases)

A I-NOC aceita termos em Português e Inglês como equivalentes. Abaixo a tabela de equivalências implementadas:

### Palavras-chave e UI
| Português  | Inglês | Significado         |
| ---------- | ------ | ------------------- |
| entrada    | input  | Campo de entrada    |
| verdadeiro | true   | Booleano verdadeiro |
| falso      | false  | Booleano falso      |
| texto      | text   | Elemento de texto   |
| botao      | button | Botão clicável      |
| janela     | window | Janela da aplicação |
| cor        | color  | Cor do elemento     |
| tamanho    | size   | Tamanho             |
| largura    | width  | Largura             |
| altura     | height | Altura              |
| se         | if     | Condicional         |
| senão      | else   | Caso contrário      |
| ou         | or     | Operador lógico OU  |
| não        | not    | Operador lógico NÃO |

### Funções Nativas (Built-ins)
| Português  | Inglês          | Função                         |
| ---------- | --------------- | ------------------------------ |
| tamanho    | size            | Retorna tamanho de lista/texto |
| texto      | text            | Converte para texto            |
| inserir    | insert          | Insere item em lista           |
| remover    | remove          | Remove item de lista           |
| tipo       | type            | Verifica tipo do dado          |
| subtexto   | substring       | Recorta parte de um texto      |
| procurar   | search / find   | Procura termo em texto         |
| chaves     | keys            | Chaves de um objeto            |
| arredondar | round           | Arredonda número               |
| absoluto   | absolute / abs  | Valor absoluto                 |
| definir    | define / set    | Altera valor de elemento UI    |
| numero     | number          | Converte para número           |

## Referências de UI e IDs

A I-NOC separa a variável lógica do estado da UI:

*   `email`: variável lógica.
*   `@email`: consulta o valor atual do elemento com ID `email`.
*   `|email|`: referência direta ao objeto da UI para uso em funções como `definir()`.

### Exemplo (v1.4.1)

```inoc
/: CadastroApp #ui web
/+ Principal

|#entrada ""| # id = campo_nome, largura = 20
|#botao "Salvar"|

& verdadeiro
    @: evento
    ? evento == "Salvar"
        nome = @ campo_nome
        ! "Usuário " + nome + " cadastrado!"
        definir(|campo_nome|, "")
```

## Como Instalar

1.  Baixe o arquivo `.vsix` da release oficial.
2.  No VS Code, vá em extensões, clique nos três pontos `...` e selecione "Install from VSIX...".

## Requisitos para Execução

A extensão utiliza o **I-NOC Runtime** para execução.

1.  A extensão tentará localizar automaticamente o executável `inoc-runtime.exe` (Windows) ou `inoc-runtime` (Unix).
2.  Caso o executável esteja em um local customizado, configure `inoc.runtimePath` nas configurações do VS Code.

---
**I-NOC: Código nativo orientado a intenção.**
