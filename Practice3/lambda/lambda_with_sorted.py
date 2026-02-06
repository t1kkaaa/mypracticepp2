#1
nums = [5,2,9,1]
print(sorted(nums))

#2
print(sorted(nums, reverse=True))

#3
words = ["apple","hi","banana"]
print(sorted(words, key=lambda x: len(x)))

#4
print(sorted(words, key=lambda x: x[0]))

#5
pairs = [(1,2),(3,1),(5,0)]
print(sorted(pairs, key=lambda x: x[1]))
