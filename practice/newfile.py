import lambdas

print(lambdas.getx())

storedfunction = None

# parenthesis run the function and can give it input
storedfunction = lambdas.xman
storedvalue = lambdas.xman()

lambdas.x += 1

print(storedfunction())  # "1" we are evaluating at real time
print(storedvalue)  # "0" stored value
