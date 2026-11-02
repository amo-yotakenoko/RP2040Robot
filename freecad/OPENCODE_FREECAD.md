# OpenCodeでFreeCADを補助する運用

## 前提

OpenCodeのモデルは、FreeCAD GUIの画面や `.FCStd` の内部形状を自動的に正しく読めるとは限りません。そのため、FreeCAD内でドキュメントのオブジェクト階層・主要寸法・バウンディングボックスをテキスト化してから相談します。

## 初回セットアップ

1. OpenCodeをインストールして、リポジトリのルートで起動します。
2. OpenCodeのTUIで `/connect` を実行し、OpenCode Consoleへ接続します。無料モデルは提供期間、地域、利用上限で変わるため、`/models` で `Free` と表示されるモデルを選択できます。
3. このプロジェクトでは `opencode.jsonc` が初期モデルを `opencode/glm-5.3-flash-free` に設定しています。利用できない場合は `/models` から別の無料モデルを選んでください。
4. FreeCADで `freecad/macros/export_document_report.FCMacro` を開いて実行します。

## FreeCADからOpenCodeへの情報共有

マクロは `freecad/context/current_document.md` を生成します。ここにはオブジェクト名、種類、ラベル、配置、寸法プロパティ、形状のバウンディングボックスが入ります。生成物はリポジトリ内に残るため、OpenCodeが読み取れます。

## OpenCodeからFreeCADへの変更

形状を変更するときは、OpenCodeに「FreeCAD用Pythonスクリプトを `freecad/scripts/` に作成して」と依頼します。生成されたスクリプトはFreeCADのPythonコンソールで確認してから実行してください。FreeCADファイルの保存は、原本ではなく複製した検証用ファイルに対して行うのが安全です。

## 重要な制約

- 無料モデルは混雑時に利用制限・モデル変更・応答失敗が起きる可能性があります。
- モデルが提案した寸法や形状が機械的に正しいとは限りません。干渉、強度、印刷方向、ねじ・サーボの実寸をFreeCADと実物で確認してください。
- APIキー、認証情報、個人情報をリポジトリへ保存しないでください。
