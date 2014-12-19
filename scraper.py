__author__ = 'Darthfrazier'


import nflgame
import json
import tablib


currentyear = 2015

def get_game_data(name):
    #w = csv.writer(open(name + '.csv', 'w+'))

    if __name__ == '__main__':
        player = nflgame.find(name)[0]

    if '(, )' in str(player):
        print "Player Inactive, or Player Not Found\n\n"
        return

    print "*" *79
    print player

    data = create_csv(player)
    firstyear = currentyear - player.years_pro

    if firstyear < 2009:
        firstyear = 2009

    for j in range(firstyear, currentyear):
        print (str(j) + '\n')
        data.append_separator(j)
        games = nflgame.games(j, home=player.team, away=player.team)
        for game in games:
            plyr = game.players.name(player.gsis_name)
            print '-'*79
            print game
            to_csv(plyr, game)


def to_csv(plyr, game):
    if plyr is None:
        row = ('', '', '', '', '')
        w.writerow(row)
        return

    if has_player(game, plyr.name) is False:
        row = ('', '', '', '', '')
        w.writerow(row)
        return
    else:
        print plyr.__dict__

    '''if plyr.receiving_rec:
        print checkstat(plyr, 'receiving_yds')
        w.writerow(row)'''

def check_stat(player, stat):
    if stat in player.__dict__:
        return player.stats[stat]
    else:
        return 0

def has_player(game, plyr):
    return len(list(game.drives.plays().players().filter(name=plyr))) > 0

def get_name(data, i):
    player = data[i]['player']
    head, sep, tail = player.partition(',')
    return head

def create_csv(plyr):
    data = tablib.Dataset()
    if plyr.position == 'RB' or 'WR' or 'TE':
        data.headers = ('Season', 'Game', 'Rushing_Att', 'Rushing_Yds',
                       'Rushing_Avg', 'Rushing_Tds', 'Received_Pass',
                       'Received_Yds', 'Received_Avg', 'Received_Tds',
                       'Fumbles', 'Fumbles_Lost')
    elif plyr.position == 'QB':
        data.headers = ('Season', 'Game', 'Pass_Comp', 'Pass_Att',
                       'Pass_Percentage', 'Pass_Yds', 'Pass_Interceptions',
                       'Pass_Sacks', 'Pass_Tds', 'Rushing_Att', 'Rushing_Yds', 'Rushing_Avg'
                       'Fumbles', 'Fumbles_Lost')
    return data

def main():
    with open('players.json', 'r') as f:
        data = json.load(f)
    print len(data)
    for i in range(0,(len(data) + 1)):
        name = get_name(data,i)
        get_game_data(name)
if __name__ == '__main__':
    main()
