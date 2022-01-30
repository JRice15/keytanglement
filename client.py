''' 
' Client.py
' Generates pairings and groupings for key generation
' Input json file name, length of key generation, output is filled in json file
'''
import sys
import random
import json

# A: 01, 23
# B: 02, 13
# C: 03, 12

# 00: phi+phi-
# 01: phi-phi+
# 10: psi+psi-
# 11: psi-psi+

# Values that correspond to pairings of 
pairings_list = [[[0, 1], [2, 3]], [[0, 2], [1, 3]], [[0, 3], [1, 2]]]

bell_state_grouping = [0, 1, 2, 3]



def generate_pairings_and_groupings(key_length):
    #start random generation
    random.seed() #uses system time
    pairings = []
    groupings = []

    for _ in range(key_length):
        random_pair = pairings_list[random.randrange(0, len(pairings_list))]
        pairings.append(random_pair)
    
    for _ in range(key_length):
        random_grouping = bell_state_grouping[random.randrange(0, len(bell_state_grouping))]
        groupings.append(random_grouping)
    
    json_output = {
        "pairings": pairings,
        "groupings": groupings
    }

    return json_output


def main():
    #get inputs
    outfile = sys.argv[1]
    key_length = int(sys.argv[2])

    json_output = generate_pairings_and_groupings(key_length)

    # output 
    with open(outfile) as fp:
        json.dump(json_output, fp)


if __name__ == "__main__":
    main()

