function drawElliotImpulseWave(startPoint, endPoint) {
    const { x: x0, y: y0 } = startPoint;
    const { x: x5, y: y5 } = endPoint;

    const x1 = x0 + (x5 - x0) * 0.2;
    const y1 = y0 + (y5 - y0) * 0.3;
    const x2 = x0 + (x5 - x0) * 0.35;
    const y2 = y0 - (y5 - y0) * 0.2;
    const x3 = x0 + (x5 - x0) * 0.6;
    const y3 = y0 + (y5 - y0) * 0.5;
    const x4 = x0 + (x5 - x0) * 0.75;
    const y4 = y0 - (y5 - y0) * 0.1;

    const points = [
        { x: x0, y: y0, type: "start" },
        { x: x1, y: y1, type: "line" },
        { x: x2, y: y2, type: "line" },
        { x: x3, y: y3, type: "line" },
        { x: x4, y: y4, type: "line" },
        { x: x5, y: y5, type: "end" }
    ];

    const adjustmentPoints = [
        { x: x1, y: y1, type: "adjustment" },
        { x: x2, y: y2, type: "adjustment" },
        { x: x3, y: y3, type: "adjustment" },
        { x: x4, y: y4, type: "adjustment" }
    ];

    return { points, adjustmentPoints };
}

function drawElliotCorrectionWave(startPoint, endPoint) {
    const { x: x0, y: y0 } = startPoint;
    const { x: xC, y: yC } = endPoint;

    const xA = x0 + (xC - x0) * 0.3;
    const yA = y0 + (xC - x0) * 0.5;
    const xB = x0 + (xC - x0) * 0.6;
    const yB = y0 - (xC - x0) * 0.3;

    const points = [
        { x: x0, y: y0, type: "start" },
        { x: xA, y: yA, type: "line" },
        { x: xB, y: yB, type: "line" },
        { x: xC, y: yC, type: "end" }
    ];

    const adjustmentPoints = [
        { x: xA, y: yA, type: "adjustment" },
        { x: xB, y: yB, type: "adjustment" }
    ];

    return { points, adjustmentPoints };
}

function drawElliotTriangleWave(startPoint, endPoint) {
    const { x: x0, y: y0 } = startPoint;
    const { x: xE, y: yE } = endPoint;

    const xA = x0 + (xE - x0) * 0.2;
    const yA = y0 + (yE - y0) * 0.3;
    const xB = x0 + (xE - x0) * 0.4;
    const yB = y0 - (yE - y0) * 0.2;
    const xC = x0 + (xE - x0) * 0.6;
    const yC = y0 + (yE - y0) * 0.3;
    const xD = x0 + (xE - x0) * 0.8;
    const yD = y0 - (yE - y0) * 0.1;

    const points = [
        { x: x0, y: y0, type: "start" },
        { x: xA, y: yA, type: "line" },
        { x: xB, y: yB, type: "line" },
        { x: xC, y: yC, type: "line" },
        { x: xD, y: yD, type: "line" },
        { x: xE, y: yE, type: "end" }
    ];

    const adjustmentPoints = [
        { x: xA, y: yA, type: "adjustment" },
        { x: xB, y: yB, type: "adjustment" },
        { x: xC, y: yC, type: "adjustment" },
        { x: xD, y: yD, type: "adjustment" }
    ];

    return { points, adjustmentPoints };
}

function drawElliotDoubleComboWave(startPoint, endPoint) {
    const { x: x0, y: y0 } = startPoint;
    const { x: xW, y: yW } = endPoint;

    const xA = x0 + (xW - x0) * 0.3;
    const yA = y0 + (yW - y0) * 0.4;
    const xB = x0 + (xW - x0) * 0.5;
    const yB = y0 - (yW - y0) * 0.2;
    const xC = x0 + (xW - x0) * 0.7;
    const yC = y0 + (yW - y0) * 0.3;
    const xX = x0 + (xW - x0) * 0.9;
    const yX = y0 - (yW - y0) * 0.1;

    const points = [
        { x: x0, y: y0, type: "start" },
        { x: xA, y: yA, type: "line" },
        { x: xB, y: yB, type: "line" },
        { x: xC, y: yC, type: "line" },
        { x: xX, y: yX, type: "line" },
        { x: xW, y: yW, type: "end" }
    ];

    const adjustmentPoints = [
        { x: xA, y: yA, type: "adjustment" },
        { x: xB, y: yB, type: "adjustment" },
        { x: xC, y: yC, type: "adjustment" },
        { x: xX, y: yX, type: "adjustment" }
    ];

    return { points, adjustmentPoints };
}

function drawElliotTripleComboWave(startPoint, endPoint) {
    const { x: x0, y: y0 } = startPoint;
    const { x: xY, y: yY } = endPoint;

    const xA = x0 + (xY - x0) * 0.25;
    const yA = y0 + (yY - y0) * 0.3;
    const xB = x0 + (xY - x0) * 0.4;
    const yB = y0 - (yY - y0) * 0.2;
    const xC = x0 + (xY - x0) * 0.6;
    const yC = y0 + (yY - y0) * 0.4;
    const xX = x0 + (xY - x0) * 0.75;
    const yX = y0 - (yY - y0) * 0.1;
    const xW = x0 + (xY - x0) * 0.9;
    const yW = y0 + (yY - y0) * 0.2;

    const points = [
        { x: x0, y: y0, type: "start" },
        { x: xA, y: yA, type: "line" },
        { x: xB, y: yB, type: "line" },
        { x: xC, y: yC, type: "line" },
        { x: xX, y: yX, type: "line" },
        { x: xW, y: yW, type: "line" },
        { x: xY, y: yY, type: "end" }
    ];

    const adjustmentPoints = [
        { x: xA, y: yA, type: "adjustment" },
        { x: xB, y: yB, type: "adjustment" },
        { x: xC, y: yC, type: "adjustment" },
        { x: xX, y: yX, type: "adjustment" },
        { x: xW, y: yW, type: "adjustment" }
    ];

    return { points, adjustmentPoints };
}

export {
    drawElliotImpulseWave,
    drawElliotCorrectionWave,
    drawElliotTriangleWave,
    drawElliotDoubleComboWave,
    drawElliotTripleComboWave
};
