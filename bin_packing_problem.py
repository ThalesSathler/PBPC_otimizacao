#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import pprint
import copy
pp = pprint.PrettyPrinter(indent=2)


# In[2]:


# get_ipython().run_line_magic('load_ext', 'ipython_unittest')


# # Bin Packing Problem with Conflicts

# ### Algorithm 1: ILS para o PBPC (KLB, ItBL) 
# 
# ```
# S ← ConstroiSoluçãoInicial();
# K ← Número de bins em S;
# enquanto K ≥ KLB and S é viável, faça: 
#   ReduzNúmeroBins(S);
#   K ← K − 1;
#   ItPERT ← 0;
#   enquanto ItPERT ≤ ItMAX and S não é viável, faça: 
#     S ← BuscaLocal(S);
#     S ← EjectionChains(S);
#     se ItBL sucessivas BL e EC sem melhora entao˜
#       S ← Perturbação(S);
#       ItPERT ← ItPERT + 1;
#       ItBL ← 0;
#       fim se
#     fim enquanto
# fim enquanto
# ```

# ## Utilidades

# In[3]:


def get_lower_limit(bin_total_space, fixtures):
    total_size = 0
    for fixture in fixtures:
        total_size += fixture["value"]
    
    lower_limit = total_size / bin_total_space
    
    if lower_limit > int(lower_limit):
        lower_limit = int(lower_limit) + 1

    return lower_limit


# In[4]:


def has_conflict(conflicts, item, bins):
    for item_bin in bins["itens"]:
        if item_bin["color"] in conflicts[str(item["color"])]:
            return True
    return False


# In[5]:


def is_solution_viable(solution, BIN_TOTAL_SPACE, conflicts):
    for bins in solution:
        if bins["space_left"] < 0:
            return False
        for item in bins["itens"]:
            if has_conflict(conflicts, item, bins):
                return False
    return True


# In[56]:


def relocate(bin_left, bin_right):
    def objective_function(bin_left, bin_right, item):
        return abs(bin_left["space_left"] + item["value"]) + abs(bin_right["space_left"] - item["value"])
    
    new_left_bin = copy.deepcopy(bin_left)
    new_right_bin = copy.deepcopy(bin_right)
    random.shuffle(new_left_bin["itens"])
    
    best_choice = abs(new_left_bin["space_left"]) + abs(new_right_bin["space_left"])
    for item in new_left_bin["itens"]:
        if len(new_left_bin["itens"]) > 1:
            test_choice = objective_function(new_left_bin, new_right_bin, item)
            if test_choice < best_choice:
                new_left_bin = remove_item_bin(new_left_bin, item)
                new_right_bin = set_item_bin(new_right_bin, item)
                best_choice = test_choice 
    return new_left_bin, new_right_bin


# In[80]:


def swap_item_bins(left_bin, right_bin, left_item, right_item):
    right_bin = remove_item_bin(right_bin, right_item)
    left_bin = remove_item_bin(left_bin, left_item)
    right_bin = set_item_bin(right_bin, left_item)
    left_bin = set_item_bin(left_bin, right_item)
    return left_bin, right_bin


# In[81]:


def swap(old_bin_left, old_bin_right):
    def objective_function(bin_left, bin_right, left_item, right_item):
        return abs(new_left_bin["space_left"] + left_item["value"] - right_item["value"]) + abs(new_right_bin["space_left"] + right_item["value"] - left_item["value"])
    
    new_left_bin = old_bin_left
    new_right_bin = old_bin_right
    best_choice = abs(new_left_bin["space_left"]) + abs(new_right_bin["space_left"])
    for item_bin_left in new_left_bin["itens"]:
        for item_bin_right in new_right_bin["itens"]:
            test_choice = objective_function(new_left_bin, new_right_bin, item_bin_left, item_bin_right)
            if test_choice < best_choice:
                best_choice = test_choice 
                new_left_bin, new_right_bin = swap_item_bins(new_left_bin, new_right_bin, item_bin_left, item_bin_right)    
                break
        
    return new_left_bin, new_right_bin


# In[8]:


def reduce_bins(bins):    
    bin_choiced = random.choice(bins)
    bins.remove(bin_choiced)
    number_bins = len(bins)
    for item in bin_choiced["itens"]:
        index_random = random.randint(0, number_bins - 1)
        set_item_bin(bins[index_random], item)
    return bins


# In[9]:


def is_bin_avaliable(bins, item, conflicts):
    return bins["space_left"] >= item["value"] and has_conflict(conflicts, item, bins) == False


# In[10]:


def set_item_bin(bin, item):
    bin["itens"].append(item)
    bin["space_left"] = bin["space_left"] - item["value"]
    return bin


# In[11]:


def remove_item_bin(bin, item):
    bin["space_left"] = bin["space_left"] + item["value"]
    bin["itens"].remove(item)    
    return bin


# In[12]:


def is_bin_conflicted(conflicts, bins):
    for item in bins["itens"]:
        if has_conflict(conflicts, item, bins):
            return True
    return False


# ## Algoritmo de construção

# In[13]:


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


# ## Busca Local

# In[88]:


def local_search(solution):
    random.shuffle(solution)
    for i in range(1,len(solution)):
        # if (solution[i-1]["space_left"] < 0 or solution[i]["space_left"] < 0):
        swap_left_bin, swap_right_bin = swap(solution[i-1], solution[i])
        relocate_left_bin, relocate_right_bin = relocate(solution[i-1], solution[i])
        if abs(swap_left_bin["space_left"]) + abs(swap_right_bin["space_left"]) <= abs(relocate_left_bin["space_left"]) + abs(relocate_right_bin["space_left"]):
            solution[i-1], solution[i] = swap_left_bin, swap_right_bin
        else:
            solution[i-1], solution[i] = relocate_left_bin, relocate_right_bin
    return solution


# ## Ejection Chains

# In[15]:


def calculate_removal_cost(bin, item):
    if item in bin["itens"]:
        return (bin["space_left"] + item["value"]) - bin["space_left"]

def calculate_swap_cost(bin, item_left, item_right):
    if item_right in bin["itens"]:
        return ((bin["space_left"] + item_right["value"]) - item_left["value"]) - bin["space_left"]
    else:
        raise Exception('item not in bin')
    
def calculate_insertion_cost(bin, item):
    return bin["space_left"] - (bin["space_left"] + item["value"])


# In[17]:


def chain_ejections(solution, decisions):
    for movement in decisions:
        if movement["method"] == 'REMOVAL':
            solution[movement["bin"]] = remove_item_bin(solution[movement["bin"]], movement["item"])
        if movement["method"] == 'INSERTION':
            solution[movement["bin"]] = set_item_bin(solution[movement["bin"]], movement["item"])
        if movement["method"] == 'SWAP':
            solution[movement["bin"]], solution[movement["bin"]-1] = swap_item_bins(solution[movement["bin"]], solution[movement["bin"]-1], movement["swap_for"], movement["item"])
    return solution


# In[18]:


def eject(start_point, solution, index):
    def make_decision(cost, item, method, bin, swap_for=None):
        return {"cost": cost, "item": item, "method": method, "bin": bin, "swap_for": swap_for}
    decision = dict()
    if start_point == "vSource":
        for item in solution[index]['itens']:
            removal_cost = calculate_removal_cost(solution[index], item)
            if "cost" in decision and removal_cost < decision["cost"]:
                decision = make_decision(removal_cost, item, 'REMOVAL', index)
            else:
                decision = make_decision(removal_cost, item, 'REMOVAL', index)
                
    else:
        insertion_cost = calculate_insertion_cost(solution[index], start_point)
        decision = make_decision(insertion_cost, start_point, 'INSERTION', index)
        for item in solution[index]['itens']:
            swap_cost = calculate_swap_cost(solution[index], start_point, item)
            if swap_cost < decision["cost"]:
                decision = make_decision(swap_cost, start_point, 'SWAP', index, swap_for=item)
    
    return decision


# In[19]:


def ejection_chains(solution):
    new_solution = solution
    random.shuffle(new_solution)
    decisions = []
    bin_index = 0
    while bin_index < len(new_solution):
        if bin_index == 0 or len(decisions) <= 0:
            if len(new_solution[bin_index]["itens"]) <= 1:
                bin_index += 1
                continue
            decisions.append(eject("vSource", new_solution, bin_index))
            bin_index += 1
        elif decisions[-1]["method"] == "INSERTION":
            if len(new_solution[bin_index-1]["itens"]) <= 1:
                bin_index += 1
                continue
            decisions.append(eject("vSource", new_solution, bin_index-1))
        else:
            decisions[-1]["item"]
            decisions.append(eject(decisions[-1]["item"], new_solution, bin_index))
            bin_index += 1
            
    new_solution = chain_ejections(new_solution,decisions)
    return new_solution

            


# # Solução

# In[20]:


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


# In[77]:


def iterated_local_search():
    
    BIN_TOTAL_SPACE = 10
    MAX_PERTUBATION = 30
    MAX_LOCAL_SEARCH = 100

    conflicts = {
        "0":[2],
        "1":[],
        "2":[0]
    }
                    
    fixtures = [
                {"value":5, "color": 2},
                {"value":4, "color": 0},
                {"value":4, "color": 0},
                {"value":4, "color": 0},
                {"value":3, "color": 2},
                {"value":2, "color": 0},
                {"value":2, "color": 0},
                {"value":2, "color": 2},
                {"value":4, "color": 0},
                {"value":5, "color": 0},
                {"value":3, "color": 0},
                {"value":2, "color": 0},
              ]

    first_solution = first_fit_decreasing(fixtures, BIN_TOTAL_SPACE, conflicts)    
    min_bins_count = get_lower_limit(BIN_TOTAL_SPACE, fixtures)
    final_solution = first_solution
    new_solution = copy.deepcopy(first_solution)
    bins_count = len(final_solution)
    
    while (bins_count > min_bins_count and is_solution_viable(final_solution, BIN_TOTAL_SPACE, conflicts)):
        new_solution = reduce_bins(new_solution)
        bins_count -= 1
        pertubation_count = 0
        local_search_count = 0

        while (pertubation_count < MAX_PERTUBATION and not is_solution_viable(new_solution, BIN_TOTAL_SPACE, conflicts)):
            new_solution = local_search(new_solution)
            if(is_solution_viable(new_solution, BIN_TOTAL_SPACE, conflicts)): 
                break
            new_solution = ejection_chains(new_solution)
            
            if local_search_count >= MAX_LOCAL_SEARCH: 
                new_solution = perturbate(conflicts, new_solution)
                pertubation_count += 1
                local_search_count = 0

            local_search_count += 1
#             print("perturbações ", pertubation_count,"busca local ", local_search_count)

        #caso não ache uma solução com a busca e a pertubação ele para
        if(is_solution_viable(new_solution, BIN_TOTAL_SPACE, conflicts)): 
            final_solution = copy.deepcopy(new_solution)
        else:
            break

    
    pp.pprint(final_solution)


# In[91]:


iterated_local_search()


# In[ ]:





# In[ ]:




