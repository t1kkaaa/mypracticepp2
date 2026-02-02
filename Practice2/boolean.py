#1
print(10 > 9)
print(10 == 9)
print(10 < 9)

#2
print(bool("Hello"))
print(bool(15))

#3
x = "Hello"
y = 15
print(bool(x))
print(bool(y))

#4
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#5
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))
