----Python Dead Code Detector & AST Toolkit---
This tool is a static code analyzer designed to find and report unused variables and functions in large Python codebases. It works by parsing the source code into an Abstract Syntax Tree (AST), allowing it to analyze the code's structure without having to run it.
## Core Features
Anaylyse any python scrpit to detect and report dead vaiable and fucntion 

## WORKING 

It used the in built ast library to make a abstract syntax tree to parse and anylyse the code without running 

It has the context of the scopes in which the program is like in global or in a local function 

It has a symbol table that keeps track of all vaiables and fuctions defined with there line number, used / defined state

And finally creates a report using the symbol tables used argument 

