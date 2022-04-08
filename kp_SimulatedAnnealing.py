#Simulated Annealing approach to the Kanpsack problem
#import python modules
import csv
import random
import math
import matplotlib.pyplot as plt

#convert csv to list
def csvConvertor():
    with open('knapsack.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

#generate a random solution to begin with 
def randomPacking(packed, unpacked, max_weight):
    data = csvConvertor() #convert CSV file
    weight = 0
    value = 0

    while weight <= max_weight:
        random_index = random.randint(1, (len(data)-1))
        item = data[random_index]

        if (weight + int(item[0])) <= max_weight:
            packed.append(item)
            data.remove(item)
            weight = weight + int(item[0])
            value = value + int(item[1])
        
        else:
            break
    
    for item in data:
        unpacked.append(item)
    
    return packed, unpacked

#find total weight
def totalWeight(packed):
    weight = 0
    for item in packed:
        weight = weight + int(item[0])

    return weight

#find total value
def totalValue(packed):
    value = 0
    for item in packed:
        value = value + int(item[1])

    return value

#randomly choose two items from the packed and unpacked lists
def randomItems(packed, unpacked):
    random_index = random.randint(1, (len(packed)-1))
    random_index_2 = random.randint(1, (len(unpacked)-1))
    item1 = packed[random_index]
    item2 = unpacked[random_index_2]

    return item1, item2

#check if the new  total weight of the packed list is okay after swapping
def weightCheck(item1, item2, packed, max_weight):
    weight = totalWeight(packed)
    new_weight = weight + int(item2[0]) - int(item1[0])
    if new_weight <= max_weight:
        return True
    else:
        return False

# determine whether or not the swap will be accepted or not
def calculateAcceptance(item1, item2, T, packed, max_weight):
    if weightCheck(item1, item2, packed, max_weight) == False:
        return False
    else:
        deltaE = int(item1[1]) - int(item2[1])
        if deltaE <= 0:
            return True
        else:
            prob_accept = math.exp(-1*deltaE/T)
            compare = random.random()
            #print(compare)                
            if compare <= prob_accept:
                return True
            else:
                return False

#display the data generated on a graph - this was used to generate data for the report only 
# by default a graph is not produced when the program is run to allow it to run multiple times and still not take too long
def displayData(packed, unpacked, x_list, value):
    print(packed)
    print(unpacked)
    print(totalWeight(packed))
    print(totalValue(packed))
    plt.plot(x_list, value)
    plt.ylabel("value")
    plt.xlabel("runtime")
    plt.title("Simulated Annealing")
   
    plt.show()

    return

#Simulated annealing algorithm - put all of the pieces together
def simulatedAnnealing(packed, unpacked, max_weight):
    
    randomPacking(packed, unpacked, max_weight)
    
    t = 1000 #lower case me
    T_min = 1
    alpha = 0.99
    value = [totalValue(packed)]
    x=0
    x_list = [0]
    
    while t > T_min:
        x = x + 1
        condition = True
        while condition == True:
            item1, item2 = randomItems(packed, unpacked)
            acceptance = calculateAcceptance(item1, item2, t, packed, max_weight)
            if acceptance == True:
                unpacked.remove(item2)
                packed.remove(item1)
                packed.append(item2)
                unpacked.append(item1)
                condition = False
            else:
                condition = True

        t = alpha * t #temp decreased
        value.append(totalValue(packed))
        x_list.append(x)

    #displayData(packed, unpacked, x_list, value)

# use this function to run simulated annealing process multiple times and thus ivestigate random initial solutions of different size
# the reason behind this is discussed in the report in more detail

def repeatSimulatedAnnealing(results, repeats):

    max_value_index = 0


    for i in range(repeats):
        packed = []
        unpacked = []
        max_weight = 1500
        simulatedAnnealing(packed, unpacked, max_weight)
        results.append([packed.copy(), totalValue(packed), totalWeight(packed)])
        
        if i > 0 and results[i][1] > results[i-1][1]:

            max_value_index = i   

    #print out data 
    print("The optimal packing is:")
    print(results[max_value_index][0])
    print("This has value:")
    print(results[max_value_index][1])
    print("This has weight:")
    print(results[max_value_index][2])
     


#call the function written above
results = []
repeatSimulatedAnnealing(results, 5)
