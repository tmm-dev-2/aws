import { createChart, LineStyle } from 'lightweight-charts';

interface StrategyResult {
    open: number[];
    high: number[];
    low: number[];
    close: number[];
    volume: number[];
    trailing_stop: number[];
    trend: number[];
    extremum: number[];
    state: string[];
    fibonacci_levels: number[];
    fibonacci_entry_signals: {
        l1: boolean;
        l2: boolean;
        l3: boolean;
        s1: boolean;
        s2: boolean;
        s3: boolean;
    };
    rsi: number[];
    stochastic: {
        k: number[];
        d: number[];
    };
    macd: {
        line: number[];
        signal: number[];
        histogram: number[];
    };
    timestamps: number[];
    visualization: {
        colors: {
            up: string;
            down: string;
            neutral: string;
        };
    };
}

export class SupportResistanceBlackflagChart {
    private chart: any;
    private candleSeries: any;
    private trailingStopSeries: any;
    private extremumSeries: any;
    private trendLineSeries: any;
    private fibonacciSeries: any[];
    private rsiSeries: any;
    private stochasticKSeries: any;
    private stochasticDSeries: any;
    private macdLineSeries: any;
    private macdSignalSeries: any;
    private macdHistogramSeries: any;

    constructor(container: HTMLElement) {
        this.chart = createChart(container, {
            layout: {
                background: { color: '#ffffff' },
                textColor: '#333',
            },
            grid: {
                vertLines: { color: '#f0f0f0' },
                horzLines: { color: '#f0f0f0' },
            },
            rightPriceScale: {
                borderColor: '#d1d4dc',
            },
            timeScale: {
                borderColor: '#d1d4dc',
                timeVisible: true,
            },
            width: container.clientWidth,
            height: container.clientHeight,
        });

        // Candlestick Series
        this.candleSeries = this.chart.addCandlestickSeries({
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderVisible: false,
            wickUpColor: '#26a69a',
            wickDownColor: '#ef5350',
        });

        // Trailing Stop Series
        this.trailingStopSeries = this.chart.addLineSeries({
            color: '#FF6B6B',
            lineWidth: 2,
            lineStyle: LineStyle.Dashed,
            title: 'Trailing Stop',
        });

        // Extremum Series
        this.extremumSeries = this.chart.addLineSeries({
            color: '#FFC107',
            lineWidth: 2,
            lineStyle: LineStyle.Dotted,
            title: 'Extremum',
        });

        // Trend Line Series
        this.trendLineSeries = this.chart.addLineSeries({
            color: '#9C27B0',
            lineWidth: 1,
            lineStyle: LineStyle.Solid,
            title: 'Trend',
        });

        // Fibonacci Series
        this.fibonacciSeries = [];

        // Indicator Series
        this.rsiSeries = this.chart.addLineSeries({
            color: '#2196F3',
            lineWidth: 1,
            title: 'RSI',
        });

        this.stochasticKSeries = this.chart.addLineSeries({
            color: '#4CAF50',
            lineWidth: 1,
            title: 'Stochastic K',
        });

        this.stochasticDSeries = this.chart.addLineSeries({
            color: '#FF9800',
            lineWidth: 1,
            title: 'Stochastic D',
        });

        this.macdLineSeries = this.chart.addLineSeries({
            color: '#673AB7',
            lineWidth: 1,
            title: 'MACD Line',
        });

        this.macdSignalSeries = this.chart.addLineSeries({
            color: '#F44336',
            lineWidth: 1,
            title: 'MACD Signal',
        });

        this.macdHistogramSeries = this.chart.addHistogramSeries({
            color: '#03A9F4',
            lineWidth: 1,
            title: 'MACD Histogram',
        });
    }

    public async updateChart(symbol: string, timeframe: string): Promise<void> {
        try {
            const response = await fetch(`/api/support-resistance-blackflag-p2?symbol=${symbol}&timeframe=${timeframe}`);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const result: StrategyResult = await response.json();

            // Candle Data
            const candleData = result.timestamps.map((time, index) => ({
                time: time,
                open: result.open[index],
                high: result.high[index],
                low: result.low[index],
                close: result.close[index],
            }));
            this.candleSeries.setData(candleData);

            // Clear previous Fibonacci lines
            this.fibonacciSeries.forEach(series => this.chart.removeSeries(series));
            this.fibonacciSeries = [];

            // Plot Trailing Stop
            const trailingStopData = result.trailing_stop.map((value, index) => ({
                time: result.timestamps[index],
                value: value
            }));
            this.trailingStopSeries.setData(trailingStopData);

            // Plot Extremum
            const extremumData = result.extremum.map((value, index) => ({
                time: result.timestamps[index],
                value: value
            }));
            this.extremumSeries.setData(extremumData);

            // Plot Trend Line
            const trendData = result.trend.map((value, index) => ({
                time: result.timestamps[index],
                value: value
            }));
            this.trendLineSeries.setData(trendData);

            // Plot Fibonacci Levels
            result.fibonacci_levels.forEach((level, index) => {
                const fibLine = this.chart.addLineSeries({
                    color: index === 0 ? '#000000' : '#808080',
                    lineWidth: 1,
                    lineStyle: LineStyle.Dotted,
                    title: `Fibonacci Level ${index + 1}`,
                });
                this.fibonacciSeries.push(fibLine);
                
                fibLine.setData([
                    { time: result.timestamps[0], value: level },
                    { time: result.timestamps[result.timestamps.length - 1], value: level }
                ]);
            });

            // Plot Indicators
            this.rsiSeries.setData(
                result.timestamps.map((time, index) => ({
                    time: time,
                    value: result.rsi[index]
                }))
            );

            this.stochasticKSeries.setData(
                result.timestamps.map((time, index) => ({
                    time: time,
                    value: result.stochastic.k[index]
                }))
            );

            this.stochasticDSeries.setData(
                result.timestamps.map((time, index) => ({
                    time: time,
                    value: result.stochastic.d[index]
                }))
            );

            this.macdLineSeries.setData(
                result.timestamps.map((time, index) => ({
                    time: time,
                    value: result.macd.line[index]
                }))
            );

            this.macdSignalSeries.setData(
                result.timestamps.map((time, index) => ({
                    time: time,
                    value: result.macd.signal[index]
                }))
            );

            this.macdHistogramSeries.setData(
                result.timestamps.map((time, index) => ({
                    time: time,
                    value: result.macd.histogram[index],
                    color: result.macd.histogram[index] > 0 ? '#4CAF50' : '#F44336'
                }))
            );

            // Fit content
            this.chart.timeScale().fitContent();

            // Optional: Log Fibonacci Entry Signals
            console.log('Fibonacci Entry Signals:', result.fibonacci_entry_signals);

        } catch (error) {
            console.error('Error updating chart:', error);
        }
    }

    public resize(width: number, height: number): void {
        this.chart.resize(width, height);
    }

    public remove(): void {
        this.chart.remove();
    }
}