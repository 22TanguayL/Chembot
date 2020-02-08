import logging, sys, cmd
import csv, re, random

GREETINGS = ["Hello.","G'day!","¡Hola!","Welcome!","Hi!","What’s up?", "Hey homie!","Salutations.",
             "Greetings.", "Hey!", "'Sup!","Howdy!","G'day mate!", "Wazzzzzup!!!"]

DEBUG = False
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
        if DEBUG: print ("name = " + self.name)
        return (self.name)
        #returns wanted variable(s)
    
    def getSymbol(self):
        if DEBUG: print ("symbol = " + self.symbol)
        return (self.symbol)
        #returns wanted variable(s)
    
    def getAtomicMass(self):
        if DEBUG: print ("atomic mass = " + str(self.atomic_mass))
        return float(self.atomic_mass)
        #returns wanted variable(s)
    
    def getAtomicNumber(self):
        if DEBUG: print ("atomic number = " + str(self.atomic_number))
        return int(self.atomic_number)
        #returns wanted variable(s)
    
    def getIonicCharge(self):
        if self.ionic_charge is not None:
            if DEBUG: print ("ionic charge = " + str(self.ionic_charge))
            return int(self.ionic_charge)
        else:
            if DEBUG: print ("ionic charge unclear")
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
        if DEBUG:
            if self.name == "Unknown":
                print ("Molar Mass of " + str(self.symbols) + " = " + str(atomicMass) + "g/mol")
            else:
                print ("Molar Mass of " + str(self.name) + " = " + str(atomicMass) + "g/mol")

        return atomicMass
        #calls the splitcompound function

    def getSymbols(self):
        return self.symbols
    def getCharge(self):
        charge = 0
        for element in self.elements:
            s = element.getSymbol()
            j = element.getIonicCharge()
            if j is None:
                if DEBUG: print ("Charge cannot be properly taken")
                return None
            else:
                charge += int(j)
        if DEBUG:
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
            if DEBUG: print (char + " is a number")
            numbers.append(char)
        else:
            if DEBUG: print (char + " is a letter")
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
        return c.getMolarMass()
    except KeyError:
        return "ERROR: Input unreadable, check capitalization"
    return

def ionicCharge(arg):
    try:
        c = Compound(arg)
        return(str(c.getCharge()))
    except KeyError:
        return "ERROR: Input unreadable, check capitalization"

# 2Fe + NH3 -> 3FH + N2
# 55g FH 3 1 NH3
# stoichGramsToGrams grams=54 sub1=Fe molRatio1 mol2 HFe
def stoichGramsToGrams(grams1, substance1, mol1 ,mol2 ,substance2):
    #grams[i] = mass of substance [i] input
    #molMass[i] = calculate for substance [i]
    #molRatio = mol1 / mol2
    #grams[2] = grams[1] / (molmass[1] / molratio) * molMass[2]
    #find molMass1
    compound1 = Compound(substance1)
    if DEBUG: print("compound1 = " + str(compound1))
    molMass1 = compound1.getMolarMass()
    if DEBUG: print("molMass1 = " + str(molMass1))
    numMoles1 = grams1 / molMass1
    if DEBUG: print("numMoles1 = " + str(numMoles1))
    molRatio = (mol1 / mol2)
    if DEBUG: print("molRatio = " + str(molRatio))
    numMoles2 = numMoles1 / (molRatio)
    if DEBUG: print("numMoles2 = " + str(numMoles2))
    compound2 = Compound(substance2)
    if DEBUG: print("compound2 = " + str(compound2))
    molMass2 = compound2.getMolarMass()
    if DEBUG: print("molMass2 = " + str(molMass2))
    grams2 = numMoles2 * molMass2
    return grams2
    
def stoichMolesToMoles(numMoles1, substance1, mol1, substance2, mol2):
    compound1 = Compound(substance1)
    if DEBUG: print("compound1 = " + str(compound1))
    molRatio = (mol1 / mol2)
    if DEBUG: print("molRatio = " + str(molRatio))
    numMoles2 = numMoles1 / (molRatio)
    if DEBUG: print("numMoles2 = " + str(numMoles2))
    return numMoles2

def stoichMolesToGrams(numMoles1, substance1, mol1 ,mol2 ,substance2):
    compound1 = Compound(substance1)
    if DEBUG: print("compound1 = " + str(compound1))
    molRatio = (mol1 / mol2)
    if DEBUG: print("molRatio = " + str(molRatio))
    numMoles2 = numMoles1 / (molRatio)
    if DEBUG: print("numMoles2 = " + str(numMoles2))
    compound2 = Compound(substance2)
    if DEBUG: print("compound2 = " + str(compound2))
    molMass2 = compound2.getMolarMass()
    if DEBUG: print("molMass2 = " + str(molMass2))
    grams2 = numMoles2 * molMass2
    return grams2

def stoichGramsToMoles(grams1, substance1, mol1 ,mol2 ,substance2):
    compound1 = Compound(substance1)
    if DEBUG: print("compound1 = " + str(compound1))
    molMass1 = compound1.getMolarMass()
    if DEBUG: print("molMass1 = " + str(molMass1))
    numMoles1 = grams1 / molMass1
    if DEBUG: print("numMoles1 = " + str(numMoles1))
    molRatio = (mol1 / mol2)
    if DEBUG: print("molRatio = " + str(molRatio))
    numMoles2 = numMoles1 / (molRatio)
    if DEBUG: print("numMoles2 = " + str(numMoles2))
    return numMoles2

class UI(cmd.Cmd):
    intro = str(random.choice(GREETINGS) + " Welcome to Leon's Chembot. Type 'help' for help")
    prompt = "Cmd>"
    file = None
    def do_ionic_charge(self, arg):
        'get ionic charge of an element or compound. Ex: ionic_charge C6H12O6'
        print(ionicCharge(arg))
    def do_mass(self, arg):
        'get mass of an element or compound. Ex: mass C6H12O6'
        print(mass(arg))
    def do_stoichg2g(self, arg):
        'apply stoichiometry to get grams of 1 substance from grams of another in an equation'
        grams1 = float(input("grams of first substance: "))
        substance1 = input("first substance symbols: ")
        mol1 = int(input("moles of substance 1 in mol ratio: "))
        mol2 = int(input("moles of substance 2 in mol ratio: "))
        substance2 = input("second  substance symbols: ")
        compound2 = Compound(substance2)
        grams2 = stoichGramsToGrams(grams1, substance1, mol1 ,mol2 ,substance2)
        print(str(grams2) + " grams of " + str(compound2.getSymbols()))
    def do_stoichg2m(self, arg):
        'apply stoichiometry to get moles of 1 substance from grams of another in an equation'
        grams1 = float(input("grams of first substance: "))
        substance1 = input("first substance symbols: ")
        mol1 = int(input("moles of substance 1 in mol ratio: "))
        mol2 = int(input("moles of substance 2 in mol ratio: "))
        substance2 = input("second  substance symbols: ")
        compound2 = Compound(substance2)
        numMoles2 = stoichGramsToMoles(grams1, substance1, mol1 ,mol2 ,substance2)
        print(str(numMoles2) + " moles of " + str(compound2.getSymbols()))
    def do_stoichm2g(self, arg):
        'apply stoichiometry to get grams of 1 substance from moles of another in an equation'
        substance1 = input("first substance symbols: ")
        numMoles1 = int(input("moles of substance 1: "))
        mol1 = int(input("moles of substance 1 in mol ratio: "))
        mol2 = int(input("moles of substance 2 in mol ratio: "))
        substance2 = input("second  substance symbols: ")
        compound2 = Compound(substance2)
        grams2 = stoichMolesToGrams(numMoles1, substance1, mol1 ,mol2 ,substance2)
        print(str(grams2) + " grams of " + str(compound2.getSymbols()))
    def do_stoichm2m(self, arg):
        'apply stoichiometry to get moles of 1 substance from moles of another in an equation'
        substance1 = input("first substance symbols: ")
        numMoles1 = int(input("moles of substance 1: "))
        mol1 = int(input("moles of substance 1 in mol ratio: "))
        mol2 = int(input("moles of substance 2 in mol ratio: "))
        substance2 = input("second  substance symbols: ")
        compound2 = Compound(substance2)
        grams2 = stoichMolesToMoles(numMoles1, substance1, mol1, substance2, mol2)
        print(str(grams2) + " moles of " + str(compound2.getSymbols()))
    def do_info(self, arg):
        'get info about an element. Ex: info Fe'
        elementInfo(arg)
    def do_toggle_dev(self, arg):
        'get additional, behind the scenes info on what is going on in the program'
        global DEBUG
        if DEBUG:
            DEBUG = False
            print("dev mode deactivated")
        else:
            DEBUG = True
            print("dev mode activated")
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
