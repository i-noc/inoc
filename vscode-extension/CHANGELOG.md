# Changelog

Todas as mudanças notáveis para a extensão I-NOC serão documentadas neste arquivo.

## [1.4.4] - 2024-06-10

### Adicionado
- Suporte para carregamento de imagens locais via conversão automática para Base64 no motor Web.
- Novo motor de renderização Web com suporte a gradientes e transparências RGBA.
- Lógica de expansão dinâmica de layout: centralização automática para cards e modo "stretch" para sistemas de tela cheia (Dashboards).
- Melhoria no sistema de alinhamento individual de elementos (`align-self`).
- Suporte para campos de tipo `senha` (password).

### Corrigido
- Localização robusta do executável `inoc-runtime` em diferentes sistemas de arquivos.
- Conflitos de alinhamento em containers aninhados.
- Tratamento de erro ao carregar o módulo principal no Extension Host (Bundling).
- Correção de espaçamentos (`gap`) e dimensões proporcionais em elementos de grade.

## [1.4.1] - 2024-06-09

### Adicionado
- LSP (Language Server Protocol) real integrado.
- Autocomplete inteligente baseado na AST da linguagem.
- Diagnósticos instantâneos via Language Server.

## [1.3.0] - 2024-06-09

### Adicionado
- Diagnósticos de erro em tempo real.
- IntelliSense / Autocomplete básico.
- Suporte a múltiplos workspaces.
