# GraphLang
GraphLang is a programming language designed for the creation, manipulation, and visualization of graphs. In GraphLang, vertices and edges are treated as variable types, similar to int, bool, or string, each having its own identifier and value.

## Language Features
GraphLang provides intuitive syntax for:

Variable Declarations: Declare variables of type int, bool, string, vertice, and edge.

```
var myNumber int = 10
var city vertice = "New York"
var road edge = "Highway 1"
```

Graph Connections: Establish connections between vertices using edges with specified directions.

```
connect vertice1 vertice2 with edge1 both
connect startNode endNode with pathEdge right
connect A B with edgeC left
```

Pathfinding: Find and display paths between vertices.

```
Println(path(vertice1, vertice2))
```

Conditional Statements: Control program flow with if-else constructs.
Loops: Iterate using for loops (often used for while loops in similar contexts).
Input/Output: Interact with the user using Scan for input and Println for output.

## Project Structure
This project implements the GraphLang interpreter in Python. It features a custom-built tokenizer and parser, eliminating the need for external tools like Flex and Bison.

- Tokenizer: Responsible for the lexical analysis of the input source code, breaking it down into individual tokens (like NUMBER, IDEN, PLUS, IF, etc.).
- Parser: Handles the syntactic analysis, taking the stream of tokens from the Tokenizer and building an Abstract Syntax Tree (AST) that represents the program's structure.
- AST Nodes: Various classes (e.g., VarDec, Connect, Println, BinaryOp) that represent the different constructs in the language. Each node has an evaluate method responsible for executing its part of the program.
- SymbolTable: Manages variable declarations and their values during program execution.
- ConnectionTable: Stores and manages all defined graph connections (vertices and edges), including their directionality.
- Pathfinding Logic: Implements algorithms to traverse the graph and find paths between specified vertices.


## How to Run
To execute a GraphLang program, simply run the main Python script and provide your GraphLang source file as an argument.

There is an inputs folder with example files to run.

```
python main.py inputs/filename.gl
```