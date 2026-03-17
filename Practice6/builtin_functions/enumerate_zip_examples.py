names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"Студент: {name}, Балл: {score}")

for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")

print(f"Тип переменной names: {type(names)}")
