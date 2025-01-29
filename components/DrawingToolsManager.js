import {  TrendLine, Ray, ExtendedLine, TrendAngle, HorizontalLine, VerticalLine, CrossLine } from '../drawing-logic/lines';
import { StandardPitchfork, ModifiedSchiffPitchfork, SchiffPitchfork, InsidePitchfork, BarleyPitchfork } from '../drawing-logic/pitchfork';
import { ParallelChannel, FlatTopBottomChannel, DisjointedChannel } from '../drawing-logic/channels';
import {  drawCyclicLines, drawTimeCycles, drawSineLine } from '../drawing-logic/cycles';
import { GannBox, GannSquareFixed, GannFan } from '../drawing-logic/gann';
import { drawElliotImpulseWave, drawElliotCorrectionWave, drawElliotTriangleWave, drawElliotDoubleComboWave, drawElliotTripleComboWave } from '../drawing-logic/elliot-wave';
import { ArrowMarker, Arrow, ArrowMarkUp, ArrowMarkDown } from '../drawing-logic/arrows';
import { rectangle, rotatedRectangle, ellipse, circle, triangle, arc, curve, doubleCurve } from '../drawing-logic/shapes';
import {fibRetracement, fibExtension, fibChannel,TrendBasedFibTime, FibCircle, FibSpeedResistanceArcs,FibWedge, Pitchfan} from '../drawing-logic/fibonacci';
import {longPosition, shortPosition, forecast, projection} from '../drawing-logic/projection';

class DrawingToolsManager {
    constructor(chart) {
        this.chart = chart;
        this.activeTool = null;
        this.isDrawing = false;
        this.points = [];
        this.currentDrawing = null;
        this.drawings = [];
    }

    setTool(toolName) {
        this.activeTool = toolName;
        this.points = [];
        this.isDrawing = false;
    }

    handleMouseDown(e) {
        if (!this.activeTool) return;
        
        const point = {
            x: this.chart.timeScale().coordinateToTime(e.x),
            y: this.chart.priceScale().coordinateToPrice(e.y)
        };
        
        this.isDrawing = true;
        this.points.push(point);
        this.startDrawing();
    }

    handleMouseMove(e) {
        if (!this.isDrawing) return;
        
        const point = {
            x: this.chart.timeScale().coordinateToTime(e.x),
            y: this.chart.priceScale().coordinateToPrice(e.y)
        };
        
        this.updateDrawing(point);
    }

    handleMouseUp(e) {
        if (!this.isDrawing) return;
        
        const point = {
            x: this.chart.timeScale().coordinateToTime(e.x),
            y: this.chart.priceScale().coordinateToPrice(e.y)
        };
        
        this.points.push(point);
        this.finishDrawing();
        this.isDrawing = false;
    }

    startDrawing() {
        switch(this.activeTool) {
            // Lines
            case 'trendLine':
                this.currentDrawing = new TrendLine(this.points[0], this.points[0]);
                break;
            case 'ray':
                this.currentDrawing = new Ray(this.points[0], this.points[0]);
                break;
            case 'extendedLine':
                this.currentDrawing = new ExtendedLine(this.points[0], this.points[0]);
                break;
            case 'horizontalLine':
                this.currentDrawing = new HorizontalLine(this.points[0].y);
                break;
            case 'verticalLine':
                this.currentDrawing = new VerticalLine(this.points[0].x);
                break;
            case 'crossLine':
                this.currentDrawing = new CrossLine(this.points[0].x, this.points[0].y);
                break;

            // Pitchforks
            case 'standardPitchfork':
                this.currentDrawing = new StandardPitchfork(this.points[0].x, this.points[0].y);
                break;
            case 'schiffPitchfork':
                this.currentDrawing = new SchiffPitchfork(this.points[0].x, this.points[0].y);
                break;
            case 'modifiedSchiffPitchfork':
                this.currentDrawing = new ModifiedSchiffPitchfork(this.points[0].x, this.points[0].y);
                break;

            // Channels
            case 'parallelChannel':
                this.currentDrawing = new ParallelChannel(this.points[0].x, this.points[0].y);
                break;
            case 'flatChannel':
                this.currentDrawing = new FlatTopBottomChannel(this.points[0].x, this.points[0].y);
                break;

            // Fibonacci
            case 'fibRetracement':
                this.currentDrawing = new fibRetracement(this.points[0], this.points[0]);
                break;
            case 'fibExtension':
                this.currentDrawing = new fibExtension(this.points[0], this.points[0]);
                break;
            case 'fibChannel':
                this.currentDrawing = new fibChannel(this.points[0], this.points[0]);
                break;
            case 'fibTime':
                this.currentDrawing = new TrendBasedFibTime(this.points[0], this.points[0]);
                break;
            case 'fibCircle':
                this.currentDrawing = new FibCircle(this.points[0], this.points[0]);
                break;

            // Gann
            case 'gannBox':
                this.currentDrawing = new GannBox(this.points[0], this.points[0]);
                break;
            case 'gannSquare':
                this.currentDrawing = new GannSquareFixed(this.points[0], this.points[0]);
                break;
            case 'gannFan':
                this.currentDrawing = new GannFan(this.points[0], this.points[0]);
                break;
            
        // Arcs// missing 
            // Inside startDrawing() method, add these cases:
            // Inside startDrawing() method, add these cases:

case 'trendAngle':
    this.currentDrawing = new TrendAngle(this.points[0], this.points[0]);
    break;

case 'arrowMarker':
    this.currentDrawing = new ArrowMarker({
        startX: this.points[0].x,
        startY: this.points[0].y,
        endX: this.points[0].x,
        endY: this.points[0].y
    });
    break;


// Additional Pitchforks
case 'insidePitchfork':
    this.currentDrawing = new InsidePitchfork(this.points[0].x, this.points[0].y);
    break;
case 'barleyPitchfork':
    this.currentDrawing = new BarleyPitchfork(this.points[0].x, this.points[0].y);
    break;

// Additional Channels
case 'disjointedChannel':
    this.currentDrawing = new DisjointedChannel(this.points[0].x, this.points[0].y);
    break;

// Cycles
case 'cyclicLines':
    this.currentDrawing = drawCyclicLines(this.points[0].x, this.points[0].x, this.points[0].y, this.points[0].y);
    break;
case 'timeCycles':
    this.currentDrawing = drawTimeCycles(this.points[0].x, this.points[0].x, this.points[0].y, this.points[0].y);
    break;
case 'sineLine':
    this.currentDrawing = drawSineLine(this.points[0].x, this.points[0].y, this.points[0].x, this.points[0].y);
    break;

// Additional Elliot Waves
case 'elliotDoubleCombo':
    this.currentDrawing = drawElliotDoubleComboWave(this.points[0], this.points[0]);
    break;
case 'elliotTripleCombo':
    this.currentDrawing = drawElliotTripleComboWave(this.points[0], this.points[0]);
    break;

// Additional Fibonacci
case 'fibSpeedResistanceArcs':
    this.currentDrawing = new FibSpeedResistanceArcs(this.points[0], this.points[0]);
    break;
case 'fibWedge':
    this.currentDrawing = new FibWedge(this.points[0], this.points[0]);
    break;
case 'pitchfan':
    this.currentDrawing = new Pitchfan(this.points[0], this.points[0], this.points[0]);
    break;

// Additional Shapes
case 'rotatedRectangle':
    this.currentDrawing = rotatedRectangle(this.points[0].x, this.points[0].y, this.points[0].x, this.points[0].y, 0);
    break;
case 'arc':
    this.currentDrawing = arc(this.points[0].x, this.points[0].y, 0, 0, Math.PI * 2);
    break;
case 'curve':
    this.currentDrawing = curve(this.points[0].x, this.points[0].y, this.points[0].x, this.points[0].y, this.points[0].x, this.points[0].y);
    break;
case 'doubleCurve':
    this.currentDrawing = doubleCurve(this.points[0].x, this.points[0].y, this.points[0].x, this.points[0].y, this.points[0].x, this.points[0].y, this.points[0].x, this.points[0].y);
    break;

// Projections
case 'longPosition':
    this.currentDrawing = longPosition(this.points[0].y, this.points[0].y, this.points[0].y, 1);
    break;
case 'shortPosition':
    this.currentDrawing = shortPosition(this.points[0].y, this.points[0].y, this.points[0].y, 1);
    break;
case 'forecast':
    this.currentDrawing = forecast(this.points[0].y, this.points[0].y, new Date(), new Date());
    break;
case 'projection':
    this.currentDrawing = projection([this.points[0]]);
    break;


            // Elliot Waves
            case 'elliotImpulse':
                this.currentDrawing = drawElliotImpulseWave(this.points[0], this.points[0]);
                break;
            case 'elliotCorrection':
                this.currentDrawing = drawElliotCorrectionWave(this.points[0], this.points[0]);
                break;
            case 'elliotTriangle':
                this.currentDrawing = drawElliotTriangleWave(this.points[0], this.points[0]);
                break;

            // Shapes
            case 'rectangle':
                this.currentDrawing = rectangle(this.points[0].x, this.points[0].y);
                break;
            case 'circle':
                this.currentDrawing = circle(this.points[0].x, this.points[0].y);
                break;
            case 'triangle':
                this.currentDrawing = triangle(this.points[0].x, this.points[0].y);
                break;
            case 'ellipse':
                this.currentDrawing = ellipse(this.points[0].x, this.points[0].y);
                break;

            // Arrows
            case 'arrow':
                this.currentDrawing = new Arrow({
                    startX: this.points[0].x,
                    startY: this.points[0].y,
                    endX: this.points[0].x,
                    endY: this.points[0].y
                });
                break;
            case 'arrowUp':
                this.currentDrawing = new ArrowMarkUp({
                    startX: this.points[0].x,
                    startY: this.points[0].y,
                    endX: this.points[0].x,
                    endY: this.points[0].y
                });
                break;
            case 'arrowDown':
                this.currentDrawing = new ArrowMarkDown({
                    startX: this.points[0].x,
                    startY: this.points[0].y,
                    endX: this.points[0].x,
                    endY: this.points[0].y
                });
                break;
        }
    }

    updateDrawing(point) {
        if (!this.currentDrawing) return;
        
        if (this.currentDrawing.updateCoordinates) {
            this.currentDrawing.updateCoordinates('end', point.x, point.y);
        }
        
        this.chart.updateAllViews();
    }

    finishDrawing() {
        if (!this.currentDrawing) return;
        this.drawings.push(this.currentDrawing);
        this.chart.updateAllViews();
    }

    removeDrawing(index) {
        this.drawings.splice(index, 1);
        this.chart.updateAllViews();
    }

    clearDrawings() {
        this.drawings = [];
        this.chart.updateAllViews();
    }
}

export default DrawingToolsManager;
