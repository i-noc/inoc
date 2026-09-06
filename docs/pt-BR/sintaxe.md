# Sintaxe e Estrutura

A I-NOC utiliza uma sintaxe baseada em símbolos e indentação significativa (4 espaços).

## Símbolos Fundamentais

| Símbolo | Significado | Exemplo |
| :--- | :--- | :--- |
| `/:` | Aplicação | `/: App #ui web` |
| `/+` | Tela | `/+ Principal` |
| `¢` | Container | `¢ meu_grupo` |
| `//` | Objeto | `// usuario` |
| `§` | Módulo | `§ utilidades` |
| `$` | Função | `$ somar(a, b)` |
| `$: ` | Retorno | `$: a + b` |
| `|...|` | Elemento UI | `|#botao "OK"|` |
| `=>` | Navegação | `|Entrar| => Home` |
| `#` | Propriedade | `# cor = "azul"` |
| `?` | Condição (Se) | `? ativo` |
| `£` | Senão (Else) | `£` |
| `&` | Enquanto (While) | `& x < 10` |
| `&:` | Para Cada (ForEach) | `&: item lista` |
| `!` | Saída (Print) | `! "Olá"` |
| `@` | Valor de UI | `val = @ campo` |
| `@:` | Evento de UI | `@: e` |
| `~~` | Comentário | `~~ nota` |
| `.` | Acesso | `obj.prop` |
| `=` | Atribuição | `x = 10` |

## Variáveis e Tipos

A I-NOC é dinamicamente tipada e suporta:
*   **Números**: `x = 10.5`
*   **Textos**: `nome = "João"`
*   **Booleanos**: `ativo = verdadeiro` (ou `true`)
*   **Listas**: `cores = ["azul", "verde"]`
*   **Objetos**: `// usuario` ou `obj = //`

## Controle de Fluxo

### Condicionais
```inoc
? x > 10
    ! "Maior"
else if x == 10
    ! "Igual"
£
    ! "Menor"
```

### Loops
```inoc
& x < 5
    ! x
    x = x + 1

&: cor cores
    ! "A cor é: " + cor
```

---
[Anterior: Instalação](instalacao.md) | [Próximo: Interface (UI)](ui.md)
