def step(gas):
    width = gas[0]['width']
    height = gas[1]['height']
    old = gas[2]['state']
    
    def wall(cell):
        return cell
        
    def reverse(direction):
        if direction is "u":
            return "d"
        elif direction is "d":
            return "u"
        elif direction is "r":
            return "l"
        elif direction is "l":
            return "r"
        
    
        
    return 0