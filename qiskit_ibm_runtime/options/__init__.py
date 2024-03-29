# This code is part of Qiskit.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
=====================================================
Primitive options (:mod:`qiskit_ibm_runtime.options`)
=====================================================

.. currentmodule:: qiskit_ibm_runtime.options

Options that can be passed to the primitives.

The :class:`Options` class encapsulates all the options you can specify
when invoking a primitive. It includes frequently used options,
such as ``optimization_level`` and ``resilience_level`` as well as
sub-categories, such as ``transpilation`` and ``execution``.
You can use auto-complete to easily find the options inside each
sub-category, for example::

   from qiskit_ibm_runtime.options import Options

   options = Options()
   options.transpilation.initial_layout = [0, 1, 2, 3]  # This an be done using auto-complete

You can also pass dictionaries to each sub-category, for example::

   from qiskit_ibm_runtime.options import Options

   options = Options(transpilation={"initial_layout": [0, 1, 2, 3]})


Classes
==========================
.. autosummary::
   :toctree: ../stubs/

   Options
   TranspilationOptions
   ResilienceOptions
   ExecutionOptions
   EnvironmentOptions
   SimulatorOptions
   TwirlingOptions
   EstimatorOptions
   SamplerOptions

"""

from .environment_options import EnvironmentOptions
from .execution_options import ExecutionOptionsV1 as ExecutionOptions
from .options import Options
from .simulator_options import SimulatorOptions
from .transpilation_options import TranspilationOptions
from .resilience_options import ResilienceOptionsV1 as ResilienceOptions
from .twirling_options import TwirlingOptions
from .estimator_options import EstimatorOptions
from .sampler_options import SamplerOptions
