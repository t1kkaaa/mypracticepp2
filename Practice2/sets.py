#1
thisset = {"apple", "banana", "cherry", "apple"}
print(thisset)

#2
thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)

#3
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
print(thisset)

#4
thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)
print(thisset)

#5
thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]
thisset.update(mylist)
print(thisset)

#6
thisset = {"apple", "banana", "cherry"}
thisset.remove("banana")
print(thisset)

#7
thisset = {"apple", "banana", "cherry"}
thisset.discard("banana")
print(thisset)

#8
thisset = {"apple", "banana", "cherry"}
del thisset
print(thisset)

#9
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = set1.union(set2)  #set3 = set1 | set2
print(set3)

#10
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1.intersection(set2)
print(set3)

#11
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set1.intersection_update(set2)

print(set1)

#12
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1.symmetric_difference(set2)

print(set3)

#13
x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))

