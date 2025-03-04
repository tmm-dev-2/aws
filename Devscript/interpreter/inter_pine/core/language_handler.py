import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
import subprocess
import sys
import re
import pygments
from pygments.lexers import PythonLexer, RLexer, RustLexer
from pygments.formatters import HtmlFormatter

class LanguageHandler:
    def __init__(self):
        self.shared_data = {}
        self.environments = {
            'python': self._setup_python(),
            'r': self._setup_r(),
            'rust': self._setup_rust(),
            'devscript': self._setup_devscript()
        }
        self.python_namespace = {
            'np': np,
            'pd': pd,
            **self.shared_data
        }
        pandas2ri.activate()
        
    def _setup_python(self):
        return {
            'exec': lambda code: exec(code, self.python_namespace),
            'eval': lambda expr: eval(expr, self.python_namespace),
            'highlight': self._highlight_python,
            'convert': lambda x: x,
            'completions': {
                'np': dir(np),
                'pd': dir(pd),
                'built_in': dir(__builtins__)
            }
        }
        
    def _setup_r(self):
        r_base_functions = list(robjects.r('ls(baseenv())'))
        return {
            'exec': lambda code: robjects.r(code),
            'eval': lambda expr: robjects.r(expr),
            'highlight': self._highlight_r,
            'convert': self._convert_r_to_python,
            'completions': {
                'base': r_base_functions,
                'stats': list(robjects.r('ls("package:stats")')),
                'utils': list(robjects.r('ls("package:utils")'))
            }
        }
        
    def _setup_rust(self):
        rust_keywords = ['fn', 'let', 'mut', 'pub', 'struct', 'enum', 'match', 'if', 'else', 'loop', 'while', 'for']
        return {
            'exec': self._execute_rust,
            'eval': self._eval_rust,
            'highlight': self._highlight_rust,
            'convert': lambda x: x,
            'completions': {
                'keywords': rust_keywords,
                'types': ['i32', 'f64', 'bool', 'String', 'Vec', 'Option', 'Result']
            }
        }
        
    def _setup_devscript(self):
        from .devscript_syntax import DEVSCRIPT_KEYWORDS, DEVSCRIPT_FUNCTIONS
        return {
            'exec': self._execute_devscript,
            'eval': self._eval_devscript,
            'highlight': self._highlight_devscript,
            'convert': lambda x: x,
            'completions': {
                'keywords': DEVSCRIPT_KEYWORDS,
                'functions': DEVSCRIPT_FUNCTIONS
            }
        }

    def _convert_r_to_python(self, r_obj):
        if isinstance(r_obj, robjects.vectors.DataFrame):
            with pandas2ri.localconverter():
                return pandas2ri.rpy2py(r_obj)
        elif isinstance(r_obj, robjects.vectors.FloatVector):
            return np.array(r_obj)
        elif isinstance(r_obj, robjects.vectors.StrVector):
            return list(r_obj)
        elif isinstance(r_obj, robjects.vectors.IntVector):
            return np.array(r_obj, dtype=int)
        elif isinstance(r_obj, robjects.vectors.BoolVector):
            return np.array(r_obj, dtype=bool)
        return r_obj

    def _execute_rust(self, code: str) -> Any:
        rust_template = """
#[allow(unused_imports)]
use std::{{collections::*, vec::Vec}};

fn main() {{
    {}
}}
"""
        full_code = rust_template.format(code)
        
        with open("D:/temp/temp.rs", "w") as f:
            f.write(full_code)
        
        try:
            compile_result = subprocess.run(
                ["rustc", "D:/temp/temp.rs", "-o", "D:/temp/output.exe"],
                capture_output=True,
                text=True,
                check=True
            )
            
            run_result = subprocess.run(
                ["D:/temp/output.exe"],
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                'stdout': run_result.stdout,
                'stderr': run_result.stderr,
                'success': True
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'stdout': '',
                'stderr': e.stderr,
                'success': False,
                'error': str(e)
            }

    def _eval_rust(self, expr: str) -> Any:
        code = f"""
fn main() {{
    let result = {expr};
    println!("{{:?}}", result);
}}
"""
        return self._execute_rust(code)

    def _execute_devscript(self, code: str) -> Any:
        from .interpreter import DevScriptInterpreter
        interpreter = DevScriptInterpreter()
        try:
            result = interpreter.execute(code)
            return {
                'result': result,
                'success': True
            }
        except Exception as e:
            return {
                'result': None,
                'success': False,
                'error': str(e)
            }

    def _eval_devscript(self, expr: str) -> Any:
        from .interpreter import DevScriptInterpreter
        interpreter = DevScriptInterpreter()
        try:
            result = interpreter.evaluate(expr)
            return {
                'result': result,
                'success': True
            }
        except Exception as e:
            return {
                'result': None,
                'success': False,
                'error': str(e)
            }

    def execute_block(self, code: str, language: str) -> Any:
        if language not in self.environments:
            raise ValueError(f"Language {language} not supported")
            
        # Extract imports and dependencies
        imports = self._extract_imports(code, language)
        
        # Handle dependencies
        self._handle_dependencies(imports, language)
        
        # Preprocess code
        processed_code = self._preprocess_code(code, language)
        
        # Execute
        try:
            result = self.environments[language]['exec'](processed_code)
            converted_result = self.environments[language]['convert'](result)
            
            return {
                'result': converted_result,
                'success': True
            }
            
        except Exception as e:
            return {
                'result': None,
                'success': False,
                'error': str(e)
            }

    def _extract_imports(self, code: str, language: str) -> list:
        if language == 'python':
            import_pattern = r'^import\s+(\w+)|^from\s+(\w+)\s+import'
            matches = re.finditer(import_pattern, code, re.MULTILINE)
            return [m.group(1) or m.group(2) for m in matches]
            
        elif language == 'r':
            library_pattern = r'library\(([^)]+)\)'
            matches = re.finditer(library_pattern, code)
            return [m.group(1) for m in matches]
            
        elif language == 'rust':
            use_pattern = r'use\s+([\w:]+)'
            matches = re.finditer(use_pattern, code)
            return [m.group(1) for m in matches]
            
        return []

    def _handle_dependencies(self, imports: list, language: str):
        if language == 'python':
            for imp in imports:
                if imp not in sys.modules:
                    exec(f"import {imp}", self.python_namespace)
                    
        elif language == 'r':
            for pkg in imports:
                robjects.r(f'if (!require({pkg})) install.packages("{pkg}")')
                robjects.r(f'library({pkg})')

    def _preprocess_code(self, code: str, language: str) -> str:
        if language == 'python':
            return code
            
        elif language == 'r':
            # Handle data frame conversions
            for var in self.shared_data:
                if isinstance(self.shared_data[var], pd.DataFrame):
                    code = f"library(data.table)\n{code}"
                    break
            return code
            
        elif language == 'rust':
            return code.strip()
            
        elif language == 'devscript':
            return code.strip()
            
        return code

    def _highlight_python(self, code: str) -> str:
        return pygments.highlight(
            code,
            PythonLexer(),
            HtmlFormatter(style='monokai')
        )

    def _highlight_r(self, code: str) -> str:
        return pygments.highlight(
            code,
            RLexer(),
            HtmlFormatter(style='monokai')
        )

    def _highlight_rust(self, code: str) -> str:
        return pygments.highlight(
            code,
            RustLexer(),
            HtmlFormatter(style='monokai')
        )

    def _highlight_devscript(self, code: str) -> str:
        # Custom DevScript lexer would go here
        return code

    def get_completions(self, prefix: str, language: str, context: str = "") -> list:
        if language not in self.environments:
            return []
            
        completions = []
        env = self.environments[language]
        
        # Add language-specific completions
        if language == 'python':
            completions.extend(self._get_python_completions(prefix, context))
        elif language == 'r':
            completions.extend(self._get_r_completions(prefix))
        elif language == 'rust':
            completions.extend(self._get_rust_completions(prefix))
        elif language == 'devscript':
            completions.extend(self._get_devscript_completions(prefix))
            
        # Add shared data completions
        completions.extend(
            [var for var in self.shared_data.keys() if var.startswith(prefix)]
        )
        
        return sorted(set(completions))

    def _get_python_completions(self, prefix: str, context: str) -> list:
        completions = []
        
        # Context-aware completions
        if '.' in prefix:
            obj_name, partial = prefix.rsplit('.', 1)
            try:
                obj = eval(obj_name, self.python_namespace)
                completions.extend(
                    [f"{obj_name}.{attr}" for attr in dir(obj) if attr.startswith(partial)]
                )
            except:
                pass
        else:
            # Add built-ins
            completions.extend(
                [name for name in self.environments['python']['completions']['built_in'] 
                 if name.startswith(prefix)]
            )
            
            # Add numpy completions
            completions.extend(
                [f"np.{name}" for name in self.environments['python']['completions']['np'] 
                 if name.startswith(prefix)]
            )
            
            # Add pandas completions
            completions.extend(
                [f"pd.{name}" for name in self.environments['python']['completions']['pd'] 
                 if name.startswith(prefix)]
            )
            
        return completions

    def _get_r_completions(self, prefix: str) -> list:
        completions = []
        
        # Base R completions
        completions.extend(
            [name for name in self.environments['r']['completions']['base'] 
             if name.startswith(prefix)]
        )
        
        # Stats package completions
        completions.extend(
            [name for name in self.environments['r']['completions']['stats'] 
             if name.startswith(prefix)]
        )
        
        # Utils package completions
        completions.extend(
            [name for name in self.environments['r']['completions']['utils'] 
             if name.startswith(prefix)]
        )
        
        return completions

    def _get_rust_completions(self, prefix: str) -> list:
        completions = []
        
        # Keywords
        completions.extend(
            [kw for kw in self.environments['rust']['completions']['keywords'] 
             if kw.startswith(prefix)]
        )
        
        # Types
        completions.extend(
            [t for t in self.environments['rust']['completions']['types'] 
             if t.startswith(prefix)]
        )
        
        return completions

    def _get_devscript_completions(self, prefix: str) -> list:
        completions = []
        
        # Keywords
        completions.extend(
            [kw for kw in self.environments['devscript']['completions']['keywords'] 
             if kw.startswith(prefix)]
        )
        
        # Functions
        completions.extend(
            [fn for fn in self.environments['devscript']['completions']['functions'] 
             if fn.startswith(prefix)]
        )
        
        return completions

    def share_data(self, name: str, value: Any):
        """Share data between language environments"""
        self.shared_data[name] = value
        
        # Update Python namespace
        self.python_namespace[name] = value
        
        # Share with R
        if isinstance(value, (list, np.ndarray)):
            self.environments['r']['exec'](
                f"{name} <- c({','.join(map(str, value))})"
            )
        elif isinstance(value, pd.DataFrame):
            with pandas2ri.localconverter():
                r_df = pandas2ri.py2rpy(value)
                robjects.globalenv[name] = r_df
        elif isinstance(value, (int, float, str, bool)):
            robjects.globalenv[name] = value
