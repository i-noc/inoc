# I-NOC: Código nativo orientado a intenção

Seja bem-vindo à documentação oficial da **I-NOC**, uma linguagem de programação criada para permitir que aplicações, dados, lógica e interfaces sejam descritos de forma direta e visual.

## Filosofia e Lema

> **"Código nativo orientado a intenção."**

O lema da I-NOC reflete seu objetivo fundamental: reduzir a distância entre o que o programador deseja realizar (a intenção) e como isso é expresso no código.

## Características Principais

*   **Sintaxe Icônica**: Uso de símbolos para representar a estrutura hierárquica e semântica do programa.
*   **UI Nativa**: A interface do usuário é parte integrante da linguagem, não uma biblioteca externa.
*   **Bilinguismo Nativo**: Suporte completo e equivalente para termos em Português e Inglês.
*   **Multi-renderer**: O mesmo código pode ser renderizado em ambientes Desktop (Tk) ou Web.
*   **Compactação**: Foco em expressar lógica complexa com o mínimo de ruído estrutural.
*   **Inteligência**: Suporte oficial para VS Code com LSP (Language Server Protocol) e autocomplete contextual.

## Primeiro Programa

Um exemplo básico de aplicação com interface e lógica de saída:

```inoc
/: OlaMundo #ui tk      ~~ Declara o App com interface Desktop
/+ Principal            ~~ Define a tela inicial

|#texto "Olá Mundo"|    ~~ Elemento de texto
|#botao "Sair"|         ~~ Botão clicável

& true                  ~~ Loop infinito de eventos
    @: e                ~~ Captura o próximo evento da interface
    ? e == "Sair"       ~~ Verifica se o evento é o botão "Sair"
        ! "Até logo!"   ~~ Exibe mensagem no console
£                       ~~ Fim do bloco
```

---
[Próximo: Instalação](instalacao.md)
