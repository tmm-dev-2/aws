import { 
    createChart, 
    LineStyle, 
    IChartApi, 
    ISeriesApi, 
    Time 
  } from 'lightweight-charts';

interface StrategyResult {
    out: number[];
    out2: number[];
    fast_trend_up: boolean[];
    fast_trend_down: boolean[];
    slow_trend_up: boolean[];
    slow_trend_down: boolean[];
    indicators: {
        RSI?: number[];
        Stochastic?: number[];
        BBPCT?: number[];
        CMO?: number[];
        CCI?: number[];
        Fisher?: number[];
        VZO?: number[];
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

export class RollingVWAPKosineP2Chart {
    private chart: IChartApi;
    private fastSignalSeries: ISeriesApi<'Line'>;
    private slowSignalSeries: ISeriesApi<'Line'>;
    private zeroLineSeries: ISeriesApi<'Line'>;

    constructor(container: HTMLElement) {
        // Initialize main chart
        this.chart = createChart(container, {
            layout: {
                background: { color: '#131722' },
                textColor: '#d1d4dc',
            },
            grid: {
                vertLines: { color: '#1e222d' },
                horzLines: { color: '#1e222d' },
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

        // Initialize fast signal series
        this.fastSignalSeries = this.chart.addLineSeries({
            color: '#5ffae0',
            lineWidth: 2,
            title: 'Fast Signal',
        });

        // Initialize slow signal series
        this.slowSignalSeries = this.chart.addLineSeries({
            color: '#c22ed0',
            lineWidth: 2,
            title: 'Slow Signal',
            lineStyle: LineStyle.Dashed,
        });

        // Initialize zero line
        this.zeroLineSeries = this.chart.addLineSeries({
            color: '#888888',
            lineWidth: 1,
            lineStyle: LineStyle.Dashed,
            title: 'Zero Line',
        });
    }

    public async updateChart(symbol: string, timeframe: string): Promise<void> {
        try {
            const response = await fetch(`/api/apirolling-vwap-kosine-p2?symbol=${symbol}&timeframe=${timeframe}`);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const result: StrategyResult = await response.json();
            
            // Prepare data for chart
            const fastSignalData = result.out.map((value, index) => ({
                time: result.timestamps[index] as Time,
                value: value,
            }));

            const slowSignalData = result.out2.map((value, index) => ({
                time: result.timestamps[index] as Time,
                value: value,
            }));

            const zeroLineData = [
                { time: result.timestamps[0] as Time, value: 0 },
                { time: result.timestamps[result.timestamps.length - 1] as Time, value: 0 }
            ];

            // Update series
            this.fastSignalSeries.setData(fastSignalData);
            this.slowSignalSeries.setData(slowSignalData);
            this.zeroLineSeries.setData(zeroLineData);

            // Fit content
            this.chart.timeScale().fitContent();

            // Optional: Add trend markers
            this.addTrendMarkers(result);

        } catch (error) {
            console.error('Error updating chart:', error);
        }
    }

    private addTrendMarkers(result: StrategyResult): void {
        // Add markers for fast trend
        const fastTrendMarkers = result.fast_trend_up.reduce((markers, isTrend, index) => {
            if (isTrend) {
                markers.push({
                    time: result.timestamps[index] as Time,
                    position: 'belowBar',
                    color: result.visualization.colors.up,
                    shape: 'arrowUp',
                    text: 'Fast Trend Up'
                });
            }
            return markers;
        }, [] as any[]);

        const fastTrendDownMarkers = result.fast_trend_down.reduce((markers, isTrend, index) => {
            if (isTrend) {
                markers.push({
                    time: result.timestamps[index] as Time,
                    position: 'aboveBar',
                    color: result.visualization.colors.down,
                    shape: 'arrowDown',
                    text: 'Fast Trend Down'
                });
            }
            return markers;
        }, [] as any[]);

        // Add markers for slow trend
        const slowTrendMarkers = result.slow_trend_up.reduce((markers, isTrend, index) => {
            if (isTrend) {
                markers.push({
                    time: result.timestamps[index] as Time,
                    position: 'belowBar',
                    color: result.visualization.colors.up,
                    shape: 'circle',
                    text: 'Slow Trend Up'
                });
            }
            return markers;
        }, [] as any[]);

        const slowTrendDownMarkers = result.slow_trend_down.reduce((markers, isTrend, index) => {
            if (isTrend) {
                markers.push({
                    time: result.timestamps[index] as Time,
                    position: 'aboveBar',
                    color: result.visualization.colors.down,
                    shape: 'circle',
                    text: 'Slow Trend Down'
                });
            }
            return markers;
        }, [] as any[]);

        // Combine and add markers
        const allMarkers = [
            ...fastTrendMarkers, 
            ...fastTrendDownMarkers, 
            ...slowTrendMarkers, 
            ...slowTrendDownMarkers
        ];

        this.chart.addMarkers(allMarkers);
    }

    public resize(width: number, height: number): void {
        this.chart.resize(width, height);
    }

    public remove(): void {
        this.chart.remove();
    }
}