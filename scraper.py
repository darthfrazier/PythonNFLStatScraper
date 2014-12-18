__author__ = 'Darthfrazier'


import nflgame
import json
import csv

currentyear = 2015

def getgamedata(name):
    w = csv.writer(open(name + '.csv', 'w+'))

    if __name__ == '__main__':
        player = nflgame.find(name)[0]

    if '(, )' in str(player):
        print "Player Inactive, or Player Not Found"
        return
    print player

    firstyear = currentyear - player.years_pro

    if firstyear < 2009:
        firstyear = 2009

    for j in range(firstyear, currentyear):
        print (str(j) + '\n')
        games = nflgame.games(j, home=player.team, away=player.team)
        nflgame.combine(games).csv("2011.csv")
        for game in games:
            plyr = game.players.name(player.gsis_name)

            print '-'*79
            print game
            #print plyr.receiving_rec, plyr.receiving_yds, plyr.receiving_tds, plyr.receiving_lng
            #if plyr.stats:
                #print plyr.stats
            tocsv(plyr, w)

def tocsv(plyr, w):
    '''if plyr.receiving_rec:
        print checkstat(plyr, 'receiving_yds')
        w.writerow(row)'''
    if plyr.__dict__ is not None:
        print plyr.__dict__

def checkstat(player, stat):
    if stat in player.__dict__:
        return player.stats[stat]
    else:
        return 0

def getname(data, i):
    player = data[i]['player']
    head, sep, tail = player.partition(',')
    return head

def main():
    with open('players.json', 'r') as f:
        data = json.load(f)
    print len(data)
    for i in range(0,(len(data) + 1)):
        name = getname(data,i)
        getgamedata(name)
if __name__ == '__main__':
    main()
