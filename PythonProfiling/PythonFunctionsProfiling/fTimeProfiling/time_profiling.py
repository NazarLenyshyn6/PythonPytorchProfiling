import time, threading, inspect 
from abc import ABC, abstractmethod
from types import FunctionType, BuiltinFunctionType
from typing import Any
from PythonProfiling.PythonFunctionsProfiling.fTimeProfiling.time_profiling_results import fTimeProfilingResult
from Internals.execution_guards import fTimeProfilingManager
from Internals.checks import check_input_type


# Interface of function time profiler
class fTimeProfilerI(ABC):
        
    @classmethod
    @abstractmethod
    def profile(cls, func: FunctionType | BuiltinFunctionType, *args, **kwargs) -> fTimeProfilingResult:
        ...

        
# Implementation of basic function time profiler
class fBaseTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func: FunctionType | BuiltinFunctionType, *args, **kwargs) -> fTimeProfilingResult:
        check_input_type(provided_input=func,
                         required_input_type=(FunctionType, BuiltinFunctionType),
                         exception_name='FunctionTimeProfilingError')
        
        with fTimeProfilingManager(profiling_timer=time.time) as time_profiler:
            func_result = func(*args, **kwargs)
            
        return fTimeProfilingResult(profiler=cls,
                                    profiled_func=func,
                                    func_args=args,
                                    func_kwargs=kwargs,
                                    func_result=func_result if time_profiler.func_result else None,
                                    func_execution_time=time_profiler.func_execution_time,
                                    func_exceptions=time_profiler.func_exception)
        
        
        
# Implementation of precise function time profiler
class fPreciseTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        check_input_type(provided_input=func,
                         required_input_type=(FunctionType, BuiltinFunctionType),
                         exception_name='FunctionTimeProfilingError')
        
        with fTimeProfilingManager(profiling_timer=time.perf_counter) as time_profiler:
            func_result = func(*args, **kwargs)
            
        return fTimeProfilingResult(profiler=cls,
                                    profiled_func=func,
                                    func_args=args,
                                    func_kwargs=kwargs,
                                    func_result=func_result if time_profiler.func_result else None,
                                    func_execution_time=time_profiler.func_execution_time,
                                    func_exceptions=time_profiler.func_exception)
        

# Implementation of cpu execution time profiler
class fCPUTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        check_input_type(provided_input=func,
                         required_input_type=(FunctionType, BuiltinFunctionType),
                         exception_name='FunctionTimeProfilingError')
        
        with fTimeProfilingManager(profiling_timer=time.process_time) as time_profiler:
            func_result = func(*args, **kwargs)
            
        return fTimeProfilingResult(profiler=cls,
                                    profiled_func=func,
                                    func_args=args,
                                    func_kwargs=kwargs,
                                    func_result=func_result if time_profiler.func_result else None,
                                    func_execution_time=time_profiler.func_execution_time,
                                    func_exceptions=time_profiler.func_exception)
        
        
# Implementation of thread base time profiling
class fThreadBasedTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        check_input_type(provided_input=func,
                         required_input_type=(FunctionType, BuiltinFunctionType),
                         exception_name='FunctionTimeProfilingError')
        
        with fTimeProfilingManager(profiling_timer=time.perf_counter) as time_profiler:
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()
            thread.join()
        
        return fTimeProfilingResult(profiler=cls,
                                    profiled_func=func,
                                    func_args=args,
                                    func_kwargs=kwargs,
                                    func_result=None,
                                    func_execution_time=time_profiler.func_execution_time,
                                    func_exceptions=time_profiler.func_exception)
        
        
# Implementation of  function monotonic time profiler
class fMonotonicTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        check_input_type(provided_input=func,
                         required_input_type=(FunctionType, BuiltinFunctionType),
                         exception_name='FunctionTimeProfilingError')
        
        with fTimeProfilingManager(profiling_timer=time.monotonic) as time_profiler:
            func_result = func(*args, **kwargs)
           
        return fTimeProfilingResult(profiler=cls,
                                    profiled_func=func,
                                    func_args=args,
                                    func_kwargs=kwargs,
                                    func_result=func_result if time_profiler.func_result else None,
                                    func_execution_time=time_profiler.func_execution_time,
                                    func_exceptions=time_profiler.func_exception)

    