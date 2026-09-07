# I-NOC

[Português (LEIA-ME)](#-clique-aqui-para-a-versão-em-português)

---

**Native intention-oriented code.**

I-NOC is a programming language designed to allow applications, data, logic, and interfaces to be described directly and visually. It focuses on reducing the gap between the programmer's intent and the code's expression.

## Key Features
*   **Iconic Syntax**: Fast visual mapping of application hierarchy and flow.
*   **Native UI**: Declarative interface building integrated into the language.
*   **Multilingual**: Seamlessly write code using Portuguese, English, or both.
*   **Multi-renderer**: Target Desktop (Tk) or Web environments from the same source.
*   **Intelligent Tooling**: Official VS Code extension with LSP support, contextual autocomplete, and real-time diagnostics.

## Short Example
```inoc
/: MySystem #ui web
/+ Main

¢ card # width = 400, color = "white", border_radius = 20, padding = 30, alignment = "center"
    |#image "logo.png"| # width = 80, margin_bottom = 20
    |#text "Welcome"| # size = 24, bold = true
    
    |#text "User"| # alignment = "left"
    |#input "Enter your name"| # id = field_name, width = "100%"
    
    |#button "Confirm"| # id = btn_confirm, width = "100%", color = "blue"

& true
    @: event
    ? event == "btn_confirm"
        name = @ field_name
        ! "Hello, " + name
```

## Documentation
*   [General Summary (English)](docs/en/general_summary.md)
*   [Modular Documentation (English)](docs/en/index.md)

## License
This project is distributed under the **Apache 2.0** license. See the [LICENSE.md](vscode-extension/LICENSE.md) file for details.

---

### 🇧🇷 Clique aqui para a versão em Português
See the [LEIA-ME.md](LEIA-ME.md) file for the Portuguese presentation.

---
**I-NOC v1.4.5** - Native intention-oriented code.
