def sumN(n):
    s = 0
    for i in range(1, n+1):
        s += i
    return s


def sum_n(n):
    return n * (n + 1) // 2


def mul2(n):
    s = 0
    for i in range(1, n+1):
        s += (i * i)
    return s


def mul21(n):
    return n * (n+1) * (2 * n + 1) // 6


def MaxN(n):
    l = len(n)
    max_n = n[0]
    for i in range(1, l):
        if n[i] > max_n:
            max_n = n[i]
    return max_n


def MinN(n):
    l = len(n)
    min_n = n[0]
    for i in range(1, l):
        if n[i] < min_n:
            min_n = n[i]
    return min_n


def countMaxN(n):
    c = 0
    l = len(n)
    for i in range(1, l):
        if n[i] > n[c]:
            c = i
    return c


def same_name(n):
    l = len(n)
    re = set()
    for i in range(0, l-1):
        for j in range(i+1, l):
            if n[i] == n[j]:
                re.add(n[i])
    return re


def add_name(n):
    l = len(n)
    re = set()
    for i in range(0, l-1):
        for j in range(i+1, l):
            re.add(n[i] + "-" + n[j])
    return re


def fact(n):
    f = 1
    for i in range(1, n+1):
        f = f * i
    return f


def fact2(n):
    if n <= 1:
        return 1
    return n * fact2(n-1)


def sumF(n):
    if n <= 1:
        return 1
    return n + sumF(n-1)


def MaxNF(n, l):
    if l <= 1:
        return 1
    max_n = MaxNF(n, l-1)
    if n[l-1] < max_n:
        return max_n
    else:
        return n[l-1]


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def fibo(n):
    if n <= 1:
        return n
    return fibo(n-2) + fibo(n-1)


print(sumN(100))
print(sum_n(100))
print(mul2(10))
print(mul21(10))
n = [17, 25, 35, 16, 98, 24, 67]
print(MaxN(n))
print(countMaxN(n))
print(MinN(n))
name = ['kim', 'tom', 'bob', 'sam', 'tom']
name2 = ['kim', 'tom', 'bob', 'sam']
print(same_name(name))
print(add_name(name2))
print(fact(10))
print(fact2(10))
print(sumF(10))
print(MaxNF(n, len(n)))
print(gcd(30, 50))
print(fibo(7))

stu_no = [39,14,67,105]
stu_name = ['kim', 'tom', 'bob', 'sam']


def find_stu(n):
    for i in range(len(stu_no)):
        if stu_no[i] == n:
            return stu_name[i]
    return "None"


print(find_stu(39))
print(find_stu(40))


sortList = [2,4,5,1,3]


def sel_sort(n):
    l = len(n)
    for i in range(0, l-1):
        min_id = i
        for j in range(i+1, l):
            if n[j] < n[min_id]:
                min_id = j
        n[i], n[min_id] = n[min_id], n[i]


sel_sort(sortList)
print(sortList)


def sel_sortU(n):
    l = len(n)
    for i in range(0, l-1):
        max_id = i
        for j in range(i+1, l):
            if n[j] > n[max_id]:
                max_id = j
        n[i], n[max_id] = n[max_id], n[i]


sortList = [2,4,5,1,3]
sel_sortU(sortList)
print(sortList)