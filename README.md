----Python Dead Code Detector & AST Toolkit---
Note: This project is a work-in-progress, focused on building a static code analyzer for Python. Have built the complete varible and funnction deed code detecion functions

This tool is a static code analyzer designed to find and report unused variables and functions in large Python codebases. It works by parsing the source code into an Abstract Syntax Tree (AST), allowing it to analyze the code's structure without having to run it.

## Core Features
Dead Code Detection (In Progress)
The primary goal of this project.

Parses Code: Reads Python files and builds a map of all defined variables and functions.

Tracks Scope: Understands which functions and variables exist within different scopes using symbol table (e.g., global vs. inside a function).

Identifies Unused Code: Compares the list of defined code with the code that is actually used or called.

Generates Reports: Will produce a clear report of all unused "dead" code, helping you clean up your projects.

