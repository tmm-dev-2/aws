import { createChart, ISeriesApi, LineStyle, UTCTimestamp, SeriesType } from 'lightweight-charts';

interface LiquidationLevel {
    timestamp: UTCTimestamp;
    price: number;
    leverage: string;
    color: string;
    width: number;
}

interface ChartStyle {
    colUp: string;
    colDn: string;
    barColor: string;
    linesWidth: number;
}

class LiquidationsSTC {
    private chartContainer: HTMLElement;
    private chart: any;
    private candlestickSeries: ISeriesApi<SeriesType.Candlestick>;
    private volumeSeries: ISeriesApi<SeriesType.Histogram>;
    private liquidationLines: ISeriesApi<SeriesType.Line>[] = [];
    private style: ChartStyle;

    constructor(
        containerId: string,
        public timePeriodMean: number = 40,
        public show5x: boolean = true,
        public show10x: boolean = true,
        public show25x: boolean = true,
        public show50x: boolean = false,
        public show100x: boolean = false,
        public pivotLeft: number = 3,
        public pivotRight: number = 3,
        style: ChartStyle = { colUp: '#22ab94', colDn: '#f7525f', barColor: '#00ff00', linesWidth: 3 }
    ) {
        this.chartContainer = document.getElementById(containerId) as HTMLElement;
        this.chart = createChart(this.chartContainer, { width: 800, height: 600 });
        this.candlestickSeries = this.chart.addCandlestickSeries();
        this.volumeSeries = this.chart.addHistogramSeries();
        this.style = style;
    }

    calculatePivots(data: any[]): { pivotHighs: number[], pivotLows: number[] } {
        const highs = data.map(d => d.high);
        const lows = data.map(d => d.low);
        const pivotHighs = new Array(highs.length).fill(NaN);
        const pivotLows = new Array(lows.length).fill(NaN);

        for (let i = this.pivotLeft; i < highs.length - this.pivotRight; i++) {
            if (highs.slice(i - this.pivotLeft, i).every(h => h < highs[i]) &&
                highs.slice(i + 1, i + this.pivotRight + 1).every(h => h < highs[i])) {
                pivotHighs[i] = highs[i];
            }
            if (lows.slice(i - this.pivotLeft, i).every(l => l > lows[i]) &&
                lows.slice(i + 1, i + this.pivotRight + 1).every(l => l > lows[i])) {
                pivotLows[i] = lows[i];
            }
        }
        return { pivotHighs, pivotLows };
    }

    calculateLiquidationLevels(volume: number[]): { _100x: boolean[], _50x: boolean[], _25x: boolean[], _10x: boolean[], _5x: boolean[] } {
        const highest = this.rollingMax(volume, this.timePeriodMean);
        const lowest = this.rollingMin(volume, this.timePeriodMean);
        const avg = highest.map((h, i) => (h + lowest[i]) / 2);
        const avgMean = this.sma(avg, this.timePeriodMean + 10);

        const _100x = avg.map((a, i) => a >= 1.2 * avgMean[i]);
        const _50x = avg.map((a, i) => a >= 1.1 * avgMean[i]);
        const _25x = avg.map((a, i) => a >= 1.05 * avgMean[i]);
        const _10x = avg.map((a, i) => a >= 1.025 * avgMean[i]);
        const _5x = avg.map((a, i) => a > avgMean[i]);

        return { _100x, _50x, _25x, _10x, _5x };
    }

    calculateLiquidationPrice(price: number, leverage: number): number {
        const percentRisk = {
            5: 0.20,
            10: 0.10,
            25: 0.04,
            50: 0.02,
            100: 0.01
        };
        return price / (1 + percentRisk[leverage]);
    }

    identifyPatterns(data: any[]): { doji: number[], bullishEngulfing: number[], bearishEngulfing: number[] } {
        const patterns = {
            doji: [],
            bullishEngulfing: [],
            bearishEngulfing: []
        };

        for (let i = 1; i < data.length; i++) {
            const { open: openPrice, close: closePrice, high: highPrice, low: lowPrice } = data[i];
            const { open: prevOpen, close: prevClose } = data[i - 1];

            const body = Math.abs(closePrice - openPrice);
            const upperShadow = highPrice - Math.max(openPrice, closePrice);
            const lowerShadow = Math.min(openPrice, closePrice) - lowPrice;

            // Doji: Small body, long shadows
            if (body < 0.1 * (highPrice - lowPrice)) {
                patterns.doji.push(data[i].timestamp as number);
            }

            // Bullish Engulfing
            if (prevClose < prevOpen && closePrice > openPrice && closePrice > prevOpen && openPrice < prevClose) {
                patterns.bullishEngulfing.push(data[i].timestamp as number);
            }

            // Bearish Engulfing
            if (prevClose > prevOpen && closePrice < openPrice && closePrice < prevOpen && openPrice > prevClose) {
                patterns.bearishEngulfing.push(data[i].timestamp as number);
            }
        }

        return patterns;
    }

    plotData(data: any[], results: any): void {
        const candlestickData = data.map(d => ({
            time: d.timestamp as number,
            open: d.open,
            high: d.high,
            low: d.low,
            close: d.close
        }));

        const volumeData = data.map(d => ({
            time: d.timestamp as number,
            value: d.volume,
            color: d.close >= d.open ? 'rgba(38,166,154,0.8)' : 'rgba(239,83,80,0.8)'
        }));

        this.candlestickSeries.setData(candlestickData);
        this.volumeSeries.setData(volumeData);

        results.liquidationLevels.forEach((level: LiquidationLevel) => {
            this.addLiquidationLevel(level);
        });

        const patterns = this.identifyPatterns(data);

        // Add markers for patterns
        patterns.doji.forEach(timestamp => {
            this.chart.addMarker({
                time: timestamp,
                position: 'aboveBar',
                color: 'orange',
                shape: 'circle',
                text: 'Doji'
            });
        });

        patterns.bullishEngulfing.forEach(timestamp => {
            this.chart.addMarker({
                time: timestamp,
                position: 'belowBar',
                color: 'green',
                shape: 'arrowUp',
                text: 'Bullish Engulfing'
            });
        });

        patterns.bearishEngulfing.forEach(timestamp => {
            this.chart.addMarker({
                time: timestamp,
                position: 'aboveBar',
                color: 'red',
                shape: 'arrowDown',
                text: 'Bearish Engulfing'
            });
        });
    }

    addLiquidationLevel(level: LiquidationLevel) {
        const lineSeries = this.chart.addLineSeries({
            color: level.color,
            lineWidth: level.width
        });
        lineSeries.setData([{ time: level.timestamp, value: level.price }]);
        this.liquidationLines.push(lineSeries);
    }

    rollingMax(arr: number[], window: number): number[] {
        return arr.map((_, i) => Math.max(...arr.slice(Math.max(0, i - window + 1), i + 1)));
    }

    rollingMin(arr: number[], window: number): number[] {
        return arr.map((_, i) => Math.min(...arr.slice(Math.max(0, i - window + 1), i + 1)));
    }

    sma(arr: number[], window: number): number[] {
        return arr.map((_, i) => {
            const start = Math.max(0, i - window + 1);
            const slice = arr.slice(start, i + 1);
            return slice.reduce((acc, val) => acc + val, 0) / slice.length;
        });
    }
}

export default LiquidationsSTC;
