README:
======

This program reads a csv file of store-locations and finds the closest
store to a query address.

See problem statement here: https://github.com/groveco/code-challenge

Finding the nearest store to a given address (or latitude/longitude) is
a nearest-neighbor search problem. There are several approaches. One could 
check the "distance" of the query address Q from each store in our CSV
file and return the minimum. This would be an O(N) algorithm where N is the 
number of stores in our CSV file.  However, the algorithm would take 
linear time for *every query*.

Other approaches could be to construct the Voronoi diagram 
(or Delaunay Triangulation) and find the Voronoi cell corresponding to the 
query address.  Alternately, we map every 3D point in space to a 2D UTM point 
on a plane and then use a 2-d search tree. We could also use a POST GIS 
database which is much more powerful and can answer any kind of query.

The approach used here is to simply employ a space-filling curve called 
the Morton curve. The curve transforms any (latitude, longitude) to a single 
number and has the interesting property that if two points in space are close 
to each other, their relative closeness is maintained in the associated 1-D 
points that make up the Morton curve as well. This means that we store these 
1-D numbers in a BST (we could use a Red Black Search Tree too for balance, 
but I kept it simple using just a regular Binary Search Tree) and searching
for a store amounts to just searching for a number in a BST. We then return 
the minimum of the predecessor and successor in the tree. There are many kinds 
of space-filling curves and they'll all do the job. Popular ones are 
Z-order curve, Hilbert curve, etc. 

Some nice videos on YouTube about Space-filling curves: 
https://www.youtube.com/watch?v=XLSm-0Moy5o

To obtain the latitude/longitude of the query address or zipcode, 
I use Google's Geocoding API.

To keep 'crow-flying-distance' calculation somewhat accurate, I use the 
haversine formula (found this on stackoverflow.com) which provides a very good 
approximation of geodetic distance -- we don't want Euclidean distance since 
the curvature of the earth might skew the calculation a bit even though all 
our stores are inside the US. If this distance were compared with Google or 
Bing's result however, it won't match exactly since Google displays walking or 
driving distance and not 'crow-flying' distance.

The running time of the algorithm is O(Nlog(N)) and while it might seem worse 
than the naive O(N) algorithm described above, it is actually O(log(N)) in 
practice because the tree needs to be constructed just once. The time to 
construct the tree is O(Nlog(N)) but all subsequent queries can be answered in 
O(log(N)) time. To keep things simple, I've not used a database to persist 
the tree to disk, so my program will take O(Nlog(N)) time since it constructs 
the tree every time for each query. It is however not too difficult to persist 
the tree to disk using some Graph DB.

To run the program, create a virtualenv environment and execute the following steps:

$ git clone https://github.com/nshanker/nearest_store.git
Cloning into 'nearest_store'...
remote: Counting objects: 16, done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 16 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (16/16), done.

$ virtualenv nearest_store
New python executable in /Users/shanker/testing/nearest_store/bin/python
Installing setuptools, pip, wheel...done.

$ cd nearest_store
$ source bin/activate

$ pip install docopt pymorton
Collecting docopt
Collecting pymorton
  Using cached https://files.pythonhosted.org/packages/c6/8d/906ba6d4266d7696547b8b70e08423975243c7339fe1ccf4bdbc42478394/pymorton-1.0.5-py2.py3-none-any.whl
Installing collected packages: docopt, pymorton
Successfully installed docopt-0.6.2 pymorton-1.0.5

$ python find_store.py 

Usage:
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

To run tests:

$ python test_find_store.py
....
----------------------------------------------------------------------
Ran 4 tests in 1.790s

OK

Some trial runs:

$ python find_store.py --address="45 Rockefeller Plaza, New York, NY"
The closest store is located at:

Address: 8801 Queens Blvd,Elmhurst,NY
City: Elmhurst
County: Queens County

Distance: 5.652 mi
Lat: 40.7353074
Lon: -73.8747611
State: NY
Store: Queens Place
Zip: 11373-4449

$ python find_store.py --address="Peach Springs, AZ"
The closest store is located at:

Address: 275 S River Rd,Saint George,UT
City: Saint George
County: Washington County

Distance: 108.928 mi
Lat: 37.1034044
Lon: -113.5538397
State: UT
Store: St George
Zip: 84790-2116


The second query shows the closest store in the neighboring state! The only
store in Arizona in our CSV file is about 3 hours driving distance from 
Peach Springs (Grand Canyon). The store in Utah is about 4 hours but the drive
is quite roundabout. The crow-flying distance to the Utah store seems
smaller.

