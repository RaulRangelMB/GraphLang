import sys
import re

class PrepPro:
    def filter(code):
        code = re.sub(r'\/\/.*', '', code)
        code = re.sub(r'\/\*[\s\S]*?\*\/', '', code)
        return code
    
class SymbolTable:
    def __init__(self):
        self.table = {}

    def create(self, identifier, ttype, value):
        if identifier not in self.table:
            self.table[identifier] = (ttype, value)
        else:
            raise Exception(f"Identificador declarado duas vezes: {identifier}")

    def get(self, identifier):
        if identifier in self.table:
            return self.table[identifier]
        raise Exception(f"Identificador não encontrado: {identifier} (no get)")

    def set(self, identifier, value):
        if identifier in self.table:
            tupla = self.table[identifier]
            new_tupla = (tupla[0], value[-1])
            self.table[identifier] = new_tupla
        else:
            raise Exception(f"Identificador não encontrado: {identifier} (no set)")
        #print(self.table)

class ConnectionTable:
    def __init__(self, symbol_table):
        self.table = {}  # Stores connections. Format: {vertice1_name: {vertice2_name: {edge_name: direction}}}
        self.symbol_table = symbol_table # Reference to the SymbolTable

    def create(self, vertice1_node, vertice2_node, edge_node, direction_token_type):
        vertice1_name = vertice1_node.value
        vertice2_name = vertice2_node.value
        edge_name = edge_node.value

        if not self.symbol_table.get(vertice1_name):
            raise Exception(f"Erro de Conexão: Vértice '{vertice1_name}' não declarado na SymbolTable.")
        vertice1_data = self.symbol_table.get(vertice1_name)
        if vertice1_data[0] != 'VERTICE':
            raise Exception(f"Erro de Conexão: '{vertice1_name}' não é do tipo VERTICE.")

        if not self.symbol_table.get(vertice2_name):
            raise Exception(f"Erro de Conexão: Vértice '{vertice2_name}' não declarado na SymbolTable.")
        vertice2_data = self.symbol_table.get(vertice2_name)
        if vertice2_data[0] != 'VERTICE':
            raise Exception(f"Erro de Conexão: '{vertice2_name}' não é do tipo VERTICE.")

        if not self.symbol_table.get(edge_name):
            raise Exception(f"Erro de Conexão: Aresta '{edge_name}' não declarada na SymbolTable.")
        edge_data = self.symbol_table.get(edge_name)
        if edge_data[0] != 'EDGE':
            raise Exception(f"Erro de Conexão: '{edge_name}' não é do tipo EDGE.")

        if vertice1_name not in self.table:
            self.table[vertice1_name] = {}
        if vertice2_name not in self.table[vertice1_name]:
            self.table[vertice1_name][vertice2_name] = {}
        
        if edge_name in self.table[vertice1_name][vertice2_name]:
            raise Exception(f"Erro de Conexão: Aresta '{edge_name}' já conecta '{vertice1_name}' e '{vertice2_name}' na direção '{self.table[vertice1_name][vertice2_name][edge_name]}'.")

        self.table[vertice1_name][vertice2_name][edge_name] = direction_token_type

        # For 'BOTH' direction, also store the reverse connection
        # if direction_token_type == 'BOTH':
        #     if vertice2_name not in self.table:
        #         self.table[vertice2_name] = {}
        #     if vertice1_name not in self.table[vertice2_name]:
        #         self.table[vertice2_name][vertice1_name] = {}
            
        #     # Optionally check for existing reverse edge
        #     if edge_name in self.table[vertice2_name][vertice1_name]:
        #          raise Exception(f"Erro de Conexão: Aresta '{edge_name}' já conecta '{vertice2_name}' e '{vertice1_name}' na direção '{self.table[vertice2_name][vertice1_name][edge_name]}'.")

        #     self.table[vertice2_name][vertice1_name][edge_name] = direction_token_type


        # print(f"Conexão criada: {vertice1_name} --({edge_name} {direction_token_type})--> {vertice2_name}")

    def get(self, vertice1_name, vertice2_name=None, edge_name=None):
        if vertice1_name in self.table:
            if vertice2_name is None:
                return self.table[vertice1_name] # Return all connections from vertice1
            elif vertice2_name in self.table[vertice1_name]:
                if edge_name is None:
                    return self.table[vertice1_name][vertice2_name] # Return all edges between vertice1 and vertice2
                elif edge_name in self.table[vertice1_name][vertice2_name]:
                    return self.table[vertice1_name][vertice2_name][edge_name] # Return direction of specific edge
        return None

    def print_connections(self):
        print("\n--- Connection Table ---")
        if not self.table:
            print("No connections made.")
            return
        
        for v1, connections_from_v1 in self.table.items():
            for v2, edges_between in connections_from_v1.items():
                for edge, direction in edges_between.items():
                    if v1 in self.symbol_table.table: v1_value = self.symbol_table.get(v1)[1]
                    if v1_value is None: v1_value = v1
                    if v2 in self.symbol_table.table: v2_value = self.symbol_table.get(v2)[1]
                    if v2_value is None: v2_value = v2
                    if edge in self.symbol_table.table: edge_value = self.symbol_table.get(edge)[1]
                    if edge_value is None: edge_value = edge
                    if direction == 'BOTH': middle = f"<-[{edge_value}]->"
                    elif direction == 'LEFT': middle = f"<-[{edge_value}]--"
                    elif direction == 'RIGHT': middle = f"--[{edge_value}]->"
                    print(f"{v1_value} {middle} {v2_value}")
        print("------------------------\n")

def findPath(vertice1, vertice2, symboltable, connections):
    # print(vertice1, vertice2)
    connections2 = {}
    for startVertice, connectedVertices in connections.table.items():
        for endVertice, direction in connectedVertices.items():
            direction = next(iter(direction.values()))
            if direction == "RIGHT":
                if startVertice not in connections2: connections2[startVertice] = []
                connections2[startVertice].append(endVertice)
            elif direction == "LEFT":
                if endVertice not in connections2: connections2[endVertice] = []
                connections2[endVertice].append(startVertice)
            elif direction == "BOTH":
                if startVertice not in connections2: connections2[startVertice] = []
                if endVertice not in connections2: connections2[endVertice] = []
                connections2[startVertice].append(endVertice)
                connections2[endVertice].append(startVertice)

    start = symboltable.get(vertice1.value)[1]
    if start is None: start = vertice1.value
    end = symboltable.get(vertice2.value)[1]
    if end is None: end = vertice2.value
    print(f"Path from {start} to {end}: ", end='')
    return goDownPath(vertice1.value, vertice2.value, connections2, symboltable)

def goDownPath(start_vertice, target_vertice, connections, symboltable, current_path=None):
    if current_path is None:
        current_path = []

    current_path = current_path + [start_vertice]

    if start_vertice == target_vertice:
        return current_path

    if start_vertice not in connections or not connections[start_vertice]:
        return None

    # Explore neighbors
    for next_vertice in connections[start_vertice]:
        if next_vertice not in current_path:
            # print(f"Exploring neighbor: {next_vertice}")
            path_found = goDownPath(next_vertice, target_vertice, connections, symboltable, list(current_path))
            if path_found:
                return path_found # If a path is found by a recursive call, propagate it up

    # print(f"Search from {start_vertice} ended, no path found through this branch. Backtracking.")
    return None

class Token:
    def __init__(self, ttype : str, value : int):
        self.type = ttype 
        self.value = value

class Tokenizer:
    def __init__(self, source: str, pos: int = 0):
        self.source = source
        self.pos = pos
        self.next = None
        self.end = len(self.source)

    def selectNext(self):
        if self.pos >= self.end:
            #print("EOF")
            self.next = Token('EOF', 0)
            return

        c = self.source[self.pos]
        #print(c)

        if c.isspace():
            self.pos += 1
            self.selectNext()
            return

        if c.isdigit():
            acumula = c
            self.pos += 1
            while self.pos < self.end and self.source[self.pos].isdigit():
                acumula += self.source[self.pos]
                self.pos += 1
            #print("NUM")
            self.next = Token('NUMBER', int(acumula))
            return
        
        if c == '"':
            acumula = ''
            self.pos += 1
            while self.pos < self.end and self.source[self.pos] != '"':
                acumula += self.source[self.pos]
                self.pos += 1
            if self.pos >= self.end or self.source[self.pos] != '"':
                raise Exception("Input Inválido: aspas não fechadas")
            self.pos += 1
            self.next = Token('STRING', acumula)
            return

        if c.isalpha():
            acumula = c
            self.pos += 1
            while self.pos < self.end and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                acumula += self.source[self.pos]
                self.pos += 1

            if acumula == "Println":
                #print("Println")
                self.next = Token('PRINT', 0)
            elif acumula == "if":
                #print("IF")
                self.next = Token('IF', 0)
            elif acumula == "else":
                #print("ELSE")
                self.next = Token('ELSE', 0)
            elif acumula == "for":
                #print("WHILE")
                self.next = Token('WHILE', 0)
            elif acumula == "Scan":
                #print("SCAN")
                self.next = Token('SCAN', 0)
            elif acumula == "var":
                #print("VAR")
                self.next = Token('VAR', 0)
            elif acumula == "int":
                #print("INT")
                self.next = Token('TYPE', 'INT')
            elif acumula == "bool":
                #print("BOOL")
                self.next = Token('TYPE', 'BOOL')
            elif acumula == "string":
                #print("STRING")
                self.next = Token('TYPE', 'STRING')
            elif acumula == "true":
                #print("TRUE")
                self.next = Token('BOOL', True)
            elif acumula == "false":
                #print("FALSE")
                self.next = Token('BOOL', False)
            elif acumula == "edge":
                #print("EDGE")
                self.next = Token('TYPE', 'EDGE')
            elif acumula == "vertice":
                #print("VERTICE")
                self.next = Token('TYPE', 'VERTICE')
            elif acumula == "connect":
                #print("CONNECT")
                self.next = Token('CONNECT', 0)
            elif acumula == "with":
                #print("WITH")
                self.next = Token('WITH', 0)
            elif acumula == "left":
                #print("LEFT")
                self.next = Token('LEFT', 0)
            elif acumula == "right":
                #print("RIGHT")
                self.next = Token('RIGHT', 0)
            elif acumula == "both":
                #print("BOTH")
                self.next = Token('BOTH', 0)
            elif acumula == "path":
                #print("PATH")
                self.next = Token('PATH', 0)
            else:
                #print(f"IDENTIFIER {acumula}")
                self.next = Token('IDEN', acumula)
            return

        self.pos += 1
        if c == '+':
            #print("PLUS")
            self.next = Token('PLUS', 0)
        elif c == '-':
            #print("MINUS")
            self.next = Token('MINUS', 0)
        elif c == '*':
            #print("MULT")
            self.next = Token('MULT', 0)
        elif c == '/':
            #print("DIV")
            self.next = Token('DIV', 0)
        elif c == '(':
            #print("OPEN_PAR")
            self.next = Token('OPEN_PAR', 0)
        elif c == ')':
            #print("CLOSE_PAR")
            self.next = Token('CLOSE_PAR', 0)
        elif c == '{':
            #print("OPEN_BRK")
            self.next = Token('OPEN_BRK', 0)
        elif c == '}':
            #print("CLOSE_BRK")
            self.next = Token('CLOSE_BRK', 0)
        elif c == '=':
            #print("ASSIGN")
            if self.pos < self.end and self.source[self.pos] == '=':
                self.pos += 1
                #print("EQUALS")
                self.next = Token('EQUALS', 0)

            #print("ASSIGN")
            else:
                self.next = Token('ASSIGN', 0)
        elif c == '&':
            if self.pos < self.end and self.source[self.pos] == '&':
                self.pos += 1
                #print("AND")
                self.next = Token('AND', 0)
            else:
                raise Exception(f"Input Inválido: '&{c}'")
        elif c == '|':
            if self.pos < self.end and self.source[self.pos] == '|':
                self.pos += 1
                #print("OR")
                self.next = Token('OR', 0)
            else:
                raise Exception(f"Input Inválido: '|{c}'")
        elif c == '>':
            #print("GREATER")
            self.next = Token('GREATER', 0)
        elif c == '<':
            #print("LESS")
            self.next = Token('LESS', 0)
        elif c == '!':
            #print("NOT")
            self.next = Token('NOT', 0)
        elif c == ',':
            #print("COMMA")
            self.next = Token('COMMA', 0)
        elif c == '\n':
            #print("NEW_LIN")
            self.next = Token('NEW_LIN', 0)
        else:
            raise Exception(f"Invalid character: {c}")


class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable, connectionTable=None):
        pass

class BinOp(Node):
    def evaluate(self, symbolTable, connectionTable=None):
        left_type, left_value = self.children[0].evaluate(symbolTable, connectionTable)
        right_type, right_value = self.children[1].evaluate(symbolTable, connectionTable)
        
        if self.value == '+':
            if left_type == 'INT' and right_type == 'INT':
                return ("INT", left_value + right_value)
            left_value = str(left_value).lower() if left_type == 'BOOL' else left_value
            right_value = str(right_value).lower() if right_type == 'BOOL' else right_value
            return ("STRING", str(left_value) + str(right_value))
            
        elif self.value == '-' or self.value == '*' or self.value == '/':
            if not (left_type == 'INT' and right_type == 'INT'):
                raise Exception(f"Invalid operation: {left_type} {self.value} {right_type}")

            if self.value == '-':
                return ("INT", left_value - right_value)
        
            elif self.value == '*':
                return ("INT", left_value * right_value)
            
            elif self.value == '/':
                if right_value == 0:
                    raise Exception("Divisão por zero!")
                return ("INT", left_value // right_value)
        
        elif self.value == '&&' or self.value == '||':
            if left_type != 'BOOL' or right_type != 'BOOL':
                raise Exception(f"Operação Inválida: {left_type} {self.value} {right_type}")
            
            if self.value == '&&':
                return ("BOOL", left_value and right_value)
            elif self.value == '||':
                return ("BOOL", left_value or right_value)
        

        elif self.value == '==' or self.value == '>' or self.value == '<':
            if left_type != right_type:
                raise Exception(f"Operação Inválida: {left_type} {self.value} {right_type}")
            
            if self.value == '==':
                return ("BOOL", left_value == right_value)
            elif self.value == '>':
                return ("BOOL", left_value > right_value)
            elif self.value == '<':
                return ("BOOL", left_value < right_value)

class UnOp(Node):
    def evaluate(self, symbolTable, connectionTable=None):
        _type, value = self.children[0].evaluate(symbolTable, connectionTable)
        if _type != 'INT' and _type != 'BOOL':
            raise Exception(f"Operação Inválida: {self.value} {_type}")
        
        if self.value == '+' and _type == 'INT':
            return ("INT", value)
        elif self.value == '-' and _type == 'INT':
            return ("INT", -value)
        elif self.value == '!' and _type == 'BOOL':
            return ("BOOL", not value)
        
class NoOp(Node):
    def evaluate(self, symbolTable, connectionTable=None):
        return None

class IntVal(Node):
    def evaluate(self, symbolTable, connectionTable=None):
        return ("INT", self.value)
    
class StrVal(Node):
    def evaluate(self, symbolTable, connectionTable=None):
        return ("STRING", self.value)
    
class BoolVal(Node):
    def evaluate(self, symbolTable, connectionTable=None):
        return ("BOOL", self.value)
    
class VarDec(Node):
    def __init__(self, identifier, _type, bexpr=None):
        self.type = _type
        self.children = [identifier, bexpr]

    def evaluate(self, symbolTable, connectionTable=None):
        if self.children[1] is not None:
            if self.type in ['EDGE', 'VERTICE']:
                symbolTable.create(self.children[0].value, self.type, self.children[1].evaluate(symbolTable, connectionTable)[1])
                return
            elif self.type != self.children[1].evaluate(symbolTable, connectionTable)[0]:
                raise Exception(f"Input Inválido: variável {self.type} {self.children[0].value} atribuída com {self.children[1].evaluate(symbolTable)[0]} (em VarDec)")
            value = self.children[1].evaluate(symbolTable, connectionTable)
            symbolTable.create(self.children[0].value, self.type, value[1])
        else:
            symbolTable.create(self.children[0].value, self.type, None)


        #print(symbolTable.table)

class Identifier(Node):
    def evaluate(self, symbolTable, connectionTable=None):
        return symbolTable.get(self.value)
    
class Println(Node):
    def __init__(self, expression):
        self.children = [expression]

    def evaluate(self, symbolTable, connectionTable):
        if isinstance(self.children[0], list):
            vertice1, vertice2 = self.children[0]

            res = findPath(vertice1, vertice2, symbolTable, connectionTable)
            if res is None:
                print(f"No path found.")
            else:
                res = " -> ".join([symbolTable.get(v)[1] if symbolTable.get(v)[1] is not None else v for v in res])
                print(res)
            return res
        
        _type, value = self.children[0].evaluate(symbolTable, connectionTable)
        if _type == 'INT':
            print(value)
        elif _type == 'STRING':
            print(value)
        elif _type == 'BOOL':
            print("true" if value else "false")
        elif _type == 'VERTICE':
            print(value)
        elif _type == 'EDGE':
            print(value)
        else:
            raise Exception(f"Tipo inválido para Println: {_type}")

class Connect(Node):
    def __init__(self, vertice1, vertice2, edge, direction):
        super().__init__(None, [vertice1, vertice2, edge, direction])
        self.vertice1 = vertice1 # Identifier node for vertice1
        self.vertice2 = vertice2 # Identifier node for vertice2
        self.edge = edge         # Identifier node for edge
        self.direction = direction # String ('LEFT', 'RIGHT', 'BOTH')

    def evaluate(self, symbol_table, connection_table):
        connection_table.create(self.vertice1, self.vertice2, self.edge, self.direction)
        return None

class Assignment(Node):
    def __init__(self, identifier, expression):
        self.children = [identifier, expression]

    def evaluate(self, symbolTable, connectionTable=None):
        _type, value = self.children[1].evaluate(symbolTable, connectionTable)

        if symbolTable.get(self.children[0].value)[0] in ['EDGE', 'VERTICE']:
            symbolTable.set(self.children[0].value, (_type, value))
        elif _type != symbolTable.get(self.children[0].value)[0]:
            raise Exception(f"Input Inválido: variável {symbolTable.get(self.children[0].value)[0]} {self.children[0].value} atribuída com {_type} (em assignment)")
        
        symbolTable.set(self.children[0].value, (_type, value))
        return value
    
    # def evaluate(self, symbolTable, connectionTable=None):
    #     if self.children[1] is not None:
    #         if self.type in ['EDGE', 'VERTICE']:
    #             symbolTable.create(self.children[0].value, self.type, self.children[1].evaluate(symbolTable, connectionTable)[1])
    #             return
    #         elif self.type != self.children[1].evaluate(symbolTable, connectionTable)[0]:
    #             raise Exception(f"Input Inválido: variável {self.type} {self.children[0].value} atribuída com {self.children[1].evaluate(symbolTable)[0]} (em VarDec)")
    #         value = self.children[1].evaluate(symbolTable, connectionTable)
    #         symbolTable.create(self.children[0].value, self.type, value[1])
    #     else:
            # symbolTable.create(self.children[0].value, self.type, None)
        
        # value = self.children[1].evaluate(symbolTable)
        # #print(f"{value} to {self.children[0].value}")
        # symbolTable.set(self.children[0].value, value)
        # return value

class Block(Node):
    def __init__(self, statements):
        self.children = statements
    
    def evaluate(self, symbolTable, connectionTable=None):
        for statement in self.children:
            statement.evaluate(symbolTable, connectionTable)

class If(Node):
    def __init__(self, condition, block_true, block_false=None):
        self.children = [condition, block_true, block_false]

    def evaluate(self, symbolTable, connectionTable = None):
        if self.children[0].evaluate(symbolTable, connectionTable)[0] != 'BOOL':
            raise Exception(f"Input Inválido: {self.children[0].evaluate(symbolTable, connectionTable)[0]} usado na condição do IF")

        if self.children[0].evaluate(symbolTable, connectionTable)[-1]:
            self.children[1].evaluate(symbolTable, connectionTable)
        elif self.children[2] is not None:
            self.children[2].evaluate(symbolTable, connectionTable)

class While(Node):
    def __init__(self, condition, block):
        self.children = [condition, block]

    def evaluate(self, symbolTable, connectionTable=None):
        if self.children[0].evaluate(symbolTable)[0] != 'BOOL':
            raise Exception(f"Input Inválido: {self.children[0].evaluate(symbolTable)[0]} (em while)")
        
        while self.children[0].evaluate(symbolTable, connectionTable)[-1]:
            self.children[1].evaluate(symbolTable, connectionTable)

class Read(Node):
    def evaluate(self, symbolTable, connectionTable=None):
        return ("INT", int(input()))

class Parser:
    def __init__(self):
        self.tokenizer = None

    def parseBExpression(self):
        node = self.parseBTerm()
        while self.tokenizer.next.type == 'OR':
            self.tokenizer.selectNext()
            node = BinOp("||", [node, self.parseBTerm()])
        return node

    def parseBTerm(self):
        node = self.parseRelExpression()
        while self.tokenizer.next.type == 'AND':
            self.tokenizer.selectNext()
            node = BinOp("&&", [node, self.parseRelExpression()])
        return node
        
    def parseRelExpression(self):
        node = self.parseExpression()
        while self.tokenizer.next.type == 'EQUALS' or self.tokenizer.next.type == 'GREATER' or self.tokenizer.next.type == 'LESS':
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            if op == 'EQUALS':
                node = BinOp("==", [node, self.parseExpression()])
            elif op == 'GREATER':
                node = BinOp(">", [node, self.parseExpression()])
            elif op == 'LESS':
                node = BinOp("<", [node, self.parseExpression()])
        return node

    def parseBlock(self):
        if self.tokenizer.next.type != 'OPEN_BRK':
            raise Exception("Input Inválido: '{' esperado (em block)")
        self.tokenizer.selectNext()
        statements = []
        while self.tokenizer.next.type != 'CLOSE_BRK':
            statements.append(self.parseStatement())
        if len(statements) == 0:
            raise Exception("Input Inválido: block vazio")
        if self.tokenizer.next.type != 'CLOSE_BRK':
            raise Exception("Input Inválido: '}' esperado (em block)")
        self.tokenizer.selectNext()
        return Block(statements)

    def parseStatement(self):
        if self.tokenizer.next.type == 'PRINT':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'OPEN_PAR':
                raise Exception("Input Inválido: '(' esperado")
            self.tokenizer.selectNext()

            if self.tokenizer.next.type == 'PATH':
                self.tokenizer.selectNext()

                if self.tokenizer.next.type != 'OPEN_PAR':
                    raise Exception("Input Inválido: '(' esperado (em path)")
                self.tokenizer.selectNext()
                                
                if self.tokenizer.next.type != 'IDEN':
                    raise Exception("Input Inválido: identificador esperado (em path)")
                vertice1 = Identifier(self.tokenizer.next.value, [])
                self.tokenizer.selectNext()

                if self.tokenizer.next.type != 'COMMA':
                    raise Exception("Input Inválido: ',' esperado (em path)")
                self.tokenizer.selectNext()

                if self.tokenizer.next.type != 'IDEN':
                    raise Exception("Input Inválido: identificador esperado (em path)")
                vertice2 = Identifier(self.tokenizer.next.value, [])
                self.tokenizer.selectNext()

                if self.tokenizer.next.type != 'CLOSE_PAR':
                    raise Exception("Input Inválido: ')' esperado (em path)")
                self.tokenizer.selectNext()

                if self.tokenizer.next.type != 'CLOSE_PAR':
                    raise Exception("Input Inválido: ')' esperado (em path)")
                self.tokenizer.selectNext()
                
                return Println([vertice1, vertice2])
            
            # Se nao for path, parse a expressão
            bexpr = self.parseBExpression()
            
            if self.tokenizer.next.type != 'CLOSE_PAR':
                raise Exception("Input Inválido: ')' esperado")
            self.tokenizer.selectNext()
            return Println(bexpr)            
        
        elif self.tokenizer.next.type == 'IDEN':
            identifier = Identifier(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != 'ASSIGN':
                raise Exception("Input Inválido")
            self.tokenizer.selectNext()

            bexpr = self.parseBExpression()

            if self.tokenizer.next.type not in ['NEW_LIN', 'CLOSE_BRK', 'EOF', 'WHILE', 'IF', 'ELSE', 'PRINT', 'IDEN', 'VAR', 'CONNECT']:
                raise Exception(f"Input Inválido: token inesperado '{self.tokenizer.next.type}' após a atribuição")

            return Assignment(identifier, bexpr)
        
        elif self.tokenizer.next.type == 'VAR':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'IDEN':
                raise Exception("Input Inválido: identificador esperado (em var)")
            
            identifier = Identifier(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != 'TYPE':
                raise Exception("Input Inválido: tipo esperado (em var)")
            
            _type = self.tokenizer.next.value
            self.tokenizer.selectNext()

            if self.tokenizer.next.type == 'ASSIGN':
                self.tokenizer.selectNext()
                bexpr = self.parseBExpression()

                if self.tokenizer.next.type not in ['NEW_LIN', 'CLOSE_BRK', 'EOF', 'WHILE', 'IF', 'ELSE', 'PRINT', 'IDEN', 'VAR', 'CONNECT']:
                    raise Exception(f"Input Inválido: token inesperado '{self.tokenizer.next.type}' após a atribuição")
                
                return VarDec(identifier, _type, bexpr)
            
            return VarDec(identifier, _type)
        
        elif self.tokenizer.next.type == 'WHILE':
            self.tokenizer.selectNext()
            bexpr = self.parseBExpression()
            if self.tokenizer.next.type != 'OPEN_BRK':
                raise Exception("Input Inválido: '{' esperado (em while)")
            block = self.parseBlock()
            return While(bexpr, block)
        
        elif self.tokenizer.next.type == 'IF':
            self.tokenizer.selectNext()
            bexpr = self.parseBExpression()
            if self.tokenizer.next.type != 'OPEN_BRK':
                raise Exception("Input Inválido: '{' esperado (em if)")
            block_true = self.parseBlock()
            block_false = None
            if self.tokenizer.next.type == 'ELSE':
                self.tokenizer.selectNext()
                if self.tokenizer.next.type != 'OPEN_BRK':
                    raise Exception("Input Inválido: '{' esperado (em else)")
                block_false = self.parseBlock()
            return If(bexpr, block_true, block_false)
        
        elif self.tokenizer.next.type == 'CONNECT':
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != 'IDEN':
                raise Exception("Input Inválido: identificador esperado (em connect)")
            vertice1 = Identifier(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != 'IDEN':
                raise Exception("Input Inválido: identificador esperado (em connect)")
            vertice2 = Identifier(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != 'WITH':
                raise Exception("Input Inválido: 'with' esperado (em connect)")
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != 'IDEN':
                raise Exception("Input Inválido: identificador esperado (em connect)")
            edge = Identifier(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()

            if self.tokenizer.next.type not in ['BOTH', 'LEFT', 'RIGHT']:
                raise Exception("Input Inválido: 'both', 'left' ou 'right' esperado (em connect)")
            direction = self.tokenizer.next.type
            self.tokenizer.selectNext()

            return Connect(vertice1, vertice2, edge, direction)

        else:
            expr = self.parseBExpression()
            return expr

    def parseFactor(self):
        if self.tokenizer.next.type == 'NUMBER':
            node = IntVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return node
        
        elif self.tokenizer.next.type == 'IDEN':
            node = Identifier(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return node
        
        elif self.tokenizer.next.type == 'STRING':
            node = StrVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return node

        elif self.tokenizer.next.type == 'BOOL':
            node = BoolVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return node

        elif self.tokenizer.next.type == 'PLUS':
            self.tokenizer.selectNext()
            return UnOp('+', [self.parseFactor()])

        elif self.tokenizer.next.type == 'MINUS':
            self.tokenizer.selectNext()
            return UnOp('-', [self.parseFactor()])

        elif self.tokenizer.next.type == 'NOT':
            self.tokenizer.selectNext()
            return UnOp('!', [self.parseFactor()])
        
        elif self.tokenizer.next.type == 'OPEN_PAR':
            self.tokenizer.selectNext()
            parenthesisTree = self.parseBExpression()
            if self.tokenizer.next.type != 'CLOSE_PAR':
                raise Exception("Input Inválido")
            self.tokenizer.selectNext()
            return parenthesisTree
        
        elif self.tokenizer.next.type == 'SCAN':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'OPEN_PAR':
                raise Exception("Input Inválido: '(' esperado")
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'CLOSE_PAR':
                raise Exception("Input Inválido: ')' esperado")
            self.tokenizer.selectNext()
            return Read(0, [])
        
        else:
            raise Exception("Input Inválido (em factor)")

    def parseTerm(self):
        node = self.parseFactor()
        while self.tokenizer.next.type == 'MULT' or self.tokenizer.next.type == 'DIV':
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            if op == 'MULT':
                node = BinOp("*", [node, self.parseFactor()])
            elif op == 'DIV':
                node = BinOp("/", [node, self.parseFactor()])
        return node

    def parseExpression(self):
        node = self.parseTerm()
        while self.tokenizer.next.type == 'PLUS' or self.tokenizer.next.type == 'MINUS':
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            if op == 'PLUS':
                node = BinOp("+", [node, self.parseTerm()])
            elif op == 'MINUS':
                node = BinOp("-", [node, self.parseTerm()])
        return node
    
    def run(self, code):
        code = PrepPro.filter(code)
        self.tokenizer = Tokenizer(code)
        self.tokenizer.selectNext()
        
        block = self.parseBlock()
        
        if self.tokenizer.next.type != 'EOF':
            raise Exception("Input Inválido: EOF esperado")
        
        return block
    
parser = Parser()
entrada = sys.argv[-1]

with open(entrada, 'r') as file:
    code = file.read()

ast = parser.run(code)
st = SymbolTable()
ct = ConnectionTable(st)
ast.evaluate(st, ct)

ct.print_connections()