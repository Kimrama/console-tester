result_palindrome = 0

def is_palindrome(sample) -> bool :
    return str(sample) == str(sample)[::-1]

def is_new_lagest_palindrome(result_palindrom, palindrome) -> bool :
    return palindrome > result_palindrome

def set_new_lagest_palindrome(palindrome) :
    global result_palindrome
    result_palindrome = palindrome

# 999 -> 100
for i in range(9999, 999, -1) :
    for j in range(i, 999, -1) :
        mul = i * j
        if is_palindrome(mul) and is_new_lagest_palindrome(result_palindrome, mul) : set_new_lagest_palindrome(mul)

print(result_palindrome)
        




