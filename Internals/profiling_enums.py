from enum import Enum


class ProfilingOutputFormat(Enum):
    JSON = '.json'
    TXT = '.txt'
    YAML = '.yaml'

class SerializationStrategy(Enum):
    JSON = 'json'
    TXT = 'txt'
    YAML = 'yaml'
    
class OvserverStrategy(Enum):
    JSON = 'json'
    TXT = 'txt'
    YAML = 'yaml'
    
    
class fTimeProfilingStrategy(Enum):
    BASE = 'Base Time Profiler'
    PRECISE = 'Precise Time Profiler'
    CPU = 'CPU Time Profiler'
    THREAD = 'Thread Time Profiler'
    MONOTONIC = 'Monotonic Time Profiler'


    