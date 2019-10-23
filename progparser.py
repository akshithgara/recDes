# Homework - 3
# Akshith Gara
# CS3500

import sys

keywords = [":=", "=", "+", "-", "*", "/", "or", "and", "~", "(", ")", "<", ">", ";", "#", "PRINT", "RETURN", "IF", "ENDIF", "ELSE", "WHILE", "ENDW", "PROC", "BEGIN", "END."]
token = ""
symbols = []
list_pos = 0
num_symbols = 0
err = ""
def getToken():
    global token
    global symbols
    global list_pos
    if (list_pos < num_symbols):
        token = symbols[list_pos]
        list_pos += 1
    else:
        return False

def isKeyword():
    if (token in keywords):
        return True
    else:
        return False

def isIdentifier():
    global err
    if (not isKeyword()):
        l = len(token)
        if (token[0].isalpha()):
            for i in range(1, l):
                if (not token[i].isalnum()):
                    return False
                    break
        else:
            return False
    else:
        err = "Error: Identifier expected, got " + "\""+ token + "\""+"."
        return False
    return True

def isInteger():
    newT = token
    if (newT[0] == "+"):
        newT = newT.replace("+", "")
    elif (newT[0] == "-"):
        newT = newT.replace("-", "")
    if (newT.find(".") > -1):
        return False
    return (newT.isnumeric())

def isDecimal():
    newT = token
    if (newT.find(".") == -1):
        return False
    else:
        pos = newT.find(".")
        return (isInteger(newT[0:pos]) and isInteger(newT[pos+1:]))


def RoutineSequence():
    if (RoutineDeclaration()):
        getToken()
        while (RoutineDeclaration()):
            getToken()
    else:
        return False
    return True

def RoutineDeclaration():
    global err
    if (token == "PROC"):
        getToken()
        if (isIdentifier()):
            getToken()
            if (token == "("):
                getToken()
                if (isIdentifier()):
                    getToken()
                    if(token == ','):
                        getToken()
                        if(isIdentifier()):
                            getToken()
                        else:
                            return False
                if (token == ")"):
                    getToken()
                    if (token == "BEGIN"):
                        getToken()
                        StatementSequence()
                        if (token == "END."):
                            return True
                        else:
                            err = "Error: END. expected, got " + "\"" + token + "\"" + "."
                            return False
                    else:
                        err = "Error: BEGIN expected, got " + "\""+ token + "\""+"."
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        err = "Error: Function declaration expected, got " + "\""+ token + "\""+"."
        return False

def StatementSequence():
    if (Statement()):
        getToken()
        while (Statement()):
            getToken()
        return True
    else:
        return False

def Statement():
    global err
    if (Assignment() or IfStatement() or LoopStatement() or printStatement() or retStatement()):
        return True
    else:
        return False

def Assignment():
    global err
    if (isIdentifier()):
        getToken()
        if (token == ":="):
            getToken()
            if (Expression()):
                if (token == ";"):
                    return True
                else:
                    # err = "Error: Assignment expected, got " + "\""+ token + "\""+"."
                    return False
            else:
                # err = "Error: Assignment expected, got " + "\""+ token + "\""+"."
                return False
        else:
            # err = "Error: Assignment expected, got " + "\""+ token + "\""+"."
            return False
    else:
        # err = "Error: Assignment expected, got " + "\""+ token + "\""+"."
        return False

def IfStatement():
    global err
    if (token == "IF"):
        getToken()
        if (token == "("):
            getToken()
            if (Expression()):
                if (token == ")"):
                    getToken()
                    if (StatementSequence()):
                        pass
                    if (token == "ELSE"):
                        getToken()
                        if (StatementSequence()):
                            pass
                    if (token == "ENDIF"):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        err = "Error: IF expected, got " + "\""+ token + "\""+"."
        return False

def LoopStatement():
    global err
    if (token == "WHILE"):
        getToken()
        if (token == "("):
            getToken()
            if (Expression()):
                if (token == ")"):
                    getToken()
                    if (StatementSequence()):
                        if (token == "ENDW"):
                            return True
                        else:
                            err = "Error: ENDW expected, got " + "\""+ token + "\""+"."
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        err = "Error: WHILE expected, got " + "\"" + token + "\"" + "."
        return False

def printStatement():
    global err
    if (token == "PRINT"):
        getToken()
        if (token == "("):
            getToken()
            if (Expression()):
                if (token == ")"):
                    getToken()
                    if (token == "!"):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        # err = "Error: PRINT expected, got " + "\"" + token + "\"" + "."
        return False

def retStatement():
    global err
    if (token == "RETURN"):
        getToken()
        if (isIdentifier()):
            getToken()
    else:
        # err = "Error: RETURN expected, got " + "\"" + token + "\"" + "."
        return False

def Expression():
    if (SimpleExpression()):
        if (Relation()):
            getToken()
            if (SimpleExpression()):
                pass
            else:
                return False
    else:
        return False
    return True

def SimpleExpression():
    if (Term()):
        while (AddOperator()):
            getToken()
            if (Term()):
                pass
            else:
                return False
        return True
    else:
        return False

def Term():
    if (Factor()):
        getToken()
        while (MulOperator()):
            getToken()
            if (Factor()):
                getToken()
            else:
                return False
    else:
        return False
    return True

def Factor():
    if (isInteger() or isDecimal() or isIdentifier()):
        return True
    elif (token == "("):
        getToken()
        if (Expression()):
            #getToken()
            if (token == ")"):
                return True
            else:
                return False
        else:
            return False
    elif (token == "~"):
        getToken()
        if (Factor()):
            return True
        else:
            return False
    else:
        return False

def Relation():
    global err
    if (token == "<" or token == ">" or token == "=" or token == "#"):
        return True
    else:
        return False

def AddOperator():
    global err
    if (token == "+" or token == "-" or token == "OR"):
        return True
    else:
        return False

def MulOperator():
    global err
    if (token == "*" or token == "/" or token == "AND"):
        return True
    else:
        return False

def main():
    global symbols
    global num_symbols
    s = ""

    for line in sys.stdin:
        s += line.strip()
        s += " "

    symbols = s.split(" ")
    num_symbols = len(symbols)

    getToken()
    if (RoutineSequence()):
        print("CORRECT")
    else:
        print("INVALID!")
        print(err)


main()
