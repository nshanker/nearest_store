#!/usr/bin/python
'''
Find Store
  find_store will locate the nearest store (as the vrow flies) from
  store-locations.csv, print the matching store address, as well as
  the distance to that store.

Usage:
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>          Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address=<address>  Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)      Display units in miles or kilometers [default: mi]
  --output=(text|json) Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
'''

import utils, bst, docopt, re, json

class StoreSearch:
    def __init__(self):
        self.t = bst.BST()
        self.read_store_locations("store-locations.csv")

    def data(self, line):
        ''' 
        A sample line from store-locations.csv looks like this:
        Crystal,SWC Broadway & Bass Lake Rd,5537 W Broadway Ave,Crystal,MN,55428-3507,45.0521539,-93.364854,Hennepin County
        '''

        row = {}
        x = re.split(r',(?! )', line)

        row['store']   = x[0]
        row['city']    = x[3]
        row['state']   = x[4]
        row['zip']     = x[5]
        row['lat']     = x[6]
        row['lon']     = x[7]
        row['county']  = x[8]
        row['address'] = x[2] + ',' + x[3] + ',' + x[4] 

        return row

    def read_store_locations(self, file):
        with open(file, 'r') as f:
            next(f)
            for line in f:
                if line.startswith('# '):
                    continue
                row = self.data(line)
                address = row['address']
                store_id = utils.convert_to_1D({ 'lat' : row['lat'], 'lon' : row['lon'] })
                self.t.put(store_id, row)

    def find_closest_store(self, address, units='mi'):
        store = utils.convert_to_1D({ 'address' : address })

        (lo, hi) = self.t.closest(store['id'])

        if lo:
            dist1 = utils.haversine(store['lat'], store['lon'], lo['lat'], lo['lon'], units)
        else:
            dist1 = float('inf')

        if hi:
            dist2 = utils.haversine(store['lat'], store['lon'], hi['lat'], hi['lon'], units)
        else:
            dist2 = float('inf')


        if dist1 < dist2:
            lo['distance'] = "%0.3f %s" % (dist1, units)
            return lo
        else:
            hi['distance'] = "%0.3f %s" % (dist2, units)
            return hi


if __name__ == '__main__':

    args = docopt.docopt(__doc__,version=1.0)
    s = StoreSearch()

    if args['--address']:
        ans = s.find_closest_store(args['--address'], args['--units'])
    else:
        ans = s.find_closest_store(args['--zip'], args['--units'])

    if ans is None:
        print('No store found!')
    else:
        if args['--output'] == 'json':
            with open("store.json", 'w') as f:
                json.dump(ans, f)
        else:
            print("The closest store is located at:\n")
            for k in sorted(ans):
                print("%s: %s" % (k.title(), ans[k]))
