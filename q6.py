inp = list(map(int, input().split(" ")))

a = max(inp)
inp.remove(a)
b = max(inp)

print(a*b)