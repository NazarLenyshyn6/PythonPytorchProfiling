import inspect
from abc import ABC, abstractmethod
from typing import Callable
from PythonProfiling.PythonFunctionsProfiling.fTimeProfiling.time_profiling import *
from Internals.exceptions import *
from functools import wraps
from Internals.checks import check_strategy, check_strategy_name


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
        check_strategy(strategy=time_profiler,
                       interface=fTimeProfilerI,
                       exception_name='InvalidTimeProfilerError')
        
        check_input_type(provided_input=time_profiler_name,
                         required_input_type=str,
                         exception_name='InvalidTimeProfilerNameError')
        
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
        check_strategy_name(strategy_name=time_profiler_name,
                            avaliable_strategies=self._avaliable_time_profilers.keys(),
                            exception_name='NonExistingTimeProfilerError')
        
        self.time_profiler = self._avaliable_time_profilers[time_profiler_name]
        
    
    def change_profiler(self, time_profiler_name: str) -> Exception | None:
        check_strategy_name(strategy_name=time_profiler_name,
                            avaliable_strategies=self._avaliable_time_profilers.keys(),
                            exception_name='NonExistingTimeProfilerError')

        self.time_profiler = self._avaliable_time_profilers[time_profiler_name]
 
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.time_profiler.profile(func, *args, **kwargs)
        return wrapper    

    def __repr__(self) -> str:
        return f'fTimeProfilerDecorator(time_profiler={self.time_profiler.__name__})'