#Steepest ascent hill climb approach to knapsack problem
import csv
import random

#convert csv to list
def csvConvertor():
    with open('knapsack.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

#generate a random solution to begin with 
def randomPacking(packed, unpacked, max_weight):
    data = csvConvertor()
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

#randomly swap a weight for another if higher value
def weightSwap(packed, unpacked, max_weight):
    #generate items to be swapped 
    random_index = random.randint(1, (len(packed)-1))
    random_index_2 = random.randint(1, (len(unpacked)-1))
    item1 = packed[random_index]
    item2 = unpacked[random_index_2]
    weight = totalWeight(packed)
    new_weight = weight + int(item2[0]) - int(item1[0])

    #check that swap increase the total value and doesn't exceed total weight
    if int(item1[1]) < int(item2[1]) and new_weight <= max_weight:
        unpacked.remove(item2)
        packed.remove(item1)
        packed.append(item2)
        unpacked.append(item1)
        return True

    else:
        return False

#steepest ascent climb implementation  
def steepestAscentHillClimbRandom(packed, unpacked, max_weight):
    
    randomPacking(packed, unpacked, max_weight)
    counter = 1

    while counter <= 250:
        sucsess = weightSwap(packed, unpacked, max_weight)
        if sucsess == True:
            counter = 1
        else:
            counter += 1

    return 


# run steepest asent climb multiple times and select best result to acccount for solutions with a different number of items in the bag

def repeatSteepestAscentClimb(results, repeats):

    max_value_index = 0


    for i in range(repeats):
        packed = []
        unpacked = []
        max_weight = 1500
        steepestAscentHillClimbRandom(packed, unpacked, max_weight)
        results.append([packed.copy(), totalValue(packed), totalWeight(packed)])
        
        if i > 0 and results[i][1] > results[i-1][1]:

            max_value_index =i

    
    #print out the results
    print("The optimal path is:")
    print(results[max_value_index][0])
    print("This has value:")
    print(results[max_value_index][1])
    print("This has weight:")
    print(results[max_value_index][2])


#call the function written above
results = []
repeatSteepestAscentClimb(results, 5)
