# woodman - Google CTF
*Solved by @r00ta and @dariosharp

This crypto challenge had a quite easy request

![image](intro.png)

So we had to choose the right number for 100 times consecutively. If we made a mistake, we had to repeat this process from the beginning (obviously with different numbers).

In the comment of the previous web page of the challenge we found this code
```python
class SecurePrng(object):
    def __init__(self):
        # generate seed with 64 bits of entropy
        self.p = 4646704883L
        self.x = random.randint(0, self.p)
        self.y = random.randint(0, self.p)

    def next(self):
        self.x = (2 * self.x + 3) % self.p
        self.y = (3 * self.y + 9) % self.p
        return (self.x ^ self.y)
```
So let's do some math

![image](mathStart.png)

so assume that we know the first two correct number (just guess that): we only have to solve this system of equations in order 
to find the first two random integer

![image](mathSystem.png)

We guessed the fist two step (not so difficult, it happens with 0.25 probability): in our case

![image](myTwoGuesses.png)

`Mathematica` refuses to solve that equation system: no problem, let's use z3!

```python
my code
```

just few notes: there are more than one solution of that system, so we check every solution that z3 propose and accept the first good one.

Running that shit we get

```bash

```
ok: we have the first two random, and now we can generate all the solution. After 100 step we got the flag
CTF{_!_aRe_y0U_tH3_NSA_:-?_!_}

