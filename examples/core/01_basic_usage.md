# Basic CMX Usage
This demonstrates the core features of CMX.
```python
doc @ "## Simple Loop"
"Let's print numbers from 0 to 9:" | doc  # Postfix pipe syntax

for i in range(10):
    doc.print(i, end=" ")
```
## Simple Loop
Let's print numbers from 0 to 9:
```
0 1 2 3 4 5 6 7 8 9 
```
```python
doc @ "## Calculations"
"CMX captures both code and output:" | doc

result = sum(range(100))
doc.print(f"Sum of 0-99: {result}")

# More complex calculation
squares = [i**2 for i in range(10)]
doc.print(f"First 10 squares: {squares}")
```
## Calculations
CMX captures both code and output:
```
Sum of 0-99: 4950
First 10 squares: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```
