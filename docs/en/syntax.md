# Syntax and Structure

I-NOC uses a syntax based on symbols and meaningful indentation (4 spaces).

## Fundamental Symbols

| Symbol | Meaning | Example |
| :--- | :--- | :--- |
| `/:` | Application | `/: App #ui web` |
| `/+` | Screen | `/+ Main` |
| `¢` | Container | `¢ my_group` |
| `//` | Object | `// user` |
| `§` | Module | `§ utilities` |
| `$` | Function | `$ sum(a, b)` |
| `$: ` | Return | `$: a + b` |
| `|...|` | UI Element | `|#button "OK"|` |
| `=>` | Navigation | `|Enter| => Home` |
| `#` | Property | `# color = "blue"` |
| `?` | Condition (If) | `? active` |
| `£` | Else | `£` |
| `&` | While | `& x < 10` |
| `&:` | ForEach | `&: item list` |
| `!` | Output (Print) | `! "Hello"` |
| `@` | UI Value | `val = @ field` |
| `@:` | UI Event | `@: e` |
| `~~` | Comment | `~~ note` |
| `.` | Access | `obj.prop` |
| `=` | Assignment | `x = 10` |

## Variables and Types

I-NOC is dynamically typed and supports:
*   **Numbers**: `x = 10.5`
*   **Strings**: `name = "John"`
*   **Booleans**: `active = true` (or `verdadeiro`)
*   **Lists**: `colors = ["blue", "green"]`
*   **Objects**: `// user` or `obj = //`

## Control Flow

### Conditionals
```inoc
? x > 10
    ! "Greater"
else if x == 10
    ! "Equal"
£
    ! "Smaller"
```

### Loops
```inoc
& x < 5
    ! x
    x = x + 1

&: color colors
    ! "Color is: " + color
```

---
[Previous: Installation](installation.md) | [Next: Interface (UI)](ui.md)
