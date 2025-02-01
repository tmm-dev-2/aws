class ArrowMarker {
    constructor({ startX, startY, endX, endY }) {
        this.startX = startX;
        this.startY = startY;
        this.endX = endX;
        this.endY = endY;
        this.adjustmentPoints = this.calculateAdjustmentPoints();
    }

    calculateAdjustmentPoints() {
        return {
            start: { x: this.startX, y: this.startY },
            end: { x: this.endX, y: this.endY },
        };
    }

    updateCoordinates(point, newX, newY) {
        if (point === 'start') {
            this.startX = newX;
            this.startY = newY;
        } else if (point === 'end') {
            this.endX = newX;
            this.endY = newY;
        }
        this.adjustmentPoints = this.calculateAdjustmentPoints();
    }

    draw(context) {
        context.beginPath();
        context.moveTo(this.startX, this.startY);
        context.lineTo(this.endX, this.endY);
        context.stroke();
    }

    toObject() {
        return {
            type: 'arrow_marker',
            startX: this.startX,
            startY: this.startY,
            endX: this.endX,
            endY: this.endY,
            adjustmentPoints: this.adjustmentPoints
        };
    }
}

class Arrow extends ArrowMarker {
    draw(context) {
        const headLength = 10;
        const angle = Math.atan2(this.endY - this.startY, this.endX - this.startX);
        
        context.beginPath();
        context.moveTo(this.startX, this.startY);
        context.lineTo(this.endX, this.endY);
        
        context.lineTo(
            this.endX - headLength * Math.cos(angle - Math.PI / 6),
            this.endY - headLength * Math.sin(angle - Math.PI / 6)
        );
        context.moveTo(this.endX, this.endY);
        context.lineTo(
            this.endX - headLength * Math.cos(angle + Math.PI / 6),
            this.endY - headLength * Math.sin(angle + Math.PI / 6)
        );
        
        context.stroke();
    }
}

class ArrowMarkUp extends ArrowMarker {
    draw(context) {
        const arrowSize = 8;
        
        context.beginPath();
        context.moveTo(this.startX, this.startY);
        context.lineTo(this.endX, this.endY);
        context.lineTo(this.endX - arrowSize, this.endY + arrowSize);
        context.moveTo(this.endX, this.endY);
        context.lineTo(this.endX + arrowSize, this.endY + arrowSize);
        context.stroke();
    }
}

class ArrowMarkDown extends ArrowMarker {
    draw(context) {
        const arrowSize = 8;
        
        context.beginPath();
        context.moveTo(this.startX, this.startY);
        context.lineTo(this.endX, this.endY);
        context.lineTo(this.endX - arrowSize, this.endY - arrowSize);
        context.moveTo(this.endX, this.endY);
        context.lineTo(this.endX + arrowSize, this.endY - arrowSize);
        context.stroke();
    }
}

export { ArrowMarker, Arrow, ArrowMarkUp, ArrowMarkDown };
