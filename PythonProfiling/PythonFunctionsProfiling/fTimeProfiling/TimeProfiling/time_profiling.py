import time, threading, inspect 
from abc import ABC, abstractmethod
from types import FunctionType, BuiltinFunctionType
from typing import Any
from Internals.common import check_if_function
from Internals.exceptions import FunctionProfilingError, NonExistingProfilerError, InvalidProfilerError, InvalidProfilerNameError
from functools import wraps


# Interface of function time profiler
class fTimeProfilerI(ABC):
    @staticmethod
    def _check_input(input_arg: Any) -> FunctionProfilingError | None:
        if not check_if_function(input_arg):
            raise FunctionProfilingError(input_arg)
    
    @classmethod
    @abstractmethod
    def profile(cls, func: FunctionType | BuiltinFunctionType, *args, **kwargs):
        ...
        

# Implementation of class which will store result of function time profiling
class fTimeProfilingResult:
    def __init__(self, profiler: fTimeProfilerI, 
                 profiled_func: FunctionType | BuiltinFunctionType,
                 profiling_summary: str | Any
                 ) -> None:
        self.profiler = profiler
        self.profiled_func = profiled_func
        self.profiling_summary = profiling_summary
        
    def __repr__(self) -> str:
        return f'fTimeProfilingResult(profiler={self.profiler.__name__}, profiled_func={self.profiled_func.__name__})'
   
        
# Implementation of basic function time profiler
class fBaseTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func: FunctionType | BuiltinFunctionType, *args, **kwargs) -> fTimeProfilingResult:
        super()._check_input(func)
        
        start_profiling = time.time()
        func(*args, **kwargs)
        stop_profiling = time.time()
        
        profiling_summary = f'''
        Profiler: fBaseTimeProfiler
        Profiled Function: {func.__name__}
        Provided arguments: {args}
        Provided keyword argumens: {kwargs}
        Function execution time: {stop_profiling - start_profiling} seconds
        '''
        
        return fTimeProfilingResult(profiler=fBaseTimeProfiler,
                                    profiled_func=func,
                                    profiling_summary=profiling_summary) 
        
        
# Implementation of precise function time profiler
class fPreciseTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        super()._check_input(func)
        
        start_profiling = time.perf_counter()
        func(*args, **kwargs)
        stop_profiling = time.perf_counter()      
        
        profiling_summary = f'''
        Profiler: fPreciseTimeProfiler
        Profiled Function: {func.__name__}
        Provided arguments: {args}
        Provided keyword argumens: {kwargs}
        Precise function execution time: {stop_profiling - start_profiling} seconds
        '''
        
        return fTimeProfilingResult(profiler=fBaseTimeProfiler,
                                    profiled_func=func,
                                    profiling_summary=profiling_summary) 
        

# Implementation of cpu execution time profiler
class fCPUTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        super()._check_input(func)
        
        start_profiling = time.process_time()
        func(*args, **kwargs)
        stop_profiling = time.process_time()      
        
        profiling_summary = f'''
        Profiler: fCPUTimeProfiler
        Profiled Function: {func.__name__}
        Provided arguments: {args}
        Provided keyword argumens: {kwargs}
        CPU time: {stop_profiling - start_profiling} seconds
        '''
        
        return fTimeProfilingResult(profiler=fBaseTimeProfiler,
                                    profiled_func=func,
                                    profiling_summary=profiling_summary) 
        
        
# Implementation of thread base time profiling
class fThreadBasedTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        super()._check_input(func)
        
        start_profiling = time.perf_counter()
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        thread.join()
        stop_profiling = time.perf_counter()      
        
        profiling_summary = f'''
        Profiler: fThreadBasedTimeProfiler
        Profiled Function: {func.__name__}
        Provided arguments: {args}
        Provided keyword argumens: {kwargs}
        Thread Execution Time: {stop_profiling - start_profiling} seconds
        '''
        
        return fTimeProfilingResult(profiler=fBaseTimeProfiler,
                                    profiled_func=func,
                                    profiling_summary=profiling_summary)  
        
        
# Implementation of  function monotonic time profiler
class fMonotonicTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        super()._check_input(func)
        
        start_profiling = time.monotonic()
        func(*args, **kwargs)
        stop_profiling = time.monotonic()      
        
        profiling_summary = f'''
        Profiler: fMonotonicTimeProfiler
        Profiled Function: {func.__name__}
        Provided arguments: {args}
        Provided keyword argumens: {kwargs}
        Execution time: {stop_profiling - start_profiling} seconds
        '''
        
        return fTimeProfilingResult(profiler=fBaseTimeProfiler,
                                    profiled_func=func,
                                    profiling_summary=profiling_summary)  
        
        
# Implementation of Time Profiling Decorator with option of choosing time profiler
class fTimeProfilerDecorator:
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
    
    
@fTimeProfilerDecorator('cpu_time_profiler')
def func(age, name):
    print(f'Hello my name is {name} and i am {age} years old')
    

result = func('hello', name='bob')
print(result.profiling_summary)






    