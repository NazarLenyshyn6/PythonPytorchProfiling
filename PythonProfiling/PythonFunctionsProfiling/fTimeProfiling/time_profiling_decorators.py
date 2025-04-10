import inspect
from abc import ABC, abstractmethod
from typing import Callable ,ClassVar, Type
from PythonProfiling.PythonFunctionsProfiling.fTimeProfiling.time_profiling import *
from Internals.exceptions import *
from functools import wraps
from Internals.checks import check_strategy, check_strategy_name
from Internals.observer import ObservationsHandler
from Internals.profiling_enums import fTimeProfilingStrategy, ProfilingOutputFormat
from pydantic import BaseModel, ConfigDict, Field



# Implementatino of the interface of python functions time profiler decorator
class fTimeProfilerDecoratorI(ABC):
    _avaliable_time_profilers = {}
    

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
    def add_time_profiler(cls, time_profiler: fTimeProfilerI, time_profiler_name: fTimeProfilingStrategy) -> None:
        check_strategy(strategy=time_profiler,
                       interface=fTimeProfilerI,
                       exception_name='InvalidTimeProfilerError')
        
        check_input_type(provided_input=time_profiler_name,
                         required_input_type=fTimeProfilingStrategy,
                         exception_name='InvalidTimeProfilerNameError')
        
        cls._avaliable_time_profilers[time_profiler_name] = time_profiler
        print(f'{time_profiler.__name__} has been added as {time_profiler_name}')  
        
    @classmethod
    def remove_time_profiler(cls, time_profiler_name: fTimeProfilingStrategy) -> None:
        if time_profiler_name in cls._avaliable_time_profilers:
            del cls._avaliable_time_profilers[time_profiler_name]
            print(f'{time_profiler_name} profiler has been removed')


class fTimeProfilerDecorator(fTimeProfilerDecoratorI, BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _avaliable_time_profilers: ClassVar[dict[fTimeProfilingStrategy, fTimeProfilerI]] = {
        fTimeProfilingStrategy.BASE: fBaseTimeProfiler,
        fTimeProfilingStrategy.PRECISE: fPreciseTimeProfiler,
        fTimeProfilingStrategy.CPU: fCPUTimeProfiler,
        fTimeProfilingStrategy.THREAD: fThreadBasedTimeProfiler,
        fTimeProfilingStrategy.MONOTONIC: fMonotonicTimeProfiler
    }

    time_profiler_name: fTimeProfilingStrategy = Field(default=fTimeProfilingStrategy.BASE)
    storages: list[tuple[ProfilingOutputFormat, str]] = Field(default_factory=list)

    time_profiler: fTimeProfilerI | None = Field(init=False, default=None)
    observer: ObservationsHandler | None= Field(init=False, default=None)

    def model_post_init(self, __context):
        self.time_profiler = self._avaliable_time_profilers[self.time_profiler_name]
        self.observer = ObservationsHandler(storages=self.storages)
        
    
    def change_profiler(self, time_profiler_name: fTimeProfilingStrategy) -> Exception | None:
        check_strategy_name(strategy_name=time_profiler_name,
                            avaliable_strategies=self._avaliable_time_profilers.keys(),
                            exception_name='NonExistingTimeProfilerError')

        self.time_profiler = self._avaliable_time_profilers[time_profiler_name]
 
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = self.time_profiler.profile(func, *args, **kwargs)
            self.observer.save_result(result)
            return result
        
        return wrapper    

    def __repr__(self) -> str:
        return f'fTimeProfilerDecorator(time_profiler={self.time_profiler.__name__})'