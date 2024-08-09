```plaintext
  _____                    __
_/ ____\_ __  ____   _____/  |_____________    ____  ____
\   __\  |  \/    \_/ ___\   __\_  __ \__  \ _/ ___\/ __ \
 |  | |  |  /   |  \  \___|  |  |  | \// __ \\  \__\  ___/
 |__| |____/|___|  /\___  >__|  |__|  (____  /\___  >___  >
                 \/     \/                 \/     \/    \/
```

**functrace** is a Python library for detailed function call tracing.
It provides logging and performance tracking to help monitor execution, measure timing, and debug effectively.

## Getting Started

To begin using `functrace`, you'll first need to install it. This can be easily done using `pip`.
Simply run the following command to install the package:

```sh
pip install functrace
```

## Quick Start

Get up and running with `functrace` quickly by following this simple example.
Below is a basic usage scenario to help you integrate `functrace` into your project and start tracing function calls.

```python
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
    # func(a=1, b=2, c=3) | Completed | 1 microsecond, 200 nanoseconds | (1, 2, 3)
```

## Summary

You can find `functrace` on [PyPI](https://pypi.org/project/functrace) for installation and package details. For comprehensive documentation and usage guides, visit [Read the Docs](https://functrace.readthedocs.io).

