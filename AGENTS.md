# RP2040Robot / OpenCode 作業ルール

## 目的

このリポジトリはRP2040ロボットの制御コード、Unity/Web表示、FreeCADの機構モデルをまとめたものです。FreeCADの補助では、主に `models/FreeCad_v3` を現行モデルとして扱います。過去版を変更する場合は、ユーザーが明示したときだけ対象にしてください。

## FreeCAD作業のルール

- `.FCStd`、`.FCBak`、`.blend` を直接編集・上書きしない。
- 形状変更は `freecad/scripts/` に再実行可能なFreeCAD Pythonスクリプトとして作る。
- スクリプトは対象ドキュメント、変更対象オブジェクト、単位、期待する結果をコメントに書く。
- 破壊的な処理（削除、移動、上書き保存）は、実行前に対象と出力先を確認する。
- 寸法が不足している場合は推測で確定せず、必要な寸法を質問する。
- FreeCADでスクリプトを実行した後、`freecad/context/current_document.md` を更新してから結果を確認する。

## CAD補助で優先すること

1. 既存のPart/Part Design構造を確認する。
2. 寸法と単位を明示する。特にFreeCADの長さはmmを標準とする。
3. 取付穴、干渉、可動範囲、3Dプリントの肉厚を確認する。
4. 変更案、実行用スクリプト、確認手順を分けて提示する。

## 通常の作業手順

1. FreeCADで対象ファイルを開く。
2. `freecad/macros/export_document_report.FCMacro` を実行する。
3. OpenCodeで `freecad/context/current_document.md` を読み、変更内容を依頼する。
4. 生成されたスクリプトをFreeCADのPythonコンソールまたはマクロから実行する。
5. FreeCADで形状を確認し、必要なら再度レポートを出力する。

## コマンド

OpenCodeのセッション中は、次のような依頼を使えます。

- 「現在のFreeCADレポートを確認して、干渉しそうな箇所を列挙して」
- 「`freecad/scripts/` に、指定寸法で部品を追加するスクリプトを作って」
- 「このスクリプトを実行する前に、変更対象と保存先をレビューして」
