# LolCode Interpreter 

Study project to code interpreter for Lolcode on python 2.7 with PLY library.
[Specification](https://ru.bmstu.wiki/LOLCODE)

Some programs in LolCode included:

- code1.lc - basic math functions
- code2.lc - sum variable with itself as astring and as a number
- code3.lc - simple if else contruction
- code4.lc - 'guess the animal' game

# REQUIREMENTS:
```
python2.7
PLY
argparse

```
# How to run it

``` sh
python LolCode.py -f code1.lc
max of 50 and 10:
50
print 2 * 2
4
print division of VAR=50 and 2
25
```
Let's loose the game
```sh
$ python LolCode.py -f code4.lc 
I imagine an animal. Try to guess it!
Guess 1:
>>> Wrong1
Guess 2:
>>> Wring2
Guess 3:
>>> Wrong3
You lose! Answer:PIG
```
Let's win the game
```sh
$ python LolCode.py -f code4.lc 
I imagine an animal. Try to guess it!
Guess 1:
>>> CAT
Guess 2:
>>> DOG
Guess 3:
>>> PIG
You win!
```