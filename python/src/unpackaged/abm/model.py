import random

# Point 0

# Set up variables
y0 = random.randint(0, 99)
x0 = random.randint(0, 99)

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


# Point 1

# Set up variables
y1 = random.randint(0, 99)
x1 = random.randint(0, 99)

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


# Calculate Pythagorian distance between point 0 and point 1
distance = ((y1 - y0)**2 + (x1 - x0)**2 )**0.5

print(distance)
