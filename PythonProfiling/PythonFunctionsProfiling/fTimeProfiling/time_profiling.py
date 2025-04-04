import time, threading, inspect 
from abc import ABC, abstractmethod
from types import FunctionType, BuiltinFunctionType
from typing import Any
from Internals.common import check_if_function
from Internals.exceptions import FunctionProfilingError, NonExistingProfilerError, InvalidProfilerError, InvalidProfilerNameError, InvalidContextError
from PythonProfiling.PythonFunctionsProfiling.fTimeProfiling.time_profiling_results import fTimeProfilingResult


# Interface of function time profiler
class fTimeProfilerI(ABC):
    @staticmethod
    def _check_input(input_arg: Any) -> FunctionProfilingError | None:
        if not check_if_function(input_arg):
            raise FunctionProfilingError(input_arg)
    
    @classmethod
    @abstractmethod
    def profile(cls, func: FunctionType | BuiltinFunctionType, *args, **kwargs) -> fTimeProfilingResult:
        ...

        
# Implementation of basic function time profiler
class fBaseTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func: FunctionType | BuiltinFunctionType, *args, **kwargs) -> fTimeProfilingResult:
        super()._check_input(func)
        
        start_profiling = time.time()
        error = None
        
        try:
            func_result = func(*args, **kwargs)
            
        except Exception as e:
            error = e.__class__.__name__
            func_result = None
            
        finally:
            stop_profiling = time.time()
             
            return fTimeProfilingResult(profiler=cls,
                                          profiled_func=func,
                                          func_args=args,
                                          func_kwargs=kwargs,
                                          func_result=func_result,
                                          func_execution_time=stop_profiling - start_profiling,
                                          func_exceptions=error)
        
        
# Implementation of precise function time profiler
class fPreciseTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        super()._check_input(func)
        
        start_profiling = time.perf_counter()
        error = None
        
        try:
            func_result = func(*args, **kwargs)
            
        except Exception as e:
            error = e.__class__.__name__
            func_result = None
            
        finally:
            stop_profiling = time.perf_counter()      
        
            return fTimeProfilingResult(profiler=cls,
                                          profiled_func=func,
                                          func_args=args,
                                          func_kwargs=kwargs,
                                          func_result=func_result,
                                          func_execution_time=stop_profiling - start_profiling,
                                          func_exceptions=error)
        

# Implementation of cpu execution time profiler
class fCPUTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        super()._check_input(func)
        
        start_profiling = time.process_time()
        error = None
        try:
            func_result = func(*args, **kwargs)
            
        except Exception as e:
            error = e.__class__.__name__
            func_result = None
            
        finally:
            stop_profiling = time.process_time()      
            
            return fTimeProfilingResult(profiler=cls,
                                          profiled_func=func,
                                          func_args=args,
                                          func_kwargs=kwargs,
                                          func_result=func_result,
                                          func_execution_time=stop_profiling - start_profiling,
                                          func_exceptions=error)
        
        
# Implementation of thread base time profiling
class fThreadBasedTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        super()._check_input(func)
        
        start_profiling = time.perf_counter()
        error = None
        
        try:
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()
            thread.join()
            
        except Exception as e:
            error = e.__class__.__name__
            func_result = None
            
        finally:
            stop_profiling = time.perf_counter()      
        
            return fTimeProfilingResult(profiler=cls,
                                          profiled_func=func,
                                          func_args=args,
                                          func_kwargs=kwargs,
                                          func_result=None,
                                          func_execution_time=stop_profiling - start_profiling,
                                          func_exceptions=error)
        
        
# Implementation of  function monotonic time profiler
class fMonotonicTimeProfiler(fTimeProfilerI):
    @classmethod
    def profile(cls, func, *args, **kwargs):
        super()._check_input(func)
        
        start_profiling = time.monotonic()
        error = None
        
        try:
            func_result = func(*args, **kwargs)
            
        except Exception as e:
            error = e.__class__.__name__
            func_result = None
            
        finally:
            stop_profiling = time.monotonic()      
        
            return fTimeProfilingResult(profiler=cls,
                                          profiled_func=func,
                                          func_args=args,
                                          func_kwargs=kwargs,
                                          func_result=None,
                                          func_execution_time=stop_profiling - start_profiling,
                                          func_exceptions=error)
        
    


# class ProfilingObserver(ABC):
#     @abstractmethod
#     def notify(self, result: fTimeProfilingResult): ...

# class ConsoleLogger(ProfilingObserver):
#     def notify(self, result): print(result.profiling_summary)

# class JSONFileLogger(ProfilingObserver):
#     def notify(self, result):
#         with open("logs/profile.json", "a") as f:
#             f.write(result.summary.to_json())

# # Then inside your profiler
# for observer in fTimeProfilerDecorator.observers:
#     observer.notify(result)








    