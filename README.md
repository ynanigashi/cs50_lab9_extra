元データ：https://cs50.jp/x/2021/week9/lab/
- ローカル環境で起動できるようにする
- ORM(SQLAlchemy)を導入する
    - Session.executeで書き込み
    - working with metadata
- Herokuで稼働させる
- HerokuのDBをPostgresSQLに切り替える
    - postgressqlをherokuにデプロイ(アプリに紐づけてデプロイすると接続URLが自動でアプリの環境変数DATABASE＿URLに入る)
    ```
    heroku addons:create heroku-postgresql:hobby-dev -a <application_name>
    ```
    https://devcenter.heroku.com/ja/articles/heroku-postgresql
    
    - postgresSQLを利用できるようにアプリを書き換える

    - DBを初期化する
    ```
    heroku run python -a <application_name>
    >>> from app import init_db
    >>> init_db()
    ```