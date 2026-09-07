# I-NOC Language Support

Official extension for the **I-NOC** programming language (v1.4.1).

## What is I-NOC?

I-NOC is a programming language built under the motto: **"Native intention-oriented code"**.

## Features

*   **Syntax Highlighting**: Reliable color coding for v1.4.1 syntax.
*   **Intelligent IntelliSense**: Contextual suggestions for elements, properties, and native functions via LSP.
*   **Multilingual Support**: Write code in Portuguese or English (or both).
*   **Error Diagnostics**: Real-time syntax error identification.
*   **Run Command**: Execute `.inoc` files directly from VS Code.

## Quick Example (v1.4.1)

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

## How to Install

1.  Download the `.vsix` file.
2.  In VS Code, go to extensions, click `...` and select "Install from VSIX...".

---
**I-NOC: Native intention-oriented code.**
