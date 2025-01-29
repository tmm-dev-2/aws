def long_position(start_price, stop_loss, take_profit, quantity, adjustment_points=None):
    """
    Calculates the potential profit, loss, risk/reward ratio, and amount for a long position,
    allowing for adjustment points for resizing, drag and drop, and adjusting height/width.

    Args:
        start_price (float): The entry price of the long position.
        stop_loss (float): The price at which to exit the position to limit losses.
        take_profit (float): The price at which to exit the position to realize profits.
        quantity (float): The quantity of the asset being traded.
        adjustment_points (list, optional): A list of points representing the adjustment handles. Defaults to None.

    Returns:
        dict: A dictionary containing the potential profit, loss, risk/reward ratio, amount, and adjusted points.
    """
    profit = (take_profit - start_price) * quantity
    loss = (start_price - stop_loss) * quantity
    if loss == 0:
        risk_reward_ratio = float('inf')
    else:
        risk_reward_ratio = profit / abs(loss)
    
    adjusted_points = adjustment_points if adjustment_points else []
    
    return {
        "profit": profit,
        "loss": loss,
        "risk_reward_ratio": risk_reward_ratio,
        "amount": profit if profit > 0 else loss,
        "adjusted_points": adjusted_points
    }


def short_position(start_price, stop_loss, take_profit, quantity, adjustment_points=None):
    """
    Calculates the potential profit, loss, risk/reward ratio, and amount for a short position,
    allowing for adjustment points for resizing, drag and drop, and adjusting height/width.

    Args:
        start_price (float): The entry price of the short position.
        stop_loss (float): The price at which to exit the position to limit losses.
        take_profit (float): The price at which to exit the position to realize profits.
        quantity (float): The quantity of the asset being traded.
        adjustment_points (list, optional): A list of points representing the adjustment handles. Defaults to None.

    Returns:
        dict: A dictionary containing the potential profit, loss, risk/reward ratio, amount, and adjusted points.
    """
    profit = (start_price - take_profit) * quantity
    loss = (stop_loss - start_price) * quantity
    if loss == 0:
        risk_reward_ratio = float('inf')
    else:
        risk_reward_ratio = profit / abs(loss)
    
    adjusted_points = adjustment_points if adjustment_points else []
    
    return {
        "profit": profit,
        "loss": loss,
        "risk_reward_ratio": risk_reward_ratio,
        "amount": profit if profit > 0 else loss,
        "adjusted_points": adjusted_points
    }


def forecast(start_price, end_price, start_time, end_time, adjustment_points=None):
    """
    Generates a price forecast based on a start and end price and time,
    allowing for adjustment points for resizing, drag and drop, and adjusting height/width.

    Args:
        start_price (float): The starting price of the forecast.
        end_price (float): The ending price of the forecast.
        start_time (int): The starting time of the forecast.
        end_time (int): The ending time of the forecast.
        adjustment_points (list, optional): A list of points representing the adjustment handles. Defaults to None.

    Returns:
        dict: A dictionary containing the forecasted price, time, and adjusted points.
    """
    
    adjusted_points = adjustment_points if adjustment_points else []
    
    return {
        "forecasted_price": end_price,
        "forecasted_time": end_time,
        "adjusted_points": adjusted_points
    }


def projection(points, adjustment_points=None):
    """
    Projects a price range based on a drawn shape,
    allowing for adjustment points for resizing, drag and drop, and adjusting height/width.

    Args:
        points (list): A list of points defining the shape.
        adjustment_points (list, optional): A list of points representing the adjustment handles. Defaults to None.

    Returns:
        dict: A dictionary containing the projected price range and adjusted points.
    """
    
    adjusted_points = adjustment_points if adjustment_points else []
    
    return {
        "projected_price_range": points,
        "adjusted_points": adjusted_points
    }