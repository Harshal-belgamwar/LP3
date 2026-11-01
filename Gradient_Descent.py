
def derivative(x):
    return 2*(x+3)

learning_rate=0.1
x=2

for i in range(100):
    x= x- learning_rate*derivative(x)

print("local minima:",round(x,4))
print("minimum value",round((x+3)**2,4))

