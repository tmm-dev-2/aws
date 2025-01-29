function rectangle(startX, startY, endX, endY) {
    const shapePoints = [
        { x: startX, y: startY },
        { x: endX, y: startY },
        { x: endX, y: endY },
        { x: startX, y: endY },
        { x: startX, y: startY }
    ];

    const adjustPoints = [
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

function rotatedRectangle(startX, startY, endX, endY, angle) {
    const centerX = (startX + endX) / 2;
    const centerY = (startY + endY) / 2;

    const points = [
        { x: startX, y: startY },
        { x: endX, y: startY },
        { x: endX, y: endY },
        { x: startX, y: endY }
    ];

    const rotatedPoints = points.map(point => ({
        x: centerX + (point.x - centerX) * Math.cos(angle) - (point.y - centerY) * Math.sin(angle),
        y: centerY + (point.x - centerX) * Math.sin(angle) + (point.y - centerY) * Math.cos(angle)
    }));

    rotatedPoints.push({ ...rotatedPoints[0] });

    const adjustPoints = rotatedPoints.map(point => ({
        x: point.x,
        y: point.y,
        type: 'adjustment'
    }));

    return { shapePoints: rotatedPoints, adjustPoints };
}

function ellipse(startX, startY, endX, endY, control1X, control1Y, control2X, control2Y) {
    const centerX = (startX + endX) / 2;
    const centerY = (startY + endY) / 2;
    const radiusX = Math.abs(endX - startX) / 2;
    const radiusY = Math.abs(endY - startY) / 2;

    const shapePoints = [];
    const steps = 100;

    for (let i = 0; i <= steps; i++) {
        const angle = (i / steps) * 2 * Math.PI;
        const x = centerX + radiusX * Math.cos(angle);
        const y = centerY + radiusY * Math.sin(angle);
        shapePoints.push({ x, y });
    }

    const adjustPoints = [
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
// ... (keeping existing rectangle, rotatedRectangle, ellipse functions)

function circle(centerX, centerY, radius, numPoints = 100) {
    const shapePoints = [];
    for (let i = 0; i < numPoints; i++) {
        const angle = 2 * Math.PI * i / numPoints;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        shapePoints.push({ x, y });
    }

    const adjustPoints = [
        { x: centerX + radius, y: centerY },
        { x: centerX - radius, y: centerY },
        { x: centerX, y: centerY + radius },
        { x: centerX, y: centerY - radius },
        { x: centerX, y: centerY }
    ];

    return { shapePoints, adjustPoints };
}

function triangle(startX, startY, endX, endY) {
    const midX = (startX + endX) / 2;
    const shapePoints = [
        { x: startX, y: endY },
        { x: midX, y: startY },
        { x: endX, y: endY },
        { x: startX, y: endY }
    ];

    const adjustPoints = [
        { x: startX, y: endY },
        { x: midX, y: startY },
        { x: endX, y: endY },
        { x: (startX + midX) / 2, y: (startY + endY) / 2 },
        { x: (midX + endX) / 2, y: (startY + endY) / 2 },
        { x: (startX + endX) / 2, y: endY },
        { x: midX, y: (startY + endY) / 2 }
    ];

    return { shapePoints, adjustPoints };
}

function arc(centerX, centerY, radius, startAngle, endAngle, numPoints = 100) {
    const shapePoints = [];
    const angleRange = endAngle - startAngle;
    
    for (let i = 0; i < numPoints; i++) {
        const angle = startAngle + angleRange * i / numPoints;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        shapePoints.push({ x, y });
    }

    const adjustPoints = [
        { x: centerX + radius * Math.cos(startAngle), y: centerY + radius * Math.sin(startAngle) },
        { x: centerX + radius * Math.cos(endAngle), y: centerY + radius * Math.sin(endAngle) },
        { x: centerX, y: centerY }
    ];

    return { shapePoints, adjustPoints };
}

function curve(startX, startY, controlX, controlY, endX, endY, numPoints = 100) {
    const shapePoints = [];
    
    for (let i = 0; i <= numPoints; i++) {
        const t = i / numPoints;
        const x = (1 - t) * (1 - t) * startX + 2 * (1 - t) * t * controlX + t * t * endX;
        const y = (1 - t) * (1 - t) * startY + 2 * (1 - t) * t * controlY + t * t * endY;
        shapePoints.push({ x, y });
    }

    const adjustPoints = [
        { x: startX, y: startY },
        { x: controlX, y: controlY },
        { x: endX, y: endY }
    ];

    return { shapePoints, adjustPoints };
}

function doubleCurve(startX, startY, control1X, control1Y, control2X, control2Y, endX, endY, numPoints = 100) {
    const shapePoints = [];
    
    for (let i = 0; i <= numPoints; i++) {
        const t = i / numPoints;
        const x = Math.pow(1 - t, 3) * startX + 
                 3 * Math.pow(1 - t, 2) * t * control1X + 
                 3 * (1 - t) * t * t * control2X + 
                 Math.pow(t, 3) * endX;
        const y = Math.pow(1 - t, 3) * startY + 
                 3 * Math.pow(1 - t, 2) * t * control1Y + 
                 3 * (1 - t) * t * t * control2Y + 
                 Math.pow(t, 3) * endY;
        shapePoints.push({ x, y });
    }

    const adjustPoints = [
        { x: startX, y: startY },
        { x: control1X, y: control1Y },
        { x: control2X, y: control2Y },
        { x: endX, y: endY }
    ];

    return { shapePoints, adjustPoints };
}

export { 
    rectangle, 
    rotatedRectangle, 
    ellipse, 
    circle, 
    triangle, 
    arc, 
    curve, 
    doubleCurve 
};


