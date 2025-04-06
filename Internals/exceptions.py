from typing import Any, Dict, Type

class ObjectProfilingError(Exception):
    def __init__(self, exception_name: str, provided_object: Any, required_object_type: str):
        self.__class__.__name__ = exception_name
        super().__init__(f'{provided_object} has to be {required_object_type}.')


class InvalidStrategyError(Exception):
    def __init__(self, exception_name: str, strategy: type, interface: type):
        self.__class__.__name__ = exception_name
        super().__init__(f'{strategy.__name__} has to be class which inherets from {interface.__name__}.')
        
        
class InvalidStrategyNameError(Exception):
    def __init__(self, exception_name: str, strategy_name: str, avaliable_strategies: dict):
        self.__class__.__name__ = exception_name
        super().__init__(f'{strategy_name} does not exist, choose from existing ones: {avaliable_strategies}.')
        
        
class InvalidInputType(Exception):
    def __init__(self, exception_name: str, input: Any, required_input_type: Any):
        self.__class__.__name__ = exception_name
        super().__init__(f'{input} has to be of type {required_input_type}, got intead: {type(input)}.')
        
            
class InvalidPathExtention(Exception):
    def __init__(self, path: str, required_extension: str):
        super().__init__(f'{path} has to have {required_extension} extension.')

