#!/usr/bin/env python3
# encoding: utf-8
'''
DockURL is a front-end to the pyshorteners package, providing URL shorteners
and other services.  This is primarily intended to run within a Docker
container, providing URL shortening, etc. as a micro-service.

@author:     deej Howard

@copyright:  2018 WildKidz, Unlimited

@license:    GPL

@contact:    wilddeej@gmail.com
'''

import logging
import pyshorteners

class DockURL:
    ''' Top-level entity. '''
    _verbosity = 0
    _action = None
    _config = {}
    _shorteners = []
    _urls = []

    def __init__(self, verbosity):
        '''
        Initialize
        '''
        self._verbosity = verbosity
        logging.basicConfig(level=logging.INFO)

    def set_action(self, action):
        '''
        Set the action
        :param action:
        '''
        self._action = action

    def set_config(self, config):
        '''
        Set the configuration
        :param config:
        '''
        self._config = config

    def set_shorteners(self, shorteners):
        '''
        Set the shorteners
        :param shorteners:
        '''
        self._shorteners = shorteners

    def set_urls(self, urls):
        '''
        Set the urls
        :param urls:
        '''
        self._urls = urls

    def shorten_url(self, shortener, url):
        '''
        Shorten the provided URL against the specified shortener.
        :param shortener:
        :param url:
        '''
        try:
            # Extract/use relevant parts of self._config as arg
            short_main = pyshorteners.Shortener(**self._config[shortener])
            result = getattr(short_main, shortener).short(url)
            print(shortener+"="+result)
        except AttributeError as exception:
            logging.error("Unable to %s %s using %s:\n%s",
                          self._action, url, shortener,
                          format(exception))

    def expand_url(self, shortener, url):
        '''
        Expand the provided URL against the specified shortener.
        :param shortener:
        :param url:
        '''
        try:
            # Extract/use relevant parts of self._config as arg
            short_main = pyshorteners.Shortener(**self._config[shortener])
            result = getattr(short_main, shortener).expand(url)
            print(shortener+"="+result)
        except (pyshorteners.exceptions.ExpandingErrorException, 
                AttributeError) as exception:
            logging.error("Unable to %s %s using %s:\n%s",
                          self._action, url, shortener,
                          format(exception))

    def url_click_stats(self, shortener, url):
        '''
        Report on click statistics of the URL against the specified shortener.
        :param shortener:
        :param url:
        '''
        try:
            # Extract/use relevant parts of self._config as arg
            short_main = pyshorteners.Shortener(**self._config[shortener])
            result = getattr(short_main, shortener).total_clicks(url)
            print(shortener+"="+str(result))
        # TODO: Better handling for unsupported function
        except AttributeError as exception:
            logging.error("Unable to %s %s using %s:\n%s",
                          self._action, url, shortener,
                          format(exception))

    def run(self):
        '''
        Execute the relevant action with appropriate parameters
        '''
        for url in self._urls:
            for shortener in self._shorteners:
                if self._verbosity:
                    logging.info("Executing %s %s on %s...", 
                                 shortener, self._action, url)
                if self._action == 'shorten':
                    self.shorten_url(shortener, url)
                elif self._action == 'expand':
                    self.expand_url(shortener, url)
                elif self._action == 'click-count':
                    self.url_click_stats(shortener, url)

