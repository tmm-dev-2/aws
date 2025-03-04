import subprocess
import os
import sys
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import numpy as np
from datetime import datetime
# Engine Imports
from ..indicators.technical import (
    TechnicalAnalysis,
    TechnicalAnalysisEngine
)

from ..indicators.patterns import (
    PatternsEngine,
    PatternSyntax,
    HarmonicEngine,
    ElliottWaveEngine,
    FibonacciEngine
)

from ..indicators.micro_structures import (
    OrderFlowEngine,
    MicroStructuresSyntax,
    AuctionMarketEngine
)

from ..data.market_data import (
    MarketDataEngine,
    TimeEngine,
    MarketDataSyntax,
    SessionEngine
)

from ..visualization.renderer import (
    ChartEngine,
    PlotEngine,
    IndicatorEngine,
    DrawingEngine,
    RenderEngine,
)

from ..data.api import (  
    APIEngine
)

from ..system.system import (
    SystemEngine
)

from ..strategies.strategy import (
    StrategyEngine,
    StrategySyntax,
    TradeEngine,
    PerformanceEngine,
    RiskEngine
)

from ..strategies.risk import (
    RiskEngine,
)

from ..ml.engine import (
    MLEngine
)

from ..data.series import (
    SeriesSyntax,
    ArrayEngine,
    MatrixEngine,
    MathEngine
)

from ..data.symbol import (
    TVSymbolEngine,
    TVSymbolSyntax
)

from language_bridge import LanguageBridge

class EnvironmentManager:
    def __init__(self):
        # Initialize paths first
        self.base_path = Path('.venv')
        self.base_path.mkdir(exist_ok=True)
        
        # Set env_paths
        self.env_paths = {
            'python': self.base_path / 'python',
            'julia': self.base_path / 'julia',
            'r': self.base_path / 'r',
            'rust': self.base_path / 'rust',
            'devscript': self.base_path / 'devscript'
        }
        
        # Create directories
        for path in self.env_paths.values():
            path.mkdir(exist_ok=True)

        # Initialize core components
        self.shared_memory = {}
        self.active_runtimes = set()
        self.bridge = LanguageBridge(self)

        # Initialize Technical Analysis Suite
        self.technical_analysis = TechnicalAnalysis()
        self.technical_engine = TechnicalAnalysisEngine()

        # Initialize Pattern Suite
        self.patterns_engine = PatternsEngine()
        self.pattern_syntax = PatternSyntax()
        self.harmonic = HarmonicEngine()
        self.elliott = ElliottWaveEngine()
        self.fibonacci = FibonacciEngine()

        # Initialize Microstructure Suite
        self.order_flow = OrderFlowEngine()
        self.micro_syntax = MicroStructuresSyntax()
        self.auction = AuctionMarketEngine()

        # Initialize Market Data Suite
        self.market_data = MarketDataEngine()
        self.time = TimeEngine()
        self.market_syntax = MarketDataSyntax()
        self.session = SessionEngine()

        # Initialize Visualization Suite
        self.chart = ChartEngine()
        self.plot = PlotEngine()
        self.indicator = IndicatorEngine()
        self.drawing = DrawingEngine()
        self.render = RenderEngine()

        # Initialize API Suite
        self.api = APIEngine()

        # Initialize System Suite
        self.system = SystemEngine()

        # Initialize Strategy Suite
        self.strategy = StrategyEngine()
        self.strategy_syntax = StrategySyntax()
        self.trade = TradeEngine()
        self.performance = PerformanceEngine()
        self.risk = RiskEngine()

        # Initialize ML Suite
        self.ml = MLEngine()

        # Initialize Series Suite
        self.series_syntax = SeriesSyntax()
        self.array = ArrayEngine()
        self.matrix = MatrixEngine()
        self.math = MathEngine()

        # Initialize Symbol Suite
        self.symbol = TVSymbolEngine()
        self.symbol_syntax = TVSymbolSyntax()
        
        # Setup environments and interpreters
        self.setup_environments()
        self.interpreters = self.init_interpreters()

    # Rest of the methods remain same but update get_env_info() and _execute_python()
    def get_env_info(self) -> Dict[str, Any]:
        return {
            'active_runtimes': list(self.active_runtimes),
            'interpreters': self.interpreters,
            'paths': {k: str(v) for k, v in self.env_paths.items()},
            'shared_memory_size': len(self.shared_memory),
            'engines': {
                'technical': {
                    'analysis': self.technical_analysis.status(),
                    'engine': self.technical_engine.status()
                },
                'patterns': {
                    'engine': self.patterns_engine.status(),
                    'harmonic': self.harmonic.status(),
                    'elliott': self.elliott.status(),
                    'fibonacci': self.fibonacci.status()
                },
                'microstructure': {
                    'order_flow': self.order_flow.status(),
                    'auction': self.auction.status()
                },
                'market_data': {
                    'engine': self.market_data.status(),
                    'time': self.time.status(),
                    'session': self.session.status()
                },
                'visualization': {
                    'chart': self.chart.status(),
                    'plot': self.plot.status(),
                    'indicator': self.indicator.status(),
                    'drawing': self.drawing.status(),
                    'render': self.render.status()
                },
                'api': {
                    'engine': self.api.status()
                },
                'system': {
                    'engine': self.system.status()
                },
                'strategy': {
                    'engine': self.strategy.status(),
                    'trade': self.trade.status(),
                    'performance': self.performance.status(),
                    'risk': self.risk.status()
                },
                'ml': {
                    'engine': self.ml.status()
                },
                'series': {
                    'array': self.array.status(),
                    'matrix': self.matrix.status(),
                    'math': self.math.status()
                },
                'symbol': {
                    'engine': self.symbol.status()
                }
            }
        }

    def _execute_python(self, code: str, params: Optional[Dict] = None) -> Any:
        local_vars = params or {}
        local_vars.update({
            'bridge': self.bridge,
            'shared_memory': self.shared_memory,
            'np': np,
            'datetime': datetime,
            'env': self,
            'technical': {
                'analysis': self.technical_analysis,
                'engine': self.technical_engine
            },
            'patterns': {
                'engine': self.patterns_engine,
                'harmonic': self.harmonic,
                'elliott': self.elliott,
                'fibonacci': self.fibonacci
            },
            'micro': {
                'order_flow': self.order_flow,
                'auction': self.auction
            },
            'market': {
                'data': self.market_data,
                'time': self.time,
                'session': self.session
            },
            'viz': {
                'chart': self.chart,
                'plot': self.plot,
                'indicator': self.indicator,
                'drawing': self.drawing,
                'render': self.render
            },
            'api': self.api,
            'system': self.system,
            'strategy': {
                'engine': self.strategy,
                'trade': self.trade,
                'performance': self.performance,
                'risk': self.risk
            },
            'ml': self.ml,
            'series': {
                'array': self.array,
                'matrix': self.matrix,
                'math': self.math
            },
            'symbol': {
                'engine': self.symbol
            }
        })
        
        context = {
            '__builtins__': __builtins__,
            **globals(),
            **local_vars
        }
        
        exec(code, context, local_vars)
        return local_vars.get('result')

    def _execute_julia(self, code: str, params: Optional[Dict] = None) -> Any:
        temp_file = self.env_paths['julia'] / 'temp.jl'
        with open(temp_file, 'w') as f:
            f.write(code)
        result = subprocess.run(['julia', str(temp_file)], capture_output=True, text=True)
        return result.stdout

    def _execute_r(self, code: str, params: Optional[Dict] = None) -> Any:
        temp_file = self.env_paths['r'] / 'temp.R'
        with open(temp_file, 'w') as f:
            f.write(code)
        result = subprocess.run(['Rscript', str(temp_file)], capture_output=True, text=True)
        return result.stdout

    def _execute_rust(self, code: str, params: Optional[Dict] = None) -> Any:
        temp_dir = self.env_paths['rust'] / 'temp'
        temp_dir.mkdir(exist_ok=True)
        src_file = temp_dir / 'main.rs'
        with open(src_file, 'w') as f:
            f.write(code)
        subprocess.run(['rustc', str(src_file), '-o', str(temp_dir / 'output')])
        result = subprocess.run([str(temp_dir / 'output')], capture_output=True, text=True)
        return result.stdout

    def _execute_devscript(self, code: str, params: Optional[Dict] = None) -> Any:
        return None

    def execute_code(self, code: str, language: str, params: Optional[Dict] = None) -> Any:
        if language not in self.interpreters:
            raise ValueError(f"Unsupported language: {language}")
        
        self.active_runtimes.add(language)
        try:
            if language == 'python':
                return self._execute_python(code, params)
            elif language == 'julia':
                return self._execute_julia(code, params)
            elif language == 'r':
                return self._execute_r(code, params)
            elif language == 'rust':
                return self._execute_rust(code, params)
            elif language == 'devscript':
                return self._execute_devscript(code, params)
        finally:
            self.active_runtimes.remove(language)
