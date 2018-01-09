![Project Calculator](https://i.imgur.com/VW49Ez0.png)
======================================================
*By Gabriel DUGNY and Thibault LEPEZ, Efrei Paris Promo 2022, December 2017.*

Introduction
------------

- We tried to respect Python writting (conventions, style, philosophy...). Ex: _ for private

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

  - TLDR; we implemented everything.

  - Expressions:
    - Integers: all integers expressions can be correctly computed, our program supports the main operators (+-*/), parenthesis and uses the correct associativity and precedences rules, so the output is correct. The screenshot with the examples from the subject is in the appendix.
    - Strings: we implemented the concatenation of strings with the operators. The screenshot with the examples of the subject is available in the appendix as well.
    - Boolean: everything works, you can use not, and, or operators with true and false, and make checks with integers, strings and booleans with the comparison operators.

  - Variables:
    - TODO

  - Promoting to string type
    - TODO

  - Error Handling:
    - Missing operand: implemented
    - Unmatched parenthesis: implemented
    - TODO

  - Code quality:
    - We tried to produce a clean code, using modules in different files, functions, comments, type hints, standard namings rules, etc... For instance, we respected the Python PEP 8 for style guidelines.

  - Bonus:
    - GUI: We implemented a simple Tkinter GUI using a library we customized. We adapted an open source code for a Python shell (made with Tkinter) to use it with our evaluator.
    - Logger: The logger added with the logging built-in lib was helpfull to debug the code, without interfering with the I/O for the user.

- Problems, solutions and what we've earned
  - Regressions: it's quite easy to break the code by changing only one line in another module. Without automated testing, implemtening a feature would often break something else, and testing only the new feature would make us think everything worked when it wasn't. Discovering that the code didn't work afterwards made it difficult a couple times to find where the mistake was.
    - We then used automated testing using unittest, with the test running each time we changed code (with the IDE Pycharm), and everytime we pushed on Github (with Travis CI).
  - Collaboration: to avoid troubles, we instantly created a Github shared project as we both know Git. We also divided the program into different modules and functions, so that there would be less or very few merging to do. Even with this setup, we had a hard time communicating and working together because of the holidays, one always being unavailable, but we managed to work, a step at a time.
    - We made the best use of availables softwares, Git, Github.com, Gitkraken (Git Client) to collaborate seemlessly.


- What we have earned
  - Collaboration: make the best use of free tools like Git, Github.com...
  - Types of operators: betetr understanding of the syntax and rules of langyuages.
  Unary operators (not, - on an int), infix binary....
  - Better understanding of maths, algorithmic:
    - We have to understand the way each expression works, term by term (factors, atoms...)
   (Precedence, associativity...)

Conclusion
----------

- Thumbs up