#1
nums = [1,2,3,4,5,6]
print(list(filter(lambda x: x%2==0, nums)))

#2
print(list(filter(lambda x: x>3, nums)))

#3
words = ["hi","hello","hey"]
print(list(filter(lambda x: len(x)>2, words)))

#4
nums = [-2,-1,0,1,2]
print(list(filter(lambda x: x<0, nums)))

#5
nums = [3,4,6,7,9]
print(list(filter(lambda x: x%3==0, nums)))
