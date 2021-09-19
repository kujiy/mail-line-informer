# これはなに
- 特定のメールをLINE通知するもの
- 動作フロー
  - [定義されたルール](https://github.com/kujiy/mail-line-informer/blob/master/models.py) `my_rules.py` に基づき特定のメールボックスから新規メールを探します
  - 未読のメールを通知します
   - 一度通知されたメールは、既読になります（重複通知を防止するため)

# 動作環境
- python scriptが走る環境
- DB等不要
- cron で 1min おきに走らせるなど

# 使い方
1. メーラー側で通知したいメールを特定のmailboxに入るようにフィルタをしておく。
   1. e.g. From: `info@school-pass.jp` を school-pass というフォルダに振り分ける
      1. メールボックス名は単語1つが吉。スペース入れて動くかは知らない。
1. LINE Notify TOKEN を取得
    1. [https: // notify-bot.line.me/ja/](https: // notify-bot.line.me/ja/)
1. `.env` ファイルを作る
    1. 中身は `.env.sample` を参照
1. `my_rules.py` ファイルを作る
    1. 中身は `my_rules.sample.py` を参照
1. install
    1. ```
        git clone https://github.com/kujiy/mail-line-informer.git
        cd mail-line-informer
        python3 -m venv venv
        . venv/bin/activate
        pip install - r requirements.txt
        python main.py
        ```
1. cronで定期実行する
    - 
   ```
   * * * * * cd <path_to>/mail-line-informer && ./venv/bin/python <path_to>/mail-line-informer/main.py 2>&1 >> /tmp/mail-line-informer.log
   ```

# Gmailを使う場合
- 「安全性の低いアプリの許可」を ON にしてください。imapで Authentication failed が返ります。
  - https://myaccount.google.com/lesssecureapps
- OFF で動くアプリの作り方、どなたか教えて下さい

# できないこと, やりたいこと
- mailbox内でfilterをすること
- 複数のメアドを使うこと
- plugins 方式にして、LINE以外の通知もしたい
  - folderが別れてるだけで、まだ動的に読み込む・蹴るコードになってない
- PRお待ちしてます

# Thanks
I edited and included several files of the repos below.

- https://github.com/10mohi6/line-notify-python/
- https://github.com/keitaoouchi/easyimap/

