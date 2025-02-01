class TrendLine {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
    }

    adjustStartPoint(newStartPoint) {
        this.startPoint = newStartPoint;
    }

    adjustEndPoint(newEndPoint) {
        this.endPoint = newEndPoint;
    }

    draw(context) {
        context.beginPath();
        context.moveTo(this.startPoint.x, this.startPoint.y);
        context.lineTo(this.endPoint.x, this.endPoint.y);
        context.stroke();
    }

    getExtendedPoints() {
        return [this.startPoint, this.endPoint];
    }
}

class Ray extends TrendLine {
    getExtendedPoints() {
        const angle = Math.atan2(
            this.endPoint.y - this.startPoint.y,
            this.endPoint.x - this.startPoint.x
        );
        const length = 10000;
        
        const extendedEndPoint = {
            x: this.startPoint.x + Math.cos(angle) * length,
            y: this.startPoint.y + Math.sin(angle) * length
        };

        return [this.startPoint, extendedEndPoint];
    }

    draw(context) {
        const points = this.getExtendedPoints();
        context.beginPath();
        context.moveTo(points[0].x, points[0].y);
        context.lineTo(points[1].x, points[1].y);
        context.stroke();
    }
}

class ExtendedLine {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.calculateAngle();
    }

    calculateAngle() {
        const dx = this.endPoint.x - this.startPoint.x;
        const dy = this.endPoint.y - this.startPoint.y;
        this.angleRad = Math.atan2(dy, dx);
    }

    adjustStartPoint(newStartPoint) {
        this.startPoint = newStartPoint;
        this.calculateAngle();
    }

    adjustEndPoint(newEndPoint) {
        this.endPoint = newEndPoint;
        this.calculateAngle();
    }

    getExtendedPoints(xRange = [-10000, 10000]) {
        const startX = xRange[0];
        const endX = xRange[1];
        const startY = this.startPoint.y + (startX - this.startPoint.x) * Math.tan(this.angleRad);
        const endY = this.startPoint.y + (endX - this.startPoint.x) * Math.tan(this.angleRad);
        return [
            { x: startX, y: startY },
            { x: endX, y: endY }
        ];
    }
}

class TrendAngle {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
    }

    calculateAngle() {
        const dx = this.endPoint.x - this.startPoint.x;
        const dy = this.endPoint.y - this.startPoint.y;
        const angleRad = Math.atan2(dy, dx);
        return angleRad * (180 / Math.PI);
    }

    getAngleText() {
        const angle = this.calculateAngle();
        return `${angle.toFixed(2)}°`;
    }
}

class HorizontalLine {
    constructor(yValue) {
        this.yValue = yValue;
    }

    adjustYValue(newYValue) {
        this.yValue = newYValue;
    }

    getExtendedPoints(xRange = [-10000, 10000]) {
        return [
            { x: xRange[0], y: this.yValue },
            { x: xRange[1], y: this.yValue }
        ];
    }
}

class VerticalLine {
    constructor(xValue) {
        this.xValue = xValue;
    }

    adjustXValue(newXValue) {
        this.xValue = newXValue;
    }

    getExtendedPoints(yRange = [-10000, 10000]) {
        return [
            { x: this.xValue, y: yRange[0] },
            { x: this.xValue, y: yRange[1] }
        ];
    }
}

class CrossLine {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    moveX(newX) {
        this.x = newX;
    }

    moveY(newY) {
        this.y = newY;
    }

    getPoints() {
        return { x: this.x, y: this.y };
    }
}

export {
    TrendLine,
    Ray,
    ExtendedLine,
    TrendAngle,
    HorizontalLine,
    VerticalLine,
    CrossLine
};
