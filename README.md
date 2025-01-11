# Weather API Program

本プロジェクトはPythonで天気APIを叩いてその結果を表示してくれるプログラムを作成します。

## 機能

- OpenWeatherMap APIを使用して天気情報を取得
- 都市名を入力することで、その都市の現在の天気情報を表示
- 以下の情報を取得・表示:
  - 天気状況
  - 気温
  - 湿度
  - 気圧
  - 風速

## セットアップ

1. リポジトリをクローン:
```bash
git clone https://github.com/Thikaru/mcp-python-repo.git
cd mcp-python-repo
```

2. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

3. 環境変数の設定:
- `.env.example` ファイルを `.env` にコピー
- OpenWeatherMap APIキーを取得し、`.env` ファイルに設定

## 使用方法

1. プログラムを実行:
```bash
python weather.py
```

2. プロンプトが表示されたら都市名を入力
   - デフォルトは「Tokyo」

## テストの実行

テストを実行するには:
```bash
pytest
```

## 注意事項

- OpenWeatherMap APIキーが必要です
- インターネット接続が必要です