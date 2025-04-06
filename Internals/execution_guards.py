import os
from functools import wraps
from Internals.exceptions import InvalidPathExtention, InvalidInputType


def safe_serialization(func):
    '''Decorator which incapsulates data serializations exceptions handling logic'''
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            
        except (InvalidPathExtention, InvalidInputType) as e:
            print(f'Impossible to serialize data because of following exeption: {str(e)}')
        
        except Exception as e:
            if 'file_path' in kwargs:
                if os.path.exists(kwargs['file_path']) and not os.path.getsize(kwargs['file_path']):
                    os.remove(kwargs['file_path'])
                    
            print(f'Impossible to serialize data because of following exeption: {str(e)}')
            
    return wrapper


class fTimeProfilingManager:
    '''Context manager for time profiling of python functions with time module'''
    
    def __init__(self, profiling_timer):
        self.profiling_timer = profiling_timer
        
    def __enter__(self):
        self.start_profiling = self.profiling_timer()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_profiling = self.profiling_timer()
        self.func_execution_time = self.stop_profiling - self.start_profiling
        
        if exc_type:
            self.func_exception = exc_value
            self.func_result = False
            
        else:
            self.func_exception = None
            self.func_result = True
            
        return True
    
    def __repr__(self) -> str:
        return f'fTimeProfilingManager(profiling_timer={self.profiling_timer})'
            
