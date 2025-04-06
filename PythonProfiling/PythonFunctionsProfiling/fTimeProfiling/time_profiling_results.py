from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import FunctionType, BuiltinFunctionType
from typing import Any
from Internals.serialization import Serializer
from Internals.checks import check_input_type


# Interface of the class which will store python functions time profiling results
class fTimeProfilingResultI(ABC):
    @property
    def profiling_data(self):
        return self.__dict__
    
    @property
    def profiling_data_str(self):
        return {key: f'{value}' for key, value in self.profiling_data.items()}
    
    def add_context(self, context: dict):
        check_input_type(provided_input=context,
                         required_input_type=dict,
                         exception_name='InvalidContextError')
        
        self.__dict__.update(context)
         
    def remove_context(self, context_element: any):
        if context_element in self.__dict__:
            del self.__dict__[context_element]
              
    def to_json(self, file_path: str, mode='w', encoding: str = 'utf-8'):
        Serializer.save(data=self.profiling_data_str, 
                        file_path=file_path, 
                        mode=mode, 
                        encoding=encoding, 
                        serializer_name='JSON')
        
    def to_txt(self, file_path: str, mode='w', encoding: str = 'utf-8'):
         Serializer.save(data=self.profiling_data_str, 
                         file_path=file_path, 
                         mode=mode, 
                         encoding=encoding, 
                         serializer_name='TXT')
        
    def to_yaml(self, file_path: str, mode='w'):
         Serializer.save(data=self.profiling_data_str, 
                         file_path=file_path, 
                         mode=mode,
                         serializer_name='YAML')
         
                 
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