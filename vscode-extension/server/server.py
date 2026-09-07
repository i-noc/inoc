import sys
import json
import os
import traceback

# Adiciona o diretório atual ao path para facilitar imports flat
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyzer import InocAnalyzer

class InocLSPServer:
    def __init__(self):
        self.analyzer = InocAnalyzer()
        self.running = True
        self.documents = {} # uri -> text

    def run(self):
        while self.running:
            try:
                line = sys.stdin.buffer.readline().decode("utf-8")
                if not line:
                    break

                if line.startswith("Content-Length:"):
                    length = int(line.split(":")[1].strip())
                    while True:
                        empty_line = sys.stdin.buffer.readline().decode("utf-8")
                        if empty_line == "\r\n" or empty_line == "\n":
                            break

                    body = sys.stdin.buffer.read(length).decode("utf-8")
                    request = json.loads(body)
                    self.handle_message(request)
            except Exception as e:
                self.log(f"Erro no loop principal: {str(e)}")

    def handle_message(self, message):
        method = message.get("method")
        params = message.get("params")
        req_id = message.get("id")

        # Request / Response patterns
        if req_id is not None:
            if method == "initialize":
                self.send_response(req_id, {
                    "capabilities": {
                        "textDocumentSync": 1, # Full sync
                        "completionProvider": {
                            "resolveProvider": False,
                            "triggerCharacters": ["#", "|", "@", "¢"]
                        }
                    }
                })
            elif method == "textDocument/completion":
                uri = params["textDocument"]["uri"]
                pos = params["position"]
                text = self.documents.get(uri, "")
                completions = self.analyzer.get_completions(text, pos["line"] + 1, pos["character"])

                lsp_completions = []
                for c in completions:
                    kind = 6 # Variable
                    if c["kind"] == "function": kind = 3 # Function
                    elif c["kind"] == "property": kind = 10 # Property
                    elif c["kind"] == "keyword": kind = 14 # Keyword
                    elif c["kind"] == "type": kind = 25 # TypeParameter
                    elif c["kind"] == "ui_element": kind = 11 # Interface

                    item = {
                        "label": c["label"],
                        "kind": kind,
                        "detail": c.get("detail", "")
                    }

                    if c["kind"] == "property":
                         item["insertText"] = f"{c['label']} = \"$1\""
                         item["insertTextFormat"] = 2 # Snippet

                    lsp_completions.append(item)

                self.send_response(req_id, lsp_completions)

            elif method == "shutdown":
                self.send_response(req_id, {})
                self.running = False

        # Notifications
        else:
            if method == "textDocument/didOpen":
                uri = params["textDocument"]["uri"]
                text = params["textDocument"]["text"]
                self.documents[uri] = text
                self.validate_document(uri)
            elif method == "textDocument/didChange":
                uri = params["textDocument"]["uri"]
                # Como usamos sync Full (1), o texto completo vem em contentChanges[0]
                text = params["contentChanges"][0]["text"]
                self.documents[uri] = text
                self.validate_document(uri)
            elif method == "exit":
                self.running = False

    def validate_document(self, uri):
        text = self.documents.get(uri, "")
        analysis = self.analyzer.analyze(text)
        errors = analysis.get("errors", [])

        diagnostics = []
        for err in errors:
            line = max(0, err["line"] - 1)
            col = max(0, err["column"] - 1)
            diagnostics.append({
                "range": {
                    "start": {"line": line, "character": col},
                    "end": {"line": line, "character": col + 1}
                },
                "message": err["message"],
                "severity": 1 # Error
            })

        self.send_notification("textDocument/publishDiagnostics", {
            "uri": uri,
            "diagnostics": diagnostics
        })

    def send_response(self, req_id, result):
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": result
        }
        self._write(response)

    def send_notification(self, method, params):
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self._write(notification)

    def _write(self, obj):
        body = json.dumps(obj).encode("utf-8")
        sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8"))
        sys.stdout.buffer.write(body)
        sys.stdout.buffer.flush()

    def log(self, message):
        # Logs no LSP são enviados via window/logMessage
        self.send_notification("window/logMessage", {
            "type": 3, # Info
            "message": f"[I-NOC Server] {message}"
        })

if __name__ == "__main__":
    # Remove logs de stdout para não quebrar o protocolo LSP
    server = InocLSPServer()
    server.run()
