import pandas as pd

def readData(filePath):
    pathExt = filePath.split('.')
    ext = pathExt[1]
    
    if ext == 'csv':
        data = pd.read_csv(filePath)
    
    return(data)


def get_yn():
    loop = 1
    while loop:
        choice = input("Confirm ([Y]/N):")
        if choice in ['y', 'Y', '1', '']:
            return True
        elif choice in ['n', 'N', '0']:
            return False
        else:
            print("Invalid choice. Please try again!\n")

def findSowDensity():
    # do something
    sowDensity = 0
    
def promptUnits():
    print("Please select the units of measurement of the land in question:")
    print("\t(1) Cuerdas")
    print("\t(2) Hectares")
    print("\t(3) Square Kilometers")
    print("\t(4) Acres")
    print("\t(5) Square Miles")
    
    select = input("Enter a number between one and five: ")
    
    if (select == 1) or (select == '1') or (select == 'one'): # cuerdas to hectares
        cuerdas = input("Enter the # of cuerdas: ")
        hectares = unitsToHectares(1,cuerdas)
        
    elif (select == 2) or (select == '2') or (select == 'two'):
        hectares = input("Enter the # of hectares: ")
        
    elif (select == 3) or (select == '3') or (select == 'three'):
        kilos = input("Enter the # of square kilometers: ")
        hectares = unitsToHectares(3, kilos)
            
    elif (select == 4) or (select == '4') or (select == 'four'):
        acres = input("Enter the # of acres: ")
        hectares = unitsToHectares(4, acres)
                
    elif (select == 5) or (select == '5') or (select == 'five'):
        miles = input("enter the # of miles: ")
        hectares = unitsToHectares(5, miles)
        
    else:
        print("Invalid input. Try again.")
    
    return(hectares)

def unitsToHectares(tipo, units):
    
    """
    This function is utilized in user input function, but is also function-al within code.
    
    """
    if (tipo == 1) or (tipo == '1'): # cuerdas to hectares
        hectares = units * 0.3930395625
        #hectares * 0.393???
        
    elif (tipo == 2) or (tipo == '2'): # hectares to hectares
        hectares = units
        
    elif (tipo == 3) or (tipo == '3'): # sq km to hectares
        hectares = 100 * units
            
    elif (tipo == 4) or (tipo == '4'): # acres to hectares
        hectares = units / 2.471
                
    elif (tipo == 5) or (tipo == '5'): # sq miles to hectares
        hectares = units * 258.999
        
    return(hectares)


def hectaresToCuerdas(hectares: float = 1) -> float:
    """
    converts hectares to cuerdas, but also converts units with a /hectares denominator (e.g. trees per hectare)
    
    """
    cuerdas = hectares * 0.3930395625
    return(cuerdas)

