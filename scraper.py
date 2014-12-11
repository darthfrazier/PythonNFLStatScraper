__author__ = 'Darthfrazier'

import nflgame

def getgamedata(year, name):

    if __name__ == '__main__':
        player = nflgame.find(name)[0]
g
    games = nflgame.games(year, home=player.team, away=player.team)
    print player
    print year
    print
    for game in games:
        plyr = game.players.name(player.gsis_name)

        print '-'*79
        print game
        #print plyr.receiving_rec, plyr.receiving_yds, plyr.receiving_tds, plyr.receiving_lng
        if plyr.stats:
            print plyr.stats
def main():
    name = 'Dez Bryant'
    for i in range(2010,2014):
        getgamedata(i,name)
        print
        print
        print


if __name__ == '__main__':
    main()
