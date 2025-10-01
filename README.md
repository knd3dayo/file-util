# Officeドキュメント、PDFからテキスト抽出するMCPサーバー

## 概要
* Officeドキュメント、PDFからテキスト抽出するMCPサーバー

### 前提条件
* 以下のソフトウェアがインストール済みであること
    * vscode
    * cline
    * Python
    * uv

## 準備
1. このGitリポジトリをclineします。
    ```bash
    git clone https://github.com/knd3dayo/extract_file_mcp.git
    ```

1. Python仮想環境を作成します.
    ```batch
    python -m venv venv
    ```

1. venv環境を有効にして、Web検索MCPサーバーをインストールします
    ```batch
    venv\Scripts\Activate
    pip install .
    ```

1. `sample_cline_mcp_settings.json`の内容を編集して、`cline_mcp_settings.json`に追加します.
    <PATH_TO_VENV>はvenvへのパス

    ```json
    "extract_file_mcp": {
      "disabled": false,
      "timeout": 60,
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "<PATH_TO_VENV>",
        "run",
        "-m",
        "extract_file_mcp.mcp_modules.mcp_server"
      ]
    }
    ```

1. ClineのMCPサーバー一覧に`extract_file_mcp`が表示されて有効になっていれば設定完了です。
