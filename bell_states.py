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

print("Authenticating")
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

with open("qi-auth.json", "r") as f:
    auth = json.load(f)

project_name = 'Keytanglement'
authentication = get_basic_authentication(auth["email"], auth["pass"])
QI.set_authentication(authentication, QI_URL, project_name=project_name)
QI_BACKEND = QI.get_backend('QX single-node simulator')



def build_circuit(bases):
    print("Building circuit")
    qbits = len(bases)
    q = QuantumRegister(qbits)
    b = ClassicalRegister(qbits)
    circuit = QuantumCircuit(q, b)

    circuit.h(q[0])
    for i in range(qbits-1):
        circuit.cx(q[i], q[i+1])
    for i,basis in enumerate(bases):
        if basis == "y":
            circuit.sdg(q[i])
            circuit.h(q[i])
        elif basis == "x":
            ...
        elif basis == "z":
            circuit.h(q[i])
        else:
            raise ValueError("bruh")

    circuit.measure_all

    return circuit

def execute_circuit(circuit):
    print("Executing")
    qi_job = execute(circuit, backend=QI_BACKEND, shots=256)
    qi_result = qi_job.result()
    histogram = qi_result.get_counts(circuit)
    print('\nState\tCounts')
    [print('{0}\t\t{1}'.format(state, counts)) for state, counts in histogram.items()]
    # Print the full state probabilities histogram
    probabilities_histogram = qi_result.get_probabilities(circuit)
    print('\nState\tProbabilities')
    [print('{0}\t\t{1}'.format(state, val)) for state, val in probabilities_histogram.items()]


def main():
    c = build_circuit(["z", "z"])
    execute_circuit(c)


if __name__ == "__main__":
    main()

