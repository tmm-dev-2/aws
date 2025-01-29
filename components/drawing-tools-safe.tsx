"use client"

import { useEffect, useRef, useState, useLayoutEffect } from 'react'
import { createChart, ColorType, IChartApi, LineStyle, ISeriesApi } from 'lightweight-charts';
import { DoubleHullTurboP1Chart } from '../strategies/double-hull-turbo-p1/double-hull-turbo-p1';
import { KernelRegressionChart } from '../strategies/kernel-regression-p1/kernel-regression-p1';

// Drawing Tools Imports
import { TrendLine, Ray, ExtendedLine, TrendAngle, HorizontalLine, VerticalLine, CrossLine } from '../drawing-logic/lines'
import { Pitchfork, SchiffPitchfork } from '../drawing-logic/pitchfork'
import { ParallelChannel, FlatTopBottomChannel, DisjointedChannel } from '../drawing-logic/channels'
import { fibRetracement, fibExtension, fibChannel, TrendBasedFibTime, FibCircle, FibSpeedResistanceArcs, FibWedge, Pitchfan } from '../drawing-logic/fibonacci'
import { GannBox, GannSquareFixed, GannFan } from '../drawing-logic/gann'
import { rectangle, rotatedRectangle, ellipse, circle, triangle, arc, curve, doubleCurve } from '../drawing-logic/shapes'
import { ArrowMarker, Arrow, ArrowMarkUp, ArrowMarkDown } from '../drawing-logic/arrows'
import { Brush, Highlighter } from '../drawing-logic/brushes'
import { longPosition, shortPosition, forecast, projection } from '../drawing-logic/projection'

interface CandleData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface MainChartProps {
  symbol: string;
  selectedPeriod: string;
  selectedStrategy: string;
  data?: CandleData[];
  activeTool?: string;
}

interface Point {
  x: number;
  y: number;
}

export const MainChart: React.FC<MainChartProps> = ({ 
    symbol, 
    selectedPeriod,
    selectedStrategy,
    data,
    activeTool
  }) => {
    const [chartData, setChartData] = useState<CandleData[]>([]);
    const chartContainerRef = useRef<HTMLDivElement>(null);
    const chartRef = useRef<IChartApi | null>(null);
    const seriesRef = useRef<ReturnType<IChartApi['addCandlestickSeries']>>(null);
    const strategyChartRef = useRef<DoubleHullTurboP1Chart | KernelRegressionChart | null>(null);
    const drawingSeriesRef = useRef<ISeriesApi<'Line'> | null>(null);
    const [isDrawing, setIsDrawing] = useState(false);
    const [drawingPoints, setDrawingPoints] = useState<Point[]>([]);
  
    // Chart initialization effect
    useEffect(() => {
      if (!chartContainerRef.current) return;
  
      const chart = createChart(chartContainerRef.current, {
        width: chartContainerRef.current.clientWidth,
        height: chartContainerRef.current.clientHeight,
        layout: {
          background: { color: '#1A1A1A' },
          textColor: '#d1d4dc',
        },
        grid: {
          vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
          horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
        },
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
        },
      });
  
      const candleSeries = chart.addCandlestickSeries({
        upColor: '#4CAF50',
        downColor: '#FF5252',
        borderVisible: false,
        wickUpColor: '#4CAF50',
        wickDownColor: '#FF5252',
      });
  
      chartRef.current = chart;
      seriesRef.current = candleSeries;
      drawingSeriesRef.current = chart.addLineSeries({
        color: '#2196F3',
        lineWidth: 2,
        lineStyle: LineStyle.Solid,
      });
  
      return () => {
        chart.remove();
      };
    }, []);
  
    // Drawing tool handlers
    useEffect(() => {
      if (!chartContainerRef.current || !chartRef.current || !activeTool) return;
  
      const handleMouseDown = (e: MouseEvent) => {
        const rect = chartContainerRef.current!.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        setIsDrawing(true);
        setDrawingPoints([{x, y}]);
      };
  
      const handleMouseMove = (e: MouseEvent) => {
        if (!isDrawing || !drawingSeriesRef.current) return;
  
        const rect = chartContainerRef.current!.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
  
        const points = [...drawingPoints, {x, y}];
        setDrawingPoints(points);
  
        // Convert screen coordinates to chart coordinates
        const chartPoints = points.map(point => {
          const timePoint = chartRef.current!.timeScale().coordinateToTime(point.x);
          const pricePoint = chartRef.current!.priceScale('right').coordinateToPrice(point.y);
          return {
            time: timePoint as number,
            value: pricePoint as number
          };
        });
  
        // Apply the active drawing tool
        applyDrawingTool(chartPoints);
      };
  
      const handleMouseUp = () => {
        if (!isDrawing) return;
        setIsDrawing(false);
        finalizeDraw();
      };
  
      chartContainerRef.current.addEventListener('mousedown', handleMouseDown);
      chartContainerRef.current.addEventListener('mousemove', handleMouseMove);
      chartContainerRef.current.addEventListener('mouseup', handleMouseUp);
  
      return () => {
        chartContainerRef.current?.removeEventListener('mousedown', handleMouseDown);
        chartContainerRef.current?.removeEventListener('mousemove', handleMouseMove);
        chartContainerRef.current?.removeEventListener('mouseup', handleMouseUp);
      };
    }, [activeTool, isDrawing, drawingPoints]);
  
    const applyDrawingTool = (chartPoints: Array<{time: number, value: number}>) => {
      if (!drawingSeriesRef.current) return;
  
      switch (activeTool) {
        const applyDrawingTool = (chartPoints: Array<{time: number, value: number}>) => {
            if (!drawingSeriesRef.current) return;
        
            switch (activeTool) {
                case 'trendLine':
                    const trendLine = new TrendLine(drawingPoints[0], drawingPoints[drawingPoints.length - 1]);
                    drawingSeriesRef.current.setData(trendLine.getExtendedPoints());
                    break;
        
                case 'ray':
                    const ray = new Ray(drawingPoints[0], drawingPoints[drawingPoints.length - 1]);
                    drawingSeriesRef.current.setData(ray.getExtendedPoints());
                    break;
        
                case 'extendedLine':
                    const extLine = new ExtendedLine(drawingPoints[0], drawingPoints[drawingPoints.length - 1]);
                    drawingSeriesRef.current.setData(extLine.getExtendedPoints());
                    break;
        
                case 'trendAngle':
                    const trendAngle = new TrendAngle(drawingPoints[0], drawingPoints[drawingPoints.length - 1]);
                    drawingSeriesRef.current.setData([drawingPoints[0], drawingPoints[drawingPoints.length - 1]]);
                    break;
        
                case 'horizontalLine':
                    const hLine = new HorizontalLine(drawingPoints[0].y);
                    drawingSeriesRef.current.setData(hLine.getExtendedPoints());
                    break;
        
                case 'verticalLine':
                    const vLine = new VerticalLine(drawingPoints[0].x);
                    drawingSeriesRef.current.setData(vLine.getExtendedPoints());
                    break;
        
                case 'crossLine':
                    const crossLine = new CrossLine(drawingPoints[0].x, drawingPoints[0].y);
                    drawingSeriesRef.current.setData([crossLine.getPoints()]);
                    break;
        
                case 'pitchfork':
                    const pitchfork = new Pitchfork(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y,
                        drawingPoints[2].x, drawingPoints[2].y
                    );
                    drawingSeriesRef.current.setData(pitchfork.getLines());
                    break;
        
                case 'schiffPitchfork':
                    const schiffPitchfork = new SchiffPitchfork(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y,
                        drawingPoints[2].x, drawingPoints[2].y
                    );
                    drawingSeriesRef.current.setData(schiffPitchfork.getLines());
                    break;
        
                case 'parallelChannel':
                    const channel = new ParallelChannel(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y,
                        drawingPoints[2].x, drawingPoints[2].y,
                        drawingPoints[3].x, drawingPoints[3].y
                    );
                    drawingSeriesRef.current.setData(channel.draw());
                    break;
        
                case 'flatChannel':
                    const flatChannel = new FlatTopBottomChannel(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y,
                        drawingPoints[2].x, drawingPoints[2].y
                    );
                    drawingSeriesRef.current.setData(flatChannel.draw());
                    break;
        
                case 'disjointedChannel':
                    const disjointedChannel = new DisjointedChannel(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y,
                        drawingPoints[2].x, drawingPoints[2].y,
                        drawingPoints[3].x, drawingPoints[3].y,
                        drawingPoints[4].x, drawingPoints[4].y,
                        drawingPoints[5].x, drawingPoints[5].y
                    );
                    drawingSeriesRef.current.setData(disjointedChannel.draw());
                    break;
        
                case 'fibonacci':
                    const fibLevels = fibRetracement(drawingPoints[0], drawingPoints[drawingPoints.length - 1]);
                    drawingSeriesRef.current.setData(Object.values(fibLevels));
                    break;
        
                case 'fibExtension':
                    const fibExt = fibExtension(drawingPoints[0], drawingPoints[1], drawingPoints[2]);
                    drawingSeriesRef.current.setData(Object.values(fibExt));
                    break;
        
                case 'fibChannel':
                    const fibChan = fibChannel(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(Object.values(fibChan));
                    break;
        
                case 'fibTime':
                    const fibTime = new TrendBasedFibTime(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(fibTime.timeLevels());
                    break;
        
                case 'fibCircle':
                    const fibCircle = new FibCircle(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(fibCircle.radii());
                    break;
        
                case 'fibSpeedResistance':
                    const fibSpeed = new FibSpeedResistanceArcs(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(fibSpeed.arcs());
                    break;
        
                case 'fibWedge':
                    const fibWedge = new FibWedge(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(fibWedge.wedgeLevels());
                    break;
        
                case 'pitchfan':
                    const pitchfan = new Pitchfan(drawingPoints[0], drawingPoints[1], drawingPoints[2]);
                    drawingSeriesRef.current.setData(pitchfan.fanLines());
                    break;
        
                case 'gannBox':
                    const gannBox = new GannBox(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(gannBox.getLines());
                    break;
        
                case 'gannSquare':
                    const gannSquare = new GannSquareFixed(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(gannSquare.getLines());
                    break;
        
                case 'gannFan':
                    const gannFan = new GannFan(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(gannFan.getLines());
                    break;
        
                case 'rectangle':
                    const rect = rectangle(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y
                    );
                    drawingSeriesRef.current.setData(rect.shapePoints);
                    break;
        
                case 'rotatedRectangle':
                    const rotRect = rotatedRectangle(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y,
                        Math.PI / 4
                    );
                    drawingSeriesRef.current.setData(rotRect.shapePoints);
                    break;
        
                case 'ellipse':
                    const ellipseShape = ellipse(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y
                    );
                    drawingSeriesRef.current.setData(ellipseShape.shapePoints);
                    break;
        
                case 'circle':
                    const circleShape = circle(
                        drawingPoints[0].x, drawingPoints[0].y,
                        Math.sqrt(Math.pow(drawingPoints[1].x - drawingPoints[0].x, 2) + 
                                 Math.pow(drawingPoints[1].y - drawingPoints[0].y, 2))
                    );
                    drawingSeriesRef.current.setData(circleShape.shapePoints);
                    break;
        
                case 'triangle':
                    const tri = triangle(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y
                    );
                    drawingSeriesRef.current.setData(tri.shapePoints);
                    break;
        
                case 'arc':
                    const arcShape = arc(
                        drawingPoints[0].x, drawingPoints[0].y,
                        Math.sqrt(Math.pow(drawingPoints[1].x - drawingPoints[0].x, 2) + 
                                 Math.pow(drawingPoints[1].y - drawingPoints[0].y, 2)),
                        0, Math.PI * 2
                    );
                    drawingSeriesRef.current.setData(arcShape.shapePoints);
                    break;
        
                case 'curve':
                    const curveShape = curve(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y,
                        drawingPoints[2].x, drawingPoints[2].y
                    );
                    drawingSeriesRef.current.setData(curveShape.shapePoints);
                    break;
        
                case 'doubleCurve':
                    const dblCurve = doubleCurve(
                        drawingPoints[0].x, drawingPoints[0].y,
                        drawingPoints[1].x, drawingPoints[1].y,
                        drawingPoints[2].x, drawingPoints[2].y,
                        drawingPoints[3].x, drawingPoints[3].y
                    );
                    drawingSeriesRef.current.setData(dblCurve.shapePoints);
                    break;
        
                case 'arrow':
                    const arrow = new Arrow({
                        startX: drawingPoints[0].x,
                        startY: drawingPoints[0].y,
                        endX: drawingPoints[1].x,
                        endY: drawingPoints[1].y
                    });
                    drawingSeriesRef.current.setData(arrow.toObject());
                    break;
        
                case 'arrowMarker':
                    const arrowMarker = new ArrowMarker({
                        startX: drawingPoints[0].x,
                        startY: drawingPoints[0].y,
                        endX: drawingPoints[1].x,
                        endY: drawingPoints[1].y
                    });
                    drawingSeriesRef.current.setData(arrowMarker.toObject());
                    break;
        
                case 'arrowUp':
                    const arrowUp = new ArrowMarkUp({
                        startX: drawingPoints[0].x,
                        startY: drawingPoints[0].y,
                        endX: drawingPoints[1].x,
                        endY: drawingPoints[1].y
                    });
                    drawingSeriesRef.current.setData(arrowUp.toObject());
                    break;
        
                case 'arrowDown':
                    const arrowDown = new ArrowMarkDown({
                        startX: drawingPoints[0].x,
                        startY: drawingPoints[0].y,
                        endX: drawingPoints[1].x,
                        endY: drawingPoints[1].y
                    });
                    drawingSeriesRef.current.setData(arrowDown.toObject());
                    break;
        
                case 'brush':
                    const brush = new Brush({
                        color: '#2196F3',
                        lineThickness: 2,
                        transparency: 1,
                        backgroundColor: '#131722'
                    });
                    drawingPoints.forEach(point => brush.addPoint(point));
                    drawingSeriesRef.current.setData(chartPoints);
                    break;
        
                case 'highlighter':
                    const highlighter = new Highlighter({
                        color: '#2196F3',
                        lineThickness: 2,
                        transparency: 0.5,
                        backgroundColor: '#131722'
                    });
                    drawingPoints.forEach(point => highlighter.addPoint(point));
                    drawingSeriesRef.current.setData(chartPoints);
                    break;
        
                case 'elliotImpulseWave':
                    const impulseWave = drawElliotImpulseWave(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(impulseWave.points);
                    break;
        
                case 'elliotCorrectionWave':
                    const correctionWave = drawElliotCorrectionWave(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(correctionWave.points);
                    break;
        
                case 'elliotTriangleWave':
                    const triangleWave = drawElliotTriangleWave(drawingPoints[0], drawingPoints[1]);
                    drawingSeriesRef.current.setData(triangleWave.points);
                    break;
        
                case 'xabcdPattern':
                    const xabcd = new XABCDPattern(
                        drawingPoints[0], drawingPoints[1], drawingPoints[2],
                        drawingPoints[3], drawingPoints[4]
                    );
                    drawingSeriesRef.current.setData(xabcd.points);
                    break;
        
                case 'cypherPattern':
                    const cypher = new CypherPattern(
                        drawingPoints[0], drawingPoints[1], drawingPoints[2],
                        drawingPoints[3], drawingPoints[4]
                    );
                    drawingSeriesRef.current.setData(cypher.points);
                    break;
        
                case 'headAndShoulders':
                    const hns = new HeadAndShouldersPattern(
                        drawingPoints[0], drawingPoints[1], drawingPoints[2],
                        drawingPoints[3], drawingPoints[4]
                    );
                    drawingSeriesRef.current.setData(hns.points);
                    break;
        
                case 'abcdPattern':
                    const abcd = new ABCDPattern(
                        drawingPoints[0], drawingPoints[1],
                        drawingPoints[2], drawingPoints[3]
                    );
                    drawingSeriesRef.current.setData(abcd.points);
                    break;
        
                case 'threeDrivesPattern':
                    const threedrives = new ThreeDrivesPattern(
                        drawingPoints[0], drawingPoints[1], drawingPoints[2],
                        drawingPoints[3], drawingPoints[4]
                    );
                    drawingSeriesRef.current.setData(threedrives.points);
                    break;
        
                case 'longPosition':
                    const long = longPosition(
                        drawingPoints[0].y,
                        drawingPoints[1].y,
                        drawingPoints[2].y,
                        1
                    );
                    drawingSeriesRef.current.setData([long]);
                    break;
        
                case 'shortPosition':
                    const short = shortPosition(
                        drawingPoints[0].y,
                        drawingPoints[1].y,
                        drawingPoints[2].y,
                        1
                    );
                    drawingSeriesRef.current.setData([short]);
                    break;
        
                case 'forecast':
                    const forecastResult = forecast(
                        drawingPoints[0].y,
                        drawingPoints[1].y,
                        new Date(drawingPoints[0].x),
                        new Date(drawingPoints[1].x)
                    );
                    drawingSeriesRef.current.setData([forecastResult]);
                    break;
        
                case 'projection':
                    const proj = projection(drawingPoints);
                    drawingSeriesRef.current.setData(proj.projectedPriceRange);
                    break;
        
                case 'cyclicLines':
                    const cycles = drawCyclicLines(
                        drawingPoints[0].x,
                        drawingPoints[1].x,
                        drawingPoints[0].y,
                        drawingPoints[1].y
                    );
                    drawingSeriesRef.current.setData(cycles);
                    break;
        
                case 'timeCycles':
                    const timeCycles = drawTimeCycles(
                        drawingPoints[0].x,
                        drawingPoints[1].x,
                        drawingPoints[0].y,
                        drawingPoints[1].y
                    );
                    drawingSeriesRef.current.setData(timeCycles);
                    break;
        
                case 'sineLine':
                    const sine = drawSineLine(
                        drawingPoints[0].x,
                        drawingPoints[0].y,
                        drawingPoints[1].x,
                        drawingPoints[1].y
                    );
                    drawingSeriesRef.current.setData(sine);
                    break;
            }
        };
        
        
  
        // Add more cases for other tools
      }
    };
  
    const finalizeDraw = () => {
      if (drawingPoints.length < 2) return;
      // Save the drawing to chart's state if needed
      setDrawingPoints([]);
    };
  
    // Handle data updates
    useEffect(() => {
      if (seriesRef.current && data && data.length > 0) {
        const formattedData = data.map(candle => ({
          time: candle.time / 1000,
          open: candle.open,
          high: candle.high,
          low: candle.low,
          close: candle.close
        }));
  
        setChartData(data);
        seriesRef.current.setData(formattedData);
      }
    }, [data]);
  
    // Handle window resize
    useLayoutEffect(() => {
      if (!chartContainerRef.current || !chartRef.current) return;
  
      const handleResize = () => {
        chartRef.current?.resize(
          chartContainerRef.current!.clientWidth,
          chartContainerRef.current!.clientHeight
        );
      };
  
      const resizeObserver = new ResizeObserver(handleResize);
      resizeObserver.observe(chartContainerRef.current);
  
      return () => {
        resizeObserver.disconnect();
      };
    }, []);
  
    return (
      <div 
        ref={chartContainerRef} 
        className="w-full h-full overflow-hidden"
        style={{ position: 'relative' }}
      />
    );
  };
  