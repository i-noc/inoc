# I-NOC: Native intention-oriented code

Welcome to the official documentation of **I-NOC**, a programming language designed to allow applications, data, logic, and interfaces to be described directly and visually.

## Philosophy and Motto

> **"Native intention-oriented code."**

I-NOC's motto reflects its fundamental goal: to reduce the distance between what the programmer wants to achieve (the intention) and how it is expressed in code.

## Key Features

*   **Iconic Syntax**: Symbols represent the hierarchical and semantic structure of the program.
*   **Native UI**: The user interface is an integral part of the language, not an external library.
*   **Native Bilingualism**: Full and equivalent support for terms in Portuguese and English.
*   **Multi-renderer**: The same code can be rendered in Desktop (Tk) or Web environments.
*   **Compactness**: Focuses on expressing complex logic with minimal structural noise.
*   **Intelligence**: Official VS Code support with LSP (Language Server Protocol) and contextual autocomplete.

## First Program

A basic example of an application with an interface and output logic:

```inoc
/: HelloWorld #ui tk    ~~ Declares the App with Desktop interface
/+ Main                 ~~ Defines the initial screen

|#text "Hello World"|   ~~ Text element
|#button "Exit"|        ~~ Clickable button

& true                  ~~ Infinite event loop
    @: e                ~~ Captures the next interface event
    ? e == "Exit"       ~~ Checks if the event is the "Exit" button
        ! "Goodbye!"    ~~ Displays message in the console
£                       ~~ End of block
```

---
[Next: Installation](installation.md)
