# Juan Salamanca - Recruiting Test


## Question A
Your goal for this question is to write a program that accepts two lines (x1,x2) and (x3,x4) on the x-axis and returns whether they overlap. As an example, (1,5) and (2,6) overlaps but not (1,5) and (6,8).

[Solution](/juan/point_a.py)

[Tests](/test/tests_for_point_a.py)

#### Example

```python3

from juan.point_a import check_overlap
a = (3, 8)
b = (6, 11)
output = check_overlap(a, b)
print(output)

```

#### Developer Observations
1. For every input vector `a` or `b`, it does not matter if `a[0]` is greater or less than `a[1]`


## Question B
The goal of this question is to write a software library that accepts 2 version string as input and returns whether one is greater than, equal, or less than the other. As an example: “1.2” is greater than “1.1”. Please provide all test cases you could think of.

[Solution](/juan/point_b.py)

[Tests](/test/tests_for_point_b.py)


#### Example

```python3

from juan.point_b import check_version
v1 = '10.1.3.0.0.0'
v2 = '10.1.3'
output = check_version(v1, v2)
print(output)

```


#### Developer Observations
`check_version` supports alpha and beta versions with literals `a` or `b` at the end of every version string.

For example `'10.1.3a'` is a valid version code



## Question C
We want to optimize every bits of software we write. Your goal is to write a new library that can be integrated to our stack. Dealing with network issues everyday, latency is our biggest problem. Thus, your challenge is to write a new Geo Distributed LRU (Least Recently Used) cache with time expiration. This library will be used extensively by many of our services so it needs to meet the following criteria:
1 - Simplicity. Integration needs to be dead simple.
2 - Resilient to network failures or crashes.
3 - Near real time replication of data across Geolocation. Writes need to be in real time. 4 - Data consistency across regions
5 - Locality of reference, data should almost always be available from the closest region 6 - Flexible Schema
7 - Cache can expire

[Solution](/juan/point_c/)

[Tests](/test/tests_for_point_c.py)

#### Examples

a. Get the nearest region cache end-point which distance is less than 600 km from a geo-location (lat, long)
```bash
curl -X GET "http://localhost:8080/v1/routes?lat=38.561387&long=-121.498287&radius=600&unit=km"
```
response must come in json format with details such as region name, lat, long and url to access


b. Add a new cache region end-point to the routes micro-service
```bash
curl -H "Content-Type: application/json" -d '{"region": "AU", "lat": "-37.810745", "long": "144.965207", "url": "http://au.mycompany.com/v1/caches"}' -X POST "http://localhost:8080/v1/routes"
```

c. Put a object to a cache region with key `juan` and content body `{"name": "juan", "id": "1000"}`
```bash
curl -H "Content-Type: application/json" -H "X-Key: juan" -d '{"name": "juan", "id": "1000"}' -X POST "http://localhost:8181/v1/caches"
```
If the key already exists, the object will be overwritten with the new content.


d. Retrieve the object with key `juan` from a given region cache end-point
```bash
curl  -X GET "http://localhost:8181/v1/caches/juan"
```
The retrieved object must come with the same content-type as it was posted originally

#### Developer Observations

