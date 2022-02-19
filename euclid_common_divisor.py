# Euclid's greatest common divisor algorithm

# Ask user to input to integers
n = int(input("First integer"))
# Test for input being zero
while (n == 0):
    n= int(input("First integer - Do Not enter zero"))
else:
  m= int(input("Second integer"))
  while (m == 0):
    m = int(input("Second integer - Do Not enter zero"))
  else:
# When both n and m input by user is not zero, then continue                 
    while (n != m):
      if (n > m):
        n=n-m
      else: 
        m=m-n
        
print "The greatest common divisor is",n
