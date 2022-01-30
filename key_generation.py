'''
' Uses output of quantum computation to generate key using Alice and Bob's pairings and groupings
' Classical communication from architecture
'''
import sys
import json
import random

alice_correct_pairings = []
alice_correct_groupings = []

bob_correct_pairings = []
bob_correct_groupings = []

def open_file(filename, mode):
    try:
        fp = open(filename, mode)
        return fp
    except Exception as e:
        print("Error opening file: ", e)
        exit(1)

def get_correct_measurements(alice_json, bob_json):
    indices = alice_json["correct_measurements"]
    alice_initial_pairings = alice_json["pairings"]
    alice_initial_groupings = alice_json["groupings"]

    bob_initial_pairings = bob_json["pairings"]
    bob_initial_groupings = bob_json["groupings"]
        #use quantum measurements to get correct values
    for i in indices:
        alice_correct_pairings.append(alice_initial_pairings[i])
        alice_correct_groupings.append(alice_initial_groupings[i])
        bob_correct_pairings.append(bob_initial_pairings[i])
        bob_correct_groupings.append(bob_initial_groupings[i])
    
def check_for_eavesdropper(correction_bits):
        #check random bits according to the number passed in the command line
    #to see if there has 
    random.seed()
    for _ in range(correction_bits):
        check_index = random(0, len(alice_correct_pairings))
        if (alice_correct_pairings[check_index] == bob_correct_pairings[check_index]
            and  alice_correct_groupings[check_index] == bob_correct_groupings[check_index]):
            #if the bits check out, we must remove from the key
            alice_correct_pairings.pop(check_index)
            alice_correct_groupings.pop(check_index)
            bob_correct_pairings.pop(check_index)
            bob_correct_groupings.pop(check_index)
            pass
        else:
            #there has been an eavesdropper, Alice and Bob's circuits do not match
            print("Error: attacker has entered the chat")
            exit(1)
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

    alice_fp = open_file(alice_fname, "r")
    bob_fp = open_file(bob_fname, "r")

    alice_json = json.load(alice_fp)
    bob_json = json.load(bob_fp)

    alice_fp.close()
    bob_fp.close()

    #Use QC output to determine matching outputs
    get_correct_measurements(alice_json, bob_json)

    #Use some correct measurements to check for an attacker
    check_for_eavesdropper(correction_bits)

    #Use correct measurements to generate codes INDIVIDUALLY
    alice_code = generate_code(alice_correct_groupings)
    bob_code = generate_code(bob_correct_groupings)

    #Send codes to users
    alice_fp = open_file(alice_fname, "w")
    bob_fp = open_file(bob_fname, "w")
    alice_json["code"] = alice_code
    bob_json["code"] = bob_code
    json.dump(alice_json, alice_fp)
    json.dump(bob_json, bob_fp)
    alice_fp.close()
    bob_fp.close()

    return

if __name__ == "__main__":
    main()






    

        


        
