def _handle_strategy_operation(self, operation_name, args):
    if operation_name == 'strategyFunc':
        return {
            'positions': [],
            'orders': [],
            'closed_trades': [],
            'settings': {
                'initial_capital': args[0] if args else 100000,
                'commission': 0.1,
                'margin_long': 1.0,
                'margin_short': 1.0
            }
        }
    
    elif operation_name == 'strategyCancelFunc':
        order_id = args[0]
        strategy = args[1]
        strategy['orders'] = [order for order in strategy['orders'] if order['id'] != order_id]
        return strategy
    
    elif operation_name == 'strategyCancelAllFunc':
        strategy = args[0]
        strategy['orders'] = []
        return strategy
    
    elif operation_name == 'strategyCloseFunc':
        strategy = args[0]
        position_id = args[1]
        price = args[2]
        strategy['positions'] = [pos for pos in strategy['positions'] if pos['id'] != position_id]
        return strategy
    
    elif operation_name == 'strategyCloseAllFunc':
        strategy = args[0]
        price = args[1]
        strategy['positions'] = []
        return strategy
    
    elif operation_name == 'strategyEntryFunc':
        strategy = args[0]
        direction = args[1]  # 'long' or 'short'
        quantity = args[2]
        price = args[3]
        
        new_position = {
            'id': len(strategy['positions']),
            'direction': direction,
            'quantity': quantity,
            'entry_price': price,
            'entry_time': time.time(),
            'profit': 0
        }
        strategy['positions'].append(new_position)
        return strategy
    
    elif operation_name == 'strategyExitFunc':
        strategy = args[0]
        position_id = args[1]
        price = args[2]
        
        for pos in strategy['positions']:
            if pos['id'] == position_id:
                profit = (price - pos['entry_price']) * pos['quantity'] if pos['direction'] == 'long' else \
                        (pos['entry_price'] - price) * pos['quantity']
                closed_trade = {
                    'entry_price': pos['entry_price'],
                    'exit_price': price,
                    'quantity': pos['quantity'],
                    'direction': pos['direction'],
                    'profit': profit,
                    'entry_time': pos['entry_time'],
                    'exit_time': time.time()
                }
                strategy['closed_trades'].append(closed_trade)
                strategy['positions'] = [p for p in strategy['positions'] if p['id'] != position_id]
                break
        return strategy
    
    elif operation_name == 'strategyOrderFunc':
        strategy = args[0]
        order_type = args[1]  # 'limit', 'market', 'stop'
        direction = args[2]  # 'long' or 'short'
        quantity = args[3]
        price = args[4]
        
        new_order = {
            'id': len(strategy['orders']),
            'type': order_type,
            'direction': direction,
            'quantity': quantity,
            'price': price,
            'time': time.time()
        }
        strategy['orders'].append(new_order)
        return strategy

