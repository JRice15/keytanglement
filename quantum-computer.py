"""Example usage of the Quantum Inspire backend with the Qiskit SDK.

A simple example that demonstrates how to use the SDK to create
a circuit to create a Bell state, and simulate the circuit on
Quantum Inspire.

For documentation on how to use Qiskit we refer to
[https://qiskit.org/](https://qiskit.org/).

Specific to Quantum Inspire is the creation of the QI instance, which is used to set the authentication
of the user and provides a Quantum Inspire backend that is used to execute the circuit.

Copyright 2018-19 QuTech Delft. Licensed under the Apache License, Version 2.0.
"""
import os
import json
import sys

from qiskit import execute
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

from quantuminspire.credentials import get_basic_authentication
from quantuminspire.qiskit import QI

# print("Authenticating")
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

with open("qi-auth.json", "r") as f:
    auth = json.load(f)

project_name = 'Keytanglement'
authentication = get_basic_authentication(auth["email"], auth["pass"])
QI.set_authentication(authentication, QI_URL, project_name=project_name)
QI_BACKEND = QI.get_backend('QX single-node simulator')
qbits = 4

class Pairing:
    def __init__(self, pair1, pair2):
        self.bit0 = pair1[0]
        self.bit1 = pair1[1]
        self.bit2 = pair2[0]
        self.bit3 = pair2[1]


########################
# Generate Bell States #
########################
def phi_plus(bit0, bit1, qc):
    qc.h(bit0)
    qc.cx(bit0, bit1)

def phi_minus(bit0, bit1, qc):
    qc.x(bit0)
    qc.h(bit0)
    qc.cx(bit0, bit1)

def psi_plus(bit0, bit1, qc):
    qc.h(bit0)
    qc.x(bit1)
    qc.cx(bit0, bit1)

def psi_minus(bit0, bit1, qc):
    qc.h(bit0)
    qc.x(bit1)
    qc.z(bit0)
    qc.z(bit1)
    qc.cx(bit0, bit1)

#####################################
# Generate pair-entangling circuits #
#####################################
def circuit00(pairs):
    q = QuantumRegister(qbits)
    b = ClassicalRegister(qbits)
    qc = QuantumCircuit(q, b)

    phi_plus(q[pairs.bit0], q[pairs.bit1], qc)
    phi_minus(q[pairs.bit2], q[pairs.bit3], qc)
    print("Alice chose group 00")
    # print(qc)
    return qc, q

def circuit01(pairs):
    q = QuantumRegister(qbits)
    b = ClassicalRegister(qbits)
    qc = QuantumCircuit(q, b)

    phi_minus(q[pairs.bit0], q[pairs.bit1], qc)
    phi_plus(q[pairs.bit2], q[pairs.bit3], qc)
    print("Alice chose group 01")
    # print(qc)
    return qc, q

def circuit10(pairs):
    q = QuantumRegister(qbits)
    b = ClassicalRegister(qbits)
    qc = QuantumCircuit(q, b)

    psi_plus(q[pairs.bit0], q[pairs.bit1], qc)
    psi_minus(q[pairs.bit2], q[pairs.bit3], qc)
    print("Alice chose group 10")
    # print(qc)
    return qc, q

def circuit11(pairs):
    q = QuantumRegister(qbits)
    b = ClassicalRegister(qbits)
    qc = QuantumCircuit(q, b)

    psi_minus(q[pairs.bit0], q[pairs.bit1], qc)
    psi_plus(q[pairs.bit2], q[pairs.bit3], qc)
    print("Alice chose group 11")
    # print(qc)
    return qc, q

################################
# Generate Reverse Bell States #
################################
def phi_plus_reverse(bit0, bit1, qc):
    qc.cx(bit0, bit1)
    qc.h(bit0)

def phi_minus_reverse(bit0, bit1, qc):
    qc.cx(bit0, bit1)
    qc.h(bit0)
    qc.x(bit0)

def psi_plus_reverse(bit0, bit1, qc):
    qc.cx(bit0, bit1)
    qc.x(bit1)
    qc.h(bit0)

def psi_minus_reverse(bit0, bit1, qc):
    qc.cx(bit0, bit1)
    qc.z(bit1)
    qc.z(bit0)
    qc.x(bit1)
    qc.h(bit0)

#############################################
# Generate Reverse Pair-Entangling Circuits #
#############################################
def reverse_circuit00(pairs, q, qc):
    phi_plus_reverse(q[pairs.bit0], q[pairs.bit1], qc)
    phi_minus_reverse(q[pairs.bit2], q[pairs.bit3], qc)

def reverse_circuit01(pairs, q, qc):
    phi_minus_reverse(q[pairs.bit0], q[pairs.bit1], qc)
    phi_plus_reverse(q[pairs.bit2], q[pairs.bit3], qc)
    # print(qc)

def reverse_circuit10(pairs, q, qc):
    psi_plus_reverse(q[pairs.bit0], q[pairs.bit1], qc)
    psi_minus_reverse(q[pairs.bit2], q[pairs.bit3], qc)
    # print(qc)

def reverse_circuit11(pairs, q, qc):
    psi_minus_reverse(q[pairs.bit0], q[pairs.bit1], qc)
    psi_plus_reverse(q[pairs.bit2], q[pairs.bit3], qc)
    # print(qc)

def verify_circuit(qc):
    job = execute(qc, backend=QI_BACKEND, shots=256)
    result = job.result()
    histogram = result.get_counts(qc)

    # If Bob guessed Alice's qubit-pairs and Bell states correctly,
    # the final state of all qubits should be 0s
    state_list = list(histogram.keys())
    if (len(state_list) == 1 and state_list[0] == "0000"):
        return 1
    return 0

entangling_circuit_map = {0: circuit00, 1: circuit01, 2: circuit10, 3: circuit11}
reversal_circuit_map = {0: reverse_circuit00, 1: reverse_circuit01, 2: reverse_circuit10, 3: reverse_circuit11}

'''
The scripts receives a file containing json objects of qubit-pairs and group codes in order to
perform key generation. Qubit-pairs and group codes are associated based
on their indices within the list (qpair[k] is associated with groupcode[k]).
An element in the qubit-pair list consists of 2 pairs of 2 qubits in our 4 qubit system
(ex. [[q0, q3], [q1, q2]]). Each element in the group code list consists a group code that maps
to a given pair of Bell states (see README for mappings of group codes to Bell states). The Bell
states corresponding to the group code will be used to entangle the qubits in each pair of the 
corresponding qubit-pairs.

Ex. Input: qpair[k] = [ [q1, q2], [q0, q3] ]
           groupcode[k] = 00 
    
    Group code 00 -> Bell state pair [ phi+, phi- ]

    => q1 and q2 are entangled using the phi+ Bell circuit
    => q0 and q3 are entangled using the phi- Bell circuit
'''
def main(alice_fname, bob_fname):
    with open(alice_fname, "r") as f:
        alice_data = json.load(f)
    
    alice_qpairs = alice_data["pairings"]
    alice_groupcodes = alice_data["groupings"]
    f.close()

    with open(bob_fname, "r") as f:
        bob_data = json.load(f)

    bob_qpairs = bob_data["pairings"]
    bob_groupcodes = bob_data["groupings"]
    f.close()

    # Keeps track of the indices in Bob's list that were correct guesses
    correct_guesses = []

    for i in range(len(alice_qpairs)): # iterate over  qubit-pairs

        # Obtain both users' group codes
        alice_gc = alice_groupcodes[i]
        bob_gc = bob_groupcodes[i]

        qpairs = Pairing(alice_qpairs[i][0], alice_qpairs[i][1])

        # Build Alice's circuits based on her inputs
        qc, q = entangling_circuit_map[alice_gc](qpairs)

        qpairs = Pairing(bob_qpairs[i][0], bob_qpairs[i][1])

        # Run Bob's test circuits on top of Alice's input
        reversal_circuit_map[bob_gc](qpairs, q, qc)

        # Add the index to the list of correct guesses to return to the users
        if (verify_circuit(qc)):
            correct_guesses.append(i)

    alice_data["correct_measurements"] = correct_guesses
    bob_data["correct-measurements"] = correct_guesses
    with open(alice_fname, "w") as f:
        json.dump(alice_data, f)
    f.close()

    with open(bob_fname, "w") as f:
        json.dump(bob_data, f)
    f.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 quantum-computer.py alice_filename bob_filename")
        exit(1)
    
    main(sys.argv[1], sys.argv[2])