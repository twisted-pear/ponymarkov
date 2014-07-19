#!/usr/bin/env python2

import argparse
from os import makedirs, path
import re
from sys import stderr
import urllib
# beautifulsoup
from bs4 import BeautifulSoup

import provider

#TODO: Load urls from file.
urls = {
    '1x1': 'http://mlp.wikia.com/wiki/Transcripts/Friendship_is_Magic,_part_1',
    '1x2': 'http://mlp.wikia.com/wiki/Transcripts/Friendship_is_Magic,_part_2',
    '1x3': 'http://mlp.wikia.com/wiki/Transcripts/The_Ticket_Master',
    '1x4': 'http://mlp.wikia.com/wiki/Transcripts/Applebuck_Season',
    '1x5': 'http://mlp.wikia.com/wiki/Transcripts/Griffon_the_Brush_Off',
    '1x6': 'http://mlp.wikia.com/wiki/Transcripts/Boast_Busters',
    '1x7': 'http://mlp.wikia.com/wiki/Transcripts/Dragonshy',
    '1x8': 'http://mlp.wikia.com/wiki/Transcripts/Look_Before_You_Sleep',
    '1x9': 'http://mlp.wikia.com/wiki/Transcripts/Bridle_Gossip',
    '1x10': 'http://mlp.wikia.com/wiki/Transcripts/Swarm_of_the_Century',
    '1x11': 'http://mlp.wikia.com/wiki/Transcripts/Winter_Wrap_Up',
    '1x12': 'http://mlp.wikia.com/wiki/Transcripts/Call_of_the_Cutie',
    '1x13': 'http://mlp.wikia.com/wiki/Transcripts/Fall_Weather_Friends',
    '1x14': 'http://mlp.wikia.com/wiki/Transcripts/Suited_For_Success',
    '1x15': 'http://mlp.wikia.com/wiki/Transcripts/Feeling_Pinkie_Keen',
    '1x16': 'http://mlp.wikia.com/wiki/Transcripts/Sonic_Rainboom',
    '1x17': 'http://mlp.wikia.com/wiki/Transcripts/Stare_Master',
    '1x18': 'http://mlp.wikia.com/wiki/Transcripts/The_Show_Stoppers',
    '1x19': 'http://mlp.wikia.com/wiki/Transcripts/A_Dog_and_Pony_Show',
    '1x20': 'http://mlp.wikia.com/wiki/Transcripts/Green_Isn%27t_Your_Color',
    '1x21': 'http://mlp.wikia.com/wiki/Transcripts/Over_a_Barrel',
    '1x22': 'http://mlp.wikia.com/wiki/Transcripts/A_Bird_in_the_Hoof',
    '1x23': 'http://mlp.wikia.com/wiki/Transcripts/The_Cutie_Mark_Chronicles',
    '1x24': 'http://mlp.wikia.com/wiki/Transcripts/Owl%27s_Well_That_Ends_Well',
    '1x25': 'http://mlp.wikia.com/wiki/Transcripts/Party_of_One',
    '1x26': 'http://mlp.wikia.com/wiki/Transcripts/The_Best_Night_Ever',
    '2x1': 'http://mlp.wikia.com/wiki/Transcripts/The_Return_of_Harmony_Part_1',
    '2x2': 'http://mlp.wikia.com/wiki/Transcripts/The_Return_of_Harmony_Part_2',
    '2x3': 'http://mlp.wikia.com/wiki/Transcripts/Lesson_Zero',
    '2x4': 'http://mlp.wikia.com/wiki/Transcripts/Luna_Eclipsed',
    '2x5': 'http://mlp.wikia.com/wiki/Transcripts/Sisterhooves_Social',
    '2x6': 'http://mlp.wikia.com/wiki/Transcripts/The_Cutie_Pox',
    '2x7': 'http://mlp.wikia.com/wiki/Transcripts/May_the_Best_Pet_Win!',
    '2x8': 'http://mlp.wikia.com/wiki/Transcripts/The_Mysterious_Mare_Do_Well',
    '2x9': 'http://mlp.wikia.com/wiki/Transcripts/Sweet_and_Elite',
    '2x10': 'http://mlp.wikia.com/wiki/Transcripts/Secret_of_My_Excess',
    '2x11': 'http://mlp.wikia.com/wiki/Transcripts/Hearth%27s_Warming_Eve',
    '2x12': 'http://mlp.wikia.com/wiki/Transcripts/Family_Appreciation_Day',
    '2x13': 'http://mlp.wikia.com/wiki/Transcripts/Baby_Cakes',
    '2x14': 'http://mlp.wikia.com/wiki/Transcripts/The_Last_Roundup',
    '2x15': 'http://mlp.wikia.com/wiki/Transcripts/The_Super_Speedy_Cider_Squeezy_6000',
    '2x16': 'http://mlp.wikia.com/wiki/Transcripts/Read_It_and_Weep',
    '2x17': 'http://mlp.wikia.com/wiki/Transcripts/Hearts_and_Hooves_Day',
    '2x18': 'http://mlp.wikia.com/wiki/Transcripts/A_Friend_in_Deed',
    '2x19': 'http://mlp.wikia.com/wiki/Transcripts/Putting_Your_Hoof_Down',
    '2x20': 'http://mlp.wikia.com/wiki/Transcripts/It%27s_About_Time',
    '2x21': 'http://mlp.wikia.com/wiki/Transcripts/Dragon_Quest',
    '2x22': 'http://mlp.wikia.com/wiki/Transcripts/Hurricane_Fluttershy',
    '2x23': 'http://mlp.wikia.com/wiki/Transcripts/Ponyville_Confidential',
    '2x24': 'http://mlp.wikia.com/wiki/Transcripts/MMMystery_on_the_Friendship_Express',
    '2x25': 'http://mlp.wikia.com/wiki/Transcripts/A_Canterlot_Wedding_-_Part_1',
    '2x26': 'http://mlp.wikia.com/wiki/Transcripts/A_Canterlot_Wedding_-_Part_2',
    '3x1': 'http://mlp.wikia.com/wiki/Transcripts/The_Crystal_Empire_-_Part_1',
    '3x2': 'http://mlp.wikia.com/wiki/Transcripts/The_Crystal_Empire_-_Part_2',
    '3x3': 'http://mlp.wikia.com/wiki/Transcripts/Too_Many_Pinkie_Pies',
    '3x4': 'http://mlp.wikia.com/wiki/Transcripts/One_Bad_Apple',
    '3x5': 'http://mlp.wikia.com/wiki/Transcripts/Magic_Duel',
    '3x6': 'http://mlp.wikia.com/wiki/Transcripts/Sleepless_in_Ponyville',
    '3x7': 'http://mlp.wikia.com/wiki/Transcripts/Wonderbolts_Academy',
    '3x8': 'http://mlp.wikia.com/wiki/Transcripts/Apple_Family_Reunion',
    '3x9': 'http://mlp.wikia.com/wiki/Transcripts/Spike_at_Your_Service',
    '3x10': 'http://mlp.wikia.com/wiki/Transcripts/Keep_Calm_and_Flutter_On',
    '3x11': 'http://mlp.wikia.com/wiki/Transcripts/Just_for_Sidekicks',
    '3x12': 'http://mlp.wikia.com/wiki/Transcripts/Games_Ponies_Play',
    '3x13': 'http://mlp.wikia.com/wiki/Transcripts/Magical_Mystery_Cure',
    '4x1': 'http://mlp.wikia.com/wiki/Transcripts/Princess_Twilight_Sparkle_-_Part_1',
    '4x2': 'http://mlp.wikia.com/wiki/Transcripts/Princess_Twilight_Sparkle_-_Part_2',
    '4x3': 'http://mlp.wikia.com/wiki/Transcripts/Castle_Mane-ia',
    '4x4': 'http://mlp.wikia.com/wiki/Transcripts/Daring_Don%27t',
    '4x5': 'http://mlp.wikia.com/wiki/Transcripts/Flight_to_the_Finish',
    '4x6': 'http://mlp.wikia.com/wiki/Transcripts/Power_Ponies',
    '4x7': 'http://mlp.wikia.com/wiki/Transcripts/Bats!',
    '4x8': 'http://mlp.wikia.com/wiki/Transcripts/Rarity_Takes_Manehattan',
    '4x9': 'http://mlp.wikia.com/wiki/Transcripts/Pinkie_Apple_Pie',
    '4x10': 'http://mlp.wikia.com/wiki/Transcripts/Rainbow_Falls',
    '4x11': 'http://mlp.wikia.com/wiki/Transcripts/Three%27s_A_Crowd',
    '4x12': 'http://mlp.wikia.com/wiki/Transcripts/Pinkie_Pride',
    '4x13': 'http://mlp.wikia.com/wiki/Transcripts/Simple_Ways',
    '4x14': 'http://mlp.wikia.com/wiki/Transcripts/Filli_Vanilli',
    '4x15': 'http://mlp.wikia.com/wiki/Transcripts/Twilight_Time',
    '4x16': 'http://mlp.wikia.com/wiki/Transcripts/It_Ain%27t_Easy_Being_Breezies',
    '4x17': 'http://mlp.wikia.com/wiki/Transcripts/Somepony_to_Watch_Over_Me',
    '4x18': 'http://mlp.wikia.com/wiki/Transcripts/Maud_Pie',
    '4x19': 'http://mlp.wikia.com/wiki/Transcripts/For_Whom_the_Sweetie_Belle_Toils',
    '4x20': 'http://mlp.wikia.com/wiki/Transcripts/Leap_of_Faith',
    '4x21': 'http://mlp.wikia.com/wiki/Transcripts/Testing_Testing_1,_2,_3',
    '4x22': 'http://mlp.wikia.com/wiki/Transcripts/Trade_Ya!',
    '4x23': 'http://mlp.wikia.com/wiki/Transcripts/Inspiration_Manifestation',
    '4x24': 'http://mlp.wikia.com/wiki/Transcripts/Equestria_Games',
    '4x25': 'http://mlp.wikia.com/wiki/Transcripts/Twilight%27s_Kingdom_-_Part_1',
    '4x26': 'http://mlp.wikia.com/wiki/Transcripts/Twilight%27s_Kingdom_-_Part_2',
    }


class MLPWikiaProvider(provider.ProviderI):

    def __init__(self, characters=None, episodes=None):
        self.CHAR = characters[0]
        self.transcripts = []
        self._cache_dir = cache_dir = (
            path.expanduser('~/.providers/mlp_wikia/'))
        if not path.exists(cache_dir):
            try:
                makedirs(cache_dir)
            except Exception as e:
                stderr.write("Failed to create cache: %s" % e)
                exit(1)
        if not episodes:
            for key, url in urls.iteritems():
                self.transcripts.append(self.fetch_transcript(url))
        else:
            for episode in episodes:
                self.transcripts.append(self.fetch_transcript(urls[episode]))

    def fetch_transcript(self, url):
        cache_dir=self._cache_dir
        title = re.sub(
            r'http\:\/\/mlp\.wikia\.com\/wiki\/Transcripts\/', '', url)
        if not path.exists(cache_dir+'/'+title):
            try:
                html_file = urllib.urlretrieve(url, cache_dir+'/'+title)
            except Exception as e:
                stderr.write("Failed to fetch transcript: %s" % e)
                exit(1)
        else:
            html_file = cache_dir+'/'+title, file
        return html_file

    def get_lines(self):
        con = []
        for transcript in self.transcripts:
            try:
                with open(transcript[0], 'r') as f:
                    soup = BeautifulSoup(''.join(f))
            except Exception as e:
                stderr.write("Failed to read transcript: %s" % e)
                exit(1)

            for dd_tag in soup.findAll('dd'):
                re_pony = r'<b>[a-zA-Z ]*%s[a-zA-Z ]*</b>' % self.CHAR
                if re.match(re_pony, unicode(dd_tag.contents[0])):
                    contents = "".join(unicode(item) for item in
                        dd_tag.contents[1:])
                    contents = re.sub(r'(^.*: ?)*(<\/?[a-z]+>)*', '', contents)
                    con.append(contents.encode('utf8'))
        return con


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--character', type=str, nargs=1, help='name of character',
        required=True)
    args = parser.parse_args()
    mlp = MLPWikiaProvider(args.character)
    text = mlp.read_transcript()
    try:
        with open('ts_out', 'w') as ofile:
            ofile.write(text)
    except Exception as e:
        stderr.write("Failed to write to file: %s" % e)
        exit(1)
    ofile.close()
