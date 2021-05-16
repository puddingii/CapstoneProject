li = []
with open("C:/Users/BBAEK/Desktop/LFW_pairs.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        li.append(line)
print(li[17247]) #2명있을때
a = li[:17247]
b = li[17247:]
with open("C:/Users/BBAEK/Desktop/LFW_pairs_re.txt", "w") as f:
    i = 0
    j = 0
    chk = True
    while True:
        if j == len(b):
            break
        if chk:
            f.write(a[i])
            i += 1
            if i % 300 == 0:
                chk = False
        else:
            f.write(b[j])
            j += 1
            if j % 300 == 0:
                chk = True