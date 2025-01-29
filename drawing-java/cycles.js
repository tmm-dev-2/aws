function drawCyclicLines(startX, endX, yMin, yMax, periodAdjust = 1) {
    const basePeriod = Math.abs(endX - startX);
    const period = basePeriod * periodAdjust;
    const lines = [];
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

function drawTimeCycles(startX, endX, yMin, yMax, periodAdjust = 1) {
    const basePeriod = Math.abs(endX - startX);
    const period = basePeriod * periodAdjust;
    const lines = [];
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

function drawSineLine(startX, startY, endX, endY, amplitudeAdjust = 1, periodAdjust = 1, numPoints = 100) {
    const baseAmplitude = Math.abs(endY - startY) / 2;
    const amplitude = baseAmplitude * amplitudeAdjust;
    const midY = (startY + endY) / 2;
    const basePeriod = Math.abs(endX - startX);
    const period = basePeriod * periodAdjust;
    
    const points = [];
    for (let i = 0; i < numPoints; i++) {
        const x = startX + (i * (endX - startX)) / (numPoints - 1);
        const y = amplitude * Math.sin(2 * Math.PI * (x - startX) / period) + midY;
        points.push({ x, y });
    }
    
    return points;
}

export { drawCyclicLines, drawTimeCycles, drawSineLine };
