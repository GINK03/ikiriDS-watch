# ikirids-watch

## 必要なもの
Twitter API, Python3, Slack API

## 環境によって設定が必要なもの
- Twitter APIの環境変数設定
- SlackのAPIの環境変数設定

## deamonで動作させる
pythonのanacondaをちょくで動作させるのがややこしく、shell scriptを経由して書くとうまくいく  

serviceファイルを配置して登録する
```
$ sudo cp deamon.service /etc/systemd/system
$ sudo systemctl deamon-reload
$ sudo systemctl start deamon
$ sudo systemctl enable deamon
```

## 動作イメージ
<div align="center">
  <img width="750px" src="https://user-images.githubusercontent.com/4949982/41266481-fa5797e6-6e31-11e8-8f69-526b78053f7d.png"> 
</div>
