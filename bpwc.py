import random

def isSolutionViable(solution, BIN_TOTAL_SPACE, conflicts):
    for bins in solution:
        if bins["space_left"] < 0:
            return False
        for item in bins["itens"]:
            if hasConflict(conflicts, item, bins):
                return False
    return True

def first_fit_decreasing(itens, BIN_TOTAL_SPACE, conflicts):
    sortedItens = sorted(itens, key=lambda k: k["value"], reverse=True)
    solution = [] #array of bins
    for item in sortedItens:
        if len(solution) == 0:
            solution.append({"itens":[item], "space_left":BIN_TOTAL_SPACE-item["value"]})
            continue
        inserted = False
        for bins in solution:
            if isBinAvaliable(bins, item, conflicts):
                bins["itens"].append(item)
                bins["space_left"] -= item["value"]
                inserted = True
                break
                
        if not inserted:
            solution.append({"itens":[item], "space_left":BIN_TOTAL_SPACE-item["value"]})
    return solution

#TODO - fazer realocate olhando se há espaço vazio no outro bin
def realocate(bin_left, bin_right):
    return True

#TODO - verificar conflitos no swap
def swap_bins(bin_left, bin_right, bin_size):
    for item_bin_left in bin_left["itens"]:
        for item_bin_right in bin_right["itens"]:
            # Verifica se o item da esquerda é menor e se o espaço no bin dele é maior
            if(item_bin_right["value"] > item_bin_left["value"]):
                if(item_bin_left["value"] + bin_left["space_left"] > item_bin_right["value"] + bin_right["space_left"]):
                    aux = item_bin_left
                    setItemBin(bin_right, aux)
                    removeItemBin(bin_left, item_bin_left)
                    aux = item_bin_right
                    setItemBin(bin_left, aux)
                    removeItemBin(bin_right, item_bin_right)
                    return bin_left, bin_right                 
        
    return bin_left, bin_right

def local_search(bins, bin_size):
    random.shuffle(bins)
    for i in range(1,len(bins)):
        if (bins[i-1]["space_left"] < 0 or bins[i]["space_left"] < 0):
            bins[i-1], bins[i] = swap_bins(bins[i-1], bins[i], bin_size)
    return bins

def isBinAvaliable(bins, item, conflicts):
    return bins["space_left"] >= item["value"] and hasConflict(conflicts, item, bins) == False

def reduce_bins(bins):    
    bin_choiced = random.choice(bins)
    bins.remove(bin_choiced)
    number_bins = len(bins)
    for item in bin_choiced["itens"]:
        index_random = random.randint(0, number_bins - 1)
        setItemBin(bins[index_random], item)
    return bins
                
def hasConflict(conflicts, item, bins):
    for item_bin in bins["itens"]:
        if item_bin["color"] in conflicts[str(item["color"])]:
            return True
    return False

def getLowerLimit(bin_total_space, fixtures):
    total_size = 0
    for fixture in fixtures:
        total_size += fixture["value"]
    
    lower_limit = total_size / bin_total_space
    
    if lower_limit > int(lower_limit):
        lower_limit = int(lower_limit) + 1

    return lower_limit

def setItemBin(bin, item):
    bin["itens"].append(item)
    bin["space_left"] = bin["space_left"] - item["value"]
    return bin

def removeItemBin(bin, item):
    bin["space_left"] = bin["space_left"] + item["value"]
    bin["itens"].remove(item)    
    return bin

def test_first_fit():
    BIN_TOTAL_SPACE = 5

    conflicts = {
        "0":[2],
        "1":[],
        "2":[0]
    }
                    
    fixture = [
                {"value":5, "color": 0},
                {"value":4, "color": 0},
                {"value":3, "color": 0},
                {"value":2, "color": 2},
                {"value":2, "color": 0}
              ]
    
    solutionExpected = [
                        {"itens":[{"value":5, "color": 0}], "space_left": 0},
                        {"itens":[{"value":4, "color": 0}], "space_left": 1},
                        {"itens":[{"value":3, "color": 0},{"value":2, "color": 0}], "space_left": 0},
                        {"itens":[{"value":1, "color": 2}], "space_left": 4},
                     ]
    
    x = getLowerLimit(BIN_TOTAL_SPACE, fixture)

    S = first_fit_decreasing(fixture, BIN_TOTAL_SPACE, conflicts)
    assert S == solutionExpected
    print("Finalziado com sucesso")

def test_solution_viability_with_conflicts():
    BIN_TOTAL_SPACE = 5
    
    conflicts = {
        "0":[2],
        "1":[],
        "2":[0]
    }

    fixture = [
                {"itens":[{"value":5, "color": 0}], "space_left": 0},
                {"itens":[{"value":4, "color": 0}, {"value":1, "color": 2}], "space_left": 0},
                {"itens":[{"value":3, "color": 0},{"value":2, "color": 0}], "space_left": 0},
              ]

    response = isSolutionViable(fixture, BIN_TOTAL_SPACE, conflicts)
    assert response == False

def bin_packing_resolve():
    
    BIN_TOTAL_SPACE = 10
    MAX_PERTUBATION = 5

    conflicts = {
        "0":[2],
        "1":[],
        "2":[0]
    }
                    
    fixtures = [
                {"value":5, "color": 0},
                {"value":4, "color": 0},
                {"value":4, "color": 0},
                {"value":4, "color": 0},
                {"value":3, "color": 0},
                {"value":2, "color": 0},
                {"value":2, "color": 0},
                {"value":2, "color": 0},
                {"value":4, "color": 0}
              ]

    solution = first_fit_decreasing(fixtures, BIN_TOTAL_SPACE, conflicts)    
    min_bins_count = getLowerLimit(BIN_TOTAL_SPACE, fixtures)
    bins_count = len(solution)   
    

    while (bins_count >= min_bins_count and isSolutionViable(solution, BIN_TOTAL_SPACE, conflicts)):
        new_solution = reduce_bins(solution)
        bins_count -= 1
        pertubation_count = 0

        while (pertubation_count <= MAX_PERTUBATION and not isSolutionViable(new_solution, BIN_TOTAL_SPACE, conflicts)):
            new_solution = local_search(new_solution, BIN_TOTAL_SPACE)
            #TODO - Ejection

            #TODO - Pertubação

        #caso não ache uma solução com a busca e a pertubação ele para
        if(isSolutionViable(new_solution, BIN_TOTAL_SPACE, conflicts)): 
            solution = new_solution
        else:
            break
        
bin_packing_resolve()