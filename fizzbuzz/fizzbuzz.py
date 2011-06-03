#!/usr/bin/env python2

print '\n'.join(['%i ' % i * (not (j or k)) + 'Fizz' * j + 'Buzz' * k
                for (i, j, k)
                in [(x, x % 3 == 0, x % 5 == 0) for x in range(1, 101)]])
