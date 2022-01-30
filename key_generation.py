'''
' Uses output of quantum computation to generate key using Alice and Bob's pairings and groupings
' Classical communication from architecture
'''
import sys
import json
import random

from utils import AttackerError


def get_correct_measurements(alice_json, bob_json):
    indices = alice_json["correct_measurements"]
    alice_initial_pairings = alice_json["pairings"]
    alice_initial_groupings = alice_json["groupings"]

    bob_initial_pairings = bob_json["pairings"]
    bob_initial_groupings = bob_json["groupings"]

    alice_correct = {"pairings": [], "groupings": []}
    bob_correct = {"pairings": [], "groupings": []}

    #use quantum measurements to get correct values
    for i in indices:
        alice_correct["pairings"].append(alice_initial_pairings[i])
        alice_correct["groupings"].append(alice_initial_groupings[i])
        bob_correct["pairings"].append(bob_initial_pairings[i])
        bob_correct["groupings"].append(bob_initial_groupings[i])
    
    return alice_correct, bob_correct
    
def check_for_eavesdropper(alice_correct, bob_correct, correction_bits):
    #check random bits according to the number passed in the command line
    #to see if there has 
    random.seed()
    for _ in range(correction_bits):
        check_index = random.randrange(0, len(alice_correct["pairings"]))
        # print("Checking index {0} for consistency".format(check_index))
        if (alice_correct["pairings"][check_index] == bob_correct["pairings"][check_index]
            and  alice_correct["groupings"][check_index] == bob_correct["groupings"][check_index]):
            #if the bits check out, we must remove from the key
            alice_correct["pairings"].pop(check_index)
            alice_correct["groupings"].pop(check_index)
            bob_correct["pairings"].pop(check_index)
            bob_correct["groupings"].pop(check_index)
            pass
        else:
            #there has been an eavesdropper, Alice and Bob's circuits do not match
            raise AttackerError()
    return alice_correct, bob_correct


def generate_code(groupings):
    code = ""
    for i in groupings:
        if i == 0:
            code += "00"
        if i == 1:
            code += "01"
        if i == 2:
            code += "10"
        if i == 3:
            code += "11"
    return code


def main():
    #alice and bob's guesses have gone through a QC
    alice_fname = sys.argv[1]
    bob_fname = sys.argv[2]
    correction_bits = int(sys.argv[3]) #how many bits to check for attacker with

    with open(alice_fname, "r") as f:
        alice_json = json.load(f)
    with open(bob_fname, "r") as f:
        bob_json = json.load(f)

    #Use QC output to determine matching outputs
    alice_correct, bob_correct = get_correct_measurements(alice_json, bob_json)

    #Use some correct measurements to check for an attacker
    alice_correct, bob_correct = check_for_eavesdropper(alice_correct, bob_correct, correction_bits)

    #Use correct measurements to generate codes INDIVIDUALLY
    alice_json["code"] = generate_code(alice_correct["groupings"])
    bob_json["code"] = generate_code(bob_correct["groupings"])

    #Send codes to users
    with open(alice_fname, "w") as f:
        json.dump(alice_json, f)
    with open(bob_fname, "w"):
        json.dump(bob_json, f)


if __name__ == "__main__":
    main()






    

        


        
