import ccxt
import websocket
import requests
from typing import Dict, Any, List, Optional, Union, Callable
import json
import hmac
import hashlib
import time
from websocket import WebSocketApp

class APIEngine:
    def __init__(self):
        self.connections: Dict[str, Any] = {}
        self.api_keys: Dict[str, Dict[str, str]] = {}
        self.active_streams: Dict[str, WebSocketApp] = {}
        self.order_cache: Dict[str, Any] = {}
        
        self.exchanges = {
            'dhan': None,
            'angelone': None,
            'zerodha': None,
            'upstox': None,
            'icici': None,
            'binance': None,
            'coinbase': None,
            'kraken': None
        }

    def _connect_zerodha(self, credentials: Dict[str, str]) -> Any:
        """Connect to Zerodha broker API"""
        api_key = credentials.get('api_key')
        api_secret = credentials.get('api_secret')
        return {'session': requests.Session(), 'auth': {'key': api_key, 'secret': api_secret}}


        
    def connect_broker(self, broker: str, credentials: Dict[str, str]) -> bool:
        """Connect to broker API"""
        try:
            if broker == 'dhan':
                self.exchanges[broker] = self._connect_dhan(credentials)
            elif broker == 'angelone':
                self.exchanges[broker] = self._connect_angelone(credentials)
            elif broker == 'zerodha':
                self.exchanges[broker] = self._connect_zerodha(credentials)
            self.api_keys[broker] = credentials
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def execute_trade(self, 
                     broker: str, 
                     symbol: str, 
                     order_type: str, 
                     quantity: int,
                     price: Optional[float] = None) -> Dict[str, Any]:
        """Execute trade on connected broker"""
        if broker not in self.exchanges or not self.exchanges[broker]:
            raise ValueError(f"Broker {broker} not connected")
            
        try:
            if broker == 'dhan':
                return self._execute_dhan_trade(symbol, order_type, quantity, price)
            elif broker == 'angelone':
                return self._execute_angelone_trade(symbol, order_type, quantity, price)
            # Add other brokers
        except Exception as e:
            print(f"Trade execution error: {e}")
            return {'status': 'error', 'message': str(e)}

    def stream_data(self, 
                   broker: str,
                   symbols: List[str],
                   callback: Callable) -> None:
        """Start websocket stream for real-time data"""
        if broker not in self.exchanges:
            raise ValueError(f"Broker {broker} not supported")
            
        ws = websocket.WebSocketApp(
            self._get_websocket_url(broker),
            on_message=lambda ws, msg: self._on_message(msg, callback),
            on_error=lambda ws, err: self._on_error(err),
            on_close=lambda ws: self._on_close(),
            on_open=lambda ws: self._on_connect(broker, symbols)
        )
        
        self.active_streams[broker] = ws
        ws.run_forever()

    def _connect_dhan(self, credentials: Dict[str, str]) -> Any:
        """Connect to Dhan broker API"""
        api_key = credentials.get('api_key')
        api_secret = credentials.get('api_secret')
        # Implement Dhan-specific connection logic
        return {'session': requests.Session(), 'auth': {'key': api_key, 'secret': api_secret}}

    def _connect_angelone(self, credentials: Dict[str, str]) -> Any:
        """Connect to Angel One broker API"""
        api_key = credentials.get('api_key')
        api_secret = credentials.get('api_secret')
        # Implement Angel One-specific connection logic
        return {'session': requests.Session(), 'auth': {'key': api_key, 'secret': api_secret}}

    def _execute_dhan_trade(self, 
                          symbol: str,
                          order_type: str,
                          quantity: int,
                          price: Optional[float]) -> Dict[str, Any]:
        """Execute trade on Dhan"""
        endpoint = "https://api.dhan.co/orders"
        payload = {
            'trading_symbol': symbol,
            'quantity': quantity,
            'order_type': order_type,
            'price': price,
            'product': 'CNC',
            'exchange': 'NSE'
        }
        
        response = requests.post(
            endpoint,
            json=payload,
            headers=self._get_dhan_headers()
        )
        
        return response.json()

    def _execute_angelone_trade(self, 
                              symbol: str,
                              order_type: str,
                              quantity: int,
                              price: Optional[float]) -> Dict[str, Any]:
        """Execute trade on Angel One"""
        endpoint = "https://api.angelbroking.com/order/v1/placeOrder"
        payload = {
            'symbol': symbol,
            'qty': quantity,
            'type': order_type,
            'price': price,
            'product': 'DELIVERY',
            'exchange': 'NSE'
        }
        
        response = requests.post(
            endpoint,
            json=payload,
            headers=self._get_angelone_headers()
        )
        
        return response.json()

    def _get_dhan_headers(self) -> Dict[str, str]:
        """Generate headers for Dhan API"""
        timestamp = str(int(time.time() * 1000))
        signature = self._generate_signature(
            self.api_keys['dhan']['api_secret'],
            timestamp
        )
        
        return {
            'X-Auth-Token': self.api_keys['dhan']['api_key'],
            'X-Auth-Signature': signature,
            'X-Auth-Timestamp': timestamp,
            'Content-Type': 'application/json'
        }

    def _get_angelone_headers(self) -> Dict[str, str]:
        """Generate headers for Angel One API"""
        return {
            'X-PrivateKey': self.api_keys['angelone']['api_key'],
            'Accept': 'application/json',
            'X-SourceID': 'WEB',
            'Content-Type': 'application/json'
        }

    def _generate_signature(self, secret: str, timestamp: str) -> str:
        """Generate API signature"""
        message = timestamp + "GET/user/verify"
        signature = hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _get_websocket_url(self, broker: str) -> str:
        """Get websocket URL for broker"""
        urls = {
            'dhan': 'wss://stream.dhan.co',
            'angelone': 'wss://stream.angelbroking.com/websocket',
            'zerodha': 'wss://ws.kite.trade'
        }
        return urls.get(broker, '')

    def _on_message(self, message: str, callback: Callable) -> None:
        """Handle websocket messages"""
        data = json.loads(message)
        callback(data)

    def _on_error(self, error: str) -> None:
        """Handle websocket errors"""
        print(f"WebSocket error: {error}")

    def _on_close(self) -> None:
        """Handle websocket connection close"""
        print("WebSocket connection closed")

    def _on_connect(self, broker: str, symbols: List[str]) -> None:
        """Handle websocket connection open"""
        subscribe_message = self._get_subscribe_message(broker, symbols)
        self.active_streams[broker].send(json.dumps(subscribe_message))

    def _get_subscribe_message(self, broker: str, symbols: List[str]) -> Dict:
        """Generate subscription message for websocket"""
        if broker == 'dhan':
            return {
                'action': 'subscribe',
                'params': {
                    'symbols': symbols,
                    'mode': 'full'
                }
            }
        elif broker == 'angelone':
            return {
                'type': 'subscribe',
                'symbols': symbols
            }
        return {}

def get_api_registry(api_engine: APIEngine) -> Dict:
    """Create registry of API functions"""
    return {
        # Broker Connections
        'connect_broker': api_engine.connect_broker,
        'execute_trade': api_engine.execute_trade,
        'stream_data': api_engine.stream_data,
        
        # Data APIs
        'data_binance': lambda symbols: api_engine.connect_broker('binance', symbols),
        'data_coinbase': lambda symbols: api_engine.connect_broker('coinbase', symbols),
        'data_kraken': lambda symbols: api_engine.connect_broker('kraken', symbols),
        'data_bitfinex': lambda symbols: api_engine.connect_broker('bitfinex', symbols),
        'data_bitmex': lambda symbols: api_engine.connect_broker('bitmex', symbols),
        'data_deribit': lambda symbols: api_engine.connect_broker('deribit', symbols),
        'data_ftx': lambda symbols: api_engine.connect_broker('ftx', symbols),
        'data_bybit': lambda symbols: api_engine.connect_broker('bybit', symbols),
        
        # API Interfaces
        'rest_api': api_engine.execute_trade,
        'websocket_api': api_engine.stream_data,
        'fix_api': lambda: None,  # Implement FIX protocol if needed
        'ccxt_api': lambda: None,  # Implement CCXT integration if needed
        'broker_api': api_engine.connect_broker,
        'exchange_api': api_engine.connect_broker,
        'data_api': api_engine.stream_data,
        'trading_api': api_engine.execute_trade
    }
