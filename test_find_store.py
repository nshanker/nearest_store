import unittest
import find_store

class TestFindStore(unittest.TestCase):
    ''' A very basic test suite '''
    def setUp(self):
        self.s = find_store.StoreSearch()

    def test_address1(self):
        a = '820 W McKinley Ave, Sunnyvale, CA'
        result = self.s.find_closest_store(a)
        # Of the stores given in the csv, this turns out to be the closest to the address provided.
        self.assertEquals('298 W McKinley Ave,Sunnyvale,CA', result['address'])

    def test_zip1(self):
        z = '95050'
        result = self.s.find_closest_store(z)
        self.assertEquals('95 Holger Way,San Jose,CA', result['address'])

    def test_km(self):
        a = '820 W McKinley Ave, Sunnyvale, CA'
        result = self.s.find_closest_store(a, units='km')
        self.assertEquals('0.650 km', result['distance'])

    def test_miles(self):
        a = '820 W McKinley Ave, Sunnyvale, CA'
        result = self.s.find_closest_store(a)
        self.assertEquals('0.404 mi', result['distance'])

if __name__ == '__main__':
    unittest.main()
        
