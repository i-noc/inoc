import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class WebHandler(BaseHTTPRequestHandler):
    renderer = None
    def do_GET(self):
        if self.path == "/":
            self.send_response(200); self.send_header("Content-type", "text/html"); self.end_headers()
            self.wfile.write(self.renderer.generate_shell_html().encode("utf-8"))
        elif self.path == "/state":
            self.send_response(200); self.send_header("Content-type", "application/json"); self.end_headers()
            state = {
                "app_name": self.renderer.runtime.app_name,
                "current_screen": self.renderer.interpreter.current_screen,
                "ui_version": self.renderer.interpreter.ui_version,
                "elements": self.renderer.interpreter.ui_registry.get(self.renderer.interpreter.current_screen, [])
            }
            self.wfile.write(json.dumps(state).encode("utf-8"))
        else: self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length).decode("utf-8"))
        if self.path == "/event":
            inputs_by_id = data.get("inputs_by_id", {})
            for tid, tval in inputs_by_id.items():
                self.renderer.interpreter._builtin_definir([tid, tval])

            for val in data.get("inputs", []):
                self.renderer.runtime.input_queue.put(val)
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

    def generate_shell_html(self):
        return """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <title>I-NOC Web</title>
    <meta charset="utf-8">
    <style>
        body { margin: 0; background-color: #f0f0f0; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: sans-serif; }
        #app { width: 100%; max-width: 400px; height: 650px; background: #fff; padding: 15px; border-radius: 30px; box-shadow: 0 30px 60px rgba(0,0,0,0.12); display: flex; flex-direction: column; overflow: hidden; }
        .row { display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; width: 100%; gap: 4px; }
        .container { display: flex; flex-direction: column; width: 100%; gap: 4px; }
        .inoc-element { display: flex; align-items: center; box-sizing: border-box; min-height: 45px; border-radius: 8px; }
        .texto { padding: 15px; font-weight: 500; background: transparent; white-space: pre-wrap; }
        button { border: none; background: #e0e0e0; cursor: pointer; font-weight: 600; justify-content: center; font-size: 18px; }
        button:active { filter: brightness(0.8); transform: scale(0.96); }
        input { border: 1px solid #ddd; padding: 10px; width: 100%; outline: none; }
        .align-center { justify-content: center; text-align: center; }
        .align-right { justify-content: flex-end; text-align: right; }
    </style>
</head>
<body>
    <div id="app"></div>
    <script>
        let lastVer = -1; let lastScr = "";
        const COLORS = { "azul": "#007bff", "verde": "#28a745", "vermelho": "#dc3545", "amarelo": "#ffc107", "preto": "#000", "branco": "#fff", "cinza": "#333", "laranja": "#ff9f0a" };
        async function sync() {
            try {
                const res = await fetch('/state'); const s = await res.json();
                if (s.ui_version !== lastVer || s.current_screen !== lastScr) { render(s); lastVer = s.ui_version; lastScr = s.current_screen; }
            } catch(e) {}
            setTimeout(sync, 200);
        }
        function render(state) {
            const app = document.getElementById('app'); app.innerHTML = '';
            const winEl = state.elements.find(el => el.type === 'janela');
            if (winEl && winEl.props.cor === 'preto') { document.body.style.backgroundColor = "#111"; app.style.backgroundColor = "#000"; app.style.color = "#fff"; }
            else { document.body.style.backgroundColor = "#f0f0f0"; app.style.backgroundColor = "#fff"; app.style.color = "#000"; }
            renderRecursive(app, state.elements);
        }
        function renderRecursive(parent, elements) {
            const rows = {};
            elements.forEach(el => {
                if (el.type === 'janela') return;
                if (!rows[el.line]) rows[el.line] = [];
                rows[el.line].push(el);
            });
            Object.keys(rows).sort((a,b) => a-b).forEach(l => {
                const rDiv = document.createElement('div'); rDiv.className = 'row';
                rows[l].forEach(el => rDiv.appendChild(buildEl(el)));
                parent.appendChild(rDiv);
            });
        }
        function buildEl(data) {
            const p = data.props || {}; let el;
            if (data.type === 'container') { el = document.createElement('div'); el.className = 'container'; renderRecursive(el, data.children); }
            else if (data.type === 'texto') { el = document.createElement('div'); el.className = 'texto'; el.innerText = data.value; }
            else if (data.type === 'botao') {
                el = document.createElement('button'); el.innerText = data.value;
                el.onclick = () => {
                    const ins = Array.from(document.querySelectorAll('input')).map(i => i.value);
                    const insById = {};
                    Array.from(document.querySelectorAll('input')).forEach(i => {
                        const inocEl = elements.find(e => e.type === 'input' && e.value === i.defaultValue) ||
                                       {props: {id: i.id}}; // Fallback simples
                        // Na verdade, o melhor e pegar pelo ID que o renderer colocou
                        if (i.id) insById[i.id] = i.value;
                    });
                    fetch('/event', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ value: data.value, action: data.action, inputs: ins, inputs_by_id: insById }) });
                };
            } else if (data.type === 'input') {
                el = document.createElement('input'); el.value = data.value;
                if (p.id) el.id = p.id;
            }
            el.classList.add('inoc-element');
            if (p.cor) el.style.backgroundColor = COLORS[p.cor] || p.cor;
            if (p.cor_texto) el.style.color = COLORS[p.cor_texto] || p.cor_texto;
            if (p.tamanho) el.style.fontSize = p.tamanho + 'px';
            if (p.largura) el.style.width = p.largura + 'px';
            if (p.altura) el.style.height = p.altura + 'px';
            if (p.alinhamento === 'centro') el.classList.add('align-center');
            if (p.alinhamento === 'direita') el.classList.add('align-right');
            if (p.margem) el.style.marginTop = p.margem + 'px';
            if (p.borda) el.style.border = p.borda + 'px solid rgba(255,255,255,0.1)';
            return el;
        }
        sync();
    </script>
</body>
</html>
"""
