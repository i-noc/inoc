# Installation

I-NOC is designed to be easy to install and use, especially through its official VS Code extension.

## 1. Using the VS Code Extension (Recommended)

The ideal flow for the end user is:

1.  Install **Visual Studio Code**.
2.  Search for **"I-NOC Language Support"** in the extensions marketplace and install it.
3.  Create a file with the `.inoc` extension.
4.  The extension already includes the necessary **Runtime** in its internal folder (`bin/`).

## 2. Runtime Configuration

The Runtime (`inoc-runtime.exe`) is the engine that runs your programs.

*   The extension tries to locate the runtime automatically.
*   If you have a custom version, you can configure the path in the VS Code settings: `inoc.runtimePath`.

## 3. System Requirements

*   **Windows**: Full support (Desktop via Tk and Web).
*   **Linux/macOS**: Support via source code execution or Web rendering (see the Renderers section).

---
[Previous: Home](index.md) | [Next: Syntax](syntax.md)
