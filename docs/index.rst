Welcome to functrace's documentation!
=====================================

`functrace` is a Python package designed to provide robust and flexible tracing of function calls.
It allows you to monitor and log function execution, track performance, and debug your code more effectively.

You can find the source code on `GitHub`_ and install the package from `PyPI`_.

Getting Started
---------------

To get started with `functrace`, you need to install the package.
You can install it via `pip`:

.. code-block:: sh

   pip install functrace

Quick Start
-----------

Here’s a quick example of how to use `functrace` in your project:

.. code-block:: python

    from functrace import TraceResult, trace

    def trace_callback(result: TraceResult) -> None:
        function_call = result.function_call.format()
        elapsed_time = result.elapsed_time.format()
        returned_value = repr(result.returned_value)
        exception = repr(result.exception)
        parts = [function_call]
        if result.is_started:
            parts.extend(['Started'])
        if result.is_completed:
            parts.extend(['Completed', elapsed_time, returned_value])
        if result.is_failed:
            parts.extend(['Failed', elapsed_time, exception])
        message = ' | '.join(parts)
        print(message)

    @trace(callback=trace_callback)
    def func(a, b, c):
        return a, b, c

    if __name__ == '__main__':
        func(1, 2, 3)
        # func(a=1, b=2, c=3) | Started
        # func(a=1, b=2, c=3) | Completed | 1.25 microseconds | (1, 2, 3)

.. _GitHub: https://github.com/idanhazan/functrace
.. _PyPI: https://pypi.org/project/functrace

.. Hidden TOCs

.. toctree::
    :hidden:
    :caption: Contents:
    :maxdepth: 0
    :glob:

    contents/*