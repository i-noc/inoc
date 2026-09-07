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
    try {
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

        // 2. Comando de Execução (Reescrito para maior compatibilidade)
        let runCommand = vscode.commands.registerCommand('inoc.runFile', async () => {
            try {
                const editor = vscode.window.activeTextEditor;
                if (!editor) return;
                const filePath = editor.document.uri.fsPath;
                const runtimeInfo = await findRuntime(editor.document.uri, context);

                if (!runtimeInfo) {
                    vscode.window.showErrorMessage('Runtime I-NOC não encontrado.');
                    return;
                }

                let execution: vscode.ProcessExecution | vscode.ShellExecution;

                if (runtimeInfo.isPython) {
                    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
                    execution = new vscode.ProcessExecution(pythonCmd, [runtimeInfo.path, filePath]);
                } else {
                    // Uso de ProcessExecution evita problemas com sintaxe de shell (& vs cmd)
                    execution = new vscode.ProcessExecution(runtimeInfo.path, [filePath]);
                }

                const task = new vscode.Task(
                    { type: 'inoc-run' },
                    vscode.TaskScope.Workspace || vscode.TaskScope.Global,
                    'Execução I-NOC',
                    'inoc',
                    execution
                );

                await vscode.tasks.executeTask(task);
            } catch (err) {
                vscode.window.showErrorMessage(`Erro ao executar arquivo: ${String(err)}`);
            }
        });
        context.subscriptions.push(runCommand);
    } catch (err) {
        console.error('Falha na ativação da extensão I-NOC:', err);
    }
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

async function findServer(context: vscode.ExtensionContext): Promise<{ path: string } | undefined> {
    const extServerPath = path.join(context.extensionPath, 'server', 'server.py');
    if (fs.existsSync(extServerPath)) {
        return { path: extServerPath };
    }

    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (workspaceFolders) {
        const rootPath = workspaceFolders[0].uri.fsPath;
        const devServerPath = path.join(rootPath, 'src', 'inoc', 'lsp', 'server.py');
        if (fs.existsSync(devServerPath)) {
            return { path: devServerPath };
        }
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
