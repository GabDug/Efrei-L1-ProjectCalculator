Project Calculator [![Build Status](https://travis-ci.com/SoFolichon/ProjectCalculator.svg?token=p5pFoFaqAiLRDSEHnrdp&branch=master)](https://travis-ci.com/SoFolichon/ProjectCalculator)
===============
*By Gabriel DUGNY and Thibault LEPEZ, Efrei Paris Promo 2022, December 2017.*


Introduction
------------



Architecture of the calculator
------------------------------
- Modules and their purpose
  - Parse.py:
    - Function parse: calls alls the needed functions, to get a tokens
     list from a string expression.
    - Function expression to list: does the work! Handle every type of
    token to be parsed, negative integers, parenthesis (parenthesis stack).
    Based on the example given.
    - Function remove parenthesis: second function used by others files,
    to remove useless parenthesis recursively.
- Main data structures
  - Tokens list: TODO bc we'll probably change the tuple way
- Main algorithms


Achievements and difficulties
-----------------------------
- Achievements with respect to the requirements
- Problems you faces
  - Regressions
  - Types of operators: betetr understanding of the syntax and rules of langyuages.
  Unary operators (not, - on an int), infix binary....
- What we have earned (unit test, collaboration...)
  - Unit test to avoid regressions
- Better understanding of maths, algorithmic:
  - We have to understand the way each expression works, term by term (factors, atoms...)
 (Precedence, associativity...)


Conclusion
----------
- Thumbs up