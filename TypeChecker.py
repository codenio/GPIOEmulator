#####################################
#####Raspberry PI GPIO Emulator #####
#####################################

# The inspect module isn't available for python 2.7
# Therefore the if/else structure pulls the funcsigs module instead of the inspect module
import sys
if sys.version_info[0] == 2 and sys.version_info[1] <= 7:
    from funcsigs import signature
elif sys.version_info[1] > 2:
    from inspect import signature
else:
    print("ERROR - Unsupported Python version\n")
    sys.exit()
    
from functools import wraps

def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                      raise TypeError(
                        'Argument {} must be {}'.format(name, bound_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorate
