#! /usr/bin/env python
# -*- coding:utf-8 -*-

''' CTO (=Chief Tamagoya Orderer)
'''

import os, sys, re, datetime, json, copy
import requests
import ConfigParser
import bs4


class tamagoya():
    '''
    '''
    weekday_japanease_list = [u'月', u'火', u'水', u'木', u'金', u'土', u'日']
    config = None
    verbose = False

    def __init__(self):
        '''
        '''
        self.config = ConfigParser.SafeConfigParser()

        path = '/etc/cto.ini'
        if os.path.exists(path) and os.path.isfile(path):
            self.config.read(path)

        '''
        path = '/etc/cto.d'
        if os.path.exists(path) and os.path.isdir(path):
            pass
        '''

        run_mode = self.getConfig('app', 'run_mode')
        if run_mode is not None and run_mode == 'debug':
            self.verbose = True


    def getConfig(self, section, key):
        ''' 設定取得
        '''
        result = None
        try:
            result = self.config.get(section, key)
        except:
            pass
        return result


    def log(self, message, force=False):
        ''' ログ出力
        '''
        if force is not True and self.verbose is not True:
            return
        sys.stderr.write("LOG : %s\n" % (message))


    def getWeb(self, url):
        '''
        '''
        response = None
        soup = None
        try:
            response = requests.get(url)
            html = response.content
            soup = bs4.BeautifulSoup(html, 'html.parser')
        except:
            pass

        if response is None:
            self.log('Failure (response is none) : get URL = %s' % (url), force=True)
            return None

        if response.status_code >= 400:
            self.log('Failure (response status code is %s) : get URL = %s' % (response.status_code, url), force=True)
            return None

        '''
        if response.status_code >= 300:
            self.log('Failure (response status code is %s) : get URL = %s' % (response.status_code, url), force=True)
            return None
        '''

        if soup is None:
            self.log('Failure : get URL = %s' % (url), force=True)
            return None

        self.log('Success (%s): get URL = %s' % (response.status_code, url))
        return soup


    def postToSlack(self, text, attachments=[], channel=None, username=None, icon_emoji=None, hooks_url=None):
        ''' Slack 投稿

            see: https://api.slack.com/incoming-webhooks
        '''

        # Incoming WebHooks URL
        if not hooks_url:
            hooks_url = self.getConfig('slack', 'hooks_url')

        if not channel:
            channel = self.getConfig('slack', 'channel')

        if not username:
            username = self.getConfig('slack', 'username')

        if not icon_emoji:
            icon_emoji = self.getConfig('slack', 'icon_emoji')

        payload = {
            'text':         text,
            'username':     username,
            'channel':      '#%s' % channel,
            'icon_emoji':   ':%s:' % icon_emoji,
            'attachments':  attachments
            '''
            'attachments': [
                {
                    'color':    'good', # good / warning / danger / ...
                    'pretext':  '...',
                    'title':    '...',
                    'text':     '...',
                },
                ...
            ],
            '''
        }
        response = requests.post(hooks_url, data=json.dumps(payload))

        if response.content != 'ok':
            self.log('Failure')
            return False

        self.log('Success')
        return True


    def findMenu(self):
        ''' 最新メニュー取得
        '''
        url = 'http://www.tamagoya.co.jp/menu.html'
        soup = self.getWeb(url)

        result = []

        for row in soup.find_all('div', class_='menu_title'):
            v = re.match(u'^(\d+)日\((.+)\)$', row.text)
            day = int(v.group(1))
            # weekday_japanease = v.group(2)
            weekday = self.weekday_japanease_list.index(v.group(2))

            # @TODO: day と weekday を元に date を算出 / 閏年ではない 2 月の場合に 3 月と曜日が合致してしまうので注意が必要
            # date =

            menu_list = soup.find_all('div', class_='menu_list')[i]
            menu_main_dish = menu_list.find('li', class_='menu_maindish').text
            for menu in menu_list.find_all('li', class_='menu_arrow'):
                menu_side_dish_list.append(menu.text)

            menu_note_text = menu_list.find('p', class_='menu_calorie').text
            menu_note_text = menu_note_text.split(u'おかずのカロリー')[1]
            # 例) 406kcal／塩分3.6g／えび

            menu_allergies = u'無'
            if len(menu_note_text.split(u'／')) == 3:
                menu_allergies = menu_note_text.split(u'／')[2]

            message = "\n".join([
                u'> ライスのカロリー : 340kcal',
                u'> おかずのカロリー : %s' % menu_note_text.split(u'／')[0],
                u'> 塩分 : %s' % menu_note_text.split(u'／')[1].split(u'塩分')[1],
                u'> ',
                u'> *アレルギー物質特定原材料7品目*',
                u'> _※アレルギー物質特定原材料7品目のうち、卵・乳成分・小麦は毎日のお弁当に含まれます。_',
                u'> その他のアレルギー物質特定原材料 : %s' % menu_allergies])

            result.append({
                # 'date': date,
                'day':          day,
                'weekday':      weekday,
                'main_dish':    menu_main_dish,
                'side_dish':    menu_side_dish_list,
                'note_text':    menu_note_text,
                'allergies':    menu_allergies,
                'message':      message,
            })


    def shareMenuOfToday(self):
        ''' 今日のメニューを共有
        '''
        today = datetime.date.today()

        if today.weekday() in [5, 6]:
            # 土日の場合は skip
            # self.postToSlack(u'本日 (%04d/%02d/%02d) は%s曜日です。玉子屋べんとうはありません。' % ())
            self.log('skip today', force=True)
            return None

        # @TODO: 12時を過ぎていた場合は次回のメニューを取得

        menu_list = self.findMenu()

        menu = None
        for row in menu_list:
            if row.day != today.day:
                continue
            if row.weekday != today.weekday():
                continue
            menu = row

        if menu is None:
            # 該当なし
            self.log('not applicable', force=True)
            return None

        attachments = [{'color': 'danger', 'text': menu['main_dish']}]
        for menu_side_dish in menu['side_dish']:
            attachments.append({'color': 'good', 'text': menu_side_dish})
        return self.postToSlack(message, attachments)


    def shareMenuOfNextDay(self):
        ''' 次回のメニューを共有
        '''
        raise NotImplementedError('Release on v1.')


    def shareMenuOfThisWeek(self):
        ''' 今週のメニューを共有
        '''
        raise NotImplementedError('Release on v1.')


    def shareMenuOfNextWeek(self):
        ''' 次週のメニューを共有
        '''
        raise NotImplementedError('Release on v1.')


    def receiveOrder(self, params={}):
        ''' 受注処理
        '''
        raise NotImplementedError('Release on v2.')


    def sendOrder(self, params={}):
        ''' 発注処理
        '''
        raise NotImplementedError('Release on v3.')


    def receiveOrder(self, params={}):
        ''' 集金処理
        '''
        raise NotImplementedError('Release on v4.')


    def sendOrder(self, params={}):
        ''' 支払処理
        '''
        raise NotImplementedError('Release on v5.')

