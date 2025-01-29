class ParallelChannel {
    constructor(
        topLeftX, topLeftY,
        topRightX, topRightY,
        bottomLeftX, bottomLeftY,
        bottomRightX, bottomRightY
    ) {
        this.topLeftX = topLeftX;
        this.topLeftY = topLeftY;
        this.topRightX = topRightX;
        this.topRightY = topRightY;
        this.bottomLeftX = bottomLeftX;
        this.bottomLeftY = bottomLeftY;
        this.bottomRightX = bottomRightX;
        this.bottomRightY = bottomRightY;
    }

    draw() {
        return `M${this.topLeftX},${this.topLeftY} L${this.topRightX},${this.topRightY} L${this.bottomRightX},${this.bottomRightY} L${this.bottomLeftX},${this.bottomLeftY} Z`;
    }

    moveTopLeft(newX, newY) {
        this.topLeftX = newX;
        this.topLeftY = newY;
    }

    moveTopRight(newX, newY) {
        this.topRightX = newX;
        this.topRightY = newY;
    }

    moveBottomLeft(newX, newY) {
        this.bottomLeftX = newX;
        this.bottomLeftY = newY;
    }

    moveBottomRight(newX, newY) {
        this.bottomRightX = newX;
        this.bottomRightY = newY;
    }

    moveHorizontal(deltaX) {
        this.topLeftX += deltaX;
        this.topRightX += deltaX;
        this.bottomLeftX += deltaX;
        this.bottomRightX += deltaX;
    }

    moveVertical(deltaY) {
        this.topLeftY += deltaY;
        this.topRightY += deltaY;
        this.bottomLeftY += deltaY;
        this.bottomRightY += deltaY;
    }

    adjustAngle(newTopRightX, newTopRightY) {
        this.topRightX = newTopRightX;
        this.topRightY = newTopRightY;
        
        const topDx = this.topRightX - this.topLeftX;
        const topDy = this.topRightY - this.topLeftY;
        const topAngle = Math.atan2(topDy, topDx);
        
        const topLength = Math.sqrt(topDx**2 + topDy**2);
        
        this.bottomRightX = this.bottomLeftX + topLength * Math.cos(topAngle);
        this.bottomRightY = this.bottomLeftY + topLength * Math.sin(topAngle);
    }
}

class FlatTopBottomChannel extends ParallelChannel {
    constructor(
        topLeftX, topLeftY,
        topRightX,
        bottomLeftX, bottomLeftY,
        bottomRightX
    ) {
        super(
            topLeftX, topLeftY,
            topRightX, topLeftY,
            bottomLeftX, bottomLeftY,
            bottomRightX, bottomLeftY
        );
    }
}

class DisjointedChannel extends ParallelChannel {
    constructor(
        topLeftX, topLeftY,
        topRightX, topRightY,
        midTopX, midTopY,
        bottomLeftX, bottomLeftY,
        bottomRightX, bottomRightY,
        midBottomX, midBottomY
    ) {
        super(topLeftX, topLeftY, topRightX, topRightY, bottomLeftX, bottomLeftY, bottomRightX, bottomRightY);
        this.midTopX = midTopX;
        this.midTopY = midTopY;
        this.midBottomX = midBottomX;
        this.midBottomY = midBottomY;
    }

    draw() {
        return `M${this.topLeftX},${this.topLeftY} L${this.midTopX},${this.midTopY} L${this.topRightX},${this.topRightY} L${this.bottomRightX},${this.bottomRightY} L${this.midBottomX},${this.midBottomY} L${this.bottomLeftX},${this.bottomLeftY} Z`;
    }
}

export { ParallelChannel, FlatTopBottomChannel, DisjointedChannel };
