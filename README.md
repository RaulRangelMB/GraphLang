# GraphLang
GraphLang is a programming language designed for the creation, manipulation, and pathfinding of graphs. In GraphLang, vertices and edges are treated as variable types, similar to int, bool, or string, each having its own identifier and value.

## Motivation
GraphLang was created to provide a simple and intuitive way to work with graph data structures directly within a programming language. While many languages offer libraries for graph manipulation, GraphLang aims to make graph components (vertices and edges) first-class citizens, simplifying the syntax for common graph operations like defining connections and finding paths. The goal is to offer a specialized tool that makes graph-related programming more accessible and expressive.

## Language Features and Characteristics
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
connect A B with C left
```

Pathfinding: Find and display paths between vertices.

```
Println(path(vertice1, vertice2))
```


Input/Output: Interact with the user using Scan for integer input and Println for output.

```
var x int
x = Scan()
Println(x)
```
Conditional Statements: Control program flow with if-else constructs.

```
var x int = 5

if x > 3 {
    Println("x is greater than 3!")
} 
```

Loops: Iterate using for loops (often used for while loops in similar contexts).

```
var x int = 5

for x > 0 {
    Println(x)
    x = x - 1
}
```

## Curiosities
- Named Vertices and Edges: GraphLang's vertices and edges can hold user-defined string values that can be altered whenever the user wishes to, making the graph elements more descriptive and human-readable.
- Directionality via Keywords: Connections explicitly define their direction using left, right, or both keywords, which simplifies the creation of both directed and undirected graph segments.
- Dynamic Typing for Graph Elements: vertice and edge types allow for flexible value assignment. They can store any type of value (like strings or numbers), providing adaptability for various graph modeling needs.

## Project Structure
This project implements the GraphLang interpreter in Python. It features a custom-built tokenizer and parser, eliminating the need for external tools like Flex and Bison.

- Tokenizer: Responsible for the lexical analysis of the input source code, breaking it down into individual tokens (like NUMBER, IDEN, PLUS, IF, etc.).
- Parser: Handles the syntactic analysis, taking the stream of tokens from the Tokenizer and building an Abstract Syntax Tree (AST) that represents the program's structure.
- AST Nodes: Various classes (e.g., VarDec, Connect, Println, BinaryOp, etc.) that represent the different constructs in the language. Each node has an evaluate method responsible for executing its part of the program.
- SymbolTable: Manages variable declarations and their values during program execution.
- ConnectionTable: Stores and manages all defined graph connections (vertices and edges), including their directionality.
- Pathfinding Logic: Implements algorithms to traverse the graph and find paths between specified vertices.


## How to Run
To execute a GraphLang program, simply run the main Python script and provide your GraphLang source file as an argument.

There is an inputs folder with example files to run.

```
python main.py inputs/(filename).gl
```