# I-NOC Language Support

Official extension for the **I-NOC** programming language (v1.4.5).

I-NOC is an intention-oriented programming language, allowing bilingual development (Portuguese/English) with a focus on productivity and declarative interfaces.

## Features

*   **Syntax Highlighting**: Precise syntax coloring for `.inoc` files.
*   **IntelliSense**: Contextual autocomplete for UI elements, properties, and native functions via LSP.
*   **Integrated Runtime**: Direct execution of `.inoc` files via the "Run File" command.
*   **Web & Desktop Rendering**: Support for interface rendering in both Web (Browser) and Desktop (Tkinter) environments.
*   **Advanced Styling**: Support for gradients, transparency (RGBA), shadows, and local image loading via Base64.
*   **Dynamic Layouts**: Support for auto-centered layouts (Card style) and automatic expansion for full-screen systems (Dashboard/Bento Grid).
*   **Error Diagnostics**: Real-time identification of syntax and logic errors.

## Code Example (v1.4.5)

```inoc
/: AppName #ui web
/+ Main

~~ Automatically centered container
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
        ! "User " + name + " confirmed!"
```

## Requirements

*   I-NOC Interpreter (included in the extension package).
*   Python environment for the LSP server.

## Installation

1.  Search for **i-noc language plugin** in the VS Code Marketplace.
2.  Click **Install**.
3.  The plugin will automatically detect the runtime executable.

---
**I-NOC: Native intention-oriented code.**
