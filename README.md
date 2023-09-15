# Qiskit Runtime IBM Client
[![License](https://img.shields.io/github/license/Qiskit/qiskit-ibm-runtime.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)
[![CI](https://github.com/Qiskit/qiskit-ibm-runtime/actions/workflows/ci.yml/badge.svg)](https://github.com/Qiskit/qiskit-ibm-runtime/actions/workflows/ci.yml)
[![](https://img.shields.io/github/release/Qiskit/qiskit-ibm-runtime.svg?style=popout-square)](https://github.com/Qiskit/qiskit-ibm-runtime/releases)
[![](https://img.shields.io/pypi/dm/qiskit-ibm-runtime.svg?style=popout-square)](https://pypi.org/project/qiskit-ibm-runtime/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage Status](https://coveralls.io/repos/github/Qiskit/qiskit-ibm-runtime/badge.svg?branch=main)](https://coveralls.io/github/Qiskit/qiskit-ibm-runtime?branch=main)


**Qiskit** is an open-source SDK for working with quantum computers at the level of extended quantum circuits, operators, and primitives.

**Qiskit IBM Runtime** is a new environment offered by IBM Quantum that streamlines quantum computations and provides optimal 
implementations of the Qiskit primitives `sampler` and `estimator` for IBM Quantum hardware. It is designed to use additional classical compute resources to execute quantum circuits with more efficiency on quantum processors, by including near-time computations such as error suppression and error mitigation. Examples of error suppression include dynamical decoupling, noise-aware compilation, error mitigation including readout mitigation, zero-noise extrapolation (ZNE), and probabilistic error cancellation (PEC).  

Using the runtime service, a research team at IBM Quantum was able to achieve a 120x speedup
in their lithium hydride simulation. For more information, see the
[IBM Research blog](https://research.ibm.com/blog/120x-quantum-speedup).

This module provides the interface to access the Qiskit Runtime service on IBM Quantum Platform or IBM Cloud.

## Installation

You can install this package using pip:

```bash
pip install qiskit-ibm-runtime
```

## Account setup

### Qiskit Runtime service on IBM Quantum Platform

The default method for using the runtime service is IBM Quantum Platform.

You will need your IBM Quantum API token to authenticate with the runtime service:

1. Create an IBM Quantum account or log in to your existing account by visiting the [IBM Quantum login page].

1. Copy (and optionally regenerate) your API token from your
   [IBM Quantum account page].

### Qiskit Runtime service on IBM Cloud

The runtime service is now part of the IBM Quantum Services on IBM Cloud. To use this service, you'll
need to create an IBM Cloud account and a quantum service instance.
[This guide](https://cloud.ibm.com/docs/quantum-computing?topic=quantum-computing-get-started)
contains step-by-step instructions, including how to find your
IBM Cloud API key and Cloud Resource Name (CRN), which you will need for authentication.


### Save your account on disk

Once you have the account credentials, you can save them on disk, so you won't have to input
them each time. The credentials are saved in the `$HOME/.qiskit/qiskit-ibm.json` file, where `$HOME` is your home directory.

| :warning: Account credentials are saved in plain text, so only do so if you are using a trusted device. |
|:---------------------------|

 ```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Save an IBM Cloud account.
QiskitRuntimeService.save_account(channel="ibm_cloud", token="MY_IBM_CLOUD_API_KEY", instance="MY_IBM_CLOUD_CRN")

# Save an IBM Quantum account.
QiskitRuntimeService.save_account(channel="ibm_quantum", token="MY_IBM_QUANTUM_TOKEN")
```

Once the account is saved on disk, you can instantiate the service without any arguments:

```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
```

### Loading account from environment variables

Alternatively, the service can discover credentials from environment variables:
```bash
export QISKIT_IBM_TOKEN="MY_IBM_CLOUD_API_KEY"
export QISKIT_IBM_INSTANCE="MY_IBM_CLOUD_CRN"
export QISKIT_IBM_CHANNEL="ibm_cloud"
```

Then instantiate the service without any arguments:
```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
```

### Enabling account for current Python session

As another alternative, you can also enable an account just for the current session by instantiating the
service with your credentials.

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# For an IBM Cloud account.
ibm_cloud_service = QiskitRuntimeService(channel="ibm_cloud", token="MY_IBM_CLOUD_API_KEY", instance="MY_IBM_CLOUD_CRN")

# For an IBM Quantum account.
ibm_quantum_service = QiskitRuntimeService(channel="ibm_quantum", token="MY_IBM_QUANTUM_TOKEN")
```

## Primitives

All quantum applications and algorithms level are fundamentally built using three steps:
1. Choose a quantum circuit to encode the quantum state.
2. Define the observable or the classical register to be measured.
4. Execute the quantum circuits by using a primitive (Estimator or Sampler).

**Primitives** are base-level functions that serve as building blocks for many quantum algorithms and applications. The [primitive interfaces](https://qiskit.org/documentation/apidoc/primitives.html) are defined in Qiskit.

The IBM Runtime service offers these primitives with additional features, such as built-in error suppression and mitigation.

There are several different options you can specify when calling the primitives. See [`qiskit_ibm_runtime.Options`](https://github.com/Qiskit/qiskit-ibm-runtime/blob/main/qiskit_ibm_runtime/options/options.py#L33) class for more information.

### Sampler

This primitive takes a list of user circuits (including measurements) as input and generates an error-mitigated readout of quasi-probability distributions. This provides users a way to better evaluate shot results using error mitigation, and enables them to more efficiently evaluate the possibility of multiple relevant data points in the context of destructive interference.

To invoke the `Sampler` primitive

```python
from qiskit_ibm_runtime import QiskitRuntimeService, Options, Sampler
from qiskit import QuantumCircuit

service = QiskitRuntimeService()
options = Options(optimization_level=1)
options.execution.shots = 1024  # Options can be set using auto-complete.

# 1. A quantum circuit for preparing the quantum state (|00> + |11>)/rt{2}
bell = QuantumCircuit(2)
bell.h(0)
bell.cx(0, 1)

# 2. Map the qubits to a classical register in ascending order
bell.measure_all()

# 3. Execute using the Sampler primitive 
backend = service.get_backend('ibmq_qasm_simulator')
sampler = Sampler(backend=backend, options=options)
job = sampler.run(circuits=bell)
print(f"Job ID is {job.job_id()}")
print(f"Job result is {job.result()}")
```

### Estimator

This primitive takes circuits and observables as input, to evaluate expectation values and variances for a given parameter input. This Estimator allows users to efficiently calculate and interpret expectation values of quantum operators required for many algorithms.

To invoke the `Estimator` primitive:

```python
from qiskit_ibm_runtime import QiskitRuntimeService, Options, Estimator
from qiskit.quantum_info import SparsePauliOp
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np

service = QiskitRuntimeService()
options = Options(optimization_level=1)
options.execution.shots = 1024  # Options can be set using auto-complete.

# 1. A quantum circuit for preparing the quantum state (|000> + e^{itheta} |111>)/rt{2}
theta = Parameter('θ')
qc_example = QuantumCircuit(3)
qc_example.h(0) # generate superposition
qc_example.p(theta, 0) # add quantum phase
qc_example.cx(0, 1) # condition 1st qubit on 0th qubit
qc_example.cx(0, 2) # condition 2nd qubit on 0th qubit

# 2. the observable to be measured
M1 = SparsePauliOp.from_list([("XXY", 1), ("XYX", 1), ("YXX", 1), ("YYY", -1)])

# batch of theta parameters to be executed 
points = 50
theta1 = []
for x in range(points):
    theta = [x*2.0*np.pi/50]
    theta1.append(theta)

# 3. Execute using the Estimator primitive 
backend = service.get_backend('ibmq_qasm_simulator')
estimator = Estimator(backend, options=options)
job = estimator.run(circuits=[qc_example]*points, observables=[M1]*points, parameter_values=theta1)
print(f"Job ID is {job.job_id()}")
print(f"Job result is {job.result().values}")
```

This code batches together 50 parameters to be executed in a single job. If a user wanted to find the `theta` that optimized the observable, they could plot and observe it occurs at `theta=np.pi/2`. For speed we recommend batching results together (note that depending on your access, there may be limits on the number of circuits, objects, and parameters that you can send).


## Session

In many algorithms and applications, an Estimator needs to be called iteratively without incurring queuing delays on each iteration. To solve this, the IBM Runtime service provides a **Session**. A session starts when the first job within the session is started, and subsequent jobs within the session are prioritized by the scheduler.

You can use the [`qiskit_ibm_runtime.Session`](https://github.com/Qiskit/qiskit-ibm-runtime/blob/main/qiskit_ibm_runtime/session.py) class to start a
session. Consider the same example above and try to find the optimal `theta`. The following example uses the [golden search method](https://en.wikipedia.org/wiki/Golden-section_search) to iteratively find the optimal theta that maximizes the observable. 

To invoke the `Estimator` primitive within a session:

```python
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, Estimator
from qiskit.quantum_info import SparsePauliOp
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np

service = QiskitRuntimeService()
options = Options(optimization_level=1)
options.execution.shots = 1024  # Options can be set using auto-complete.

# 1. A quantum circuit for preparing the quantum state (|000> + e^{itheta} |111>)/rt{2}
theta = Parameter('θ')
qc_example = QuantumCircuit(3)
qc_example.h(0) # generate superpostion
qc_example.p(theta,0) # add quantum phase
qc_example.cx(0, 1) # condition 1st qubit on 0th qubit
qc_example.cx(0, 2) # condition 2nd qubit on 0th qubit

# 2. the observable to be measured
M1 = SparsePauliOp.from_list([("XXY", 1), ("XYX", 1), ("YXX", 1), ("YYY", -1)])


gr = (np.sqrt(5) + 1) / 2 # golden ratio   
thetaa = 0 # lower range of theta
thetab = 2*np.pi # upper range of theta
tol = 1e-1 # tol 

# 3. Execute iteratively using the Estimator primitive 
with Session(service=service, backend="ibmq_qasm_simulator") as session:
    estimator = Estimator(session=session, options=options)
    #next test range 
    thetac = thetab - (thetab - thetaa) / gr
    thetad = thetaa + (thetab - thetaa) / gr
    while abs(thetab - thetaa) > tol:
        print(f"max value of M1 is in the range theta = {[thetaa, thetab]}")
        job = estimator.run(circuits=[qc_example]*2, observables=[M1]*2, parameter_values=[[thetac],[thetad]])
        test =job.result().values
        if test[0] > test[1]:
            thetab = thetad
        else:
            thetaa = thetac
        thetac = thetab - (thetab - thetaa) / gr
        thetad = thetaa + (thetab - thetaa) / gr
        
    # Final job to evaluate Estimator at midpoint found using golden search method 
    theta_mid = (thetab + thetaa) / 2
    job = estimator.run(circuits=qc_example, observables=M1, parameter_values=theta_mid)
    print(f"Session ID is {session.session_id}")
    print(f"Final Job ID is {job.job_id()}")
    print(f"Job result is {job.result().values} at theta = {theta_mid}")
```

This code returns `Job result is [4.] at theta = 1.575674623307102` using only nine iterations. This is a very powerful extension to the primitives. However, using too much code between iterative calls can lock the QPU and use excessive QPU time, which is expensive. We recommend only using sessions when needed. The Sampler can also be used within a session, but there are not any well-defined examples for this.

## Instances

Access to IBM Quantum Platform services is controlled by the instances (previously called providers) to which you are assigned. An instance is defined by a hierarchical organization of hub, group, and project. A hub is the top level of a given hierarchy (organization) and contains within it one or more groups. These groups are in turn populated with projects. The combination of hub/group/project is called an instance. Users can belong to more than one instance at any time. 

> **_NOTE:_** IBM Cloud instances are different from IBM Quantum Platform instances.  IBM Cloud does not use the hub/group/project structure for user management. To view and create IBM Cloud instances, visit the [IBM Cloud Quantum Instances page](https://cloud.ibm.com/quantum/instances).

To view a list of your instances, visit your [account settings page](https://www-dev.quantum-computing.ibm.com/account) or use the `instances()` method.

You can specify an instance when initializing the service or provider, or when picking a backend: 

```python
 
# Optional: Specify the instance at service level. This becomes the default unless overwritten.
service = QiskitRuntimeService(channel='ibm_quantum', instance="hub1/group1/project1")
backend1 = service.backend("ibmq_manila")
 
# Optional: Specify the instance at the backend level, which overwrites the service-level specification when this backend is used. 
backend2 = service.backend("ibmq_manila", instance="hub2/group2/project2")
 
sampler1 = Sampler(backend=backend1)    # this will use hub1/group1/project1
sampler2 = Sampler(backend=backend2)    # this will use hub2/group2/project2
```

If you do not specify an instance, then the code will select one in the following order:

1. If your account only has access to one instance, it is selected by default.
2. If your account has access to multiple instances, but only one can access the requested backend, the instance with access is selected.
3. In all other cases, the code selects the first instance other than ibm-q/open/main that has access to the backend.

## Access your IBM Quantum backends

A **backend** is a quantum device or simulator capable of running quantum circuits or pulse schedules.

You can query for the backends you have access to. Attributes and methods of the returned instances
provide information, such as qubit counts, error rates, and statuses, of the backends.

```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()

# Display all backends you have access.
print(service.backends())

# Get a specific backend.
backend = service.backend('ibmq_qasm_simulator')

# Print backend coupling map.
print(backend.coupling_map)
```

## Next Steps

Now you're set up and ready to check out some of the [tutorials].

## Contribution guidelines

If you'd like to contribute to qiskit-ibm-runtime, please take a look at our
[contribution guidelines]. This project adheres to Qiskit's [code of conduct].
By participating, you are expected to uphold to this code.

We use [GitHub issues] for tracking requests and bugs. Please use our [slack]
for discussion and simple questions. To join our Slack community use the
invite link at [Qiskit.org]. For questions that are more suited for a forum we
use the `Qiskit` tag in [Stack Exchange].

## License

[Apache License 2.0].


[IBM Quantum]: https://www.ibm.com/quantum-computing/
[IBM Quantum login page]:  https://quantum-computing.ibm.com/login
[IBM Quantum account page]: https://quantum-computing.ibm.com/account
[contribution guidelines]: https://github.com/Qiskit/qiskit-ibm-runtime/blob/main/CONTRIBUTING.md
[code of conduct]: https://github.com/Qiskit/qiskit-ibm-runtime/blob/main/CODE_OF_CONDUCT.md
[GitHub issues]: https://github.com/Qiskit/qiskit-ibm-runtime/issues
[slack]: https://qiskit.slack.com
[Qiskit.org]: https://qiskit.org
[Stack Exchange]: https://quantumcomputing.stackexchange.com/questions/tagged/qiskit
[many people]: https://github.com/Qiskit/qiskit-ibm-runtime/graphs/contributors
[BibTeX file]: https://github.com/Qiskit/qiskit/blob/master/Qiskit.bib
[Apache License 2.0]: https://github.com/Qiskit/qiskit-ibm-runtime/blob/main/LICENSE.txt
[tutorials]: https://github.com/Qiskit/qiskit-ibm-runtime/tree/main/docs/tutorials
