import inspect
from types import FunctionType, BuiltinFunctionType
from typing import Any
from Internals.exceptions import *


def check_strategy(strategy: type, interface: type, exception_name: str):
  if not inspect.isclass(strategy) or not issubclass(strategy, interface):
    raise InvalidStrategyError(exception_name=exception_name,
                               strategy=strategy,
                               interface=interface)
    
    
def check_strategy_name(strategy_name: str, avaliable_strategies: dict, exception_name: str):    
  if not strategy_name in avaliable_strategies:
    raise InvalidStrategyNameError(exception_name=exception_name,
                                   strategy_name=strategy_name,
                                   avaliable_strategies=avaliable_strategies)
    
    
def check_path(file_path: str, required_extension: str, exception_name: str):
  if not isinstance(file_path, str):
    raise InvalidInputType(exception_name=exception_name,
                           input=file_path,
                           required_input_type=str)
    
  if not file_path.endswith(required_extension):
    raise InvalidPathExtention(path=file_path,
                               required_extension=required_extension)
  

def check_input_type(provided_input: Any, required_input_type: Any, exception_name: str):
  if not isinstance(provided_input, required_input_type):
    raise InvalidInputType(exception_name=exception_name,
                           input=provided_input,
                           required_input_type=required_input_type)

        
    

    