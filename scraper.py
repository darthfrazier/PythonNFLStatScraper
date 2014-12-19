__author__ = 'Darthfrazier'


import nflgame
import json
import tablib


currentyear = 2015

def get_game_data(name, book):
    #w = csv.writer(open(name + '.csv', 'w+'))

    if __name__ == '__main__':
        player = nflgame.find(name)[0]

    if '(, )' in str(player):
        print "Player Inactive, or Player Not Found\n\n"
        return

    print "*" *79
    print player

    data = create_csv(player)
    data.append_separator(name)
    firstyear = currentyear - player.years_pro

    if firstyear < 2009:
        firstyear = 2009

    for j in range(firstyear, currentyear):
        print (str(j) + '\n')
        data.append_separator(str(j))
        games = nflgame.games(j, home=player.team, away=player.team)
        for game in games:
            plyr = game.players.name(player.gsis_name)
            print '-'*79
            print game
            to_csv(data, plyr, game, j, player.position)

    with open(name + '.xls', 'wb') as f:
        f.write(data.xls)
    book.add_sheet(data)

def to_csv(data, plyr, game, j, position):
    if plyr is None:
        row = ((j, str(game), '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'))
        data.append(row)
        return

    if has_player(game, plyr.name) is False:
        row = ((j, str(game), '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'))
        data.append(row)
        return
    else:
        print plyr.__dict__

    if position == 'RB' or 'WR' or 'TE':
        row = (j, str(game), check_stat(plyr,'rushing_att'), check_stat(plyr,'rushing_yds'), '0',
               check_stat(plyr,'rushing_tds'), check_stat(plyr,'receiving_rec'), check_stat(plyr,'receiving_yds'),
               '0', check_stat(plyr,'receiving_tds'),
               check_stat(plyr,'fumbles_tot'), check_stat(plyr,'fumbles_lost'))
        data.append(row)
    elif position == 'QB':
        row = (j, str(game), check_stat(plyr,'passing_cmp'), check_stat(plyr,'passing_att'), '0',
               check_stat(plyr,'passing_yds'), check_stat(plyr,'passing_int'), check_stat(plyr,'passing_sk'),
               check_stat(plyr,'passing_tds'),check_stat(plyr,'rushing_att'), check_stat(plyr,'rushing_yds'), '0',
               check_stat(plyr, 'fumbles_tot'), check_stat(plyr, 'fumbles_lost'))
        data.append(row)
    elif position == 'K':
        row = (j, str(game), check_stat(plyr,'kicking_fga'), check_stat(plyr,'kicking_fgm'),
               check_stat(plyr,'kicking_fgb'), check_stat(plyr,'kicking_fgm_yds'), check_stat(plyr,'kicking_tot'),
               check_stat(plyr,'kickret_touchback'),check_stat(plyr,'kicking_yds'), check_stat(plyr,'kicking_ret'))
        data.append(row)

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
    elif plyr.position == 'K':
        data.headers = ('Season', 'Game', 'Field_Goal_Att', 'Field_Goal_Made',
                       'Field_Goal_Block', 'Field_Goal_Length', 'KickOff_Total',
                       'KickOff_TouchBack', 'KickOff_Yds', 'KickOff_Return')
    return data

def main():
    book = tablib.Databook()

    with open('players.json', 'r') as f:
        data = json.load(f)
    print len(data)

    for i in range(0,(len(data))):
        name = get_name(data,i)
        get_game_data(name, book)

    with open('top_300_fantasy_2014.xls', 'wb') as f:
        f.write(book.xls)
if __name__ == '__main__':
    main()
