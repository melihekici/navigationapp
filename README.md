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
that the api is called, we can create day ids (Ex:incrementing day number starting from first  
records day) and cache(or save to a db) the id of the first navigation record for that day.  
  
When you send a request to the api for the last 48 hours (or last n hours) of records,  
first, the day number for the 48 hours (or n hours) earlier will be calculated   
(lets say it returned day 410) before querying the database.  

Then using the time stamp(410) we will get the id of the first record for that day from the cache (or db).  
After, we will filter the navigation records that has id greater than returned id from the cache.  
(Assuming later records have greater id(primary key) value).  
  
If you have asked for last 48 hours of records, this would return from last 48 hours up to last 72 hours of records. 
Then we can filter the records inside api function and return last 48 hours of records.    
  
I think slicing data from database using id field (which is the primary key) would be much faster and cheaper  
than filtering a whole data by comparison of date time with now.  
  

## Last Points Api with cache  
I have wrote a function to make caching for you.  
First you need to send get request to the "/cache-dates" end-point.  
  
GET "/cache-dates"  
* This will create a caching which shows a first navigation record for each day.  
  
After caching the dates is completed, you can use "/last-points-cache/{n}" end-point to get last points in optimized way.  
  
GET "/last-points-cache"
* This will return the same list with "last-points" end-point but this one uses the Suggested caching method before getting data from database.  
* This will filter the database on primary key, not on datetime.  
* You need to run cache-dates before using this end-point.


  





  


