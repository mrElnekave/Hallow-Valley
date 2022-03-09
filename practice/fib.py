# 1, 1, 2, 3, 5, 8, 13, …)


# recursion:
# when you call a function inside itself

def fib(a, b):
    # infinite loop
    return [a] + fib(b, a+b)

# [1] + [1] + [2] + [3] + fib(5, 8)...
# fib(1, 1)

def fib(a, b, times_left=10):
    if times_left != 0:
        return [a] + fib(b, a+b, times_left-1)
    else:
        # at 0
        return []

print(fib(1, 1))