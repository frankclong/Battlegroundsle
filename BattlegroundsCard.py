

class BattlegroundsCard:
    def __init__(self, id, name, tier, health, attack, minion_types):
        self.id = id,
        self.name = name,
        self.tier = tier,
        self.health = health,
        self.attack = attack,
        self.minion_types = minion_types
    
    def __init__(self, json):
        self.id = json['id']
        self.name = json['name']
        self.tier = json['battlegrounds']['tier']
        self.health = json['health']
        self.attack = json['attack']
        minion_types = []
        if 'minionTypeId' in json:
            minion_types.append(json['minionTypeId'])
            if 'multiTypeIds' in json:
                for multiTypeId in json['multiTypeIds']:
                    minion_types.append(multiTypeId)
        else:
            minion_types.append(-1) 
        self.minion_types = minion_types
        self.image_url = json['battlegrounds']['image']