n = 1_000_000
a = 0
b = 1
next = b  
count = 1

while count <= n:
    count += 1
    a, b = b, next
    next = a + b
    print(count)
