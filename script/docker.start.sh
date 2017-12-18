#! /bin/bash

APP_DIR=$(cd $(dirname $0) && pwd)
APP_DIR="$APP_DIR/.."

if [ -e "$APP_DIR/env.ini" ]; then
  source $APP_DIR/env.ini
fi

# Required
if [ ! $SLACK_HOOKS_URL ]; then
  echo "ERROR: " >&2
  exit 1
fi

# Optional
if [ ! $SLACK_CHANNEL ]; then
  SLACK_CHANNEL=general
fi
if [ ! $SLACK_USERNAME ]; then
  SLACK_USERNAME=tamagoya
fi
if [ ! $SLACK_ICON_EMOJI ]; then
  SLACK_ICON_EMOJI=hatching_chick
fi

if [ ! $BATCH_RUN_HOUR ]; then
  BATCH_RUN_HOUR=9
fi
if [ ! $BATCH_RUN_MINUTE ]; then
  BATCH_RUN_MINUTE=0
fi

if [ ! $RUN_MODE ]; then
  RUN_MODE="production"
fi

# @TODO: $BATCH_RUN_XXX 値の判定

# Slack 試験 通知
SLACK_POST_MESSAGE="It is a test post to Slack."
SLACK_POST_RESULT=`curl -X POST -H 'Content-type: application/json' \
  --data "{
    \"channel\": \"#$SLACK_CHANNEL\",
    \"username\": \"$SLACK_USERNAME\",
    \"icon_emoji\": \":$SLACK_ICON_EMOJI:\",
    \"text\": \"$SLACK_POST_MESSAGE\",
  }" $SLACK_HOOKS_URL`
if [ "$SLACK_POST_RESULT" != "ok" ]; then
  echo "ERROR: post to Slack failed." >&2
  exit 1
fi

# crontab 設定
cp $APP_DIR/config/crontab.txt /tmp/crontab.txt
sed -i "s|%%BATCH_RUN_MINUTE%%|$BATCH_RUN_MINUTE|" /tmp/crontab.txt
sed -i "s|%%BATCH_RUN_HOUR%%|$BATCH_RUN_HOUR|" /tmp/crontab.txt
/usr/bin/crontab /tmp/crontab.txt
rm -f /tmp/crontab.txt

# app.ini 設定
# APP_INI=$APP_DIR/app.ini
APP_INI=/etc/cto.ini
cp $APP_DIR/cto.ini.template $APP_INI
sed -i "s|%%RUN_MODE%%|$RUN_MODE|" $APP_INI
sed -i "s|%%SLACK_HOOKS_URL%%|$SLACK_HOOKS_URL|" $APP_INI
sed -i "s|%%SLACK_CHANNEL%%|$SLACK_CHANNEL|" $APP_INI
sed -i "s|%%SLACK_USERNAME%%|$SLACK_USERNAME|" $APP_INI
sed -i "s|%%SLACK_ICON_EMOJI%%|$SLACK_ICON_EMOJI|" $APP_INI

# Supervisor 設定
cp $APP_DIR/config/supervisord.conf /etc/supervisord.conf
# cp $APP_DIR/config/supervisord.crond.conf /etc/supervisord.d/crond.conf

# Supervisor 起動
supervisord -c /etc/supervisord.conf

# Slack 通知
SLACK_POST_MESSAGE="*Success : CTO (=Chief Tamagoya Orderer) has started.*"
curl -X POST -H 'Content-type: application/json' \
  --data "{
    \"channel\": \"#$SLACK_CHANNEL\",
    \"username\": \"$SLACK_USERNAME\",
    \"icon_emoji\": \":$SLACK_ICON_EMOJI:\",
    \"text\": \"$SLACK_POST_MESSAGE\",
  }" $SLACK_HOOKS_URL

exit 0
