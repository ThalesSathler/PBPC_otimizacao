import random

def is_solution_viable(solution, BIN_TOTAL_SPACE, conflicts):
    for bins in solution:
        if bins["space_left"] < 0:
            return False
        for item in bins["itens"]:
            if has_conflict(conflicts, item, bins):
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
            if is_bin_avaliable(bins, item, conflicts):
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

def swap_bins(bin_left, bin_right, bin_size):
    for item_bin_left in bin_left["itens"]:
        for item_bin_right in bin_right["itens"]:
            # Verifica se o item da esquerda é menor e se o espaço no bin dele é maior
            if(item_bin_right["value"] > item_bin_left["value"]):
                if(item_bin_left["value"] + bin_left["space_left"] > item_bin_right["value"] + bin_right["space_left"]):
                    aux = item_bin_left
                    set_item_bin(bin_right, aux)
                    remove_item_bin(bin_left, item_bin_left)
                    aux = item_bin_right
                    set_item_bin(bin_left, aux)
                    remove_item_bin(bin_right, item_bin_right)
                    return bin_left, bin_right                 
        
    return bin_left, bin_right

def local_search(bins, bin_size):
    random.shuffle(bins)
    for i in range(1,len(bins)):
        if (bins[i-1]["space_left"] < 0 or bins[i]["space_left"] < 0):
            bins[i-1], bins[i] = swap_bins(bins[i-1], bins[i], bin_size)
    return bins

def is_bin_avaliable(bins, item, conflicts):
    return bins["space_left"] >= item["value"] and has_conflict(conflicts, item, bins) == False

def reduce_bins(bins):    
    bin_choiced = random.choice(bins)
    bins.remove(bin_choiced)
    number_bins = len(bins)
    for item in bin_choiced["itens"]:
        index_random = random.randint(0, number_bins - 1)
        set_item_bin(bins[index_random], item)
    return bins
                
def has_conflict(conflicts, item, bins):
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

def set_item_bin(bin, item):
    bin["itens"].append(item)
    bin["space_left"] = bin["space_left"] - item["value"]
    return bin

def remove_item_bin(bin, item):
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

    response = is_solution_viable(fixture, BIN_TOTAL_SPACE, conflicts)
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
    min_bins_count = get_lower_limit(BIN_TOTAL_SPACE, fixtures)
    bins_count = len(solution)   
    

    while (bins_count >= min_bins_count and is_solution_viable(solution, BIN_TOTAL_SPACE, conflicts)):
        new_solution = reduce_bins(solution)
        bins_count -= 1
        pertubation_count = 0

        while (pertubation_count <= MAX_PERTUBATION and not is_solution_viable(new_solution, BIN_TOTAL_SPACE, conflicts)):
            new_solution = local_search(new_solution, BIN_TOTAL_SPACE)
            #TODO - Ejection

            #TODO - Pertubação

        #caso não ache uma solução com a busca e a pertubação ele para
        if(is_solution_viable(new_solution, BIN_TOTAL_SPACE, conflicts)): 
            solution = new_solution
        else:
            break
        
bin_packing_resolve()