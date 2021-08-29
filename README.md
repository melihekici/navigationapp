# Install Requirements
`pip install django`  
`pip install djangorestframework`  
`pip install django-cors-headers`  
`sudo apt install sqlite3`  

# Run Server
`python manage.py runserver`  

# Api
## Vehicles
Vehicle Model has two fields.  

### Vehicle Model
Vehicle  
id: Primary Key 
plate: CharField

### End Points

GET "/vehicles"
* Returns the list of vehicles.  
  
POST "/vehicles"  
body: {plate: str}  
* Adds a vehicle record to the database.  

PUT "/vehicles"  
body: {"id": vehicle id, "plate": str}  
* Update an existing vehicle.  

DELETE "/vehicle/{id}"  
* Removes the vehicle record from database.  
* When vehicle is removed, associated navigation records will be removed as well.  


## Navigation Records

### Navigation Model
NavigationRecord  
id: Primary Key  
vehicle: Foreign Key  
datetime: DateTimeField  
latitude: FloatField  
longitude: FloatField  
  
### End Points  
  
GET "/navigation"  
* Returns the list of navigation records.  
  
POST "/navigation"  
body: {"vehicle": vehicle id, "datetime": "2021-08-28 17:25:33", "latitude": float, "longitude":float}  
* Adds a navigation record to the database.  

PUT "/navigation"  
body: {"id": navigation record id, "vehicle": vehicle id, "datetime": "2021-08-28 17:25:33", "latitude": float, "longitude":float}  
* Update a navigation record.  
  
DELETE "/navigation/{id}"  
* Removes the navigation record from database.  
  
  
## Last Points Api
GET "/last-points/{n}"
* Returns the list of last points per vehicle that have sent navigation data in the last n hours.


# Suggestion to get Last Points Info more efficiently  
Assuming: NavigationRecord model takes too many queries, every query to this model is very costly in
terms of performance.  
  
Aim: A method to get data from database more efficiently.  
  
Suggestion:  
Instead of calculating the last 48 hours of records by filtering datetimes with query every time  
that the api is called, we can use caching.  
  
I have created a cache for the last points data for each hour interval except the last hour.  
  
When you send a request to the api for the last 48 hours (or last n hours) of records,  
first, the results for the 47 hours (or n-1 hours) will be get from the cache without querying the database.  
  
Then the query to get last points for the last hour is executed.  
I have decided not to cache the last one hour because there might be new records.  
  
I have decided to cache the queries with 1 hour intervals but this can be changed within the code quite easily.  
I also have prepared two end-points for you:  
* One to perform caching automatically.  
* Another for optimized data fetching.
  
  
## Last Points Api with cache  
I have wrote a function to make caching for you.  
First you need to send a GET request to the "/cache-dates" end-point.  
  
GET "/cache-dates"  
* This will create a caching which keeps query results for 1 hour intervals staring from smallest datetime record.   
  
After caching the dates is completed, you can use "/last-points-cache/{n}" end-point to get last points in n hours in optimized way.  
  
GET "/last-points-cache"
* This will return the same list with "last-points" end-point but this one uses the Suggested caching method before getting data from database.  
* This will only query the last hour from database and get other data from cache.    
* You need to run cache-dates before using this end-point.   
  
With a small set of data(i have posted around 1000 data to database) optimized query will cause ~7 ms execution time on database, while not optimized version causing ~60ms execution time.


  





  


