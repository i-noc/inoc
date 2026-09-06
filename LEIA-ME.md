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
/+ Inicio

|#entrada "Usuário"| # id = usuario
|#botao "Entrar"|

& verdadeiro
    @: evento
    ? evento == "Entrar"
        nome = @ usuario
        ! "Olá, " + nome
```

## Documentação
*   [Resumo Geral (Português)](docs/pt-BR/resumo_geral.md)
*   [Documentação Modular (Português)](docs/pt-BR/index.md)

## Licença
Este projeto é distribuído sob a licença **Apache 2.0**. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

### 🇺🇸 Click here for the English version
Check the [README.md](README.md) file for the English presentation.

---
**I-NOC v1.4.1** - Código nativo orientado a intenção.
