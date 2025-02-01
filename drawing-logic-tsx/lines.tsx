import { Point } from './types';

export type LineSegment = Point[];

export class TrendLine {
	protected startPoint: Point;
	protected endPoint: Point;

	constructor(startPoint: Point, endPoint: Point) {
		this.startPoint = startPoint;
		this.endPoint = endPoint;
	}

	adjustStartPoint(newStartPoint: Point): void {
		this.startPoint = newStartPoint;
	}

	adjustEndPoint(newEndPoint: Point): void {
		this.endPoint = newEndPoint;
	}

	draw(context: CanvasRenderingContext2D): void {
		context.beginPath();
		context.moveTo(this.startPoint.x, this.startPoint.y);
		context.lineTo(this.endPoint.x, this.endPoint.y);
		context.stroke();
	}

	getExtendedPoints(): Point[] {
		return [this.startPoint, this.endPoint];
	}
}

export class Ray extends TrendLine {
	getExtendedPoints(): Point[] {
		const angle = Math.atan2(
			this.endPoint.y - this.startPoint.y,
			this.endPoint.x - this.startPoint.x
		);
		const length = 10000; // Extended length
		
		// Calculate the extended endpoint
		const extendedEndPoint: Point = {
			x: this.startPoint.x + Math.cos(angle) * length,
			y: this.startPoint.y + Math.sin(angle) * length
		};

		return [this.startPoint, extendedEndPoint];
	}

	draw(context: CanvasRenderingContext2D): void {
		const points = this.getExtendedPoints();
		context.beginPath();
		context.moveTo(points[0].x, points[0].y);
		context.lineTo(points[1].x, points[1].y);
		context.stroke();
	}
}

export class ExtendedLine {
	private startPoint: Point;
	private endPoint: Point;
	private angleRad: number;

	constructor(startPoint: Point, endPoint: Point) {
		this.startPoint = startPoint;
		this.endPoint = endPoint;
		this.calculateAngle();
	}

	private calculateAngle(): void {
		const dx = this.endPoint.x - this.startPoint.x;
		const dy = this.endPoint.y - this.startPoint.y;
		this.angleRad = Math.atan2(dy, dx);
	}

	adjustStartPoint(newStartPoint: Point): void {
		this.startPoint = newStartPoint;
		this.calculateAngle();
	}

	adjustEndPoint(newEndPoint: Point): void {
		this.endPoint = newEndPoint;
		this.calculateAngle();
	}

	getExtendedPoints(xRange: [number, number] = [-10000, 10000]): [Point, Point] {
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

export class TrendAngle {
	private startPoint: Point;
	private endPoint: Point;

	constructor(startPoint: Point, endPoint: Point) {
		this.startPoint = startPoint;
		this.endPoint = endPoint;
	}

	calculateAngle(): number {
		const dx = this.endPoint.x - this.startPoint.x;
		const dy = this.endPoint.y - this.startPoint.y;
		const angleRad = Math.atan2(dy, dx);
		return angleRad * (180 / Math.PI);
	}

	getAngleText(): string {
		const angle = this.calculateAngle();
		return `${angle.toFixed(2)}°`;
	}
}

export class HorizontalLine {
	private yValue: number;

	constructor(yValue: number) {
		this.yValue = yValue;
	}

	adjustYValue(newYValue: number): void {
		this.yValue = newYValue;
	}

	getExtendedPoints(xRange: [number, number] = [-10000, 10000]): [Point, Point] {
		return [
			{ x: xRange[0], y: this.yValue },
			{ x: xRange[1], y: this.yValue }
		];
	}
}

export class VerticalLine {
	private xValue: number;

	constructor(xValue: number) {
		this.xValue = xValue;
	}

	adjustXValue(newXValue: number): void {
		this.xValue = newXValue;
	}

	getExtendedPoints(yRange: [number, number] = [-10000, 10000]): [Point, Point] {
		return [
			{ x: this.xValue, y: yRange[0] },
			{ x: this.xValue, y: yRange[1] }
		];
	}
}

export class CrossLine {
	private x: number;
	private y: number;

	constructor(x: number, y: number) {
		this.x = x;
		this.y = y;
	}

	moveX(newX: number): void {
		this.x = newX;
	}

	moveY(newY: number): void {
		this.y = newY;
	}

	getPoints(): Point {
		return { x: this.x, y: this.y };
	}
}