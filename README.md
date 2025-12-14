# File Util MCPサーバー

## 概要
* Officeドキュメント、PDF、ZIP、テキストなどのファイル操作を行うユーティリティ機能を提供
* APIサーバーおよびMCPサーバーとして動作可能
* Clineや他のMCP対応クライアントから利用可能

### 前提条件
* 以下のソフトウェアがインストール済みであること
    * vscode
    * cline
    * Python
    * uv

## セットアップ手順

1. このGitリポジトリをクローンします。
    ```bash
    git clone https://github.com/knd3dayo/file-util.git
    ```

1. クローンしたディレクトリでuv syncを実行
    ```batch
    uv sync
    ```

## APIサーバーの起動

APIサーバーを起動するには以下を実行します。

```bash
uv run -m file_util.api.api_server
```

デフォルトでは `http://localhost:8000` で起動します。

### APIサーバー概要
このAPIサーバーはFastAPIベースで構築されており、ファイル操作をHTTP経由で提供します。  
主な特徴:
- RESTful API設計
- JSON形式での入出力
- ファイルアップロード対応（multipart/form-data）
- ログ出力・エラーハンドリング対応

#### 主なエンドポイント
| エンドポイント | メソッド | 説明 |
|----------------|----------|------|
| `/get_mime_type` | GET | 指定ファイルのMIMEタイプを取得 |
| `/get_sheet_names` | GET | Excelファイルのシート名一覧を取得 |
| `/extract_excel_sheet` | POST | 指定シートからテキストを抽出 |
| `/extract_text_from_file` | POST | ファイルからテキストを抽出 |
| `/extract_base64_to_text` | GET | Base64データからテキストを抽出 |
| `/export_to_excel` | GET | データをExcelファイルにエクスポート |
| `/import_from_excel` | GET | Excelファイルからデータをインポート |


## MCPサーバー設定

`sample_cline_mcp_settings.json`を参考に、`cline_mcp_settings.json`に以下を追加します。
`<PATH_TO_PROJECT_DIR>`はこのプロジェクトのパスに置き換えてください。

```json
"file_util_mcp": {
  "disabled": false,
  "timeout": 60,
  "type": "stdio",
  "command": "uv",
  "args": [
    "--directory",
    "<PATH_TO_PROJECT_DIR>",
    "run",
    "-m",
    "file_util.mcp.mcp_server"
  ]
}
```
