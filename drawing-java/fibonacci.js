function fibRetracement(startPoint, endPoint, adjustmentPoint1 = null, adjustmentPoint2 = null) {
    let [x1, y1] = [startPoint.x, startPoint.y];
    let [x2, y2] = [endPoint.x, endPoint.y];

    if (adjustmentPoint1 && adjustmentPoint2) {
        y1 = adjustmentPoint1.y;
        y2 = adjustmentPoint2.y;
    }

    const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
    const diff = y2 - y1;
    
    const retracementLevels = {};
    levels.forEach(level => {
        retracementLevels[level] = y1 + diff * level;
    });
    
    return retracementLevels;
}

function fibExtension(startPoint, middlePoint, endPoint, adjustmentPoint1 = null, adjustmentPoint2 = null, adjustmentPoint3 = null) {
    let [x1, y1] = [startPoint.x, startPoint.y];
    let [x2, y2] = [middlePoint.x, middlePoint.y];
    let [x3, y3] = [endPoint.x, endPoint.y];

    if (adjustmentPoint1 && adjustmentPoint2 && adjustmentPoint3) {
        y1 = adjustmentPoint1.y;
        y2 = adjustmentPoint2.y;
        y3 = adjustmentPoint3.y;
    }

    const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236];
    const diff = y2 - y1;
    const extensionDiff = y3 - y2;

    const extensionLevels = {};
    levels.forEach(level => {
        extensionLevels[level] = level <= 1 ? 
            y1 + diff * level : 
            y3 + extensionDiff * (level - 1);
    });
    
    return extensionLevels;
}

function fibChannel(startPoint, endPoint, adjustmentPoint1 = null, adjustmentPoint2 = null, channelWidthFactor = 1) {
    let [x1, y1] = [startPoint.x, startPoint.y];
    let [x2, y2] = [endPoint.x, endPoint.y];

    if (adjustmentPoint1 && adjustmentPoint2) {
        y1 = adjustmentPoint1.y;
        y2 = adjustmentPoint2.y;
    }

    const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236];
    const diff = y2 - y1;
    
    const channelLines = {};
    levels.forEach(level => {
        channelLines[level] = y1 + diff * level * channelWidthFactor;
    });
    
    return channelLines;
}

class TrendBasedFibTime {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
    }

    timeLevels() {
        const timeDiff = this.endPoint.x - this.startPoint.x;
        return this.levels.map(level => this.startPoint.x + level * timeDiff);
    }

    getAdjusters() {
        return [this.startPoint, this.endPoint];
    }
}

class FibCircle {
    constructor(centerPoint, radiusPoint) {
        this.centerPoint = centerPoint;
        this.radiusPoint = radiusPoint;
        this.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.5, 2.5, 3.618, 4.236, 4.618];
    }

    radii() {
        const radius = Math.sqrt(
            Math.pow(this.radiusPoint.x - this.centerPoint.x, 2) + 
            Math.pow(this.radiusPoint.y - this.centerPoint.y, 2)
        );
        return this.levels.map(level => level * radius);
    }

    getAdjusters() {
        return [this.centerPoint, this.radiusPoint];
    }
}

class FibSpeedResistanceArcs {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236, 4.618];
    }

    arcs() {
        const radius = Math.sqrt(
            Math.pow(this.endPoint.x - this.startPoint.x, 2) + 
            Math.pow(this.endPoint.y - this.startPoint.y, 2)
        );
        return this.levels.map(level => level * radius);
    }

    getAdjusters() {
        return [this.startPoint, this.endPoint];
    }
}

class FibWedge {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
    }

    wedgeLevels() {
        const angle = Math.atan2(
            this.endPoint.y - this.startPoint.y,
            this.endPoint.x - this.startPoint.x
        );
        return this.levels.map(level => angle * level);
    }

    getAdjusters() {
        return [this.startPoint, this.endPoint];
    }
}

class Pitchfan {
    constructor(startPoint, middlePoint, endPoint) {
        this.startPoint = startPoint;
        this.middlePoint = middlePoint;
        this.endPoint = endPoint;
        this.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
    }

    fanLines() {
        const angle1 = Math.atan2(
            this.middlePoint.y - this.startPoint.y,
            this.middlePoint.x - this.startPoint.x
        );
        const angle2 = Math.atan2(
            this.endPoint.y - this.startPoint.y,
            this.endPoint.x - this.startPoint.x
        );
        return this.levels.map(level => angle1 + (angle2 - angle1) * level);
    }

    getAdjusters() {
        return [this.startPoint, this.middlePoint, this.endPoint];
    }
}

export {
    fibRetracement,
    fibExtension,
    fibChannel,
    TrendBasedFibTime,
    FibCircle,
    FibSpeedResistanceArcs,
    FibWedge,
    Pitchfan
};
