import datetime

def calculate_price_range(start_price, end_price, start_x=None, start_y=None, end_x=None, end_y=None):
    """
    Calculates the absolute price range between two prices.
    Also includes adjustment points.

    Args:
        start_price (float): The starting price.
        end_price (float): The ending price.
        start_x (float, optional): The x-coordinate of the starting point. Defaults to None.
        start_y (float, optional): The y-coordinate of the starting point. Defaults to None.
        end_x (float, optional): The x-coordinate of the ending point. Defaults to None.
        end_y (float, optional): The y-coordinate of the ending point. Defaults to None.

    Returns:
        dict: A dictionary containing the price range and adjustment/resize points.
    """
    price_range = abs(end_price - start_price)
    adjustment_points = [{"x": start_x, "y": start_y}, {"x": end_x, "y": end_y}] if start_x is not None and start_y is not None and end_x is not None and end_y is not None else []
    return {
        "price_range": price_range,
        "adjustment_points": adjustment_points,
        "resize_points": [],
    }

def calculate_percentage_change(start_price, end_price):
    """
    Calculates the percentage change between two prices.

    Args:
        start_price (float): The starting price.
        end_price (float): The ending price.

    Returns:
        float: The percentage change between the start and end prices.
    """
    if start_price == 0:
        return 0
    return ((end_price - start_price) / start_price) * 100

def calculate_data_range(start_time, end_time, start_x=None, start_y=None, end_x=None, end_y=None):
    """
    Calculates the time difference between two timestamps.
    Also includes adjustment points.

    Args:
        start_time (datetime): The starting timestamp.
        end_time (datetime): The ending timestamp.
        start_x (float, optional): The x-coordinate of the starting point. Defaults to None.
        start_y (float, optional): The y-coordinate of the starting point. Defaults to None.
        end_x (float, optional): The x-coordinate of the ending point. Defaults to None.
        end_y (float, optional): The y-coordinate of the ending point. Defaults to None.

    Returns:
        dict: A dictionary containing the time difference and adjustment/resize points.
    """
    time_range = end_time - start_time
    adjustment_points = [{"x": start_x, "y": start_y}, {"x": end_x, "y": end_y}] if start_x is not None and start_y is not None and end_x is not None and end_y is not None else []
    return {
        "time_range": time_range,
        "adjustment_points": adjustment_points,
        "resize_points": [],
    }

def calculate_data_price_range(start_time, end_time, start_price, end_price, start_x, start_y, end_x, end_y):
    """
    Calculates the price range, time range, and formats the price range string.
    Also calculates adjustment and resize points.

    Args:
        start_time (datetime): The starting timestamp.
        end_time (datetime): The ending timestamp.
        start_price (float): The starting price.
        end_price (float): The ending price.
        start_x (float): The x-coordinate of the starting point.
        start_y (float): The y-coordinate of the starting point.
        end_x (float): The x-coordinate of the ending point.
        end_y (float): The y-coordinate of the ending point.

    Returns:
        dict: A dictionary containing the time difference (timedelta), formatted price range string,
              and adjustment/resize points.
    """
    time_range_data = calculate_data_range(start_time, end_time, start_x, start_y, end_x, end_y)
    price_range_data = calculate_price_range(start_price, end_price, start_x, start_y, end_x, end_y)
    price_range = price_range_data["price_range"]
    percentage_change = calculate_percentage_change(start_price, end_price)
    
    price_range_str = f"{end_price - start_price:.2f} ({percentage_change:.2f}%) {price_range:.0f}"

    # Adjustment points are the start and end points
    adjustment_points = [{"x": start_x, "y": start_y}, {"x": end_x, "y": end_y}]

    # Resize points are the corners of the bounding box
    resize_points = [
        {"x": min(start_x, end_x), "y": min(start_y, end_y)},
        {"x": max(start_x, end_x), "y": min(start_y, end_y)},
        {"x": max(start_x, end_x), "y": max(start_y, end_y)},
        {"x": min(start_x, end_x), "y": max(start_y, end_y)},
    ]

    return {
        "time_range": time_range_data["time_range"],
        "price_range_str": price_range_str,
        "adjustment_points": adjustment_points,
        "resize_points": resize_points,
    }