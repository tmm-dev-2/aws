import { Point } from './types';

interface ShapePoints {
	shapePoints: Point[];
	adjustPoints: Point[];
}

export function rectangle(startX: number, startY: number, endX: number, endY: number): ShapePoints {
	const shapePoints: Point[] = [
		{ x: startX, y: startY },
		{ x: endX, y: startY },
		{ x: endX, y: endY },
		{ x: startX, y: endY },
		{ x: startX, y: startY }
	];

	const adjustPoints: Point[] = [
		{ x: startX, y: startY },
		{ x: endX, y: startY },
		{ x: endX, y: endY },
		{ x: startX, y: endY },
		{ x: (startX + endX) / 2, y: startY },
		{ x: (startX + endX) / 2, y: endY },
		{ x: startX, y: (startY + endY) / 2 },
		{ x: endX, y: (startY + endY) / 2 },
		{ x: (startX + endX) / 2, y: (startY + endY) / 2 }
	];

	return { shapePoints, adjustPoints };
}

export function rotatedRectangle(
	startX: number,
	startY: number,
	endX: number,
	endY: number,
	angle: number
): ShapePoints {
	const centerX = (startX + endX) / 2;
	const centerY = (startY + endY) / 2;

	const points: Point[] = [
		{ x: startX, y: startY },
		{ x: endX, y: startY },
		{ x: endX, y: endY },
		{ x: startX, y: endY }
	];

	const rotatedPoints: Point[] = points.map(point => ({
		x: centerX + (point.x - centerX) * Math.cos(angle) - (point.y - centerY) * Math.sin(angle),
		y: centerY + (point.x - centerX) * Math.sin(angle) + (point.y - centerY) * Math.cos(angle)
	}));

	// Add the first point again to close the shape
	rotatedPoints.push({ ...rotatedPoints[0] });

	const adjustPoints: Point[] = rotatedPoints.map(point => ({
		x: point.x,
		y: point.y,
		type: 'adjustment'
	}));

	return { shapePoints: rotatedPoints, adjustPoints };
}

export function ellipse(
	startX: number, 
	startY: number, 
	endX: number, 
	endY: number, 
	control1X?: number, 
	control1Y?: number, 
	control2X?: number, 
	control2Y?: number
): ShapePoints {
	const centerX = (startX + endX) / 2;
	const centerY = (startY + endY) / 2;
	const radiusX = Math.abs(endX - startX) / 2;
	const radiusY = Math.abs(endY - startY) / 2;

	const shapePoints: Point[] = [];
	const steps = 100;

	for (let i = 0; i <= steps; i++) {
		const angle = (i / steps) * 2 * Math.PI;
		const x = centerX + radiusX * Math.cos(angle);
		const y = centerY + radiusY * Math.sin(angle);
		shapePoints.push({ x, y });
	}

	const adjustPoints: Point[] = [
		{ x: startX, y: startY },
		{ x: endX, y: startY },
		{ x: endX, y: endY },
		{ x: startX, y: endY },
		{ x: centerX, y: startY },
		{ x: centerX, y: endY },
		{ x: startX, y: centerY },
		{ x: endX, y: centerY },
		{ x: centerX, y: centerY }
	];

	return { shapePoints, adjustPoints };
}