
def compare_tier(target, guess):
    if target.tier == guess.tier:
        return 0
    if target.tier > guess.tier:
        return 2
    else:
        return -2

def compare_health(target, guess):
    if target.health == guess.health:
        return 0
    if target.health > guess.health:
        return 2
    else:
        return -2
    
def compare_attack(target, guess):
    if target.attack == guess.attack:
        return 0
    if target.attack > guess.attack:
        return 2
    else:
        return -2

def compare_minion_types(target, guess, minion_type_dict):
    guess_types = guess.minionTypes
    target_types = target.minionTypes
    
    # Check for all 
    if minion_type_dict[target_types[0]] == 'All': 
        guess_type = guess_types[0]
        # match
        if guess_type == target_types[0]:
            return 0
        # none
        elif minion_type_dict[guess_type] == 'None':
            return 2
        # partial
        else:
            return 1
    elif minion_type_dict[guess_types[0]] == 'All': 
        target_type = target_types[0]
        if minion_type_dict[target_type] == 'None':
                return 2
        else:
            return 1
    
    match = True
    partial_match = False
    for minion_type in guess_types:
        if minion_type not in target_types:
            match = False
        else: 
            partial_match = True
    if match == True and len(guess_types) == len(target_types):
        return 0
    if partial_match:
        return 1
    else:
        return 2

# return dictionary of comparison results
def compare_cards(target, guess, minion_type_dict):
    response_dict = {}
    response_dict['Tier'] = compare_tier(target, guess)
    response_dict['Health'] = compare_health(target, guess)
    response_dict['Attack'] = compare_attack(target, guess)
    response_dict['Minion Type'] = compare_minion_types(target, guess, minion_type_dict)
    return response_dict
    
