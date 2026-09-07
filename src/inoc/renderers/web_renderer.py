import json
import os
import mimetypes
import urllib.parse
import base64
import copy
from http.server import HTTPServer, BaseHTTPRequestHandler

class WebHandler(BaseHTTPRequestHandler):
    renderer = None
    def do_GET(self):
        url_path = urllib.parse.unquote(self.path)
        if url_path == "/":
            self.send_response(200); self.send_header("Content-type", "text/html"); self.end_headers()
            self.wfile.write(self.renderer.generate_shell_html().encode("utf-8"))
        elif url_path == "/state":
            self.send_response(200); self.send_header("Content-type", "application/json"); self.end_headers()
            raw_elements = self.renderer.interpreter.ui_registry.get(self.renderer.interpreter.current_screen, [])
            state = {"app_name": self.renderer.runtime.app_name, "current_screen": self.renderer.interpreter.current_screen, "ui_version": self.renderer.interpreter.ui_version, "elements": self.renderer.process_elements(raw_elements)}
            self.wfile.write(json.dumps(state).encode("utf-8"))
        else: self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length).decode("utf-8"))
        if self.path == "/event":
            inputs_by_id = data.get("inputs_by_id", {})
            for tid, tval in inputs_by_id.items(): self.renderer.interpreter._builtin_definir([tid, tval])
            if data.get("action"):
                act = data["action"]
                if act["type"] == "navegacao": self.renderer.interpreter.current_screen = act["target"]
                elif act["type"] == "funcao": self.renderer.interpreter.event_queue.put({"type": "call", "name": act["name"]})
            else: self.renderer.interpreter.event_queue.put(data.get("value"))
            self.send_response(200); self.end_headers()

class WebRenderer:
    def __init__(self, runtime):
        self.runtime = runtime
        self.interpreter = runtime.interpreter

    def start(self):
        port = 8080
        WebHandler.renderer = self
        server = HTTPServer(("127.0.0.1", port), WebHandler)
        print(f"[UI Runtime] Servidor Web ativo: http://127.0.0.1:8080")
        server.serve_forever()

    def process_elements(self, elements):
        processed = []
        for el in elements:
            el_copy = copy.deepcopy(el)
            if el_copy['type'] == 'imagem':
                path = el_copy['value']
                if not path.startswith('http') and os.path.exists(path):
                    try:
                        with open(path, "rb") as f:
                            encoded = base64.b64encode(f.read()).decode('utf-8')
                            mime_type, _ = mimetypes.guess_type(path)
                            el_copy['value'] = f"data:{mime_type or 'image/png'};base64,{encoded}"
                    except Exception: pass
            if 'children' in el_copy: el_copy['children'] = self.process_elements(el_copy['children'])
            processed.append(el_copy)
        return processed

    def generate_shell_html(self):
        return """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <title>I-NOC Web</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; font-family: 'Segoe UI', sans-serif; background: #fff; color: #1e293b; overflow: hidden; }
        #app { display: flex; flex-direction: column; width: 100%; height: 100vh; }
        .row { display: flex; flex-direction: row; box-sizing: border-box; width: 100%; align-items: stretch; }
        .container { display: flex; flex-direction: column; box-sizing: border-box; }
        .inoc-element { display: flex; box-sizing: border-box; position: relative; }
        .texto { background: transparent; white-space: pre-wrap; display: flex; }
        button { border: none; cursor: pointer; justify-content: center; display: flex; align-items: center; padding: 10px; transition: filter 0.2s; }
        button:hover { filter: brightness(1.2); }
        input { border: 1px solid rgba(255,255,255,0.1); outline: none; box-sizing: border-box; padding: 8px; }
        img { display: block; max-width: 100%; }
        .align-center { margin-left: auto; margin-right: auto; text-align: center; }
        .align-right { margin-left: auto; text-align: right; }
        .align-left { margin-right: auto; text-align: left; }
    </style>
</head>
<body>
    <div id="app"></div>
    <script>
        let lastVer = -1; let lastScr = "";
        const COLORS = { "azul": "#2563eb", "preto": "#020617", "branco": "#ffffff", "cinza": "#475569", "laranja": "#f59e0b" };
        async function sync() {
            try {
                const res = await fetch('/state'); const s = await res.json();
                if (s.ui_version !== lastVer || s.current_screen !== lastScr) { render(s); lastVer = s.ui_version; lastScr = s.current_screen; }
            } catch(e) {}
            setTimeout(sync, 300);
        }
        function render(state) {
            const app = document.getElementById('app'); app.innerHTML = '';
            renderRecursive(app, state.elements, null);
        }
        function renderRecursive(parent, elements, parentProps) {
            const isHorizontal = parentProps && parentProps.direcao === 'horizontal';

            if (isHorizontal) {
                // Se o container pai for horizontal, ignoramos as linhas e colocamos tudo lado a lado
                elements.forEach(el => parent.appendChild(buildEl(el)));
            } else {
                const lines = {};
                elements.forEach(el => { if (!lines[el.line]) lines[el.line] = []; lines[el.line].push(el); });
                Object.keys(lines).sort((a,b) => a-b).forEach(l => {
                    const rowDiv = document.createElement('div'); rowDiv.className = 'row';
                    if (parentProps && parentProps.alinhamento === 'centro') rowDiv.style.justifyContent = 'center';
                    lines[l].forEach(el => rowDiv.appendChild(buildEl(el)));
                    parent.appendChild(rowDiv);
                });
            }
        }
        function buildEl(data) {
            const p = data.props || {}; let el;
            if (data.type === 'container') {
                el = document.createElement('div'); el.className = 'container';
                if (data.children) renderRecursive(el, data.children, p);
            } else if (data.type === 'texto') {
                el = document.createElement('div'); el.className = 'texto'; el.innerText = data.value;
            } else if (data.type === 'botao') {
                el = document.createElement('button'); el.innerText = data.value;
                el.onclick = () => sendEvent(data.value, data.action);
            } else if (data.type === 'entrada' || data.type === 'input' || data.type === 'senha') {
                el = document.createElement('input'); el.placeholder = data.value;
                if (data.type === 'senha') el.type = 'password';
                if (p.id) el.id = p.id;
            } else if (data.type === 'imagem') {
                el = document.createElement('img'); el.src = data.value;
            } else if (data.type === 'link') {
                el = document.createElement('a'); el.innerText = data.value; el.style.cursor = 'pointer';
                el.onclick = () => sendEvent(data.value, data.action);
            } else { el = document.createElement('div'); el.innerText = data.value; }
            applyStyles(el, p);
            el.classList.add('inoc-element');
            return el;
        }
        function applyStyles(el, p) {
            if (p.largura) el.style.width = isNaN(p.largura) ? p.largura : p.largura + 'px';
            if (p.altura) el.style.height = isNaN(p.altura) ? p.altura : p.altura + 'px';
            if (p.fundo) el.style.background = p.fundo;
            if (p.cor_fundo || p.cor) el.style.backgroundColor = COLORS[p.cor_fundo || p.cor] || p.cor_fundo || p.cor;
            if (p.cor_texto) el.style.color = COLORS[p.cor_texto] || p.cor_texto;
            if (p.tamanho) el.style.fontSize = p.tamanho + 'px';
            if (p.negrito) el.style.fontWeight = 'bold';
            if (p.arredondamento) el.style.borderRadius = p.arredondamento + 'px';
            if (p.padding) el.style.padding = p.padding + 'px';
            if (p.sombra) el.style.boxShadow = p.sombra;
            if (p.borda) el.style.border = isNaN(p.borda) ? p.borda : p.borda + 'px solid rgba(0,0,0,0.1)';
            if (p.margem_baixo) el.style.marginBottom = p.margem_baixo + 'px';
            if (p.margem_topo) el.style.marginTop = p.margem_topo + 'px';
            if (p.gap) el.style.gap = p.gap + 'px';
            if (p.direcao === 'horizontal') { el.style.flexDirection = 'row'; el.style.alignItems = 'stretch'; }

            if (p.alinhamento === 'centro') el.classList.add('align-center');
            else if (p.alinhamento === 'direita') el.classList.add('align-right');
            else if (p.alinhamento === 'esquerda') el.classList.add('align-left');
        }
        function sendEvent(val, action) {
            const inputs = Array.from(document.querySelectorAll('input'));
            const insById = {}; inputs.forEach(i => { if (i.id) insById[i.id] = i.value; });
            fetch('/event', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ value: val, action: action, inputs: inputs.map(i => i.value), inputs_by_id: insById }) });
        }
        sync();
    </script>
</body>
</html>
"""
