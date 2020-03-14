import random

# Variable set 1

# Set up variables
y0 = 50
x0 = 50

# Random walk one step
if random.random() < 0.5:
    y0 += 1
else:
    y0 -= 1

if random.random() < 0.5:
    x0 += 1
else:
    x0 -= 1

# Random walk one step
if random.random() < 0.5:
    y0 += 1
else:
    y0 -= 1

if random.random() < 0.5:
    x0 += 1
else:
    x0 -= 1

print(y0, x0)


# Variable set 2

# Set up variables
y1 = 50
x1 = 50

# Random walk one step
if random.random() < 0.5:
    y1 += 1
else:
    y1 -= 1

if random.random() < 0.5:
    x1 += 1
else:
    x1 -= 1

# Random walk one step
if random.random() < 0.5:
    y1 += 1
else:
    y1 -= 1

if random.random() < 0.5:
    x1 += 1
else:
    x1 -= 1

print(y1, x1)


distance = ((y1 - y0)**2 + (x1 - x0)**2 )**0.5

print(distance)
