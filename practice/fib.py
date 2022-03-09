# 1, 1, 2, 3, 5, 8, 13, …)


# recursion:
# when you call a function inside itself

def fib(a, b):
    # infinite loop
    return [a] + fib(b, a+b)

# [1] + [1] + [2] + [3] + fib(5, 8)...
# fib(1, 1)

# Yuan's code
def fibonacci(a,b,level,listThing): 
    if level > 0: 
        print(a) 
        listThing.append(a)
        fibonacci(b,a+b,level-1,listThing)
    else: 
        print(listThing)
def ex13(): 
    outputList = []
    number = int(input("Enter a number: "))
    fibonacci(1,1,number,outputList)

# Max's code
def fib(a, b, times_left=10):
    if times_left != 0:
        return [a] + fib(b, a+b, times_left-1)
    else:
        # at 0
        return []

print(fib(1, 1))

