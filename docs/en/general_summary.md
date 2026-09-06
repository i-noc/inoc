# Technical Specification and Reference Guide: I-NOC v1.4.1

I-NOC is a programming language created to allow applications, data, logic, and interfaces to be described directly, using a compact syntax where the program structure is visually evident.

The language was designed to reduce the distance between the programmer's intent and how that intent is expressed in code. Its syntax uses symbols to identify fundamental language structures and words to represent the program's semantics, such as variable names, functions, data, and conditions.

I-NOC allows you to build the logic of an application, work with data, use functions and modules, and declare user interfaces within the language itself. The interface and logic remain conceptually separate: the interface declares the elements that exist, while the logic queries, modifies, and reacts to the state of those elements.

A fundamental feature of I-NOC is that the same application can use different interface renderers. The choice between, for example, Tk and Web is made in the application declaration itself, without requiring a second implementation of the program logic.

The language therefore seeks to make the structure and intent of the code recognizable at first glance, avoiding implementation details from dominating how the program is written.

---

## Objectives

I-NOC was designed with the following fundamental objectives:

### 1. Declare intent
The code directly expresses what the programmer wants to achieve, reducing the number of details needed to represent an intent. The language seeks to bring program writing closer to the concept being implemented.

### 2. Be simple, easy to read and write
The syntax is accessible and predictable, allowing code to be understood without requiring a large number of syntactic elements. Reading the code reveals its structure and behavior naturally.

### 3. Be extremely compact
I-NOC seeks to represent functionality with the minimum necessary code, without sacrificing clarity. Compactness in I-NOC does not mean simply writing fewer characters, but reducing the amount of structure needed to express an intent.

### 4. Have native logic and UI
The language has its own features for building application logic and declaring user interfaces, without depending on external frameworks to represent fundamental language concepts. The interface is part of the language itself, not just a layer added later by a framework.

### 5. Be multiplatform
I-NOC allows the same language and logic to be used in different environments through its renderers and execution architecture. In v1.4.1, this is mainly represented by the Tk and Web renderers. The existence of different renderers allows the application description to be separated from the technology used to present it.

### 6. Have potential for multi-agent workflows
I-NOC is also designed with potential for use in multi-agent workflows, where different artificial intelligence agents can analyze, generate, modify, or execute parts of a program in a structured way. Its compact, structured, and intent-oriented syntax can favor communication between agents and programmatic code generation.

*Note: This objective represents a language development direction and does not mean that I-NOC v1.4.1 already has its own agent or multi-agent execution system.*

---

## 1. Introduction

I-NOC was developed to offer a development experience where the "left margin" of the code acts as an instant visual map of the application's flow and hierarchy.

### First Program
```inoc
/: HelloWorld #ui tk    ~~ Structure: Declares the App
/+ Main                 ~~ Structure: Declares the Screen

|#text "Hello World"|   ~~ UI: Visual Element
|#button "Exit"|        ~~ UI: Event Point

& true                  ~~ Logic: Infinite Loop
    @: e                ~~ Logic: Capture Event
    ? e == "Exit"       ~~ Logic: Condition
        ! "Goodbye!"    ~~ IO: Console output
£                       ~~ End of Block
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
| `=>` | Navigation | Navigation between screens (within UI) | `|Enter| => Home` |
| `#` | Property | Element configuration | `# color = "blue"` |
| `?` | Condition | Starts a condition (If) | `? active` |
| `£` | Else | Starts alternative block | `£` |
| `&` | While | Conditional repetition | `& x < 10` |
| `&:` | For Each | Iteration over collection | `&: item list` |
| `!` | Output | Displays a value in the console | `! "Hello"` |
| `@` | Input/UI | Queries the value of a UI element | `@ email` |
| `@:` | Event | Captures an interface event | `@: event` |
| `~~` | Comment | Line comment | `~~ comment` |
| `.` | Dot | Property or namespace access | `user.name` |
| `,` | Comma | Collection or parameter separator | `[1, 2, 3]` |
| `( )` | Parentheses | Grouping and function calls | `sum(2, 2)` |
| `[ ]` | List/Index | List creation and index access | `list[0]` |
| `=` | Assignment | Assigns a value to a variable | `x = 10` |
| `==` | Equality | Compares equality between values | `? x == 10` |

---

## 3. Program Anatomy

Every I-NOC program starts with the application configuration and its screens.

*   `/:`: **Application Symbol**. Defines the system name and global settings.
*   `/+`: **Screen Symbol**. Defines the name of a visual context.
*   `#ui`: Mandatory property in `/:` to define the graphics engine (`tk` for desktop, `web` for browser).
*   **Indentation**: I-NOC uses significant indentation (4 spaces) to define blocks.

---

## 4. Lexicon and Syntax

I-NOC recognizes five fundamental categories of lexical atoms:

1.  **Identifiers**: Names without quotes (e.g., `user`). Used for variables and UI IDs.
2.  **Numbers**: Decimal or integer literals (e.g., `3.14`).
3.  **Texts (Strings)**: Always in double quotes (e.g., `"blue"`).
4.  **Booleans**: `true` and `false` literals.
5.  **Symbols**: Single or double characters that define the structure.

---

## 5. Supported Languages

I-NOC is a native multilingual language, allowing the programmer to freely choose between **Portuguese** and **English** as equivalent ways to write code. There is no functional difference between the languages; words are normalized internally.

### Equivalence Table

| Portuguese | English | Semantic Meaning |
| :--- | :--- | :--- |
| `verdadeiro` | `true` | True boolean value |
| `falso` | `false` | False boolean value |
| `ou` | `or` | Logical OR operator |
| `não` | `not` | Logical NOT operator |
| `se` | `if` | Start of conditional block |
| `senão` | `else` | Alternative conditional block |
| `entrada` | `input` | UI element for text input |
| `botao` | `button` | Clickable UI element |
| `texto` | `text` | Label UI element / Built-in function |
| `janela` | `window` | UI element for screen settings |
| `cor` | `color` | Background color property |
| `cor_texto` | `text_color` | Font color property |
| `tamanho` | `size` | Size property / Built-in function |
| `fonte` | `font` | Font family property |
| `largura` | `width` | Fixed width property |
| `altura` | `height` | Fixed height property |
| `borda` | `border` | Border thickness property |
| `margem` | `margin` | Spacing property |
| `alinhamento`| `alignment` | Visual alignment property |
| `numero` | `number` | Function: Converts to number |
| `inserir` | `insert` | Function: Adds to list |
| `remover` | `remove` | Function: Removes from list |
| `tipo` | `type` | Function: Checks data type |
| `subtexto` | `substring` | Function: Extracts text piece |
| `procurar` | `search` / `find` | Function: Searches term in text |
| `chaves` | `keys` | Function: Lists object keys |
| `arredondar` | `round` | Function: Rounds number |
| `absoluto` | `absolute` / `abs` | Function: Absolute value |
| `definir` | `define` / `set` | Function: Changes UI element |

### Example in English
```inoc
/: App #ui web
|#input "Name"| # id = user
& true
    @: e
    ? e == "Ok"
        ! "User: " + @ user
```

### Example in Portuguese
```inoc
/: App #ui web
|#entrada "Nome"| # id = usuario
& verdadeiro
    @: e
    ? e == "Ok"
        ! "Usuario: " + @ usuario
```

---

## 6. Variables and Assignment

*   **Assignment**: Performed with the `=` operator.
    `age = 25`
*   **Namespace**: Logic variables reside in a separate memory space from **UI IDs**. Assigning to `email` does not change the input with `id = email`.

---

## 7. Data Types

The I-NOC interpreter natively manages the following types:

1.  **Number**: Floating point numerical values.
2.  **Text**: Character strings.
3.  **Boolean**: `true` or `false` values.
4.  **List**: Ordered collection of heterogeneous values.
5.  **Object**: Collection of key-value pairs.

---

## 8. Lists

Lists are dynamic collections accessed by numerical index.

*   **Creation**: `list = [10, "text", true]`
*   **Indexing**: Index starts at **zero**. Access via `list[0]`.
*   **Change**: `list[0] = 50`
*   **Iteration**:
```inoc
numbers = [1, 2, 3]
&: n numbers
    ! n
```

---

## 9. Objects (`//`)

Objects allow organizing data in key-value pairs.

*   **Declaration**: `// user` (Initializes in global scope).
*   **Literal**: `obj = //` (Creates empty object).
*   **Access**: Dot (`.`) is used for properties. `user.name = "Jose"`.
*   **Note**: `~~` is for comments. `//` is for objects.

---

## 10. Operators and Precedence

Operators are evaluated in the following priority order (lowest to highest):

1.  **Logical**: `or` → `and` → `not`.
2.  **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`.
3.  **Arithmetic**: `+`, `-` → `*`, `/`.
4.  **UI Query**: `@` (Unary operator).

---

## 11. Flow Control

### Conditional (`?` and `£`)
The conditional block starts with `?` and can contain `else if` chains. The final block (else) starts with `£`.
```inoc
? balance > 100
    ! "Rich"
else if balance > 0
    ! "Stable"
£
    ! "Attention"
```

### Repetitions (`&` and `&:`)
*   **`&` (While)**: Runs while the condition is true.
*   **`&:` (For Each)**: Iterates over each element of a list.

---

## 12. Functions (`$`)

Reusable logic blocks with parameters and return.

*   **Declaration**: `$ sum(a, b)`
*   **Return (`$:`)**: Interrupts execution and returns the value.
```inoc
$ calculate(x)
    ? x > 10
        $: x * 2
    £
        $: x
```
*Note: If the function ends without `$:`, it returns a null value (`nada`).*

---

## 13. Modules (`§`)

Allows organizing code into multiple files.

*   **Import**: `§ util` (Searches for `util.inoc`).
*   **Namespace**: Access is done by file name. `util.validate()`.
*   **Scope**: Each module has its own isolated global variables.

---

## 14. Native Functions (Built-ins)

| Function | Purpose | Parameters | Return |
| :--- | :--- | :--- | :--- |
| `size(v)` | List or text length | 1 (any) | Number |
| `text(v)` | Converts to string | 1 (any) | Text |
| `number(v)` | Converts to number | 1 (text) | Number |
| `type(v)` | Identifies data type | 1 (any) | Text |
| `insert(l, i)`| Adds item to list end | 2 (list, item) | The item |
| `remove(l, x)`| Removes item by index | 2 (list, num) | Removed item |
| `substring(t,i,f)`| Extracts text part | 3 (text, num, num) | Text |
| `search(t,s)` | Searches term in text | 2 (text, term) | Position or -1 |
| `keys(obj)` | Returns key list | 1 (object) | List |
| `round(n)` | Rounds numerical value | 1 (number) | Number |
| `abs(n)` | Positive value of a number | 1 (number) | Number |
| `set(id, v)`| Changes UI element via ID | 2 (id, value) | Value |

---

## 15. Input and Output (IO)

I-NOC clearly distinguishes between capturing actions and querying states.

*   **`!` (Output)**: Displays values in the console.
*   **`@ id` (Query)**: Expression operator that reads the current value of a UI element.
    `value = @ input_field`
*   **`@: event` (Capture)**: Command that pauses execution until an action occurs in the UI.
    `@: e`

---

## 16. User Interface (UI)

The interface is declared through the hierarchy of containers and elements.

*   **`|...|`**: Visual elements (Buttons, Inputs, Texts).
*   **`¢`**: Containers for grouping and layout.
*   **Hierarchy**: Rigidly defined by **4-space indentation**.

Example structure:
```inoc
¢ top # margin = 10
    |#text "Title"|
¢ body
    |#input ""| # id = entry
    |#button "OK"|
```

---

## 17. UI Properties

Properties configure the appearance and behavior of elements.

| Property | Tk (Desktop) | Web (Browser) | Expected Value |
| :--- | :--- | :--- | :--- |
| `# id` | Yes | Yes | Identifier |
| `# color` | Yes | Yes | Text (e.g., "green") |
| `# size` | Yes | Yes | Number (px) |
| `# font` | Yes | No | Text |
| `# width` | No | Yes | Number (px) |
| `# height` | No | Yes | Number (px) |
| `# border` | Yes | Yes | Number (px) |
| `# margin` | Yes | Yes | Number (px) |
| `# alignment`| Yes | Yes | "center", "right" |

---

## 18. UI IDs vs Variables

Fundamental distinction of v1.4.1 to ensure UI/Logic separation:
1.  **ID**: Element label in UI (`id = login`). Not a variable.
2.  **Variable**: Memory space in logic (`u = @ login`).
*Note: Changing element order in UI does not break logic, as long as the ID remains the same.*

---

## 19. Renderers

I-NOC uses a multi-renderer architecture:
*   **Tk Renderer**: Native desktop.
*   **Web Renderer**: Browser-based. Uses optimized communication between runtime and web interface.

---

## 20. Complete Examples

### Interactive Login (v1.4.1)
```inoc
/: App #ui web
/+ Main
|#input ""| # id = user
|#input ""| # id = pass
|#button "Enter"|
& true
    @: e
    ? e == "Enter"
        u = @ user
        p = @ pass
        ? u == "admin" and p == "123"
            ! "Success"
        £
            ! "Failure"
```

---

## 21. Internal Architecture and Tooling

### Execution
`Lexer` (Tokens) → `Parser` (AST) → `Interpreter` (Environment/Namespace) → `UIRuntime` (Events) → `Renderers` (Visualization).

### Development (LSP)
For support in IDEs like VS Code, I-NOC uses the following chain:
`Language Client` → `JSON-RPC` → `Language Server` → `InocAnalyzer` → `AST/Symbols`.
This architecture allows autocomplete and diagnostics to be based on the actual structure of the language in real-time.

---

## 22. Limitations and Future

*   **Renderers**: The Web Renderer does not yet map all operating system fonts and has limitations in complex layouts.
*   **Media**: No native support for direct audio or video manipulation (must be done via renderer extensions).
*   **Extension**: Official v1.4.1 support available with real LSP, contextual autocomplete, bilingual IntelliSense support, and instant diagnostics.

---
**I-NOC: Native intention-oriented code.**
