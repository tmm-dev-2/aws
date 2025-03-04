from typing import Any, Dict, List, Optional, Union
import numpy as np
from pathlib import Path
import json

class LanguageBridge:
    def __init__(self, env_manager):
        self.env_manager = env_manager
        self.shared_namespace = {}
        self.type_mappings = {
            'python': {
                'float': float,
                'int': int,
                'str': str,
                'list': list,
                'dict': dict,
                'array': np.ndarray
            },
            'julia': {
                'Float64': float,
                'Int64': int,
                'String': str,
                'Array': list,
                'Dict': dict
            },
            'r': {
                'numeric': float,
                'integer': int,
                'character': str,
                'vector': list,
                'list': dict
            },
            'rust': {
                'f64': float,
                'i64': int,
                'String': str,
                'Vec': list,
                'HashMap': dict
            }
        }

    def convert_data(self, data: Any, from_lang: str, to_lang: str) -> Any:
        """Convert data between different language types"""
        if from_lang == to_lang:
            return data
            
        if isinstance(data, np.ndarray):
            return self._convert_array(data, to_lang)
        elif isinstance(data, (list, tuple)):
            return self._convert_sequence(data, to_lang)
        elif isinstance(data, dict):
            return self._convert_dict(data, to_lang)
        return data

    def _convert_array(self, data: np.ndarray, target_lang: str) -> Any:
        """Convert numpy arrays to target language format"""
        if target_lang == 'python':
            return data
        elif target_lang == 'julia':
            return data.tolist()
        elif target_lang == 'r':
            return data.tolist()
        elif target_lang == 'rust':
            return data.tobytes()
        return data

    def _convert_sequence(self, data: Union[list, tuple], target_lang: str) -> Any:
        """Convert sequences to target language format"""
        if target_lang == 'python':
            return np.array(data)
        elif target_lang in ['julia', 'r']:
            return list(data)
        elif target_lang == 'rust':
            return np.array(data).tobytes()
        return data

    def _convert_dict(self, data: dict, target_lang: str) -> Any:
        """Convert dictionaries to target language format"""
        if target_lang in ['python', 'julia', 'r']:
            return data
        elif target_lang == 'rust':
            return json.dumps(data)
        return data

    def share_data(self, name: str, data: Any, source_lang: str) -> None:
        """Share data between languages through shared namespace"""
        self.shared_namespace[name] = {
            'data': data,
            'source': source_lang,
            'type': type(data).__name__
        }

    def get_shared_data(self, name: str, target_lang: str) -> Optional[Any]:
        """Retrieve shared data converted to target language format"""
        if name in self.shared_namespace:
            data_info = self.shared_namespace[name]
            return self.convert_data(
                data_info['data'],
                data_info['source'],
                target_lang
            )
        return None

    def serialize_data(self, data: Any, format: str = 'json') -> Union[str, bytes]:
        """Serialize data for cross-language transport"""
        if format == 'json':
            return json.dumps(self._make_serializable(data))
        elif format == 'binary':
            return self._serialize_binary(data)
        return str(data)

    def deserialize_data(self, data: Union[str, bytes], format: str = 'json') -> Any:
        """Deserialize data from cross-language transport"""
        if format == 'json':
            return json.loads(data)
        elif format == 'binary':
            return self._deserialize_binary(data)
        return data

    def _make_serializable(self, data: Any) -> Any:
        """Convert data to JSON serializable format"""
        if isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, (list, tuple)):
            return [self._make_serializable(item) for item in data]
        elif isinstance(data, dict):
            return {k: self._make_serializable(v) for k, v in data.items()}
        return data

    def _serialize_binary(self, data: Any) -> bytes:
        """Serialize data to binary format"""
        if isinstance(data, np.ndarray):
            return data.tobytes()
        elif isinstance(data, (list, tuple)):
            return np.array(data).tobytes()
        return str(data).encode()

    def _deserialize_binary(self, data: bytes) -> Any:
        """Deserialize data from binary format"""
        try:
            return np.frombuffer(data)
        except:
            return data.decode()

    def get_type_mapping(self, from_type: str, from_lang: str, to_lang: str) -> str:
        """Get equivalent type between languages"""
        if from_lang in self.type_mappings and to_lang in self.type_mappings:
            for to_type, py_type in self.type_mappings[to_lang].items():
                if py_type == self.type_mappings[from_lang].get(from_type):
                    return to_type
        return from_type

    def clear_shared_memory(self) -> None:
        """Clear shared namespace"""
        self.shared_namespace.clear()

    def get_memory_usage(self) -> Dict[str, int]:
        """Get shared memory usage statistics"""
        return {
            'items': len(self.shared_namespace),
            'types': len(set(info['type'] for info in self.shared_namespace.values()))
        }
