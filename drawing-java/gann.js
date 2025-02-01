class GannBox {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.adjusters = [startPoint, endPoint];
    }

    getLines() {
        const { x: x1, y: y1 } = this.startPoint;
        const { x: x2, y: y2 } = this.endPoint;
        const midX = (x1 + x2) / 2;
        const midY = (y1 + y2) / 2;

        const lines = [
            // Box lines
            { start: { x: x1, y: y1 }, end: { x: x2, y: y1 } },
            { start: { x: x2, y: y1 }, end: { x: x2, y: y2 } },
            { start: { x: x2, y: y2 }, end: { x: x1, y: y2 } },
            { start: { x: x1, y: y2 }, end: { x: x1, y: y1 } },
            // Diagonal lines
            { start: { x: x1, y: y1 }, end: { x: x2, y: y2 } },
            { start: { x: x1, y: y2 }, end: { x: x2, y: y1 } },
            // Middle lines
            { start: { x: midX, y: y1 }, end: { x: midX, y: y2 } },
            { start: { x: x1, y: midY }, end: { x: x2, y: midY } }
        ];

        return lines;
    }
}

class GannSquareFixed {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.adjusters = [startPoint, endPoint];
    }

    getLines() {
        const { x: x1, y: y1 } = this.startPoint;
        const { x: x2, y: y2 } = this.endPoint;

        const side = Math.min(Math.abs(x2 - x1), Math.abs(y2 - y1));
        const newX2 = x2 > x1 ? x1 + side : x1 - side;
        const newY2 = y2 > y1 ? y1 + side : y1 - side;

        return [
            { start: { x: x1, y: y1 }, end: { x: newX2, y: y1 } },
            { start: { x: newX2, y: y1 }, end: { x: newX2, y: newY2 } },
            { start: { x: newX2, y: newY2 }, end: { x: x1, y: newY2 } },
            { start: { x: x1, y: newY2 }, end: { x: x1, y: y1 } }
        ];
    }
}

class GannFan {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.adjusters = [startPoint, endPoint];
    }

    getLines() {
        const { x: x1, y: y1 } = this.startPoint;
        const { x: x2, y: y2 } = this.endPoint;
        const dx = x2 - x1;
        const dy = y2 - y1;
        
        const angles = [0, 1/8, 2/8, 3/8, 4/8, 5/8, 6/8, 7/8, 1];
        const lines = [];

        angles.forEach(angle => {
            const angleRad = angle * Math.PI / 2;
            const newDx = dx * Math.cos(angleRad) - dy * Math.sin(angleRad);
            const newDy = dx * Math.sin(angleRad) + dy * Math.cos(angleRad);
            
            lines.push({
                start: { x: x1, y: y1 },
                end: { x: x1 + newDx, y: y1 + newDy }
            });
        });

        return lines;
    }
}
class GannSquare {
    constructor(startPoint, endPoint) {
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.adjusters = [startPoint, endPoint];
        this.priceRatios = [1, 2, 3, 4, 8];
        this.timeRatios = [1, 2, 3, 4, 8];
    }

    getLines() {
        const { x: x1, y: y1 } = this.startPoint;
        const { x: x2, y: y2 } = this.endPoint;
        const lines = [];

        // Calculate square dimensions
        const width = Math.abs(x2 - x1);
        const height = Math.abs(y2 - y1);
        const squareSize = Math.max(width, height);

        // Add outer square
        lines.push(...this.createSquare(x1, y1, squareSize));

        // Add price levels
        this.priceRatios.forEach(ratio => {
            const y = y1 + (squareSize * ratio / 8);
            lines.push({
                start: { x: x1, y },
                end: { x: x1 + squareSize, y }
            });
        });

        // Add time divisions
        this.timeRatios.forEach(ratio => {
            const x = x1 + (squareSize * ratio / 8);
            lines.push({
                start: { x, y: y1 },
                end: { x, y: y1 + squareSize }
            });
        });

        // Add Gann angles
        const angles = [15, 30, 45, 60, 75];
        angles.forEach(angle => {
            lines.push(...this.createGannAngle(x1, y1, squareSize, angle));
        });

        return lines;
    }

    createSquare(x, y, size) {
        return [
            { start: { x, y }, end: { x: x + size, y } },
            { start: { x: x + size, y }, end: { x: x + size, y: y + size } },
            { start: { x: x + size, y: y + size }, end: { x, y: y + size } },
            { start: { x, y: y + size }, end: { x, y } }
        ];
    }

    createGannAngle(x, y, size, angle) {
        const angleRad = (angle * Math.PI) / 180;
        const endX = x + size * Math.cos(angleRad);
        const endY = y + size * Math.sin(angleRad);
        
        return [{
            start: { x, y },
            end: { x: endX, y: endY }
        }];
    }

    calculatePriceLevels(basePrice) {
        return this.priceRatios.map(ratio => basePrice * ratio);
    }

    calculateTimeLevels(baseDate) {
        return this.timeRatios.map(ratio => {
            const newDate = new Date(baseDate);
            newDate.setDate(baseDate.getDate() + ratio);
            return newDate;
        });
    }

    getIntersectionPoints() {
        const points = [];
        const { x: x1, y: y1 } = this.startPoint;
        const squareSize = Math.abs(this.endPoint.x - x1);

        this.priceRatios.forEach(priceRatio => {
            this.timeRatios.forEach(timeRatio => {
                points.push({
                    x: x1 + (squareSize * timeRatio / 8),
                    y: y1 + (squareSize * priceRatio / 8)
                });
            });
        });

        return points;
    }
}

export { GannBox, GannSquareFixed, GannFan, GannSquare };

