interface Point {
	x: number;
	y: number;
}

interface PositionResult {
	profit: number;
	loss: number;
	riskRewardRatio: number;
	amount: number;
	adjustmentPoints: Point[];
}

interface ForecastResult {
	forecastedPrice: number;
	forecastedTime: Date;
	adjustmentPoints: Point[];
}

interface ProjectionResult {
	projectedPriceRange: Point[];
	adjustmentPoints: Point[];
}

export function calculateLongPosition(
	startPrice: number,
	stopLoss: number,
	takeProfit: number,
	quantity: number,
	adjustmentPoints?: Point[]
): PositionResult {
	const profit = (takeProfit - startPrice) * quantity;
	const loss = (startPrice - stopLoss) * quantity;
	const riskRewardRatio = loss === 0 ? Infinity : profit / Math.abs(loss);

	return {
		profit,
		loss,
		riskRewardRatio,
		amount: profit > 0 ? profit : loss,
		adjustmentPoints: adjustmentPoints || []
	};
}

export function calculateShortPosition(
	startPrice: number,
	stopLoss: number,
	takeProfit: number,
	quantity: number,
	adjustmentPoints?: Point[]
): PositionResult {
	const profit = (startPrice - takeProfit) * quantity;
	const loss = (stopLoss - startPrice) * quantity;
	const riskRewardRatio = loss === 0 ? Infinity : profit / Math.abs(loss);

	return {
		profit,
		loss,
		riskRewardRatio,
		amount: profit > 0 ? profit : loss,
		adjustmentPoints: adjustmentPoints || []
	};
}

export function calculateForecast(
	startPrice: number,
	endPrice: number,
	startTime: Date,
	endTime: Date,
	adjustmentPoints?: Point[]
): ForecastResult {
	return {
		forecastedPrice: endPrice,
		forecastedTime: endTime,
		adjustmentPoints: adjustmentPoints || []
	};
}

export function calculateProjection(
	points: Point[],
	adjustmentPoints?: Point[]
): ProjectionResult {
	return {
		projectedPriceRange: points,
		adjustmentPoints: adjustmentPoints || []
	};
}