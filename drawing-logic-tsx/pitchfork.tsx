import { Point } from './types';

interface Line {
	startPoint: Point;
	endPoint: Point;
}

export class Pitchfork {
	protected startX: number;
	protected startY: number;
	protected middleX: number;
	protected middleY: number;
	protected endX: number;
	protected endY: number;
	protected lines: Line[];

	constructor(startX: number, startY: number, middleX: number, middleY: number, endX: number, endY: number) {
		this.startX = startX;
		this.startY = startY;
		this.middleX = middleX;
		this.middleY = middleY;
		this.endX = endX;
		this.endY = endY;
		this.lines = this.calculateLines();
	}

	protected calculateLines(): Line[] {
		const lines: Line[] = [];
		
		// Start to middle line
		lines.push({
			startPoint: { x: this.startX, y: this.startY },
			endPoint: { x: this.middleX, y: this.middleY }
		});

		// Calculate median line
		const medianX = (this.startX + this.endX) / 2;
		const medianY = (this.startY + this.endY) / 2;
		lines.push({
			startPoint: { x: this.middleX, y: this.middleY },
			endPoint: { x: medianX, y: medianY }
		});

		// Calculate parallel lines
		const dx = this.endX - this.startX;
		const dy = this.endY - this.startY;
		lines.push({
			startPoint: { x: this.middleX + dx, y: this.middleY + dy },
			endPoint: { x: this.endX, y: this.endY }
		});

		return lines;
	}

	moveStart(newX: number, newY: number): void {
		const dx = newX - this.startX;
		const dy = newY - this.startY;
		this.startX = newX;
		this.startY = newY;
		this.moveAll(dx, dy);
	}

	moveMiddle(newX: number, newY: number): void {
		const dx = newX - this.middleX;
		const dy = newY - this.middleY;
		this.middleX = newX;
		this.middleY = newY;
		this.moveAll(dx, dy);
	}

	moveEnd(newX: number, newY: number): void {
		const dx = newX - this.endX;
		const dy = newY - this.endY;
		this.endX = newX;
		this.endY = newY;
		this.moveAll(dx, dy);
	}

	protected moveAll(dx: number, dy: number): void {
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

	adjustAngle(newEndX: number, newEndY: number): void {
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

	private rotatePoint(centerX: number, centerY: number, x: number, y: number, angle: number): [number, number] {
		const dx = x - centerX;
		const dy = y - centerY;
		const newX = centerX + dx * Math.cos(angle) - dy * Math.sin(angle);
		const newY = centerY + dx * Math.sin(angle) + dy * Math.cos(angle);
		return [newX, newY];
	}
}

export class SchiffPitchfork extends Pitchfork {
	protected calculateLines(): Line[] {
		const lines: Line[] = [];
		
		lines.push({
			startPoint: { x: this.startX, y: this.startY },
			endPoint: { x: this.middleX, y: this.middleY }
		});

		const medianX = (this.startX + this.middleX) / 2;
		const medianY = (this.startY + this.middleY) / 2;
		lines.push({
			startPoint: { x: medianX, y: medianY },
			endPoint: { x: this.endX, y: this.endY }
		});

		const dx = this.endX - this.startX;
		const dy = this.endY - this.startY;
		lines.push({
			startPoint: { x: this.middleX + dx, y: this.middleY + dy },
			endPoint: { x: this.endX, y: this.endY }
		});

		return lines;
	}
}