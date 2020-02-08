import logging, sys, cmd
import csv, re, random

GREETINGS = ["Hello.","G'day!","¡Hola!","Welcome!","Hi!","What’s up?", "Hey homie!","Salutations.",
             "Greetings.", "Hey!", "'Sup!","Howdy!","G'day mate!", "Wazzzzzup!!!"]

#TODO LIST: Balance ionic charge of compound, balance equations, stoichiometry

class ElementMaster:
    def __init__(self):
        self.__elements = {}
        
    def getElement(self, arg):
        return self.__elements[arg]

    def addElement(self, element):
        self.__elements[element.name.lower()] = element
        self.__elements[element.symbol] = element
        self.__elements[str(element.atomic_number)] = element
        
class Element:
    def __init__(self, name, symbol, atomic_number, atomic_mass, ionic_charge=None,electronegativity=None,isMetal=True):
        self.name = name
        self.symbol = symbol
        self.atomic_number = int(atomic_number)
        self.atomic_mass = float(atomic_mass)
        self.ionic_charge = ionic_charge
        self.electronegativity = electronegativity
        self.isMetal = isMetal 
        #defines variables
        
    def getName(self):
        #print (self.name)
        return (self.name)
        #returns wanted variable(s)
    
    def getSymbol(self):
        #print (self.symbol)
        return (self.symbol)
        #returns wanted variable(s)
    
    def getAtomicMass(self):
        #print (self.atomic_mass)
        return float(self.atomic_mass)
        #returns wanted variable(s)
    
    def getAtomicNumber(self):
        #print (self.atomic_number)
        return int(self.atomic_number)
        #returns wanted variable(s)
    
    def getIonicCharge(self):
        if self.ionic_charge is not None:
            #print (self.ionic_charge)
            return int(self.ionic_charge)
        else:
            #print ("ionic charge unclear")
            return None
        #returns wanted variable(s) only when present
    def getIsMetal(self):
        return self.isMetal
    
    def getElectronegativity(self):
        return self.electronegativity
    
class Compound:
    def __init__(self, symbols, name="Unknown"):
        self.name = name
        self.symbols = symbols
        symbolList = splitcompound(self.symbols)
        self.elements = []
        for symbol in symbolList:
            elementSymbol, elementCount = splitelementandnum(symbol)
            element = elementMaster.getElement(elementSymbol)
            for i in range(elementCount):
                self.elements.append(element) 



        
    def getMolarMass(self):
        atomicMass = sum([e.getAtomicMass() for e in self.elements])
        if self.name == "Unknown":
            print ("Molar Mass of " + str(self.symbols) + " = " + str(atomicMass) + "g/mol")
        else:
            print ("Molar Mass of " + str(self.name) + " = " + str(atomicMass) + "g/mol")

        return atomicMass
        #calls the splitcompound function
    
    def getCharge(self):
        charge = 0
        for element in self.elements:
            s = element.getSymbol()
            j = element.getIonicCharge()
            if j is None:
                print ("Charge cannot be properly taken")
                return None
            else:
                charge += int(j)

        if self.name == "Unknown":
            print ("Charge of " + str(self.symbols) + " = " + str(charge))
        else:
            print ("Charge of " + str(self.name) + " = " + str(charge))
        return charge

def splitcompound(compound):
    compound = str(compound)
    e = re.sub( r"([A-Z])", r" \1", compound).split()
    #splits compound up
    #print(e)
    return e

def splitelementandnum(string):
    letters = []
    numbers = []
    for char in string:
        if char.isdigit():
            #print (char + " is a number")
            numbers.append(char)
        else:
            #print (char + " is a letter")
            letters.append(char)
            
    rletters = ''.join(letters)
    
    if numbers == []:
        numbers = 1
        
    else:
        numbers = int(''.join(numbers))
        
    #print ("there are " + str(numbers) + " of " + rletters)
    return (rletters, numbers)

def cumsum(listvar):
    s = 0
    #sets variable to 0
    for n in listvar:
        s += n
        #adds to variable
    return s
    #returns final sum

def helpMenu():
    print("'molar mass' - find molar mass of any compound or element")
    print("'ionic charge' - find ionic charge of an element or compound")
    print("'element info' - find information about any 1 element")
    return

def elementInfo(arg):
    try:
        e = elementMaster.getElement(arg)
        print("Name: " + e.getName())
        print("Symbol: " + e.getSymbol())
        print("Atomic Number: " + str(e.getAtomicNumber()))
        print("Average Atomic Mass: " + str(e.getAtomicMass()) + " amu")
        chrg = e.getIonicCharge()
        if chrg == None:
            chrg = "N/A"
        print("Ionic Charge: " + str(chrg))
        mtl = ""
        if e.getIsMetal() == False:
            mtl = "nonmetal"
        elif e.getIsMetal() == True:
            mtl = "metal"
        print(e.getName() + " is a " + str(mtl))
        print("")
    except KeyError:
        print ("ERROR: Input unreadable, check capitalization")
    return

def mass(arg):
    try:
        c = Compound(arg)
        c.getMolarMass()
        print("")
    except KeyError:
        print ("ERROR: Input unreadable, check capitalization")
    return

def ionicCharge(arg):
    try:
        c = Compound(arg)
        result = c.getCharge()
        print ("Ionic charge is " + str(result))
        print("")
    except KeyError:
        print ("ERROR: Input unreadable, check capitalization")
                
class UI(cmd.Cmd):
    intro = str(random.choice(GREETINGS) + " Welcome to Leon's Chembot. Type 'help' for help")
    prompt = "Cmd>"
    file = None
    def do_ionic_charge(self, arg):
        'get ionic charge of an element or compound. Ex: ionic_charge C6H12O6'
        ionicCharge(arg)
    def do_mass(self, arg):
        'get mass of an element or compound. Ex: mass C6H12O6'
        mass(arg)
    def do_info(self, arg):
        'get info about an element. Ex: info Fe'
        elementInfo(arg)
    def do_exit(self, arg):
        'Exit Chembot UI'
        print('Thank you for using Chembot')
        return True
    
FORMAT = '[%(asctime)s] %(message)s'
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format=FORMAT, datefmt='%H:%M:%S')

elementMaster = ElementMaster()
with open('data/elements.csv',newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    #creates 3 so that elements can be referenced by either name, symbol, or atomic number
    for row in csv_reader:
        if line_count == 0:
            logging.debug(f'Column names are {", ".join(row)}')
            line_count += 1
            #defines the titles of each row
        else:
            try:
                ionic_charge = int(row[4])
                logging.debug("%s: ionic charge = %d"%(row[0],int(row[4])))
            except ValueError:
                logging.debug("%s: no ionic charge found"%(row[0]))
                ionic_charge = None
                #makes elements without defined ionic charge without an ionic charge
            try:
                electronegativity = float(row[5])
                logging.debug("%s: electronegativity = %f"%(row[0],electronegativity))
            except ValueError:
                logging.debug("%s: no electronegativity found"%(row[0]))
                electronegativity = None
            logging.debug (row[6])
            is_metal = (int(row[6]) > 0) 
            logging.debug("%s: ismetal = %s"%(row[0],str(is_metal)))
                #makes elements without defined ionic charge without an ionic charge  
            element = Element(row[0].lower(),row[1],row[2],row[3],ionic_charge, electronegativity,is_metal)
            elementMaster.addElement(element)
            line_count += 1
    print(f'Processed {line_count} lines.')

#mainMenu()
if __name__ == '__main__':
    UI().cmdloop()
