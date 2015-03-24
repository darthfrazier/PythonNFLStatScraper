__author__ = 'Darthfrazier'


import nflgame
import json
import tablib
import atexit


def get_game_data(name, team, book, year):

    if __name__ == '__main__':
        try:
            player = nflgame.find(name)[0]
        except BaseException:
            return

    if '(, )' in str(player):
        print ("Player Inactive, or Player Not Found\n\n")
        return

    print ("*" *79)
    print (player)

    data = create_csv(player)
    data.append_separator(name)

    print (str(year) + '\n')
    data.append_separator(year)
    games = nflgame.games(year, home=team, away=team)
    for game in games:
        plyr = game.players.name(player.gsis_name)
        print ('-'*79)
        print (game)
        to_csv(data, plyr, game, year, player.position)

    with open(name + '.xls', 'wb') as f:
        f.write(data.xls)
    book.add_sheet(data)

def to_csv(data, plyr, game, j, position):
    if plyr is None:
        if data.width < 12:
            row = (('N/A', j, str(game), '0', '0', '0', '0', '0', '0', '0', '0'))
        else:
            row = (('N/A', j, str(game), '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0'))
        data.append(row)
        return

    if has_player(game, plyr.name) is False:
        if data.width < 12:
            row = (('N/A', j, str(game), '0', '0', '0', '0', '0', '0', '0', '0'))
        else:
            row = (('N/A', j, str(game), '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0'))
        data.append(row)
        return
    else:
        print (plyr.__dict__)

    if position == 'RB' or position == 'WR' or position == 'TE':
        row = (plyr.team, j, str(game), check_stat(plyr,'rushing_att'), check_stat(plyr,'rushing_yds'),
               check_stat(plyr,'rushing_tds'), check_stat(plyr,'receiving_rec'), check_stat(plyr,'receiving_yds'),
                check_stat(plyr,'receiving_tds'),
               check_stat(plyr,'fumbles_tot'), check_stat(plyr,'fumbles_lost'))
        data.append(row)
    elif position == 'QB':
        row = (plyr.team, j, str(game), check_stat(plyr,'passing_cmp'), check_stat(plyr,'passing_att'),
               check_stat(plyr,'passing_yds'), check_stat(plyr,'passing_ints'), check_stat(plyr,'passing_sk'),
               check_stat(plyr,'passing_tds'),check_stat(plyr,'rushing_att'), check_stat(plyr,'rushing_yds'),
               check_stat(plyr, 'fumbles_tot'), check_stat(plyr, 'fumbles_lost'), check_stat(plyr, "rushing_tds"))
        data.append(row)
    else:
        row = (plyr.team, j, str(game), check_stat(plyr,'kicking_fga'), check_stat(plyr,'kicking_fgm'),
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
    player = data[i]['Player']
    head, sep, tail = player.partition(',')
    return head

def get_team(data, i):
    player = data[i]['Player']
    head, sep, tail = player.partition(', ')
    return tail

def create_csv(plyr):
    data = tablib.Dataset()
    if plyr.position == 'RB' or plyr.position == 'WR' or plyr.position == 'TE':
        data.headers = ('Team', 'Season', 'Game', 'Rushing_Att', 'Rushing_Yds',
                        'Rushing_Tds', 'Received_Pass',
                       'Received_Yds', 'Received_Tds',
                       'Fumbles', 'Fumbles_Lost')

    elif plyr.position == 'QB':
        data.headers = ('Team','Season', 'Game', 'Pass_Comp', 'Pass_Att',
                        'Pass_Yds', 'Pass_Interceptions',
                       'Pass_Sacks', 'Pass_Tds', 'Rushing_Att', 'Rushing_Yds',
                       'Fumbles', 'Fumbles_Lost', 'Rushing_Tds')
    else:
        data.headers = ('Team','Season', 'Game', 'Field_Goal_Att', 'Field_Goal_Made',
                       'Field_Goal_Block', 'Field_Goal_Length', 'KickOff_Total',
                       'KickOff_TouchBack', 'KickOff_Yds', 'KickOff_Return')
    return data

def main():
    book = tablib.Databook()

    year = input('Year: ')

    with open(str(year) + '.json', 'r') as f:
        data = json.load(f)
    print (len(data))

    for i in range(0,(len(data))):
        name = get_name(data,i)
        team = get_team(data, i)
        get_game_data(name, team, book, year)

    with open('top_300_fantasy_2014.xls', 'wb') as f:
        f.write(book.xls)

    def exit_handler():
        print ('All Done!')

    atexit.register(exit_handler)

if __name__ == '__main__':
    main()

