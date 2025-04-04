from abc import ABC, abstractmethod
from typing import Callable
from PythonProfiling.PythonFunctionsProfiling.fTimeProfiling.time_profiling import *
from Internals.exceptions import *
from functools import wraps


# Implementatino of the interface of python functions time profiler decorator
class fTimeProfilerDecoratorI(ABC):
    _avaliable_time_profilers = {}
    
    @abstractmethod
    def __init__(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    def __call__(self, func: Callable) -> Callable:
        ...
        
    @abstractmethod
    def change_profiler(self, time_profiler):
        ...
        
    @classmethod
    def avaliable_time_profilers(cls):
        return cls._avaliable_time_profilers.keys()
        
    @classmethod
    def add_time_profiler(cls, time_profiler: fTimeProfilerI, time_profiler_name: str) -> None:
        if not inspect.isclass(time_profiler) or not issubclass(time_profiler, fTimeProfilerI):
            raise InvalidProfilerError(provided_profiler=time_profiler,
                                       profiler_interface=fTimeProfilerI)
        
        if not isinstance(time_profiler_name, str):
            raise InvalidProfilerNameError(provided_profiler_name=time_profiler_name,
                                           valid_profilers_names=cls._avaliable_time_profilers.keys())
        
        cls._avaliable_time_profilers[time_profiler_name] = time_profiler
        print(f'{time_profiler.__name__} has been added as {time_profiler_name}')
        
        
    @classmethod
    def remove_time_profiler(cls, time_profiler_name: str) -> None:
        if time_profiler_name in cls._avaliable_time_profilers:
            del cls._avaliable_time_profilers[time_profiler_name]
            print(f'{time_profiler_name} profiler has been removed')


# Implementation of time profiling decorator for time_profiling module
class fTimeProfilerDecorator(fTimeProfilerDecoratorI):
    _avaliable_time_profilers = {'base_time_profiler': fBaseTimeProfiler,
                                 'precise_time_profiler': fPreciseTimeProfiler,
                                 'cpu_time_profiler': fCPUTimeProfiler,
                                 'thread_time_profiler': fThreadBasedTimeProfiler,
                                 'monotonic_time_profiler': fMonotonicTimeProfiler}
    
    
    def __init__(self, time_profiler_name: str = 'base_time_profiler') -> Exception | None:
        if not time_profiler_name in self._avaliable_time_profilers:
            raise NonExistingProfilerError(non_existing_profiler_name=time_profiler_name,
                                           avaliable_profilers=self._avaliable_time_profilers.keys())
        
        self.time_profiler = self._avaliable_time_profilers[time_profiler_name]
        
    
    def change_profiler(self, time_profiler_name: str) -> Exception | None:
        if not isinstance(time_profiler_name, str):
            raise InvalidProfilerNameError(provided_profiler_name=time_profiler_name,
                                           valid_profilers_names=self._avaliable_time_profilers.keys())
        
        if not time_profiler_name in self._avaliable_time_profilers:
            raise NonExistingProfilerError(non_existing_profiler_name=time_profiler_name,
                                           avaliable_profilers=self._avaliable_time_profilers.keys())
        
        self.time_profiler = self._avaliable_time_profilers[time_profiler_name]
 
  
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.time_profiler.profile(func, *args, **kwargs)
        return wrapper    
    
    
    def __repr__(self) -> str:
        return f'fTimeProfilerDecorator(time_profiler={self.time_profiler.__name__})'