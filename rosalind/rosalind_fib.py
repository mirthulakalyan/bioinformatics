# Rosalind Problem 3: Fibonacci Rabbits

def fibonacci_rabbits(n, k):
    if n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        rabbits = [0] * (n + 1)
        rabbits[1] = 1
        rabbits[2] = 1
        for month in range(3, n + 1):
            rabbits[month] = rabbits[month - 1] + k * rabbits[month - 2]
        return rabbits[n]   