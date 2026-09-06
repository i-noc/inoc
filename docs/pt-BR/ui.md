# Interface de Usuário (UI)

A interface na I-NOC é declarativa e hierárquica.

## Elementos Básicos

*   **Texto**: `|#texto "Olá"|`
*   **Botão**: `|#botao "Confirmar"|`
*   **Entrada (Input)**: `|#input ""| # id = campo_nome`

## Containers (`¢`)

Containers agrupam elementos e definem o layout.

```inoc
¢ topo # cor = "cinza"
    |#texto "Minha App"|
```

## Propriedades

Configurações de aparência e comportamento:
*   `# id`: Identificador único.
*   `# cor` / `color`: Cor de fundo.
*   `# cor_texto` / `text_color`: Cor da fonte.
*   `# tamanho` / `size`: Tamanho da fonte ou elemento.
*   `# largura` / `width`: Largura fixa (Web).
*   `# altura` / `height`: Altura fixa (Web).
*   `# alinhamento` / `alignment`: "centro", "direita".

## Bilinguismo na UI

Você pode usar termos em Português ou Inglês indistintamente:
*   `|#entrada "Nome"|` é equivalente a `|#input "Nome"|`.
*   `# cor = "azul"` é equivalente a `# color = "azul"`.

---
[Anterior: Sintaxe](sintaxe.md) | [Próximo: Referência Completa](referencia.md)
