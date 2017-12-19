#! /usr/bin/env python
# -*- coding:utf-8 -*-

'''
'''

import os, sys, unittest

# @TODO: 別ディレクトリにすると読み込めない件、対応
# sys.path.append('%s/..' % os.path.dirname(os.path.abspath(__file__)))
import CTO


class TestCTO(unittest.TestCase):
    '''
    '''

    def setUp(self):
         '''
         '''
         pass


    def tearDown(self):
         '''
         '''
         pass


    def test_postToSlack(self):
        '''
        '''
        o = CTO.tamagoya()
        result = o.postToSlack('test')
        self.assertEqual(result, True)


    def test_findMenu(self):
        '''
        '''
        o = CTO.tamagoya()
        result = o.findMenu()
        self.assertEqual(isinstance(result, list), True)



if __name__ == '__main__':
    unittest.main()

