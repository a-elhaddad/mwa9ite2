# -*- coding: utf-8 -*-
class User(object):
    def __init__(self, **kwargs):

        self.fb_id = kwargs.get('fb_id', "a")
        self.name = kwargs.get('name', "a")
        self.last_name = kwargs.get('last_name', "a")
        self.last_message = kwargs.get('last_message', "a")
        self.last_time = kwargs.get('last_time', "a")
    
