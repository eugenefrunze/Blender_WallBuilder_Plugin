class Some():
    a = 5

b = []



for el in b:
    try:
        a = el.a
    except IndexError:
        print('there is no objects in the list')
    else:
        print(a)

print(b[0].a)