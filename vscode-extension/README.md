# I-NOC Language Support

Suporte oficial para a linguagem de programação **I-NOC** (v1.4.4).

I-NOC é uma linguagem de programação orientada à intenção, permitindo o desenvolvimento bilingue (Português/Inglês) com foco em produtividade e interfaces declarativas.

## Funcionalidades

*   **Syntax Highlighting**: Coloração sintática precisa para arquivos `.inoc`.
*   **IntelliSense**: Autocomplete contextual para elementos de UI, propriedades e funções nativas via LSP.
*   **Integrated Runtime**: Execução direta de arquivos `.inoc` através do comando "Run File".
*   **Web & Desktop Rendering**: Suporte para renderização de interfaces tanto em ambiente Web (Navegador) quanto Desktop (Tkinter).
*   **Advanced Styling**: Suporte a gradientes, transparências (RGBA), sombras e carregamento de imagens locais.
*   **Error Diagnostics**: Identificação de erros sintáticos e lógicos em tempo real.

## Exemplo de Código (v1.4.4)

```inoc
/: CadastroApp #ui web
/+ Principal

¢ card # largura = 400, cor = "branco", arredondamento = 20, padding = 30, alinhamento = "centro"
    |#imagem "logo.png"| # largura = 80, margem_baixo = 20
    |#texto "Bem-vindo"| # tamanho = 24, negrito = verdadeiro
    
    |#texto "Usuário"| # alinhamento = "esquerda"
    |#entrada "Digite seu nome"| # id = campo_nome, largura = "100%"
    
    |#botao "Confirmar"| # id = btn_confirmar, largura = "100%", cor = "azul"

& verdadeiro
    @: evento
    ? evento == "btn_confirmar"
        nome = @ campo_nome
        ! "Usuário " + nome + " confirmado!"
```

## Requisitos

*   Interpretador I-NOC (incluído no pacote da extensão).
*   Ambiente Python para execução do servidor LSP.

## Instalação

1.  Pesquise por **i-noc language plugin** no VS Code Marketplace.
2.  Clique em **Install**.
3.  O plugin detectará automaticamente o executável do runtime.

---
**I-NOC: Native intention-oriented code.**
