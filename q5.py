inp = list(map(int, input().split(" ")))
print(inp)

inp.sort()

for i in range(len(inp)-1):
    if inp[i] == 0:
        pass
    else:
        first = inp.pop(i)
        break

print(str(first) + "".join(list(map(str, inp))))