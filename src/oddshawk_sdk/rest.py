from urllib.parse import urlencode

import requests


class Rest:
    def __init__(self, user, key):
        self.user = user
        self.key = key

    def __generate_hash(self):
        # get unix timestamp
        import time
        timestamp = int(time.time())
        # get hexidecimal timestamp
        hex_timestamp = hex(timestamp)[2:]
        # get sha256 hash of secret + timestamp
        import hashlib
        hash_key = hashlib.sha256((self.key + str(timestamp)).encode('UTF-8')).hexdigest() + hex_timestamp
        return hash_key

    def __get_headers(self):
        return {
            'X-OH-User': self.user,
            'X-OH-Hash': self.__generate_hash()
        }

    # Add documentation docstrings

    def __get(self, url):
        return requests.get('https://www.odds.software' + url, headers=self.__get_headers()).json()

    def sports(self, from_now=True):
        """
        :param bool from_now: Only get sports that have events that start after now
        :return: Array list of sport names
        """
        return self.__get('/rest/odds/sports?fromNow=' + str(from_now))

    def competitions(self, from_now=True, search_params={}):
        """
        :param bool from_now: Only get competitions that have events that start after now
        :param dictionary search_params: Search parameters. Options are sport and provider. Example: {'sport': 'Horse Racing', 'provider': 'Bet365'}. Note that specifying provider will avoid cache and may be slower.
        :return: Array list of competition objects
        """
        search = urlencode(search_params)
        return self.__get('/rest/odds/competitions?fromNow=' + str(from_now) + '&' + search)

    def events(self, from_now=True, search_params={}):
        """
        :param bool from_now: Only get events that start after now
        :param dictionary search_params: Search parameters. Options are sport, provider, competition (using the competition ID), and market. Example: {'sport': 'Football', 'provider': 'Bet365', 'market': 'Match Odds'}. Note that specifying provider or market (or competition without also specifying sport) will avoid cache and may be slower.
        :return: Array list of event objects
        """
        search = urlencode(search_params)
        return self.__get('/rest/odds/events?fromNow=' + str(from_now) + '&' + search)

    def markets(self, from_now=True, search_params={}):
        """
        :param bool from_now: Only get markets that have events that start after now
        :param dictionary search_params: Search parameters. Options are sport, provider, and competition (using the competition ID). Example: {'sport': 'Football', 'provider': 'Bet365'}. Note that specifying provider or competition will avoid cache and may be slower.
        :return: Array list of market names
        """
        search = urlencode(search_params)
        return self.__get('/rest/odds/markets?fromNow=' + str(from_now) + '&' + search)

    def providers(self, from_now=True, search_params={}):
        """
        :param bool from_now: Only get providers that have events that start after now
        :param dictionary search_params: Search parameters. Options are sport and competition (using the competition ID). Example: {'sport': 'Football'}. Note that specifying competition will avoid cache and may be slower.
        :return: Array list of provider names
        """
        search = urlencode(search_params)
        return self.__get('/rest/odds/providers?fromNow=' + str(from_now) + '&' + search)

    def odds(self, search_params={}):
        """
        :param dictionary search_params: Search parameters.
        Options are eventTime, eventName, sport, sports, provider, competition (using the competition ID), competitionName, selectionStatus, sortField, sortDirection, limit, skip, and market.
        To request more than 200 items at a time you must provide either eventTime & eventName or sport & provider.
        Example: {'sport': 'Football', 'provider': 'Bet365', 'market': 'Match Odds', 'selectionStatus': 'ACTIVE'}. Never cached.
        :return: Array of odds objects
        """
        search = urlencode(search_params)
        return self.__get('/rest/odds?' + search)
