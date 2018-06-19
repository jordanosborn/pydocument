"""Built in generators."""
from collections import OrderedDict


# Output should be long information plus final value (reinterpreted long info)
def recall(variables: OrderedDict, var: str, *args: list) -> str:
    """Recalls the value of var using new arguments.

    Arguments:
        variables {OrderedDict} -- variables container
        var {str} -- variable whose value you want to pick out
        args {[str]} -- arguments used to reinterpret var's value

    Returns:
        str -- returns new value.

    """
    return variables[var]['value']
