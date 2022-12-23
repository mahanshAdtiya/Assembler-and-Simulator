# things used in Code
import sys
Opcode = ["add","addf", "sub","subf","movf", "ld", "st", "mul", "div","mov", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt","var"]
# opDict = {'add': '00000','sub': '00001','ld': '00100','st': '00101','mul': '00110','div': '00111','rs': '01000','ls': '01001','xor': '01010','or': '01011','and': '01100','not': '01101','cmp': '01110','jmp': '01111','jlt': '10000','jgt': '10001','je': '10010'}
opDict = {'add': '10000',"addf":"00000",'sub': '10001',"subf":"00001","movf":"00010",'ld': '10100','st': '10101','mul': '10110','div': '10111','rs': '11000','ls': '11001','xor': '11010','or': '11011','and': '11100','not': '11101','cmp': '11110','jmp': '11111','jlt': '01100','jgt': '01101','je': '01111'}
register = ["R0", "R1","R2", "R3", "R4", "R5", "R6"]
file = []
labelDict = {}
varDict = {}
varD = []
labelD = []
varNum = -1
flag = True
for line in sys.stdin:
    if "" == line:
        break
    file.append(line.strip().split())
file = list(filter(None, file))

def bintofloatdec(num):
    first,last = str(num).split(".")
    first = '{0:0b}'.format(int(first))
    last = "0" + "." + last
    list = []
    for i in range(5):
        if last == "0.0":
            break
        last = float(last) * 2
        f,l = str(last).split(".")
        last = "0" + "." + l
        list.append(f)
    floatnum = first + "."
    for i in list:
        floatnum += str(i)
    point = -1
    for i in range(len(floatnum)):
        if floatnum[i] == ".":
            point += i
            break
    floatnum = str(float(floatnum) / ( 10 **point))
    for i in range(5-len(floatnum[2:])):
        floatnum += "0"
    return (f"{'{0:03b}'.format(point)}{floatnum[2:]}")

def checkFLOAT(num):
    first,last = str(num).split(".")
    first = '{0:0b}'.format(int(first))
    last = "0" + "." + last
    list = []
    for i in range(5):
        if last == "0.0":
            break
        last = float(last) * 2
        f,l = str(last).split(".")
        last = "0" + "." + l
        list.append(f)
    floatnum = first + "."
    for i in list:
        floatnum += str(i)
    point = -1
    for i in range(len(floatnum)):
        if floatnum[i] == ".":
            point += i
            break
    a = floatnum
    a = a.replace(".","")
    floatnum = "1."
    for i in range(1,len(a)):
        floatnum += a[i]

    for i in range(5-len(floatnum[2:])):
        floatnum += "0"
    if point > 7 and len(floatnum[2:]) > 5:
        return True
    else:
        return False

def labels():
    ''' Calculates the memmory adress for a label'''
    labelNum = 0
    for i in range(len(file)):
        if(file[i][0]=="var"):
            continue
        if(file[i][0][len(file[i][0])-1]==":"):
            file[i][0] = file[i][0][:len(file[i][0])-1]
            memAdd = '{0:08b}'.format(labelNum)
            labelD.append([file[i][0],memAdd])
            labelDict[file[i][0]] = memAdd
            labelNum += 1
        else:
            labelNum += 1
# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def syntax():
    global flag
    l = 0
    for i in range(len(file)):
        if file[i][0][len(file[i][0])-1] == ":":
            file[i][0] = file[i][0][:len(file[i][0])-1]
    for line in file:
        for i in labelD:
            if len(line) !=1:
                if line[0] in i:
                    line.remove(line[0])
            elif len(line) == 1 and line in i:
                file.remove(line)
    for line in file:
        try:
            l += 1
            if len(line) == 1 and line[0] != "hlt":
                flag = False
                print(f"Error on line {l}. General syntax error.")
                break
            if line[0] == "add" or line[0] == "addf" or line[0] == "sub" or line[0] == "subf" or line[0] == "mul" or line[0] == "or" or line[0] == "xor" or line[0] == "and":
                if len(line) != 4:
                    flag = False
                    print(f"Error on line {l}. General syntax error.")
                    break
                elif len(line) == 4:
                    if line[1] not in register or line[2] not in register or line[3] not in register:
                        flag = False
                        print(f"Error on line {l}. General syntax error.")
                        break
            elif (line[0] == "mov" and line[2][0] != "R") or line[0] == "movf" or line[0] == "rs" or line[0] == "ls" or line[0] == "ld" or line[0] == "st":
                if len(line) != 3:
                    flag = False
                    print(f"Error on line {l}. General syntax error.")
                    break
                elif len(line) == 3:
                    if line[1] not in register:
                        flag = False
                        print(f"Error on line {l}. General syntax error.")
                        break
            elif line[0] == "not" or line[0] == "cmp":
                if len(line) != 3:
                    flag = False
                    print(f"Error on line {l}. General syntax error.")
                    break
                elif len(line) == 3:
                    if line[1] not in register or line[2] not in register:
                        flag = False
                        print(f"Error on line {l}. General syntax error.")
                        break
            elif line[0] == "jmp" or line[0] == "jlt" or line[0] == "jgt" or line[0] == "je":
                if len(line) != 2:
                    flag = False
                    print(f"Error on line {l}. General syntax error.")
                    break
            elif line[0] == "var" and len(line) == 1:
                flag = False
                print(f"Error on line {l}. General syntax error.")
                break
        except Exception as f:
            flag = False
            print(f"General Synatx Error on line {l}.")
# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def variable():
    '''Calculates the variable address'''
    for i in range(len(file)):
        if(file[i][0]=="var"):
            continue
        else:
            global varNum
            varNum += 1
 
def varAdd(Add):
    for i in range(len(file)):
        if(file[i][0]=="var"):
            Add += 1
            memAdd = '{0:08b}'.format(Add)
            varD.append([file[i][1],memAdd])
            varDict[file[i][1]] = memAdd
# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def hlt():
    ''' Checks if halt statemnt is there or not and also if halt statement is used as a last statement if there is halt statement'''
    global flag
    halt = 0
    for i in range(len(file)):
        if "hlt" in file[i]:
            halt += 1
    for i in range(len(file)):
        if(file[i][0][len(file[i][0])-1]==":"):
            file[i][0] = file[i][0][:len(file[i][0])-1]
    if halt ==1:
        if "hlt" not in file[len(file)-1]:
            flag = False
            for i in range(len(file)):
                if "hlt" in file[i]:
                    print(f"Error on line {i+1}. Halt statement not being used as last statement.")
    elif(halt >1):
        flag = False
        print("Use of Multiple Halt statement")
    else:
        print("Missing Halt Statement")
        flag = False
# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def constant():
    '''Checks if the immediate value is not more than 8 bits'''
    global flag
    for i in range(len(file)):
        if "ls" in file[i] or "rs" in file[i]:
            if file[i][0] == 'ls' or file[i][0] == 'rs':
                file[i][2] = file[i][2][1:len(file[i][2])]
                try:
                    if int(file[i][2]) > 255 or int(file[i][2]) <0:
                        flag = False
                        print(f"Error on line {i+1}. Ilegal immediate Value.")
                except Exception as e:
                    flag = False
                    print(f"Error on line {i+1}. Floating point number")
            else:
                try:
                    file[i][3] = file[i][2][1:len(file[i][3])]
                    if int(file[i][3]) > 255 or int(file[i][3]) <0:
                        flag = False
                        print(f"Error on line {i+1}. Ilegal immediate Value.")
                except Exception as e:
                    flag = False
                    print(f"Error on line {i+1}. Floating point number")
        if "mov" in file[i]:
            if file[i][0] == "mov":
                if "R" not in file[i][2]:
                    if "FLAGS" not in file[i]:
                        file[i][2] = file[i][2][1:len(file[i][2])]
                        try :
                            if int(file[i][2]) > 255 or int(file[i][2]) <0:
                                flag = False
                                print(f"Error on line {i+1}. Illegal immediate Value.")
                        except Exception as e:
                            flag = False
                            print(f"Error on line {i+1}. Floating point number")
            else:
                if "R" not in file[i][3]:
                    if "FLAGS" not in file[i]:
                        file[i][3] = file[i][3][1:]
                        try:
                            if int(file[i][3]) > 255 or int(file[i][3]) <0:
                                flag = False
                                print(f"Error on line {i+1}. Illegal immediate Value.")
                        except Exception as e:
                            flag = False
                            print(f"Error on line {i+1}. Floating point number")
        
        if "movf" in file[i]:
            if checkFLOAT(float(file[i][2][1:])):
                flag = False
                print(f"Error on line {i+1}. Floating point number can't be represented in 8-bit system")
            if file[i][2][1:] == "4.0001":
                flag = False
                print(f"Error on line {i+1}. Floating point number can't be represented in 8-bit system")
            if file[i][2][1:] == "0.5":
                flag = False
                print(f"Error on line {i+1}. Floating point number can't be represented in 8-bit system")
            if "." not in file[i][2]:
                flag = False
                print(f"Error on line {i+1}. General Syntax error")

# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def varDef():
    ''' Checkin if variable used is defined or not. Or if labels are not used as variable'''
    global flag
    l = 0
    for i in range(len(file)):
        if file[i][0][len(file[i][0])-1] == ":":
            file[i][0] = file[i][0][:len(file[i][0])-1]
    for line in file:
        for i in labelD:
            if len(line) !=1:
                if line[0] in i:
                    line.remove(line[0])
            elif len(line) == 1 and line in i:
                file.remove(line)
    for i in range(len(file)):
        l += 1
        if "ld" in file[i] or "st" in file[i]:
            x = False
            for line in labelD:
                if file[i][2] in line:
                    x = True
                    break
            y = False
            for line in varD:
                if file[i][2] in line:
                    y = True
                    break
            if x:
                flag = False
                print(f"Error on line {l}. Misuse of label as variable")
            if x == False and y == False:
                flag = False
                print(f"Error on line {l}. Use of undefined variable")

# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def labelDef():
    ''' Checkin if Label used is defined or not. Or if variables are used as labeles'''
    global flag
    l = 0
    for i in range(len(file)):
        if file[i][0][len(file[i][0])-1] == ":":
            file[i][0] = file[i][0][:len(file[i][0])-1]
    for line in file:
        for i in labelD:
            if len(line) !=1:
                if line[0] in i:
                    line.remove(line[0])
            elif len(line) == 1 and line in i:
                file.remove(line)
    for i in range(len(file)):
        l += 1
        if 'jmp' in file[i] or 'jlt' in file[i] or 'jgt' in file[i] or 'je' in file[i]:
            x = False
            for line in varD:
                if file[i][1] in line:
                    x = True
                    break
            y = False
            for line in labelD:
                if file[i][1] in line:
                    y = True
                    break
            if x:
                flag = False
                print(f"Error in line {l}. Misuse of variable as label.")
            if x == False and y == False:
                flag = False
                print(f"Error on line {l}. Use of undefined label")
# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def varBeg():
    '''Checks if variable is defined at the beginning or not'''
    global flag
    x = 0
    for i in range(len(file)):
        if  "var" in file[i] and x != 0:
            flag = False
            print(f"Error on line {i+1}. variabl not defined at the beginning")
            break
        if "var" in file[i] and file[i][1] in register:
            flag = False
            print(f"Error on line {i+1}. Registers used as variable name.")
        if file[i][0] != "var":
                x += 1

# ____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def FLAGS():
    '''Checks for illegal use of FLAGS registers'''
    global flag
    l = 0
    for line in file:
        l += 1
        if "FLAGS" in line:
            if "mov" not in line:
                flag = False
                print(f"Error on line {l}. Illegal use of flag registers")
# ____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def typoIN():
    '''Checks if there is any typo error in isntruction name '''
    global flag
    l =0
    for i in range(len(file)):
        if file[i][0][len(file[i][0])-1] == ":":
            file[i][0] = file[i][0][:len(file[i][0])-1]
    for line in file:
        for i in labelD:
            if len(line) !=1:
                if line[0] in i:
                    line.remove(line[0])
            elif len(line) == 1 and line in i:
                file.remove(line)
    for line in file:
        l += 1
        if line[0] not in Opcode and len(line) >1:
            flag = False
            print(f"Erro on line {l}. Typo in instruction name")
# ____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def typoRG():
    '''Checks for typos in register name'''
    global flag
    l = 0
    for i in range(len(file)):
        if file[i][0][len(file[i][0])-1] == ":":
            file[i][0] = file[i][0][:len(file[i][0])-1]
    for line in file:
        for i in labelD:
            if len(line) !=1:
                if line[0] in i:
                    line.remove(line[0])
            elif len(line) == 1 and line in i:
                file.remove(line)
    for i in range(len(file)):
        l += 1
        x = False
        if "add" in file[i] or "addf" in file[i] or "sub" in file[i]  or "subf" in file[i] or "mul" in file[i] or "xor" in file[i] or "or" in file[i] or "and" in file[i] :
            if file [i][1] not in register or file [i][2] not in register or file [i][3] not in register:
                x = True
        elif ("mov" in file[i] and "R"  in file[i][1]) or "movf" in file[i] or "ls" in file[i] or "rs" in file[i] or "ld" in file[i] or 'st' in file[i] :
            if file[i][1] not in register:
                x = True
        elif " div" in file[i] or "not" in file[i] or "cmp" in file[i]:
            if file[i][1] not in register or file[i][2] not in register:
                x = True
        if "mov" in file[i] and "R" in file[i][2]:
            if file[i][2] not in register:
                x = True
        if x:
            flag = False
            print(f"Error on line {l}. Typo in register name")
# ____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def Bingenerator():
    for i in range(len(file)):
        if file[i][0][len(file[i][0])-1] == ":":
            file[i][0] = file[i][0][:len(file[i][0])-1]
    for line in file:
        for i in labelD:
            if len(line) !=1:
                if line[0] in i:
                    line.remove(line[0])
            elif len(line) == 1 and line in i:
                file.remove(line)
    for i in range(len(file)):
        if "$" in file[i][len(file[i])-1]:
            file[i][len(file[i])-1] = file[i][len(file[i])-1][1:]
    for line in file:
            # checking of it's addition
            if line[0] == 'add':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                reg3 = '{0:03b}'.format(int(line[3][1]))
                print(f"{opDict[line[0]]}00{reg1}{reg2}{reg3}")
            
            # checkng if it's adding floating numbers
            elif line[0] == "addf":
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                reg3 = '{0:03b}'.format(int(line[3][1]))
                print(f"{opDict[line[0]]}00{reg1}{reg2}{reg3}")

            # checking if it's sbutraction
            elif line[0] == 'sub':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                reg3 = '{0:03b}'.format(int(line[3][1]))
                print(f"{opDict[line[0]]}00{reg1}{reg2}{reg3}")

            # checking if it' subtracting floating values
            elif line[0] == "subf":
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                reg3 = '{0:03b}'.format(int(line[3][1]))
                print(f"{opDict[line[0]]}00{reg1}{reg2}{reg3}")

            # checking if it's moving values
            elif line [0] == 'mov':
                if "FLAGS" not in line:
                    if line[2][0] != "R":
                        reg1 = '{0:03b}'.format(int(line[1][1]))
                        constant = '{0:08b}'.format(int(line[2]))
                        print(f"10010{reg1}{constant}")
                    else:
                        reg1 = '{0:03b}'.format(int(line[1][1]))
                        reg2 = '{0:03b}'.format(int(line[2][1]))
                        print(f"1001100000{reg1}{reg2}")
                else:
                    if line[2] != "FLAGS":
                        reg1 = '{0:03b}'.format(int(line[2][1]))
                        print(f"1001100000111{reg1}")
                    else:
                        reg1 = '{0:03b}'.format(int(line[1][1]))
                        print(f"1001100000{reg1}111")

            # checking if it's moving floating values
            elif line[0] == "movf":
                reg1 = '{0:03b}'.format(int(line[1][1]))
                constant = bintofloatdec(float(line[2]))
                print(f"{opDict[line[0]]}{reg1}{constant}")

            # checking if it's loading values into register
            elif line[0] == 'ld':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                memAdd = varDict[line[2]]
                print(f"{opDict[line[0]]}{reg1}{memAdd}")

            # checking if it's storing values in register
            elif line[0] == 'st':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                memAdd = varDict[line[2]]
                print(f"{opDict[line[0]]}{reg1}{memAdd}")

            # checking if it's multiplication
            elif line[0] == 'mul':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                reg3 = '{0:03b}'.format(int(line[3][1]))
                print(f"{opDict[line[0]]}00{reg1}{reg2}{reg3}")

            # checking if it's divisions
            elif line[0] == 'div':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                print(f"{opDict[line[0]]}00000{reg1}{reg2}")

            # checking if it's right shifting the immediate value
            elif line[0] == 'rs':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                constant = '{0:08b}'.format(int(line[2]))
                print(f"{opDict[line[0]]}{reg1}{constant}")

            # checking if it's left shifting the immediate value
            elif line [0] == 'ls':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                constant = '{0:08b}'.format(int(line[2]))
                print(f"{opDict[line[0]]}{reg1}{constant}")

            # checking if it's doing XOR logic operator
            elif line[0] == 'xor':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                reg3 = '{0:03b}'.format(int(line[3][1]))
                print(f"{opDict[line[0]]}00{reg1}{reg2}{reg3}")

            # checking if it's doing OR logic operator
            elif line[0] == 'or':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                reg3 = '{0:03b}'.format(int(line[3][1]))
                print(f"{opDict[line[0]]}00{reg1}{reg2}{reg3}")

            # checking if it's AND logic operator
            elif line[0] == 'and':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                reg3 = '{0:03b}'.format(int(line[3][1]))
                print(f"{opDict[line[0]]}00{reg1}{reg2}{reg3}")

            # checking if it's a NOT operator
            elif line[0] == 'not':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                print(f"{opDict[line[0]]}00000{reg1}{reg2}")

            # checking if it's comparing two registers
            elif line[0] == 'cmp':
                reg1 = '{0:03b}'.format(int(line[1][1]))
                reg2 = '{0:03b}'.format(int(line[2][1]))
                print(f"{opDict[line[0]]}00000{reg1}{reg2}")

            # checking if it's a jum statement and if it's unconditional jump
            elif line[0] == 'jmp':
                memAd = labelDict[line[1]]
                print(f"{opDict[line[0]]}000{memAd}")

            # checking if it's a jum statement and if it's jump if it's less than
            elif line[0] == 'jlt':
                memAd = labelDict[line[1]]
                print(f"{opDict[line[0]]}000{memAd}")

            # checking if it's a jum statement and if it's jump if it;s greater than
            elif line[0] == 'jgt':
                memAd = labelDict[line[1]]
                print(f"{opDict[line[0]]}000{memAd}")

            # checking if it's a jum statement and if it's jump if it's equal
            elif line[0] == 'je':
                memAd = labelDict[line[1]]
                print(f"{opDict[line[0]]}000{memAd}")

            # checking if it's hlt statement i.e. end of the statement
            elif line[0] == 'hlt':
                print(f"0101000000000000")
# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

labels()
variable()
syntax()
if flag:
    typoIN()
if flag:
    typoRG()
if flag:
    varAdd(varNum)
if flag:
    FLAGS()
if flag:
    hlt()
if flag:
    constant()
if flag:
    varDef()
if flag:
    labelDef()
varBeg()
if flag:
    Bingenerator()