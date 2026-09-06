# Instalação

A I-NOC foi projetada para ser fácil de instalar e usar, especialmente através da sua extensão oficial para o VS Code.

## 1. Usando a Extensão VS Code (Recomendado)

O fluxo ideal para o usuário final é:

1.  Instale o **Visual Studio Code**.
2.  Procure por **"I-NOC Language Support"** no marketplace de extensões e instale.
3.  Crie um arquivo com a extensão `.inoc`.
4.  A extensão já inclui o **Runtime** necessário em sua pasta interna (`bin/`).

## 2. Configuração do Runtime

O Runtime (`inoc-runtime.exe`) é o motor que executa seus programas. 

*   A extensão tenta localizar o runtime automaticamente.
*   Se você tiver uma versão personalizada, pode configurar o caminho nas configurações do VS Code: `inoc.runtimePath`.

## 3. Requisitos de Sistema

*   **Windows**: Suporte total (Desktop via Tk e Web).
*   **Linux/macOS**: Suporte via execução do código fonte ou através de renderização Web (consulte a seção de Renderizadores).

---
[Anterior: Início](index.md) | [Próximo: Sintaxe](sintaxe.md)
