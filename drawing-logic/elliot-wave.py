# Elliot Wave Logic

def draw_elliot_impulse_wave(start_point, end_point):
    """
    Draws an Elliot Impulse Wave (12345).
    Returns a dictionary containing points with types for drawing the wave and adjustment points.
    """
    x0, y0 = start_point
    x5, y5 = end_point

    # Calculate intermediate points based on the start and end points
    x1 = x0 + (x5 - x0) * 0.2
    y1 = y0 + (y5 - y0) * 0.3
    x2 = x0 + (x5 - x0) * 0.35
    y2 = y0 - (y5 - y0) * 0.2
    x3 = x0 + (x5 - x0) * 0.6
    y3 = y0 + (y5 - y0) * 0.5
    x4 = x0 + (x5 - x0) * 0.75
    y4 = y0 - (y5 - y0) * 0.1

    points = [
        {"x": x0, "y": y0, "type": "start"},
        {"x": x1, "y": y1, "type": "line"},
        {"x": x2, "y": y2, "type": "line"},
        {"x": x3, "y": y3, "type": "line"},
        {"x": x4, "y": y4, "type": "line"},
        {"x": x5, "y": y5, "type": "end"},
    ]
    adjustment_points = [
        {"x": x1, "y": y1, "type": "adjustment"},
        {"x": x2, "y": y2, "type": "adjustment"},
        {"x": x3, "y": y3, "type": "adjustment"},
        {"x": x4, "y": y4, "type": "adjustment"},
    ]
    return {"points": points, "adjustment_points": adjustment_points}


def draw_elliot_correction_wave(start_point, end_point):
    """
    Draws an Elliot Correction Wave (ABC).
    Returns a dictionary containing points with types for drawing the wave and adjustment points.
    """
    x0, y0 = start_point
    xC, yC = end_point

    # Calculate intermediate points based on the start and end points
    xA = x0 + (xC - x0) * 0.3
    yA = y0 + (xC - x0) * 0.5
    xB = x0 + (xC - x0) * 0.6
    yB = y0 - (xC - x0) * 0.3

    points = [
        {"x": x0, "y": y0, "type": "start"},
        {"x": xA, "y": yA, "type": "line"},
        {"x": xB, "y": yB, "type": "line"},
        {"x": xC, "y": yC, "type": "end"},
    ]
    adjustment_points = [
        {"x": xA, "y": yA, "type": "adjustment"},
        {"x": xB, "y": yB, "type": "adjustment"},
    ]
    return {"points": points, "adjustment_points": adjustment_points}


def draw_elliot_triangle_wave(start_point, end_point):
    """
    Draws an Elliot Triangle Wave (ABCDE).
    Returns a dictionary containing points with types for drawing the wave and adjustment points.
    """
    x0, y0 = start_point
    xE, yE = end_point

    # Calculate intermediate points based on the start and end points
    xA = x0 + (xE - x0) * 0.2
    yA = y0 + (xE - x0) * 0.4
    xB = x0 + (xE - x0) * 0.4
    yB = y0 - (xE - x0) * 0.2
    xC = x0 + (xE - x0) * 0.6
    yC = y0 + (xE - x0) * 0.3
    xD = x0 + (xE - x0) * 0.8
    yD = y0 - (xE - x0) * 0.1

    points = [
        {"x": x0, "y": y0, "type": "start"},
        {"x": xA, "y": yA, "type": "line"},
        {"x": xB, "y": yB, "type": "line"},
        {"x": xC, "y": yC, "type": "line"},
        {"x": xD, "y": yD, "type": "line"},
        {"x": xE, "y": yE, "type": "end"},
    ]
    adjustment_points = [
        {"x": xA, "y": yA, "type": "adjustment"},
        {"x": xB, "y": yB, "type": "adjustment"},
        {"x": xC, "y": yC, "type": "adjustment"},
        {"x": xD, "y": yD, "type": "adjustment"},
    ]
    return {"points": points, "adjustment_points": adjustment_points}


def draw_elliot_double_combo_wave(start_point, end_point):
    """
    Draws an Elliot Double Combo Wave (WXY).
    Returns a dictionary containing points with types for drawing the wave and adjustment points.
    """
    x0, y0 = start_point
    xY, yY = end_point

    # Calculate intermediate points based on the start and end points
    xW = x0 + (xY - x0) * 0.3
    yW = y0 + (xY - x0) * 0.5
    xX = x0 + (xY - x0) * 0.6
    yX = y0 - (xY - x0) * 0.3

    points = [
        {"x": x0, "y": y0, "type": "start"},
        {"x": xW, "y": yW, "type": "line"},
        {"x": xX, "y": yX, "type": "line"},
        {"x": xY, "y": yY, "type": "end"},
    ]
    adjustment_points = [
        {"x": xW, "y": yW, "type": "adjustment"},
        {"x": xX, "y": yX, "type": "adjustment"},
    ]
    return {"points": points, "adjustment_points": adjustment_points}


def draw_elliot_triple_combo_wave(start_point, end_point):
    """
    Draws an Elliot Triple Combo Wave (WXYXZ).
     Returns a dictionary containing points with types for drawing the wave and adjustment points.
    """
    x0, y0 = start_point
    xZ, yZ = end_point

    # Calculate intermediate points based on the start and end points
    xW = x0 + (xZ - x0) * 0.2
    yW = y0 + (xZ - x0) * 0.4
    xX = x0 + (xZ - x0) * 0.4
    yX = y0 - (xZ - x0) * 0.2
    xY = x0 + (xZ - x0) * 0.6
    yY = y0 + (xZ - x0) * 0.3

    points = [
        {"x": x0, "y": y0, "type": "start"},
        {"x": xW, "y": yW, "type": "line"},
        {"x": xX, "y": yX, "type": "line"},
        {"x": xY, "y": yY, "type": "line"},
        {"x": xZ, "y": yZ, "type": "end"},
    ]
    adjustment_points = [
        {"x": xW, "y": yW, "type": "adjustment"},
        {"x": xX, "y": yX, "type": "adjustment"},
        {"x": xY, "y": yY, "type": "adjustment"},
    ]
    return {"points": points, "adjustment_points": adjustment_points}