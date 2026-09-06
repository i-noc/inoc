import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} from 'vscode-languageclient/node';

let client: LanguageClient;

export async function activate(context: vscode.ExtensionContext) {
    // 1. Localiza o servidor LSP
    const serverInfo = await findServer(context);

    if (serverInfo) {
        const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

        const serverOptions: ServerOptions = {
            run: { command: pythonCmd, args: [serverInfo.path], transport: TransportKind.stdio },
            debug: { command: pythonCmd, args: [serverInfo.path], transport: TransportKind.stdio }
        };

        const clientOptions: LanguageClientOptions = {
            documentSelector: [{ scheme: 'file', language: 'inoc' }],
            synchronize: {
                fileEvents: vscode.workspace.createFileSystemWatcher('**/*.inoc')
            }
        };

        client = new LanguageClient(
            'inocLSP',
            'I-NOC Language Server',
            serverOptions,
            clientOptions
        );

        client.start();
    } else {
        vscode.window.showWarningMessage('Servidor LSP I-NOC não encontrado. Algumas funcionalidades podem estar limitadas.');
    }

    // 2. Comando de Execução (mantido)
    let runCommand = vscode.commands.registerCommand('inoc.runFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        const filePath = editor.document.uri.fsPath;
        const runtimeInfo = await findRuntime(editor.document.uri, context);

        if (!runtimeInfo) {
            vscode.window.showErrorMessage('Runtime I-NOC não encontrado.');
            return;
        }

        const terminal = vscode.window.activeTerminal || vscode.window.createTerminal('I-NOC Runtime');
        terminal.show();

        if (runtimeInfo.isPython) {
            const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
            const interpreterDir = path.dirname(runtimeInfo.path);
            terminal.sendText(`cd "${interpreterDir}"`);
            terminal.sendText(`${pythonCmd} "${runtimeInfo.path}" "${filePath}"`);
        } else {
            terminal.sendText(`& "${runtimeInfo.path}" "${filePath}"`);
        }
    });
    context.subscriptions.push(runCommand);
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

async function findServer(context: vscode.ExtensionContext): Promise<{ path: string } | undefined> {
    // Tenta encontrar o server.py baseado na estrutura do projeto
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (workspaceFolders) {
        const rootPath = workspaceFolders[0].uri.fsPath;
        const serverPath = path.join(rootPath, 'src', 'inoc', 'lsp', 'server.py');
        if (fs.existsSync(serverPath)) {
            return { path: serverPath };
        }
    }

    // Fallback para a pasta da extensão (se estivermos empacotando o source)
    const extServerPath = path.join(context.extensionPath, 'src', 'inoc', 'lsp', 'server.py');
    if (fs.existsSync(extServerPath)) {
        return { path: extServerPath };
    }

    return undefined;
}

interface RuntimeInfo {
    path: string;
    isPython: boolean;
}

async function findRuntime(currentFileUri: vscode.Uri, context: vscode.ExtensionContext): Promise<RuntimeInfo | undefined> {
    const config = vscode.workspace.getConfiguration('inoc');
    const customPath = config.get<string>('runtimePath');

    if (customPath && fs.existsSync(customPath)) {
        return { path: customPath, isPython: customPath.endsWith('.py') };
    }

    const exeName = process.platform === 'win32' ? 'inoc-runtime.exe' : 'inoc-runtime';
    const extRuntimePath = path.join(context.extensionPath, 'bin', exeName);
    if (fs.existsSync(extRuntimePath)) {
        return { path: extRuntimePath, isPython: false };
    }

    const workspaceFolder = vscode.workspace.getWorkspaceFolder(currentFileUri);
    if (workspaceFolder) {
        const distExePath = path.join(workspaceFolder.uri.fsPath, 'dist', exeName);
        if (fs.existsSync(distExePath)) {
            return { path: distExePath, isPython: false };
        }

        let currentDir = path.dirname(currentFileUri.fsPath);
        const rootLimit = path.dirname(workspaceFolder.uri.fsPath);
        while (currentDir !== rootLimit) {
            const mainPy = path.join(currentDir, 'main.py');
            if (fs.existsSync(mainPy)) {
                return { path: mainPy, isPython: true };
            }
            const parentDir = path.dirname(currentDir);
            if (parentDir === currentDir) break;
            currentDir = parentDir;
        }
    }

    return undefined;
}
