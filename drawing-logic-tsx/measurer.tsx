interface Point {
	x: number;
	y: number;
}

interface PriceRangeResult {
	priceRange: number;
	adjustmentPoints: Point[];
	resizePoints: Point[];
}

interface DataPriceRangeResult {
	timeRange: number;
	priceRangeStr: string;
	adjustmentPoints: Point[];
	resizePoints: Point[];
}

export function calculatePriceRange(
	startPrice: number,
	endPrice: number,
	startX?: number,
	startY?: number,
	endX?: number,
	endY?: number
): PriceRangeResult {
	const priceRange = Math.abs(endPrice - startPrice);
	const adjustmentPoints: Point[] = startX !== undefined && startY !== undefined && endX !== undefined && endY !== undefined
		? [{ x: startX, y: startY }, { x: endX, y: endY }]
		: [];

	return {
		priceRange,
		adjustmentPoints,
		resizePoints: []
	};
}

export function calculatePercentageChange(
	startPrice: number,
	endPrice: number
): number {
	if (startPrice === 0) return 0;
	return ((endPrice - startPrice) / startPrice) * 100;
}

export function calculateDataRange(
	startTime: Date,
	endTime: Date,
	startX?: number,
	startY?: number,
	endX?: number,
	endY?: number
): { timeRange: number; adjustmentPoints: Point[]; resizePoints: Point[] } {
	const timeRange = endTime.getTime() - startTime.getTime();
	const adjustmentPoints: Point[] = startX !== undefined && startY !== undefined && endX !== undefined && endY !== undefined
		? [{ x: startX, y: startY }, { x: endX, y: endY }]
		: [];

	return {
		timeRange,
		adjustmentPoints,
		resizePoints: []
	};
}

export function calculateDataPriceRange(
	startTime: Date,
	endTime: Date,
	startPrice: number,
	endPrice: number,
	startX: number,
	startY: number,
	endX: number,
	endY: number
): DataPriceRangeResult {
	const timeRangeData = calculateDataRange(startTime, endTime, startX, startY, endX, endY);
	const priceRangeData = calculatePriceRange(startPrice, endPrice, startX, startY, endX, endY);
	const percentageChange = calculatePercentageChange(startPrice, endPrice);
	
	const priceRangeStr = `${endPrice - startPrice} (${percentageChange.toFixed(2)}%) ${priceRangeData.priceRange.toFixed(0)}`;

	const adjustmentPoints: Point[] = [
		{ x: startX, y: startY },
		{ x: endX, y: endY }
	];

	const resizePoints: Point[] = [
		{ x: Math.min(startX, endX), y: Math.min(startY, endY) },
		{ x: Math.max(startX, endX), y: Math.min(startY, endY) },
		{ x: Math.max(startX, endX), y: Math.max(startY, endY) },
		{ x: Math.min(startX, endX), y: Math.max(startY, endY) }
	];

	return {
		timeRange: timeRangeData.timeRange,
		priceRangeStr,
		adjustmentPoints,
		resizePoints
	};
}