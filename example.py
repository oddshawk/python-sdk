from src.oddshawk_sdk import rest

def main():
    client = rest.Rest('', '')
    sports = client.sports()
    for sport in sports:
        print(sport)
        print('Available Markets:')
        markets = client.markets(True, {'sport': sport})
        print(markets)
        competitions = client.competitions(True, {'sport': sport})
        if len(competitions) > 0:
            print(competitions[0]['name'])
            events = client.events(True, {'sport': sport, 'competition': competitions[0]['id']})
            if len(events) > 0:
                print(events[0]['name'])
                print(events[0]['time'])
                odds = client.odds({'fromNow': True, 'sport': sport, 'eventName': events[0]['name'], 'eventTime': events[0]['time'], 'limit': 1})
                print(odds)


if __name__ == '__main__':
    main()