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
[Solution](/juan/point_c/)

