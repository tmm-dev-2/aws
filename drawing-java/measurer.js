function calculatePriceRange(startPrice, endPrice, startX, startY, endX, endY) {
    const priceRange = Math.abs(endPrice - startPrice);
    const adjustmentPoints = startX !== undefined && startY !== undefined && endX !== undefined && endY !== undefined
        ? [{ x: startX, y: startY }, { x: endX, y: endY }]
        : [];

    return {
        priceRange,
        adjustmentPoints,
        resizePoints: []
    };
}

function calculatePercentageChange(startPrice, endPrice) {
    if (startPrice === 0) return 0;
    return ((endPrice - startPrice) / startPrice) * 100;
}

function calculateDataRange(startTime, endTime, startX, startY, endX, endY) {
    const timeRange = endTime.getTime() - startTime.getTime();
    const adjustmentPoints = startX !== undefined && startY !== undefined && endX !== undefined && endY !== undefined
        ? [{ x: startX, y: startY }, { x: endX, y: endY }]
        : [];

    return {
        timeRange,
        adjustmentPoints,
        resizePoints: []
    };
}

function calculateDataPriceRange(startTime, endTime, startPrice, endPrice, startX, startY, endX, endY) {
    const timeRangeData = calculateDataRange(startTime, endTime, startX, startY, endX, endY);
    const priceRangeData = calculatePriceRange(startPrice, endPrice, startX, startY, endX, endY);
    const percentageChange = calculatePercentageChange(startPrice, endPrice);
    
    const priceRangeStr = `${endPrice - startPrice} (${percentageChange.toFixed(2)}%) ${priceRangeData.priceRange.toFixed(0)}`;

    const adjustmentPoints = [
        { x: startX, y: startY },
        { x: endX, y: endY }
    ];

    const resizePoints = [
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

export {
    calculatePriceRange,
    calculatePercentageChange,
    calculateDataRange,
    calculateDataPriceRange
};
