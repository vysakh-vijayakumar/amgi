import requests
import json
from datetime import date, timedelta, datetime
import requests
import argparse
from _datetime import date
import csv

class Playlist:
    # playlist_list = []

    def __init__(self, server, token, feed_id):
        self.server = server
        self.token = token
        self.feed_id = feed_id
        
    def get_playlists_by_date(self, date):    
        query_params = {'feed_id': self.feed_id,'start_date':date, 'end_date':date, 'state':'published',
        'ptype':'normal', 'token': self.token }
        r = requests.get(self.server + '/v1/api/playlist.json',params=query_params)
        return r.json()

    def get_playlist_items(self, id):
        query_params = {'feed_id': self.feed_id, 'token': self.token }
        r = requests.get(self.server + '/v1/api/playlist/'+str(id)+'.json', query_params)
        return r.json()
        print("r.json : "+r.json)

    def get_latest_playlist(self, playlists):
        for playlist in playlists['playlists']:
            if playlist['status'] == 'published':
                print("id: "+str(playlist['id']))
                return playlist['id']
        return None

    def playlist_items_by_type(self, playlist_items, item_types):
        playlist_list = []
        for item in playlist_items['items']:
            if item['type'] == 'primary' and item['sub_type'] in item_types:
                day, time = self.get_formatted_datetime(item['start_time'])
                playlist_list.append({
                    'asset_id' : item['asset_id'],
                    'title' : item['title'],
                    'start_day' : day,
                    'start_time' : time
                })
        
        return playlist_list

    def get_formatted_datetime(self, datetimetext):
        dt = datetime.strptime(datetimetext, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt.strftime("%d %b %Y"), dt.strftime("%H:%M:%S")

    def iterate_date(self, date_list):
        data_bean = []
        for day in date_list:
            date = day
            playlists = self.get_playlists_by_date(date)
            latest_playlist_id = self.get_latest_playlist(playlists)
            playlist_items = self.get_playlist_items(latest_playlist_id)
            playlist_list = self.playlist_items_by_type(playlist_items, ['media'])
            data_bean.extend(playlist_list)
        return data_bean

def get_dates(input_day, number_of_day):
    start_date = input_day - timedelta(days = number_of_day)
    list_of_dates = []
    delta = input_day - start_date
    for i in range(delta.days + 1):
        day = start_date + timedelta(days = i)
        list_of_dates.append(day)

   # print(list_of_dates)
    return list_of_dates

def create_csv(data, filepath):
    with open(filepath, 'w') as output_file:
        keys = data[0].keys()
        writer = csv.DictWriter(output_file, keys)
        writer.writeheader()
        last_asset_id = ""
        for row in data:
            if row["asset_id"] != last_asset_id:
                writer.writerow(row)
                last_asset_id = row["asset_id"]

def load_json(filename):
    with open(filename) as file:
        config_data = json.load(file)
    return config_data

def main():
    json_path = "config.json"
    config_data = load_json(json_path)
    server = config_data['server']
    token = config_data['token']
    feed_id = config_data['feed_id']


    ap = argparse.ArgumentParser()

    ap.add_argument("-d", "--date", required = False, help ="date from, DD-MM-YYYY")
    ap.add_argument("-n", "--number_of_days", required = False, help="number of days from date")
    ap.add_argument("-o", "--output", required = False, help="output file name")
    args = vars(ap.parse_args())

    if args['date'] == None:
        start_day = date.today()
    else:
        start_day = datetime.strptime(args['date'], "%d-%m-%Y")

    if args['number_of_days'] == None:
        no_days = 0
    else:
        no_days = int(args['number_of_days']) - 1
    
    if args['output'] == None:
        filepath = "playlist.csv"
    else:
        filepath = args['output']


    #server = 'https://curiosity.amagi.tv'
    #token = '2sPor9AoLCpbTosYVSuJ'
    #feed_id = '1'

    playlist = Playlist(server, token, feed_id)

    date_list = get_dates(start_day, no_days)
    final_data = playlist.iterate_date(date_list)

    create_csv(final_data, filepath)
    print(final_data)

if __name__ == "__main__":
    main()

