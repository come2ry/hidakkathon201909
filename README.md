# :checkered_flag: 学生版ヒダッカソン -API編- (2019/09)

## :computer: 競技者のアプリケーション動作環境

GitHubリポジトリの概要辺りにリンクがあります。

そこからアクセスしてください。

## :books: データベースについて

データベースにはMySQLを利用しています。

###  接続情報

以下の環境変数に情報があります。適切に利用してください。

- `DB_HOST`: ホスト名 / 接続先
- `DB_PORT`: ポート番号
- `DB_NAME`: データベース名
- `DB_USER`: ユーザ名
- `DB_PASS`: パスワード

## :page_facing_up: 対応言語

現状対応している言語は以下のものです。

- go
- python
- ruby
- php

### 使用言語について

言語のランタイムや初期コードを用意していないだけで、自前で用意できれば言語の選択は自由です。

## :beginner: 初期実装について

初期実装はサーバーとしては動作するものの、APIは何も実装されていません。

HTTPステータス `501 Not Implemented` を返すだけのものになっています。

Frameworkは導入してあります。差し替えについては問題ありません。

また、Libraryの導入自由にしていただいて構いません。

## :arrows_counterclockwise: 使用言語の切替について

初期状態ではPythonが実行されています。

別の言語に切り替えるためのヘルパーシェル `switch-app.sh` を用意しておきました。

コマンドのあとに使用したい言語を指定することで切り替えることが出来ます。

例として、 `go` に切り替えたい場合には以下のように実行します。

```sh
./switch-app.sh go
```

:warning: このスクリプトはリモートのサーバーでのみ正しく動作します。

## :rocket: アプリ起動方法について

### 起動・停止・再起動

リモートのサーバーでのアプリケーションの管理は `systemd` で行っています。これをCLIで制御する `systemctl` コマンドを使って操作を行います。

各言語のアプリケーション名は以下のようになっています。

- go: `hidakkathon-go`
- python: `hidakkathon-python`
- ruby: `hidakkathon-ruby`
- php: `hidakkathon-php`

以下からgoを例にあげて解説します。

#### アプリケーションの起動

以下のように実行します。

```sh
systemctl start hidakkathon-go
```

#### アプリケーションの停止

以下のように実行します。

```sh
systemctl stop hidakkathon-go
```

#### アプリケーションの再起動

以下のように実行します。

```sh
systemctl restart hidakkathon-go
```

### 起動方法の変更

フレームワークなどを導入した際にアプリの起動する方法を変更したくなる場合があるでしょう。

その場合は `units` フォルダ内にある、各言語に対応するファイルを編集します。

- go: `hidakkathon-go.service`
- python: `hidakkathon-python.service`
- ruby: `hidakkathon-ruby.service`
- php: `hidakkathon-php.service`

ファイル内の `ExecStart` の部分を変更することで起動コマンドを変更することが出来ます。

また、**このファイルを変更したら必ず `systemctl daemon-reload` を実行してください！**

## :computer: ローカル環境について

各言語のローカル環境でDocker/docker-composeを使った設定ファイルを用意してあります。

### 概要

ローカル環境を起動すると下記のポートでアクセスできます。

- [localhost:8080](http://localhost:8080) : Webページ
- [localhost:8081](http://localhost:8081) : APIサーバー

上記の通り、 `8080` / `8081` ポートを使用するので他のソフトウェアで既に使用されてないように注意してください。

### 起動方法

ローカル環境として利用したい言語のフォルダで `docker-compose up -d` を実行してください。

### コードを変更した場合

アプリケーションのコードやライブラリなどを追加した場合は `docker-compose build` でイメージのビルドを行ってください。

その後、 `docker-compose up -d` を実行することで再作成の必要があるコンテナだけ再作成を行ってくれます。

### Cleanup

`docker-compose down` で環境の停止及び削除ができます。

## :calling: gitを使ったリモートサーバーへのデプロイについて

ローカル環境を使った場合にリモートサーバーへのデプロイ方法の手順です。

1. 変更したコードをコミットし、リポジトリの `master` ブランチへPush
2. リモートサーバーのリポジトリで変更が無いことを確認(`Changes not staged for commit` の部分。 `Untracked files` の部分は大抵大丈夫)
3. `deploy-app.sh` を実行(例: `./deploy-app.sh go` )

`deploy-app.sh` はリポジトリをpullして指定言語のパッケージインストール、ビルド、再起動を行ってくれます。

活用してみてください。

## :information_source: その他

リモートサーバーについての付加情報です。

チューニングや設定変更の際に参考にしてみてください。

### フロントエンドのサーバー

アプリケーションはポート番号 `8080` 番でListenしています。
この前段に `nginx` がおり、APIについてのリクエストはアプリケーションへプロキシしてくれています。

設定ファイルは `/etc/nginx/site-available` / `/etc/nginx/site-enabled` にあります。

#### URLの仕様について

現状のnginxの設定では、

1. `/initialize` にアクセスがあった場合、 `initialize.sh` を実行し、出力結果を返す
2. `DocumentRoot` を `static` としてファイルを検索し、存在したらそのコンテンツを返す
3. 見つからなかった場合、バックエンドのアプリケーションへプロキシする

という設定になっています。

例として、

- `/` のアクセスは `static/index.html` を返却
- `/js/app.js` のアクセスは `static/js/app.js` を返却
- `/top` のアクセスはバックエンドのアプリケーションへプロキシ

というような処理になります。

### 初期化処理(Initialize)

初期化処理では `initialize.sh` が実行され、データベースのデータの初期化を行っています。

データベースにインデックスの追加などをしたい場合は `initialize.sh` の適切な変更をおすすめします。

