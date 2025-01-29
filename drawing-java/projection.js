function longPosition(startPrice, stopLoss, takeProfit, quantity, adjustmentPoints = []) {
    const profit = (takeProfit - startPrice) * quantity;
    const loss = (startPrice - stopLoss) * quantity;
    const riskRewardRatio = loss === 0 ? Infinity : profit / Math.abs(loss);

    return {
        profit,
        loss,
        riskRewardRatio,
        amount: profit > 0 ? profit : loss,
        adjustmentPoints
    };
}

function shortPosition(startPrice, stopLoss, takeProfit, quantity, adjustmentPoints = []) {
    const profit = (startPrice - takeProfit) * quantity;
    const loss = (stopLoss - startPrice) * quantity;
    const riskRewardRatio = loss === 0 ? Infinity : profit / Math.abs(loss);

    return {
        profit,
        loss,
        riskRewardRatio,
        amount: profit > 0 ? profit : loss,
        adjustmentPoints
    };
}

function forecast(startPrice, endPrice, startTime, endTime, adjustmentPoints = []) {
    return {
        forecastedPrice: endPrice,
        forecastedTime: endTime,
        adjustmentPoints
    };
}

function projection(points, adjustmentPoints = []) {
    return {
        projectedPriceRange: points,
        adjustmentPoints
    };
}

export {
    longPosition,
    shortPosition,
    forecast,
    projection
};
