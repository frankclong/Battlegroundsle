

class BattlegroundsCard:
    def __init__(self, id, name, tier, health, attack, minionTypes):
        self.id = id,
        self.name = name,
        self.tier = tier,
        self.health = health,
        self.attack = attack,
        self.minionTypes = minionTypes
    
    def __init__(self, json):
        self.id = json['id']
        self.name = json['name']
        self.tier = json['battlegrounds']['tier']
        self.health = json['health']
        self.attack = json['attack']
        minionTypes = []
        if 'minionTypeId' in json:
            minionTypes.append(json['minionTypeId'])
            if 'multiTypeIds' in json:
                for multiTypeId in json['multiTypeIds']:
                    minionTypes.append(multiTypeId)
        else:
            minionTypes.append(-1) 
        self.minionTypes = minionTypes
        