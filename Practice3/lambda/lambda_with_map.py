#1
nums = [1,2,3]
print(list(map(lambda x: x*2, nums)))

#2
nums = [1,2,3]
print(list(map(lambda x: str(x), nums)))

#3
nums = [2,3,4]
print(list(map(lambda x: x**2, nums)))

#4
def add_one(x):
    return x+1
print(list(map(add_one, nums)))

#5
nums = [10,20,30]
print(list(map(lambda x,y: x+y, nums, [1,2,3])))
