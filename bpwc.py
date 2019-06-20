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
            if bin_avaliable(bins, item, conflicts):
                bins["itens"].append(item)
                bins["space_left"] -= item["value"]
                inserted = True
                break
                
        if not inserted:
            solution.append({"itens":[item], "space_left":BIN_TOTAL_SPACE-item["value"]})
    return solution

def bin_avaliable(bins, item, conflicts):
    return bins["space_left"] >= item["value"] and hasConflict(conflicts, item, bins) == False

def reduce_bins(bins):    
    bin_choiced = random.choice(bins)
    bins.remove(bin_choiced)
    number_bins = len(bins)
    for item in bin_choiced["itens"]:
        index_random = random.randint(0, number_bins - 1)
        add_item_in_bin(bins[index_random], item)
    return bins
                
def hasConflict(conflicts, item, bins):
    for item_bin in bins["itens"]:
        if item_bin["color"] in conflicts[str(item["color"])]:
            return True
    return False

def get_lower_limit(bin_total_space, fixtures):
    total_size = 0
    for fixture in fixtures:
        total_size += fixture["value"]
    
    lower_limit = total_size / bin_total_space
    
    if lower_limit > int(lower_limit):
        lower_limit = int(lower_limit) + 1

    return lower_limit

def add_item_in_bin(bin, item):
    bin["itens"].append(item)
    bin["space_left"] = bin["space_left"] - item["value"]
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
    
    x = get_lower_limit(BIN_TOTAL_SPACE, fixture)

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
    
    BIN_TOTAL_SPACE = 5

    conflicts = {
        "0":[2],
        "1":[],
        "2":[0]
    }
                    
    fixtures = [
                {"value":5, "color": 0},
                {"value":4, "color": 0},
                {"value":3, "color": 0},
                {"value":2, "color": 2},
                {"value":2, "color": 0}
              ]

    inital_solution = first_fit_decreasing(fixtures, BIN_TOTAL_SPACE, conflicts)
    bins_count = len(inital_solution)
    min_bins_count = get_lower_limit(BIN_TOTAL_SPACE, fixtures)

    

    #while (bins_count >= min_bins_count and isSolutionViable(inital_solution, BIN_TOTAL_SPACE, conflicts)):
    reduce_bins(inital_solution)
        
bin_packing_resolve()