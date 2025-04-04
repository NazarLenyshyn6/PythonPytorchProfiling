from typing import Any, Dict, Type


class FunctionProfilingError(Exception):
    ''' Exception which will be raise when use provide for profiling anything but not function.'''
    def __init__(self, arg: Any):
        super().__init__(f'Input argumens has to be function, got instead {type(arg)}.')
        
        
class NonExistingProfilerError(Exception):
    ''' Exception which will be raised when provide unexisting profiler.'''
    def __init__(self, non_existing_profiler_name: str, avaliable_profilers: Dict):
        super().__init__(f'Profiler {non_existing_profiler_name} does not exist choose from existing ones: {avaliable_profilers}.')
        

class InvalidProfilerError(Exception):
    ''' Exception which will be raise when invalid profiling class provided'''
    def __init__(self, provided_profiler: Any, profiler_interface: Type):
        super().__init__(f'{provided_profiler.__name__} has to be class which inherets from {profiler_interface.__name__}.')
        
    
class InvalidProfilerNameError(Exception):
    ''' Exception which will be raise when provided invalid type of profiler'''
    def __init__(self, provided_profiler_name: Any, avaliable_profilers: Dict):
        super().__init__(f'Profiler name has to be one of {avaliable_profilers}, got instead: {provided_profiler_name}.')
  
        
class InvalidContextError(Exception):
    ''' Exceptoin which will be raise when as context provided anything but not dictionary'''
    def __init__(self, provided_context: Any):
        super().__init__(f'Context has to be provovided as dictionary, got instead: {type(provided_context)}')
        