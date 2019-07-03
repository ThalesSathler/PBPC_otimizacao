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
def relocate(bin_left, bin_right):
    random.shuffle(bin_left["itens"])
    for item in bin_left["itens"]:
        if bin_right["space_left"] - item["value"] >= 0:
            bin_left = remove_item_bin(bin_left, item)
            bin_right = set_item_bin(bin_right, item)
            break
    return bin_left, bin_right

def swap(bin_left, bin_right, bin_size):
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

def local_search(solution, bin_size):
    random.shuffle(solution)
    for i in range(1,len(solution)):
        if (solution[i-1]["space_left"] < 0 or solution[i]["space_left"] < 0):
            swap_left_bin, swap_right_bin = swap(solution[i-1], solution[i], bin_size)
            relocate_left_bin, relocate_right_bin = relocate(solution[i-1], solution[i])
            if swap_left_bin["space_left"] + swap_right_bin["space_left"] <= relocate_left_bin["space_left"] + relocate_right_bin["space_left"]:
            	solution[i-1], solution[i] = swap_left_bin, swap_right_bin
            else:
            	solution[i-1], solution[i] = relocate_left_bin, relocate_right_bin
    return solution

def is_bin_avaliable(bins, item, conflicts):
    return bins["space_left"] >= item["value"] and has_conflict(conflicts, item, bins) == False

def is_bin_conflicted(conflicts, bins):
    for item in bins["itens"]:
        if has_conflict(conflicts, item, bins):
            return True
    return False

def perturbate(conflicts, solution):
    new_solution = solution
    perturbated = False
    for index, bins in enumerate(new_solution):
        if is_bin_conflicted(conflicts,bins) or bins["space_left"] < 0:
            if index > 0:
                new_solution[index], new_solution[index-1] = relocate(bins, new_solution[index-1])
            else:
                new_solution[index], new_solution[index+1] = relocate(bins, new_solution[index+1])
            perturbated = True
            break
    if not perturbated:
        new_solution[0], new_solution[1] = relocate(new_solution[0], new_solution[1])
    return new_solution

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
    MAX_PERTUBATION = 10
    MAX_LOCAL_SEARCH = 10

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
        local_search_count = 0

        while (pertubation_count <= MAX_PERTUBATION and not is_solution_viable(new_solution, BIN_TOTAL_SPACE, conflicts)):
            new_solution = local_search(new_solution, BIN_TOTAL_SPACE)
            
            #TODO - Ejection
            
            if local_search_count >= MAX_LOCAL_SEARCH: 
            	new_solution = perturbate(conflicts, new_solution)
            	pertubation_count += 1
            	local_search_count = 0

            local_search_count += 1
            print("perturbações ", pertubation_count,"busca local ", local_search_count)

        #caso não ache uma solução com a busca e a pertubação ele para
        if(is_solution_viable(new_solution, BIN_TOTAL_SPACE, conflicts)): 
            solution = new_solution
        else:
            break

    print(solution)
        
bin_packing_resolve()