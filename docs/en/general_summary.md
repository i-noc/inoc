# Technical Specification and Reference Guide: I-NOC v1.4.5

I-NOC is a programming language created to allow applications, data, logic, and interfaces to be described directly, using a compact syntax where the program structure is visually evident.

The language was designed to reduce the distance between the programmer's intent and how that intent is expressed in code. Its syntax uses symbols to identify fundamental language structures and words to represent the program's semantics, such as variable names, functions, data, and conditions.

I-NOC allows you to build the logic of an application, work with data, use functions and modules, and declare user interfaces within the language itself. The interface and logic remain conceptually separate: the interface declares the elements that exist, while the logic queries, modifies, and reacts to the state of those elements.

A fundamental feature of I-NOC is that the same application can use different interface renderers. The choice between, for example, Tk and Web is made in the application declaration itself, without requiring a second implementation of the program logic.

---

## Objectives

### 1. Declare intent
The code directly expresses what the programmer wants to achieve, reducing the number of details needed to represent an intent.

### 2. Be simple, easy to read and write
The syntax is accessible and predictable, revealing the code's structure and behavior naturally.

### 3. Be extremely compact
I-NOC seeks to represent functionality with the minimum necessary code, reducing the structure needed to express an intent.

### 4. Have native logic and UI
The interface is part of the language itself, allowing logic construction and UI declaration without external frameworks.

### 5. Be multiplatform
The same logic is used in different environments (Desktop/Tk and Browser/Web) through specialized renderers.

---

## 1. Introduction

I-NOC acts as an instant visual map of the application's flow and hierarchy.

### First Program
```inoc
/: HelloWorld #ui web
/+ Main

¢ card # width = 400, color = "white", border_radius = 20, alignment = "center"
    |#text "Hello World"|   ~~ UI: Visual Element
    |#button "Exit"|        ~~ UI: Event Point

& true
    @: e
    ? e == "Exit"
        ! "Goodbye!"
```

---

## 2. Table of Fundamental Symbols

| Symbol | Name | Semantic Meaning | Example |
| :--- | :--- | :--- | :--- |
| `/:` | Application | Defines application and renderer | `/: App #ui web` |
| `/+` | Screen | Defines a new UI screen/section | `/+ Main` |
| `¢` | Container | Groups elements and visual hierarchy | `¢ container` |
| `//` | Object | Object/dictionary structure | `// user` |
| `§` | Module | Loads external module with namespace | `§ math` |
| `$` | Function | Declares a function | `$ sum(a, b)` |
| `$: ` | Return | Returns function value | `$: a + b` |
| `|...|` | UI | Declares an interface element | `|#button "OK"|` |
| `#` | Property | Element configuration | `# color = "blue"` |
| `?` | Condition | Starts a condition (If) | `? active` |
| `£` | Else | Starts alternative block | `£` |
| `&` | While | Conditional repetition | `& x < 10` |
| `&:` | For Each | Iteration over collection | `&: item list` |
| `!` | Output | Displays a value in the console | `! "Hello"` |
| `@` | Input/UI | Queries the value of a UI element | `@ email` |
| `@:` | Event | Captures an interface event | `@: event` |
| `~~` | Comment | Line comment | `~~ comment` |
| `=` | Assignment | Assigns a value to a variable | `x = 10` |
| `==` | Equality | Compares equality between values | `? x == 10` |

---

## 3. Supported Languages

I-NOC allows you to freely choose between **Portuguese** and **English**. Words are normalized internally.

### UI and Properties Equivalence
*   `input` / `entrada`
*   `button` / `botao`
*   `text` / `texto`
*   `color` / `cor`
*   `width` / `largura`
*   `height` / `altura`
*   `alignment` / `alinhamento`

---

## 4. Advanced Web Rendering (v1.4.5)

The Web engine now supports modern design properties:
*   **Styling**: `fundo` (supports linear-gradient), `sombra` (box-shadow), `arredondamento` (border-radius), and `padding`.
*   **Images**: Support for local image loading via automatic Base64 conversion.
*   **Dynamic Layout**: Automatic centering for cards and expansion mode for full screens (`100vw/100vh`).
*   **Types**: New `|#senha|` (password) element for protected fields.

---

## 5. Architecture and Tooling

I-NOC uses an LSP-based architecture for VS Code, offering:
*   **Contextual Autocomplete**: Intelligent suggestions based on the AST.
*   **Diagnostics**: Real-time identification of syntax errors.
*   **Integrated Runtime**: Execution via a native binary included in the extension.

---
**I-NOC v1.4.5: Native intention-oriented code.**
