# User Interface (UI)

Interfaces in I-NOC are declarative and hierarchical.

## Basic Elements

*   **Text**: `|#text "Hello"|`
*   **Button**: `|#button "Confirm"|`
*   **Input**: `|#input ""| # id = name_field`

## Containers (`¢`)

Containers group elements and define the layout.

```inoc
¢ top # color = "gray"
    |#text "My App"|
```

## Properties

Appearance and behavior settings:
*   `# id`: Unique identifier.
*   `# color` / `cor`: Background color.
*   `# text_color` / `cor_texto`: Font color.
*   `# size` / `tamanho`: Font or element size.
*   `# width` / `largura`: Fixed width (Web).
*   `# height` / `altura`: Fixed height (Web).
*   `# alignment` / `alinhamento`: "center", "right".

## Bilingual UI

You can use terms in Portuguese or English interchangeably:
*   `|#entrada "Name"|` is equivalent to `|#input "Name"|`.
*   `# color = "blue"` is equivalent to `# cor = "blue"`.

---
[Previous: Syntax](syntax.md) | [Next: Full Reference](reference.md)
