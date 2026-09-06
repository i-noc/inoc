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
/+ Home

|#input "Username"| # id = user
|#button "Login"|

& true
    @: event
    ? event == "Login"
        name = @ user
        ! "Hello, " + name
```

## Documentation
*   [General Summary (English)](docs/en/general_summary.md)
*   [Modular Documentation (English)](docs/en/index.md)

## License
This project is distributed under the **Apache 2.0** license. See the [LICENSE](LICENSE) file for details.

---

### 🇧🇷 Clique aqui para a versão em Português
Veja o arquivo [LEIA-ME.md](LEIA-ME.md) para a apresentação em português.

---
**I-NOC v1.4.1** - Native intention-oriented code.
