interface Point {
	x: number;
	y: number;
}

interface Line {
	start: Point;
	end: Point;
}

export class GannBox {
	private startPoint: Point;
	private endPoint: Point;
	private adjusters: Point[];

	constructor(startPoint: Point, endPoint: Point) {
		this.startPoint = startPoint;
		this.endPoint = endPoint;
		this.adjusters = [startPoint, endPoint];
	}

	getLines(): Line[] {
		const { x: x1, y: y1 } = this.startPoint;
		const { x: x2, y: y2 } = this.endPoint;
		const midX = (x1 + x2) / 2;
		const midY = (y1 + y2) / 2;

		const lines: Line[] = [
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

export class GannSquareFixed {
	private startPoint: Point;
	private endPoint: Point;
	private adjusters: Point[];

	constructor(startPoint: Point, endPoint: Point) {
		this.startPoint = startPoint;
		this.endPoint = endPoint;
		this.adjusters = [startPoint, endPoint];
	}

	getLines(): Line[] {
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

export class GannFan {
	private startPoint: Point;
	private endPoint: Point;
	private adjusters: Point[];

	constructor(startPoint: Point, endPoint: Point) {
		this.startPoint = startPoint;
		this.endPoint = endPoint;
		this.adjusters = [startPoint, endPoint];
	}

	getLines(): Line[] {
		const { x: x1, y: y1 } = this.startPoint;
		const { x: x2, y: y2 } = this.endPoint;
		const dx = x2 - x1;
		const dy = y2 - y1;
		
		const angles = [0, 1/8, 2/8, 3/8, 4/8, 5/8, 6/8, 7/8, 1];
		const lines: Line[] = [];

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