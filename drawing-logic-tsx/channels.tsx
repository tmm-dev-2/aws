export class ParallelChannel {
	private topLeftX: number;
	private topLeftY: number;
	private topRightX: number;
	private topRightY: number;
	private bottomLeftX: number;
	private bottomLeftY: number;
	private bottomRightX: number;
	private bottomRightY: number;

	constructor(
		topLeftX: number,
		topLeftY: number,
		topRightX: number,
		topRightY: number,
		bottomLeftX: number,
		bottomLeftY: number,
		bottomRightX: number,
		bottomRightY: number
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

	draw(): string {
		return `M${this.topLeftX},${this.topLeftY} L${this.topRightX},${this.topRightY} L${this.bottomRightX},${this.bottomRightY} L${this.bottomLeftX},${this.bottomLeftY} Z`;
	}

	moveTopLeft(newX: number, newY: number): void {
		this.topLeftX = newX;
		this.topLeftY = newY;
	}

	moveTopRight(newX: number, newY: number): void {
		this.topRightX = newX;
		this.topRightY = newY;
	}

	moveBottomLeft(newX: number, newY: number): void {
		this.bottomLeftX = newX;
		this.bottomLeftY = newY;
	}

	moveBottomRight(newX: number, newY: number): void {
		this.bottomRightX = newX;
		this.bottomRightY = newY;
	}

	moveHorizontal(deltaX: number): void {
		this.topLeftX += deltaX;
		this.topRightX += deltaX;
		this.bottomLeftX += deltaX;
		this.bottomRightX += deltaX;
	}

	moveVertical(deltaY: number): void {
		this.topLeftY += deltaY;
		this.topRightY += deltaY;
		this.bottomLeftY += deltaY;
		this.bottomRightY += deltaY;
	}

	adjustAngle(newTopRightX: number, newTopRightY: number): void {
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

export class FlatTopBottomChannel extends ParallelChannel {
	constructor(
		topLeftX: number,
		topLeftY: number,
		topRightX: number,
		bottomLeftX: number,
		bottomLeftY: number,
		bottomRightX: number
	) {
		super(
			topLeftX, 
			topLeftY, 
			topRightX, 
			topLeftY, // Flat top, so Y is the same
			bottomLeftX, 
			bottomLeftY, 
			bottomRightX, 
			bottomLeftY // Flat bottom, so Y is the same
		);
	}
}

export class DisjointedChannel extends ParallelChannel {
	private midTopX: number;
	private midTopY: number;
	private midBottomX: number;
	private midBottomY: number;

	constructor(
		topLeftX: number,
		topLeftY: number,
		topRightX: number,
		topRightY: number,
		midTopX: number,
		midTopY: number,
		bottomLeftX: number,
		bottomLeftY: number,
		bottomRightX: number,
		bottomRightY: number,
		midBottomX: number,
		midBottomY: number
	) {
		super(
			topLeftX, topLeftY, 
			topRightX, topRightY, 
			bottomLeftX, bottomLeftY, 
			bottomRightX, bottomRightY
		);
		this.midTopX = midTopX;
		this.midTopY = midTopY;
		this.midBottomX = midBottomX;
		this.midBottomY = midBottomY;
	}

	draw(): string {
		return `M${this.topLeftX},${this.topLeftY} L${this.midTopX},${this.midTopY} L${this.topRightX},${this.topRightY} L${this.bottomRightX},${this.bottomRightY} L${this.midBottomX},${this.midBottomY} L${this.bottomLeftX},${this.bottomLeftY} Z`;
	}
}