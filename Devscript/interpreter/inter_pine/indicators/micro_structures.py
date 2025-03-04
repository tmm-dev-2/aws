import numpy as np
from datetime import datetime
import pandas as pd
from scipy import stats

class OrderFlowEngine:
    def __init__(self):
        self.tick_data = []
        self.order_book = {}
    
    def calculate_volume_delta(self, trades):
        buy_volume = sum(trade['volume'] for trade in trades if trade['side'] == 'buy')
        sell_volume = sum(trade['volume'] for trade in trades if trade['side'] == 'sell')
        return buy_volume - sell_volume
    
    def calculate_volume_imbalance(self, trades):
        buy_volume = sum(trade['volume'] for trade in trades if trade['side'] == 'buy')
        sell_volume = sum(trade['volume'] for trade in trades if trade['side'] == 'sell')
        total_volume = buy_volume + sell_volume
        return (buy_volume - sell_volume) / total_volume if total_volume > 0 else 0
    
    def calculate_order_flow_imbalance(self, orders):
        bid_volume = sum(order['volume'] for order in orders if order['side'] == 'bid')
        ask_volume = sum(order['volume'] for order in orders if order['side'] == 'ask')
        return {
            'bid_volume': bid_volume,
            'ask_volume': ask_volume,
            'imbalance': bid_volume - ask_volume
        }
    
    def analyze_trade_flow(self, trades):
        large_trades = [t for t in trades if t['volume'] > self._calculate_large_trade_threshold(trades)]
        return {
            'large_trades': large_trades,
            'average_size': sum(t['volume'] for t in trades) / len(trades),
            'trade_count': len(trades),
            'volume_profile': self._generate_volume_profile(trades)
        }
    
    def analyze_liquidity(self, orderbook):
        return {
            'bid_liquidity': sum(level['volume'] for level in orderbook['bids']),
            'ask_liquidity': sum(level['volume'] for level in orderbook['asks']),
            'spread': orderbook['asks'][0]['price'] - orderbook['bids'][0]['price'],
            'depth_imbalance': self._calculate_depth_imbalance(orderbook)
        }
    
    def calculate_market_depth(self, orderbook):
        depth_levels = 10
        return {
            'bids': self._aggregate_depth(orderbook['bids'], depth_levels),
            'asks': self._aggregate_depth(orderbook['asks'], depth_levels)
        }
    
    def calculate_spread(self, quotes):
        return {
            'spread': quotes['ask'] - quotes['bid'],
            'relative_spread': (quotes['ask'] - quotes['bid']) / quotes['bid'],
            'mid_price': (quotes['ask'] + quotes['bid']) / 2
        }
    
    def analyze_ticks(self, ticks):
        return {
            'tick_count': len(ticks),
            'average_size': sum(t['size'] for t in ticks) / len(ticks),
            'price_movement': self._analyze_price_movement(ticks),
            'tick_distribution': self._analyze_tick_distribution(ticks)
        }
    
    def _calculate_large_trade_threshold(self, trades):
        volumes = [t['volume'] for t in trades]
        return np.percentile(volumes, 90)
    
    def _generate_volume_profile(self, trades):
        prices = [t['price'] for t in trades]
        volumes = [t['volume'] for t in trades]
        return np.histogram(prices, weights=volumes, bins='auto')
    
    def _calculate_depth_imbalance(self, orderbook):
        bid_depth = sum(level['volume'] * level['price'] for level in orderbook['bids'])
        ask_depth = sum(level['volume'] * level['price'] for level in orderbook['asks'])
        return (bid_depth - ask_depth) / (bid_depth + ask_depth)
    
    def _aggregate_depth(self, levels, depth):
        aggregated = []
        for i in range(min(depth, len(levels))):
            aggregated.append({
                'price': levels[i]['price'],
                'volume': sum(l['volume'] for l in levels[:i+1])
            })
        return aggregated
    
    def _analyze_price_movement(self, ticks):
        prices = [t['price'] for t in ticks]
        return {
            'high': max(prices),
            'low': min(prices),
            'range': max(prices) - min(prices),
            'volatility': np.std(prices)
        }
    
    def _analyze_tick_distribution(self, ticks):
        sizes = [t['size'] for t in ticks]
        return {
            'mean': np.mean(sizes),
            'median': np.median(sizes),
            'std': np.std(sizes),
            'skew': stats.skew(sizes)
        }

class AuctionMarketEngine:
    def __init__(self):
        self.tpo_map = {}
        self.volume_profile = {}
    
    def generate_market_profile(self, data):
        price_levels = self._create_price_levels(data)
        tpo_count = self._count_tpo(data, price_levels)
        return {
            'price_levels': price_levels,
            'tpo_count': tpo_count,
            'value_area': self.calculate_value_area(tpo_count),
            'poc': self.find_poc(tpo_count)
        }
    
    def generate_volume_profile(self, data):
        volume_by_price = self._aggregate_volume_by_price(data)
        return {
            'volume_profile': volume_by_price,
            'vwap': self._calculate_vwap(data),
            'volume_poc': self._find_volume_poc(volume_by_price)
        }
    
    def calculate_tpo(self, data):
        tpo_map = self._generate_tpo_map(data)
        return {
            'tpo_map': tpo_map,
            'profile_structure': self._analyze_profile_structure(tpo_map),
            'distribution_type': self._determine_distribution_type(tpo_map)
        }
    
    def calculate_value_area(self, profile):
        total_tpo = sum(profile.values())
        value_area_volume = total_tpo * 0.70  # 70% value area
        
        sorted_prices = sorted(profile.items(), key=lambda x: x[1], reverse=True)
        value_area_prices = []
        cumulative_volume = 0
        
        for price, volume in sorted_prices:
            value_area_prices.append(price)
            cumulative_volume += volume
            if cumulative_volume >= value_area_volume:
                break
                
        return {
            'high': max(value_area_prices),
            'low': min(value_area_prices),
            'volume_covered': cumulative_volume / total_tpo
        }
    
    def find_poc(self, profile):
        return max(profile.items(), key=lambda x: x[1])[0]
    
    def identify_balance_areas(self, profile):
        poc = self.find_poc(profile)
        balance_threshold = max(profile.values()) * 0.5
        
        balance_areas = []
        current_area = []
        
        for price in sorted(profile.keys()):
            if profile[price] >= balance_threshold:
                current_area.append(price)
            elif current_area:
                balance_areas.append({
                    'high': max(current_area),
                    'low': min(current_area),
                    'volume': sum(profile[p] for p in current_area)
                })
                current_area = []
                
        return balance_areas
    
    def identify_excess_areas(self, profile):
        value_area = self.calculate_value_area(profile)
        excess_threshold = max(profile.values()) * 0.2
        
        excess_areas = []
        for price, volume in profile.items():
            if price > value_area['high'] or price < value_area['low']:
                if volume < excess_threshold:
                    excess_areas.append({
                        'price': price,
                        'volume': volume,
                        'side': 'high' if price > value_area['high'] else 'low'
                    })
                    
        return excess_areas
    
    def identify_auction_zones(self, profile):
        poc = self.find_poc(profile)
        value_area = self.calculate_value_area(profile)
        
        return {
            'acceptance': self._identify_acceptance_zones(profile, value_area),
            'rejection': self._identify_rejection_zones(profile, value_area),
            'rotation': self._identify_rotation_zones(profile, poc)
        }
    
    def _create_price_levels(self, data):
        prices = [d['price'] for d in data]
        min_price = min(prices)
        max_price = max(prices)
        tick_size = self._calculate_tick_size(data)
        
        return np.arange(min_price, max_price + tick_size, tick_size)
    
    def _count_tpo(self, data, price_levels):
        tpo_count = {price: 0 for price in price_levels}
        for d in data:
            price_level = self._find_nearest_price_level(d['price'], price_levels)
            tpo_count[price_level] += 1
        return tpo_count
    
    def _aggregate_volume_by_price(self, data):
        volume_profile = {}
        for d in data:
            price = self._round_to_tick(d['price'])
            if price not in volume_profile:
                volume_profile[price] = 0
            volume_profile[price] += d['volume']
        return volume_profile
    
    def _calculate_vwap(self, data):
        volume_price_sum = sum(d['price'] * d['volume'] for d in data)
        total_volume = sum(d['volume'] for d in data)
        return volume_price_sum / total_volume if total_volume > 0 else None
    
    def _generate_tpo_map(self, data):
        tpo_map = {}
        for d in data:
            time_period = self._get_time_period(d['timestamp'])
            price = self._round_to_tick(d['price'])
            if price not in tpo_map:
                tpo_map[price] = set()
            tpo_map[price].add(time_period)
        return tpo_map
    
    def _analyze_profile_structure(self, tpo_map):
        return {
            'shape': self._determine_profile_shape(tpo_map),
            'balance': self._calculate_profile_balance(tpo_map),
            'development': self._analyze_profile_development(tpo_map)
        }
    
    def _determine_distribution_type(self, tpo_map):
        poc_location = self._find_poc_location(tpo_map)
        distribution = {
            'type': 'normal',
            'skew': self._calculate_distribution_skew(tpo_map),
            'kurtosis': self._calculate_distribution_kurtosis(tpo_map)
        }
        
        if poc_location < 0.4:
            distribution['type'] = 'buying_tail'
        elif poc_location > 0.6:
            distribution['type'] = 'selling_tail'
            
        return distribution
    
    def _identify_acceptance_zones(self, profile, value_area):
        acceptance_zones = []
        threshold = max(profile.values()) * 0.6
        
        for price, volume in profile.items():
            if volume >= threshold:
                if price >= value_area['low'] and price <= value_area['high']:
                    acceptance_zones.append({
                        'price': price,
                        'volume': volume,
                        'strength': volume / max(profile.values())
                    })
                    
        return acceptance_zones
    
    def _identify_rejection_zones(self, profile, value_area):
        rejection_zones = []
        threshold = max(profile.values()) * 0.3
        
        for price, volume in profile.items():
            if volume <= threshold:
                if price < value_area['low'] or price > value_area['high']:
                    rejection_zones.append({
                        'price': price,
                        'volume': volume,
                        'strength': 1 - (volume / max(profile.values()))
                    })
                    
        return rejection_zones
    
    def _identify_rotation_zones(self, profile, poc):
        rotation_zones = []
        sorted_prices = sorted(profile.keys())
        poc_index = sorted_prices.index(poc)
        
        for i in range(1, len(sorted_prices)-1):
            prev_vol = profile[sorted_prices[i-1]]
            curr_vol = profile[sorted_prices[i]]
            next_vol = profile[sorted_prices[i+1]]
            
            if curr_vol < prev_vol and curr_vol < next_vol:
                rotation_zones.append({
                    'price': sorted_prices[i],
                    'type': 'low' if i < poc_index else 'high',
                    'strength': min(prev_vol, next_vol) / max(profile.values())
                })
                
        return rotation_zones
    
    def _calculate_tick_size(self, data):
        prices = sorted(set(d['price'] for d in data))
        differences = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
        return min(differences) if differences else 0.01
    
    def _find_nearest_price_level(self, price, price_levels):
        return price_levels[np.abs(price_levels - price).argmin()]
    
    def _round_to_tick(self, price):
        tick_size = self._calculate_tick_size([{'price': price}])
        return round(price / tick_size) * tick_size
    
    def _get_time_period(self, timestamp):
        return timestamp.strftime('%H%M')
    
    def _determine_profile_shape(self, tpo_map):
        distribution = [len(tpos) for tpos in tpo_map.values()]
        skewness = stats.skew(distribution)
        kurtosis = stats.kurtosis(distribution)
        
        if abs(skewness) < 0.5 and abs(kurtosis) < 1:
            return 'normal'
        elif skewness > 0.5:
            return 'right_skewed'
        else:
            return 'left_skewed'
    
    def _calculate_profile_balance(self, tpo_map):
        poc = self.find_poc(tpo_map)
        prices = sorted(tpo_map.keys())
        poc_index = prices.index(poc)
        
        volume_above = sum(len(tpo_map[p]) for p in prices[poc_index:])
        volume_below = sum(len(tpo_map[p]) for p in prices[:poc_index])
        
        return {
            'ratio': volume_above / volume_below if volume_below > 0 else float('inf'),
            'balance_type': 'balanced' if 0.8 <= volume_above/volume_below <= 1.2 else 'imbalanced'
        }
    
    def _analyze_profile_development(self, tpo_map):
        total_tpo = sum(len(tpos) for tpos in tpo_map.values())
        development_stages = []
        cumulative_tpo = 0
        
        for price, tpos in sorted(tpo_map.items()):
            cumulative_tpo += len(tpos)
            if cumulative_tpo / total_tpo >= 0.25 and not development_stages:
                development_stages.append(('initial_balance', price))
            elif cumulative_tpo / total_tpo >= 0.5 and len(development_stages) == 1:
                development_stages.append(('development', price))
            elif cumulative_tpo / total_tpo >= 0.75 and len(development_stages) == 2:
                development_stages.append(('completion', price))
                
        return development_stages

class MicroStructuresSyntax:
    def __init__(self):
        self.orderflow_engine = OrderFlowEngine()
        self.auction_engine = AuctionMarketEngine()
        
        self.syntax_mappings = {
            # Order Flow Analysis
            'volume_delta': lambda trades: self.orderflow_engine.calculate_volume_delta(trades),
            'volume_imbalance': lambda trades: self.orderflow_engine.calculate_volume_imbalance(trades),
            'order_flow_imbalance': lambda orders: self.orderflow_engine.calculate_order_flow_imbalance(orders),
            'trade_flow': lambda trades: self.orderflow_engine.analyze_trade_flow(trades),
            'liquidity_analysis': lambda orderbook: self.orderflow_engine.analyze_liquidity(orderbook),
            'market_depth': lambda orderbook: self.orderflow_engine.calculate_market_depth(orderbook),
            'bid_ask_spread': lambda quotes: self.orderflow_engine.calculate_spread(quotes),
            'tick_analysis': lambda ticks: self.orderflow_engine.analyze_ticks(ticks),

            # Auction Market Analysis
            'market_profile': lambda data: self.auction_engine.generate_market_profile(data),
            'volume_profile': lambda data: self.auction_engine.generate_volume_profile(data),
            'time_price_opportunity': lambda data: self.auction_engine.calculate_tpo(data),
            'value_area': lambda profile: self.auction_engine.calculate_value_area(profile),
            'point_of_control': lambda profile: self.auction_engine.find_poc(profile),
            'balance_areas': lambda profile: self.auction_engine.identify_balance_areas(profile),
            'excess_areas': lambda profile: self.auction_engine.identify_excess_areas(profile),
            'auction_zones': lambda profile: self.auction_engine.identify_auction_zones(profile)
        }
