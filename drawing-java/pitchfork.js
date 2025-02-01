class BasePitchfork {
    constructor(startX, startY, middleX, middleY, endX, endY) {
        this.startX = startX;
        this.startY = startY;
        this.middleX = middleX;
        this.middleY = middleY;
        this.endX = endX;
        this.endY = endY;
        this.lines = this.calculateLines();
    }

    moveStart(newX, newY) {
        const dx = newX - this.startX;
        const dy = newY - this.startY;
        this.startX = newX;
        this.startY = newY;
        this.moveAll(dx, dy);
    }

    moveMiddle(newX, newY) {
        const dx = newX - this.middleX;
        const dy = newY - this.middleY;
        this.middleX = newX;
        this.middleY = newY;
        this.moveAll(dx, dy);
    }

    moveEnd(newX, newY) {
        const dx = newX - this.endX;
        const dy = newY - this.endY;
        this.endX = newX;
        this.endY = newY;
        this.moveAll(dx, dy);
    }

    moveAll(dx, dy) {
        this.lines = this.lines.map(line => ({
            startPoint: {
                x: line.startPoint.x + dx,
                y: line.startPoint.y + dy
            },
            endPoint: {
                x: line.endPoint.x + dx,
                y: line.endPoint.y + dy
            }
        }));
    }

    adjustAngle(newEndX, newEndY) {
        const dx = this.endX - this.startX;
        const dy = this.endY - this.startY;
        const baseAngle = Math.atan2(dy, dx);
        
        const newDx = newEndX - this.startX;
        const newDy = newEndY - this.startY;
        const newAngle = Math.atan2(newDy, newDx);
        
        const rotationAngle = newAngle - baseAngle;
        
        [this.middleX, this.middleY] = this.rotatePoint(
            this.startX, this.startY,
            this.middleX, this.middleY,
            rotationAngle
        );
        
        [this.endX, this.endY] = [newEndX, newEndY];
        this.lines = this.calculateLines();
    }

    rotatePoint(centerX, centerY, x, y, angle) {
        const dx = x - centerX;
        const dy = y - centerY;
        const newX = centerX + dx * Math.cos(angle) - dy * Math.sin(angle);
        const newY = centerY + dx * Math.sin(angle) + dy * Math.cos(angle);
        return [newX, newY];
    }
}

class StandardPitchfork extends BasePitchfork {
    calculateLines() {
        const lines = [];
        
        // Handle line
        lines.push({
            startPoint: { x: this.startX, y: this.startY },
            endPoint: { x: this.middleX, y: this.middleY }
        });

        // Median line
        const medianX = (this.startX + this.endX) / 2;
        const medianY = (this.startY + this.endY) / 2;
        lines.push({
            startPoint: { x: this.middleX, y: this.middleY },
            endPoint: { x: medianX, y: medianY }
        });

        // Parallel lines
        const dx = this.endX - this.startX;
        const dy = this.endY - this.startY;
        lines.push({
            startPoint: { x: this.middleX + dx, y: this.middleY + dy },
            endPoint: { x: this.endX, y: this.endY }
        });

        return lines;
    }
}

class ModifiedSchiffPitchfork extends BasePitchfork {
    calculateLines() {
        const lines = [];
        
        // Modified handle
        const handleMidX = (this.startX + this.middleX) / 2;
        const handleMidY = (this.startY + this.middleY) / 2;
        lines.push({
            startPoint: { x: this.startX, y: this.startY },
            endPoint: { x: handleMidX, y: handleMidY }
        });

        // Modified median
        lines.push({
            startPoint: { x: handleMidX, y: handleMidY },
            endPoint: { x: this.endX, y: this.endY }
        });

        // Modified parallel lines
        const dx = this.endX - handleMidX;
        const dy = this.endY - handleMidY;
        lines.push({
            startPoint: { x: this.middleX + dx, y: this.middleY + dy },
            endPoint: { x: this.endX + dx, y: this.endY + dy }
        });

        return lines;
    }
}

class SchiffPitchfork extends BasePitchfork {
    calculateLines() {
        const lines = [];
        
        // Schiff handle
        lines.push({
            startPoint: { x: this.startX, y: this.startY },
            endPoint: { x: this.middleX, y: this.middleY }
        });

        // Schiff median
        const medianX = (this.startX + this.middleX) / 2;
        const medianY = (this.startY + this.middleY) / 2;
        lines.push({
            startPoint: { x: medianX, y: medianY },
            endPoint: { x: this.endX, y: this.endY }
        });

        // Schiff parallel lines
        const dx = this.endX - this.startX;
        const dy = this.endY - this.startY;
        lines.push({
            startPoint: { x: this.middleX + dx, y: this.middleY + dy },
            endPoint: { x: this.endX, y: this.endY }
        });

        return lines;
    }
}

class InsidePitchfork extends BasePitchfork {
    calculateLines() {
        const lines = [];
        
        // Inside handle
        lines.push({
            startPoint: { x: this.startX, y: this.startY },
            endPoint: { x: this.middleX, y: this.middleY }
        });

        // Inside median
        const medianX = (this.startX + this.endX) / 2;
        const medianY = (this.startY + this.endY) / 2;
        lines.push({
            startPoint: { x: this.middleX, y: this.middleY },
            endPoint: { x: medianX, y: medianY }
        });

        // Inside parallel lines (internal tines)
        const dx = (this.endX - this.startX) * 0.5;
        const dy = (this.endY - this.startY) * 0.5;
        lines.push({
            startPoint: { x: this.middleX - dx, y: this.middleY - dy },
            endPoint: { x: this.middleX + dx, y: this.middleY + dy }
        });

        return lines;
    }
}

class BarleyPitchfork extends BasePitchfork {
    calculateLines() {
        const lines = [];
        
        // Barley handle
        lines.push({
            startPoint: { x: this.startX, y: this.startY },
            endPoint: { x: this.middleX, y: this.middleY }
        });

        // Barley median with warning line
        const medianX = (this.startX + this.endX) / 2;
        const medianY = (this.startY + this.endY) / 2;
        lines.push({
            startPoint: { x: this.middleX, y: this.middleY },
            endPoint: { x: medianX, y: medianY }
        });

        // Barley parallel lines with warning lines
        const dx = this.endX - this.startX;
        const dy = this.endY - this.startY;
        
        // Main parallel lines
        lines.push({
            startPoint: { x: this.middleX + dx, y: this.middleY + dy },
            endPoint: { x: this.endX, y: this.endY }
        });

        // Warning lines (0.618 and 1.618 extensions)
        const phi = 1.618;
        lines.push({
            startPoint: { x: this.middleX + dx * phi, y: this.middleY + dy * phi },
            endPoint: { x: this.endX + dx * (phi - 1), y: this.endY + dy * (phi - 1) }
        });
        
        lines.push({
            startPoint: { x: this.middleX + dx * 0.618, y: this.middleY + dy * 0.618 },
            endPoint: { x: this.endX - dx * 0.382, y: this.endY - dy * 0.382 }
        });

        return lines;
    }
}

export { 
    BasePitchfork,
    StandardPitchfork,
    ModifiedSchiffPitchfork,
    SchiffPitchfork,
    InsidePitchfork,
    BarleyPitchfork
};
