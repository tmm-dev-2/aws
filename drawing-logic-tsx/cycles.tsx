interface LineSegment {
	x1: number;
	y1: number;
	x2: number;
	y2: number;
}

interface Point {
	x: number;
	y: number;
}

export function drawCyclicLines(
	startX: number,
	endX: number,
	yMin: number,
	yMax: number,
	periodAdjust: number = 1
): LineSegment[] {
	const basePeriod = Math.abs(endX - startX);
	const period = basePeriod * periodAdjust;
	const lines: LineSegment[] = [];
	let x = startX;
	
	while (x <= endX) {
		lines.push({
			x1: x,
			y1: yMin,
			x2: x,
			y2: yMax
		});
		x += period;
	}
	return lines;
}

export function drawTimeCycles(
	startX: number,
	endX: number,
	yMin: number,
	yMax: number,
	periodAdjust: number = 1
): LineSegment[] {
	const basePeriod = Math.abs(endX - startX);
	const period = basePeriod * periodAdjust;
	const lines: LineSegment[] = [];
	let x = startX;
	
	while (x <= endX) {
		lines.push({
			x1: x,
			y1: yMin,
			x2: x,
			y2: yMax
		});
		x += period;
	}
	return lines;
}

export function drawSineLine(
	startX: number,
	startY: number,
	endX: number,
	endY: number,
	amplitudeAdjust: number = 1,
	periodAdjust: number = 1,
	numPoints: number = 100
): Point[] {
	const baseAmplitude = Math.abs(endY - startY) / 2;
	const amplitude = baseAmplitude * amplitudeAdjust;
	const midY = (startY + endY) / 2;
	const basePeriod = Math.abs(endX - startX);
	const period = basePeriod * periodAdjust;
	
	const points: Point[] = [];
	for (let i = 0; i < numPoints; i++) {
		const x = startX + (i * (endX - startX)) / (numPoints - 1);
		const y = amplitude * Math.sin(2 * Math.PI * (x - startX) / period) + midY;
		points.push({ x, y });
	}
	
	return points;
}