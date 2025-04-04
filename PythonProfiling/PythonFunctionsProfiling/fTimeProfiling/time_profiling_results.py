from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import FunctionType, BuiltinFunctionType
from typing import Any
from Internals.exceptions import *


# Interface of the class which will store python functions time profiling results
class fTimeProfilingResultI(ABC):
    @property
    def profiling_data(self):
        return self.__dict__
    
    
    def add_context(self, context: dict):
        if not isinstance(context, dict):
            raise InvalidContextError(provided_context=context)
        
        self.__dict__.update(context)
        
        
    def remove_context(self, context_element: any):
        if context_element in self.__dict__:
            del self.__dict__[context_element]
            
            
            
# Implementation of class which will store result of function time profiling with time module
@dataclass
class fTimeProfilingResult(fTimeProfilingResultI):
    profiler: type
    profiled_func: FunctionType | BuiltinFunctionType
    func_args: tuple
    func_kwargs: dict
    func_result: Any
    func_execution_time: float
    func_exceptions: str = None
    
    def __str__(self) -> str:
        return (f"Profiler: {self.profiler}\n"
                f"Profiled Function: {self.profiled_func.__name__}\n"
                f"Function Args: {self.func_args}\n"
                f"Function Kwargs: {self.func_kwargs}\n"
                f"Function Result: {self.func_result}\n"
                f"Function Executions Time: {self.func_execution_time:.6f} seconds\n"
                f"Function Exception: {self.func_exceptions or 'None'}")
        
        
    def __repr__(self) -> str:
        return f'fTimeProfilingResult(profiler={self.profiler.__name__}, profiled_func={self.profiled_func.__name__})'