# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from ibm_quantum_widgets import *

# qiskit-ibmq-provider has been deprecated.
# Please see the Migration Guides in https://ibm.biz/provider_migration_guide for more detail.
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Estimator, Session, Options

# Loading your IBM Quantum account(s)
service = QiskitRuntimeService(channel="ibm_quantum")

# Create the quantum circuit with 3 qubits and 3 classical bits
q = QuantumRegister(3, 'q')  # Quantum register
c0 = ClassicalRegister(1, 'c0')  # Classical register for Alice's qubit
c1 = ClassicalRegister(1, 'c1')  # Classical register for Bob's qubit
c2 = ClassicalRegister(1, 'c2')  # Classical register for the result
circuit = QuantumCircuit(q, c0, c1, c2)

# Prepare the initial state to be teleported
circuit.initialize([0, 1], q[0])  # Apply X gate to put in state |1>
circuit.barrier()

# Create an entanglement between Alice's and Bob's qubits
circuit.h(q[1])
circuit.cx(q[1], q[2])
circuit.barrier()

# Teleportation process
circuit.cx(q[0], q[1])
circuit.h(q[0])
circuit.barrier()

# Measure Alice's qubits and send the measurement results to Bob
circuit.measure(q[0], c0[0])
circuit.measure(q[1], c1[0])

# Apply corrective operations on Bob's qubit based on the measurement results
circuit.x(q[2]).c_if(c1, 1)
circuit.z(q[2]).c_if(c0, 1)

# Measure the teleported qubit
circuit.measure(q[2], c2[0])

# Visualize the circuit
print(circuit)
circuit_drawer(circuit, output='mpl')

# Simulate the circuit using the QASM simulator
simulator = Aer.get_backend('qasm_simulator')
job = execute(circuit, simulator, shots=1)
result = job.result()
teleported_state = result.get_counts(circuit)

# Print the teleported state
print("Teleported state:", teleported_state)

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute, IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library import QFT
import numpy as np

pi = np.pi

# provider = IBMQ.get_provider(hub='ibm-q')

backend = provider.get_backend('ibmq_qasm_simulator')

q = QuantumRegister(5,'q')
c = ClassicalRegister(5,'c')

circuit = QuantumCircuit(q,c)

circuit.x(q[4])
circuit.x(q[2])
circuit.x(q[0])
circuit.append(QFT(num_qubits=5, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False), q)
circuit.measure(q,c)
circuit.draw(output='mpl', filename='qft1.png')
print(circuit)

job = execute(circuit, backend, shots=1000)

job_monitor(job)

counts = job.result().get_counts()

print("\n QFT Output")
print("-------------")
print(counts)

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute,IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library import QFT
import numpy as np

pi = np.pi


provider = IBMQ.get_provider(hub='ibm-q')

backend = provider.get_backend('ibmq_qasm_simulator')

q = QuantumRegister(5,'q')
c = ClassicalRegister(5,'c')

circuit = QuantumCircuit(q,c)

circuit.x(q[4])
circuit.x(q[2])
circuit.x(q[0])
circuit.append(QFT(num_qubits=5, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), q)
circuit.measure(q,c)
circuit.draw(output='mpl', filename='qft1.png')
print(circuit)

job = execute(circuit, backend, shots=1000)

job_monitor(job)

counts = job.result().get_counts()

print("\n QFT Output")
print("-------------")
print(counts)
input()

q = QuantumRegister(5,'q')
c = ClassicalRegister(5,'c')

circuit = QuantumCircuit(q,c)

circuit.x(q[4])
circuit.x(q[2])
circuit.x(q[0])
circuit.append(QFT(num_qubits=5, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), q)
circuit.measure(q,c)
circuit.draw(output='mpl',filename='qft2.png')

print(circuit)

job = execute(circuit, backend, shots=1000)

job_monitor(job)

counts = job.result().get_counts()

print("\n QFT with inverse QFT Output")
print("------------------------------")
print(counts)
input()
