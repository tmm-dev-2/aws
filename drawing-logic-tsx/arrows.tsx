import { Point } from './types';

interface ArrowProps {
	startX: number;
	startY: number;
	endX: number;
	endY: number;
}

export class ArrowMarker {
	private startX: number;
	private startY: number;
	private endX: number;
	private endY: number;
	private adjustmentPoints: Record<string, Point>;

	constructor({ startX, startY, endX, endY }: ArrowProps) {
		this.startX = startX;
		this.startY = startY;
		this.endX = endX;
		this.endY = endY;
		this.adjustmentPoints = this.calculateAdjustmentPoints();
	}

	private calculateAdjustmentPoints(): Record<string, Point> {
		return {
			start: { x: this.startX, y: this.startY },
			end: { x: this.endX, y: this.endY },
		};
	}

	updateCoordinates(point: 'start' | 'end', newX: number, newY: number): void {
		if (point === 'start') {
			this.startX = newX;
			this.startY = newY;
		} else if (point === 'end') {
			this.endX = newX;
			this.endY = newY;
		}
		this.adjustmentPoints = this.calculateAdjustmentPoints();
	}

	draw(context: CanvasRenderingContext2D): void {
		// Implementation for drawing arrow marker
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

// Similar classes for Arrow, ArrowMarkUp, and ArrowMarkDown would follow the same pattern
export class Arrow extends ArrowMarker {
	// Additional arrow-specific implementations
}

export class ArrowMarkUp extends ArrowMarker {
	// Additional arrow mark up-specific implementations
}

export class ArrowMarkDown extends ArrowMarker {
	// Additional arrow mark down-specific implementations
}