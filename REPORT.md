![Project Calculator](https://i.imgur.com/VW49Ez0.png)
======================================================

[![Build Status](https://travis-ci.com/SoFolichon/ProjectCalculator.svg?token=p5pFoFaqAiLRDSEHnrdp&branch=master)](https://travis-ci.com/SoFolichon/ProjectCalculator) [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

*By Gabriel DUGNY and Thibault LEPEZ, Efrei Paris Promo 2022, December 2017.*


Introduction
------------



Architecture of the calculator
------------------------------
- Modules and their purpose
  - Parse.py:
    - Function parse: calls all the needed functions, to get a token
     list from a string expression.
    - Function expression to list: does the work! Handle every type of
    token to be parsed, negative integers, parenthesis (use of parenthesis stack).
    Parser based on the example given.
    - Function remove parenthesis: used by others modules,
    to remove useless parenthesis recursively when they aren't needed.
- Main data structures
  - Tokens list: TODO bc we'll probably change the tuple way
- Main algorithms
  - Search operator: this algorithms searches for the operator where to split
  an expression into 2 expressions. It searches for operators, from lowest to highest priority,
  from the end of the expression to its beggining.


Achievements and difficulties
-----------------------------
- Achievements with respect to the requirements
- Problems you faced
  - Regressions: it's quite easy to break the code by changing only one line in another module.

- What we have earned
  - Test to avoid regressions: automaticaly ran localy, and also at each commit
  - Collaboration: make the best use of free tools like Git, Github.com...
  - Types of operators: betetr understanding of the syntax and rules of langyuages.
  Unary operators (not, - on an int), infix binary....
  - Better understanding of maths, algorithmic:
    - We have to understand the way each expression works, term by term (factors, atoms...)
   (Precedence, associativity...)


Conclusion
----------
- Thumbs up