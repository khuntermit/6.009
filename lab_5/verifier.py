import traceback

bag_list = [
  { (0,0), (1,0), (2,0) },  # vertical 3x1 bag
  { (0,0), (0,1), (0,2) },  # horizontal 1x3 bag
  { (0,0), (0,1), (1,0), (1,1) }, # square bag
  { (0,0), (1,0), (1,1) },  # L-shaped bag
  { (0,0), (0,1), (1,0), (2,0), (2,1) },  # C-shaped bag
  { (0,0), (0,1), (1,1), (2,0), (2,1) },  # reverse C-shaped bag
]

def verify(result, input_data, gold):
    if result[0] == 'error':
        return False,result[1]
    result = result[1]

    #print(result)

    ok = True
    end = False
    message = "looks good, yay!"
    try:
        # There may be multiple valid tilings, so strict equality is not useful.
        # Gold files store the _count_ of tiles to pack (None for impossible cases).

        if gold == False:
            ok = (result == None)
            if not ok:
                message = "Proposed a packing for an impossible tent!"

        elif result == None:
            ok = (gold == False)
            if not ok:
                message = "Failed to find a solution where one exists."

        elif type(result) != list:
            message = ("expected a list result :( " + str(result))
            ok = False

        else:
            # validate cover
            (rows,cols) = input_data["tent_size"]
            covered = input_data["rocks"]
            tent = [[0 for c in range(cols)]
                    for r in range(rows)]

            # mark rocks
            for r,c in input_data["rocks"]: tent[r][c] = 'r'

            # mark tents
            for bag in result:
                btype = bag.get("shape")
                anchor = bag.get("anchor")

                if btype is None or anchor is None:
                    ok = False
                    message = "Person dictionary missing 'anchor' or 'shape' key."
                    break

                if not isinstance(btype,int) or btype < 0 or btype > len(bag_list)-1:
                    ok = False
                    message = "Person shape not an int or out of range."
                    break

                if not isinstance(anchor,tuple) or len(anchor) != 2 or \
                   not isinstance(anchor[0],int) or not isinstance(anchor[1],int):
                    ok = False
                    message = "Person anchor not of the form (int,int)."
                    break

                if anchor[0] < 0 or anchor[0] >= rows or anchor[1] < 0 or anchor[1] >= cols:
                    ok = False
                    message = "Person anchor coords out of range."
                    break
                
                squares = [(anchor[0] + r, anchor[1] + c)
                           for r,c in bag_list[btype]]

                for (r,c) in squares:
                    if r < 0 or r >= rows or c < 0 or c >= cols:
                        ok = False
                        end = True
                        message = "One of your sleeping bags is not in the tent"
                        break
                    if tent[r][c] == "r":
                        ok = False
                        message = "Found a sleeping bag over a rock"
                        end = True
                        break
                    elif tent[r][c] == "b":
                        ok = False
                        end = True
                        message= "Found overlapping sleeping bags"
                        break
                    else:
                        tent[r][c] = "b"
                if end:
                    break

            # if still okay, check all squares filled
            if ok:
                if not all(tent[r][c] != 0
                           for c in range(cols)
                           for r in range(rows)):
                    ok = False
                    message = "Oops, there's an empty square."

    except:
        print(traceback.format_exc());
        ok = False
        message = "CRASHED! :(. See above for details"

    return (ok, message)
