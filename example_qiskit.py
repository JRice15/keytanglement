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

from qiskit import execute
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

from quantuminspire.credentials import get_basic_authentication
from quantuminspire.qiskit import QI

from utils import ROOT_DIR

print("Authenticating")
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

with open(ROOT_DIR+"qi-auth.json", "r") as f:
    auth = json.load(f)

project_name = 'Keytanglement'
authentication = get_basic_authentication(auth["email"], auth["pass"])
QI.set_authentication(authentication, QI_URL, project_name=project_name)
QI_BACKEND = QI.get_backend('QX single-node simulator')


'''
Builds a quantum circuit to perform the bases measurements
specified by each user
'''
def build_circuit(chosenBases):
    print("Building circuit...")
    qbits = len(chosenBases)
    q = QuantumRegister(qbits)
    c = ClassicalRegister(qbits)
    circuit = QuantumCircuit(q, c)

    # Set up initial Hadamard for qubit 0
    circuit.h(q[0])

    # CNOT all qubit pairs
    for i in range(qbits-1):
        circuit.cx(q[i], q[i+1])
    
    # Add in the chosen basis measurements for each user
    for i,basis in enumerate(chosenBases):
        if basis == "y": # SDG + H gate prepare qubit for y-basis measurement
            circuit.sdg(q[i])
            circuit.h(q[i])
        elif basis == "x": # H gate prepares qubit for x-basis measruement
            circuit.h(q[i])
        elif basis == "z": # z-basis measurement is the default
            pass
        else:
            raise ValueError("Invalid basis specified by user")
    
    print("Output results:")
    for i in range(qbits):
        circuit.measure(q[i], c[i])
        print("Qubit {0}: {1}".format(i, c[i]))

    print(c)

    
    print(circuit)
    return circuit

'''
Executes a provided quantum circuits and performs measurements
on each qubit
'''
def execute_circuit(circuit):
    print("Executing circuit...")

    qi_job = execute(circuit, backend=QI_BACKEND, shots=4096)
    qi_result = qi_job.result()
    histogram = qi_result.get_counts(circuit)
    print('\nState\tCounts')
    [print('{0}\t\t{1}'.format(state, counts)) for state, counts in histogram.items()]
    
    # Print the full state probabilities histogram
    probabilities_histogram = qi_result.get_probabilities(circuit)
    print('\nState\tProbabilities')
    [print('{0}\t\t{1}'.format(state, val)) for state, val in probabilities_histogram.items()]


def main():
    c = build_circuit(["z","y"])
    execute_circuit(c)


if __name__ == "__main__":
    main()

