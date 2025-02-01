import { Point } from './types';

interface AdjustmentPoint extends Point {
	type: string;
}

export class XABCDPattern {
	private x: Point;
	private a: Point;
	private b: Point;
	private c: Point;
	private d: Point;
	private adjustmentPointers: AdjustmentPoint[];

	constructor(x: Point, a: Point, b: Point, c: Point, d: Point) {
		this.x = x;
		this.a = a;
		this.b = b;
		this.c = c;
		this.d = d;
		this.adjustmentPointers = this.createAdjustmentPoints();
	}

	private createAdjustmentPoints(): AdjustmentPoint[] {
		return [
			{ ...this.x, type: 'adjustment' },
			{ ...this.a, type: 'adjustment' },
			{ ...this.b, type: 'adjustment' },
			{ ...this.c, type: 'adjustment' },
			{ ...this.d, type: 'adjustment' }
		];
	}

	isValid(): boolean {
		const xa = Math.sqrt((this.a.x - this.x.x) ** 2 + (this.a.y - this.x.y) ** 2);
		const ab = Math.sqrt((this.b.x - this.a.x) ** 2 + (this.b.y - this.a.y) ** 2);
		const bc = Math.sqrt((this.c.x - this.b.x) ** 2 + (this.c.y - this.b.y) ** 2);
		const cd = Math.sqrt((this.d.x - this.c.x) ** 2 + (this.d.y - this.c.y) ** 2);

		const abRetracement = ab / xa;
		if (!(0.382 <= abRetracement && abRetracement <= 0.886)) {
			return false;
		}

		const bcRetracement = bc / ab;
		if (!(0.382 <= bcRetracement && bcRetracement <= 0.886)) {
			return false;
		}

		const cdExtension = cd / bc;
		if (!(1.272 <= cdExtension && cdExtension <= 1.618)) {
			return false;
		}

		return true;
	}
}

export class CypherPattern {
	private x: Point;
	private a: Point;
	private b: Point;
	private c: Point;
	private d: Point;
	private adjustmentPointers: AdjustmentPoint[];

	constructor(x: Point, a: Point, b: Point, c: Point, d: Point) {
		this.x = x;
		this.a = a;
		this.b = b;
		this.c = c;
		this.d = d;
		this.adjustmentPointers = this.createAdjustmentPoints();
	}

	private createAdjustmentPoints(): AdjustmentPoint[] {
		return [
			{ ...this.x, type: 'adjustment' },
			{ ...this.a, type: 'adjustment' },
			{ ...this.b, type: 'adjustment' },
			{ ...this.c, type: 'adjustment' },
			{ ...this.d, type: 'adjustment' }
		];
	}
}

export class HeadAndShouldersPattern {
	private leftShoulder: Point;
	private head: Point;
	private rightShoulder: Point;
	private necklineStart: Point;
	private necklineEnd: Point;
	private adjustmentPointers: AdjustmentPoint[];

	constructor(
		leftShoulder: Point,
		head: Point,
		rightShoulder: Point,
		necklineStart: Point,
		necklineEnd: Point
	) {
		this.leftShoulder = leftShoulder;
		this.head = head;
		this.rightShoulder = rightShoulder;
		this.necklineStart = necklineStart;
		this.necklineEnd = necklineEnd;
		this.adjustmentPointers = this.createAdjustmentPoints();
	}

	private createAdjustmentPoints(): AdjustmentPoint[] {
		return [
			{ ...this.leftShoulder, type: 'adjustment' },
			{ ...this.head, type: 'adjustment' },
			{ ...this.rightShoulder, type: 'adjustment' },
			{ ...this.necklineStart, type: 'adjustment' },
			{ ...this.necklineEnd, type: 'adjustment' }
		];
	}
}

export class ABCDPattern {
	private a: Point;
	private b: Point;
	private c: Point;
	private d: Point;
	private adjustmentPointers: AdjustmentPoint[];

	constructor(a: Point, b: Point, c: Point, d: Point) {
		this.a = a;
		this.b = b;
		this.c = c;
		this.d = d;
		this.adjustmentPointers = this.createAdjustmentPoints();
	}

	private createAdjustmentPoints(): AdjustmentPoint[] {
		return [
			{ ...this.a, type: 'adjustment' },
			{ ...this.b, type: 'adjustment' },
			{ ...this.c, type: 'adjustment' },
			{ ...this.d, type: 'adjustment' }
		];
	}
}

export class TrianglePattern {
	private start: Point;
	private top: Point;
	private bottom: Point;
	private adjustmentPointers: AdjustmentPoint[];

	constructor(start: Point, top: Point, bottom: Point) {
		this.start = start;
		this.top = top;
		this.bottom = bottom;
		this.adjustmentPointers = this.createAdjustmentPoints();
	}

	private createAdjustmentPoints(): AdjustmentPoint[] {
		return [
			{ ...this.start, type: 'adjustment' },
			{ ...this.top, type: 'adjustment' },
			{ ...this.bottom, type: 'adjustment' }
		];
	}
}

export class ThreeDrivesPattern {
	private start: Point;
	private drive1: Point;
	private drive2: Point;
	private drive3: Point;
	private end: Point;
	private adjustmentPointers: AdjustmentPoint[];

	constructor(start: Point, drive1: Point, drive2: Point, drive3: Point, end: Point) {
		this.start = start;
		this.drive1 = drive1;
		this.drive2 = drive2;
		this.drive3 = drive3;
		this.end = end;
		this.adjustmentPointers = this.createAdjustmentPoints();
	}

	private createAdjustmentPoints(): AdjustmentPoint[] {
		return [
			{ ...this.start, type: 'adjustment' },
			{ ...this.drive1, type: 'adjustment' },
			{ ...this.drive2, type: 'adjustment' },
			{ ...this.drive3, type: 'adjustment' },
			{ ...this.end, type: 'adjustment' }
		];
	}
}