s = "I like python programming language"
s = list(s)
res = ""

itr = 0
b = itr + 1
while itr < len(s):
    if s[itr] == 'like':
        res += s[itr]
        while s[b] != 'language' or b < len(s):
            res += s[b]
            b += 1
    itr += 1
print(res)



