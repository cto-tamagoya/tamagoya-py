# tamagoya-py : CTO (=Chief Tamagoya Orderer)

* [玉子屋](http://www.tamagoya.co.jp/) の当日分のメニューを Slack に通知

----

## Usage

### Build

```
$ git clone git@github.com:ukyooo/cto.git cto
$ cd cto
$ docker build --no-cache --force-rm -t ukyooo/cto:latest .
```

* **NOTE: Docker Hub に build 済みの Docker Image があります。**
    * see: https://hub.docker.com/r/ukyooo/cto/

### Run

```
$ docker run -d \
    -e SLACK_HOOKS_URL=<Slack Incoming WebHooks URL> \
    [-e SLACK_CHANNEL=...] \
    [-e SLACK_USERNAME=...] \
    [-e SLACK_ICON_EMOJI=...] \
    [-e BATCH_RUN_HOUR=...] \
    [-e BATCH_RUN_MINUTE=...] \
    [-e RUN_MODE=...] \
    [--name cto] \
    ukyooo/cto:latest ;
```

#### Environment

| key                   | Req / Opt | type      | default           | description                                                           | NOTE      |
|-----------------------|:---------:|-----------|-------------------|-----------------------------------------------------------------------|-----------|
| `SLACK_HOOKS_URL`     | Required  | string    |                   | Slack Incoming WebHooks URL (`https://hooks.slack.com/services/...`)  |           |
| `SLACK_CHANNEL`       | Optional  | string    | general           | Slack 投稿先の Channel                                                | `#` 不要  |
| `SLACK_USERNAME`      | Optional  | string    | tamagoya          | Slack 投稿時の User Name                                              | `@` 不要  |
| `SLACK_ICON_EMOJI`    | Optional  | string    | hatching_chick    | Slack 投稿時のアイコン絵文字                                          | `:` 不要  |
| `BATCH_RUN_HOUR`      | Optional  | integer   | 9                 | メニュー通知 時 設定                                                  | `0 - 23`  |
| `BATCH_RUN_MINUTE`    | Optional  | integer   | 0                 | メニュー通知 分 設定                                                  | `0 - 59`  |
| `RUN_MODE`            | Optional  | string    | production        | `debug` を指定した場合はデバッグモードで起動                          |           |

----

## Future Release

| Version   | Summary       | Description                                   |
|:---------:|:--------------|:----------------------------------------------|
| `v1.x.x`  | 宣伝処理 対応 | 週末に次週分のメニューを Slack に通知する。   |
| `v2.x.x`  | 受注処理 対応 | 週末までに次週分の注文を受注する。            |
| `v3.x.x`  | 発注処理 対応 | 週頭に今週分の注文を発注する。                |
| `v4.x.x`  | 集金処理 対応 | 週末までに今週分の代金を集金する。            |
| `v5.x.x`  | 支払処理 対応 | 週末に今週分の代金を支払う。                  |

----

## NOTE

* **これ以上の開発が進むことは (おそらく) ありません。**
* **本件は [ex-mixi Advent Calendar 2017](https://qiita.com/advent-calendar/2017/ex-mixi) の 2017/12/21 用として作られました。**
    * see: [2017/12/21 : What does a CTO do ?]()

----

## Contributing

* ...

----

## License

* ...

