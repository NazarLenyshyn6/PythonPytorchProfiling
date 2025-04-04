from types import FunctionType, BuiltinFunctionType
from typing import Any


def check_if_function(input_arg: Any) -> bool:
    ''' Helper function which chech if input argument is function or not
    
    Args: 
		* input_arg(Any) - argument which will be check if it function
  
	Returns:
		* bool - True if input argument is function False otherwise
    '''
    return isinstance(input_arg, (FunctionType, BuiltinFunctionType))


    