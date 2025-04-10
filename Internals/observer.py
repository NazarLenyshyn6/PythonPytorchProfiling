from abc import ABC, abstractmethod
from PythonProfiling.PythonFunctionsProfiling.fTimeProfiling.time_profiling_results import fTimeProfilingResultI
from Internals.checks import check_strategy, check_path, check_input_type, check_strategy_name
from Internals.exceptions import InvalidStrategyError, InvalidPathExtention
from Internals.profiling_enums import ProfilingOutputFormat, SerializationStrategy, OvserverStrategy


# Implementation of Observer Interface
class ProfilingObserverI(ABC):
    @staticmethod
    @abstractmethod
    def save_result(result: fTimeProfilingResultI, file_path: str) -> InvalidStrategyError | InvalidPathExtention | None:
        ...

# Implementation of JSON Observer
class JSONObserver(ProfilingObserverI):
    @staticmethod
    def save_result(result: fTimeProfilingResultI, file_path: str) ->  InvalidStrategyError | InvalidPathExtention | None:
        check_input_type(provided_input=result,
                         required_input_type=fTimeProfilingResultI,
                         exception_name='InvalidfTimeProfilingResultError')
        
        check_path(file_path=file_path,
                   required_extension='.json',
                   exception_name='InvalidJSONFilePath')
        
        result.dump(file_path=file_path, extension=ProfilingOutputFormat.JSON)
    
    
# Implementation of TXT Observer
class TXTObserver(ProfilingObserverI):
    @staticmethod
    def save_result(result: fTimeProfilingResultI, file_path: str) ->  InvalidStrategyError | InvalidPathExtention | None:
        check_input_type(provided_input=result,
                         required_input_type=fTimeProfilingResultI,
                         exception_name='InvalidfTimeProfilingResultError')
        
        check_path(file_path=file_path,
                   required_extension='.txt',
                   exception_name='InvalidTXTFilePath')
        
        result.dump(file_path=file_path, extension=ProfilingOutputFormat.TXT)
    
    
# Implementation of YAML Observer
class YAMLObserver(ProfilingObserverI):
    @staticmethod
    def save_result(result: fTimeProfilingResultI, file_path: str) ->  InvalidStrategyError | InvalidPathExtention | None:
        check_input_type(provided_input=result,
                         required_input_type=fTimeProfilingResultI,
                         exception_name='InvalidfTimeProfilingResultError')
        
        check_path(file_path=file_path,
                   required_extension='.yaml',
                   exception_name='InvalidYAMLFilePath')
        
        result.dump(file_path=file_path, extension=ProfilingOutputFormat.YAML)
        
        
# Implementation of the class 
class ObservationsHandler:
    _avaliable_observers = {OvserverStrategy.JSON: JSONObserver,
                            OvserverStrategy.TXT: TXTObserver,
                            OvserverStrategy.YAML: YAMLObserver}
    
    def __init__(self, storages: list[tuple[ProfilingOutputFormat, str]]):
        self._storages = set(storages)
        
    @classmethod
    def add_observer(cls, observer: ProfilingObserverI, observer_name: str):
        check_strategy(strategy=observer,
                       interface=ProfilingObserverI,
                       exception_name='InvalidfTimeProfilingObserverError')
        
        check_input_type(provided_input=observer_name,
                         required_input_type=str,
                         exception_name='InvalidProfilingObserverName')
        
        cls._avaliable_observers[observer_name] = observer
        
        
    @classmethod
    def remove_observer(cls, observer_name: str):
        if observer_name in cls._avaliable_observers:
            del cls._avaliable_observers[observer_name]
        
        
    def save_result(self, result: fTimeProfilingResultI) -> InvalidStrategyError | None:
        check_input_type(provided_input=result,
                         required_input_type=fTimeProfilingResultI,
                         exception_name='InvalidfTimeProfilingResultError')
        
        for storage_format, storage_file_path in self._storages:
            self._avaliable_observers[storage_format].save_result(result, storage_file_path)
            
        
        