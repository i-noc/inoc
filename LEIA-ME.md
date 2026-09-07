# I-NOC

[English (README)](#-click-here-for-the-english-version)

---

**Código nativo orientado a intenção.**

A I-NOC é uma linguagem de programação criada para permitir que aplicações, dados, lógica e interfaces sejam descritos de forma direta e visual. O foco é reduzir a distância entre a intenção do programador e a expressão do código.

## Principais Características
*   **Sintaxe Icônica**: Mapeamento visual rápido da hierarquia e do fluxo da aplicação.
*   **UI Nativa**: Construção de interface declarativa integrada à linguagem.
*   **Multilíngue**: Escreva código em Português, Inglês ou ambos, sem distinção.
*   **Multi-renderer**: Suporte para Desktop (Tk) ou Web a partir do mesmo código.
*   **Ferramental Inteligente**: Extensão oficial para VS Code com LSP, autocomplete contextual e diagnósticos em tempo real.

## Exemplo Rápido
```inoc
/: MeuSistema #ui web
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
        ! "Olá, " + nome
```

## Documentação
*   [Resumo Geral (Português)](docs/pt-BR/resumo_geral.md)
*   [Documentação Modular (Português)](docs/pt-BR/index.md)

## Licença
Este projeto é distribuído sob a licença **Apache 2.0**. Veja o arquivo [LICENSE.md](vscode-extension/LICENSE.md) para detalhes.

---

### 🇺🇸 Click here for the English version
Check the [README.md](README.md) file for the English presentation.

---
**I-NOC v1.4.5** - Código nativo orientado a intenção.
