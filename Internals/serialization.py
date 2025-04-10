import inspect, json, yaml, pickle
from abc import ABC, abstractmethod
from typing import Any
from Internals.execution_guards import safe_serialization
from Internals.checks import *
from Internals.profiling_enums import ProfilingOutputFormat, SerializationStrategy


# Intorducing interface of Data Serialization class
class DataSerializerI(ABC):
    @abstractmethod
    def save(self, data: Any, file_path: str, encoding: str) -> None:
        ...
        
# Inplementation of JSON data serializer
class JSONSerializer(DataSerializerI):
    @classmethod
    @safe_serialization
    def save(cls, data: dict, file_path: str, mode: str = 'w', encoding: str = 'utf-8', indent: int = 4):
        check_path(file_path=file_path,
                   required_extension='.json',
                   exception_name='InvalidJSONFilePath')
        
        with open(file_path, mode=mode, encoding=encoding) as f:
            json.dump(data, f, indent=indent)
        
        
# Inplementation of TXT data serializer
class TXTSerializer(DataSerializerI):
    @classmethod
    @safe_serialization
    def save(cls, data: dict, file_path: str, mode='w', encoding: str = 'utf-8'):
        check_path(file_path=file_path,
                   required_extension='.txt',
                   exception_name='InvalidTXTFilePath')

        with open(file_path, mode=mode, encoding=encoding) as f:
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
                
        
# Inplementation of YAML data serializer
class YAMLSerializer(DataSerializerI):
    @classmethod
    @safe_serialization
    def save(cls, data: dict, file_path: str, mode='w', encoding: str = 'utf-8'):
        check_path(file_path=file_path,
                   required_extension='.yaml',
                   exception_name='InvalidYAMLFilePath')
        
        with open(file_path, mode=mode, encoding=encoding) as f:
            yaml.safe_dump(data, f)    
        
        
# Implementation of the class which will ...
class Serializer:
    _avaliable_serializers = {SerializationStrategy.JSON: JSONSerializer,
                             SerializationStrategy.TXT: TXTSerializer,
                             SerializationStrategy.YAML: YAMLSerializer}  
        
    @classmethod
    def add_serializer(cls, serializer: DataSerializerI, serializer_name: SerializationStrategy):
        check_strategy(strategy=serializer,
                       interface=DataSerializerI,
                       exception_name='InvalidSerializerError')
        
        check_input_type(provided_input=serializer_name,
                         required_input_type=SerializationStrategy,
                         exception_name='InvalidSerializerName')
            
        cls._avaliable_serializers[serializer_name] = serializer
        
        
    @classmethod
    def remove_serializer(cls, serializer_name: SerializationStrategy):
        if serializer_name in cls._avaliable_serializers:
            del cls._avaliable_serializers[serializer_name]
       
            
    @classmethod
    def avaliable_serializers(cls):
        return cls._avaliable_serializers
    
    
    @classmethod
    def save(cls, 
             data: Any, 
             file_path: str, mode='w', 
             encoding: str = 'utf-8', 
             serializer_name: SerializationStrategy = SerializationStrategy.TXT
             ) -> None:
        
        check_strategy_name(strategy_name=serializer_name,
                            avaliable_strategies=cls._avaliable_serializers.keys(),
                            exception_name='NonExistingSerializerError')
        
        cls._avaliable_serializers[serializer_name].save(data=data, 
                                                        file_path=file_path, 
                                                        mode=mode, encoding=encoding)
        