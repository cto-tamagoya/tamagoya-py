#! /usr/bin/env python
# -*- coding:utf-8 -*-

import json
import CTO

o = CTO.tamagoya()

try:
    o.shareMenuOfToday()
except Exception as e:
    message = 'Error : %s' % (str(e))
    attachments = [
        {'color': 'danger', 'text': 'type = %s' % (str(type(e)))},
        {'color': 'danger', 'text': 'args = %s' % (str(e.args))},
        {'color': 'danger', 'text': 'message = %s' % (e.message)},
    ]
    o.log('%s : %s' % (message, json.dumps(attachments)), force=True)
    o.postToSlack(message, attachments)
