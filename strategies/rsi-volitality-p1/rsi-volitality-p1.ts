import { LineStyle, LineStyleType } from 'lightweight-charts';

interface StrategyResult {
    rsi: number[];
    volatility: number[];
    vol_sma: number[];
    long_signals: boolean[];
    short_signals: boolean[];
    timestamps: number[];
    visualization: {
        colors: {
            rsi_line: string;
            overbought_line: string;
            oversold_line: string;
            vol_high: string;
            vol_normal: string;
            signal_long: string;
            signal_short: string;
        };
        line_widths: {
            rsi_line: number;
            level_lines: number;
            vol_line: number;
        };
    };
}

export class RSIVolatilityChart {
    private chart: any;
    private rsiSeries: any;
    private volatilitySeries: any;
    private volSmaSeries: any;
    private signalMarkers: any;
    private overboughtLine: any;
    private oversoldLine: any;

    constructor(container: HTMLElement) {
        // Initialize main chart
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

        // Initialize RSI series
        this.rsiSeries = this.chart.addLineSeries({
            title: 'RSI',
            color: '#2196F3',
            lineWidth: 2,
            priceFormat: {
                type: 'custom',
                minMove: 0.1,
                formatter: (price: number) => price.toFixed(1),
            },
        });

        // Initialize Volatility series
        this.volatilitySeries = this.chart.addLineSeries({
            title: 'Volatility',
            color: '#FF9800',
            lineWidth: 2,
            priceFormat: {
                type: 'custom',
                minMove: 0.0001,
                formatter: (price: number) => price.toFixed(4),
            },
        });

        // Initialize Volatility SMA series
        this.volSmaSeries = this.chart.addLineSeries({
            title: 'Vol SMA',
            color: '#9E9E9E',
            lineWidth: 1,
            lineStyle: LineStyle.Dotted,
            priceFormat: {
                type: 'custom',
                minMove: 0.0001,
                formatter: (price: number) => price.toFixed(4),
            },
        });

        // Initialize signal markers series
        this.signalMarkers = this.chart.addLineSeries({
            title: 'Signals',
            lineVisible: false,
            lastValueVisible: false,
            priceFormat: {
                type: 'custom',
                minMove: 0.1,
                formatter: (price: number) => price.toFixed(1),
            },
        });

        // Initialize overbought and oversold lines
        this.overboughtLine = this.chart.addLineSeries({
            title: 'Overbought',
            color: '#FF5252',
            lineWidth: 1,
            lineStyle: LineStyle.Dashed,
        });

        this.oversoldLine = this.chart.addLineSeries({
            title: 'Oversold',
            color: '#4CAF50',
            lineWidth: 1,
            lineStyle: LineStyle.Dashed,
        });
    }

    public async updateChart(symbol: string, timeframe: string): Promise<void> {
        try {
            // Use Next.js API route
            const response = await fetch(`/api/rsi-volatility?symbol=${symbol}&timeframe=${timeframe}`);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const result: StrategyResult = await response.json();
            
            // Prepare data series
            const rsiData = result.rsi.map((value, index) => ({
                time: result.timestamps[index] as number,
                value: value,
            }));

            const volatilityData = result.volatility.map((value, index) => ({
                time: result.timestamps[index] as number,
                value: value,
            }));

            const volSmaData = result.vol_sma.map((value, index) => ({
                time: result.timestamps[index] as number,
                value: value,
            }));

            // Prepare signal markers
            const markers = result.timestamps.map((time, index) => {
                if (result.long_signals[index] || result.short_signals[index]) {
                    return {
                        time: time as number,
                        position: result.long_signals[index] ? 'belowBar' : 'aboveBar',
                        color: result.long_signals[index] ? 
                            result.visualization.colors.signal_long : 
                            result.visualization.colors.signal_short,
                        shape: result.long_signals[index] ? 'arrowUp' : 'arrowDown',
                        text: result.long_signals[index] ? 'BUY' : 'SELL',
                    };
                }
                return null;
            }).filter(marker => marker !== null);

            // Update all series
            this.rsiSeries.setData(rsiData);
            this.volatilitySeries.setData(volatilityData);
            this.volSmaSeries.setData(volSmaData);
            this.signalMarkers.setMarkers(markers);

            // Set overbought and oversold lines
            const timeRange = {
                from: Math.min(...result.timestamps),
                to: Math.max(...result.timestamps),
            };

            this.overboughtLine.setData([
                { time: timeRange.from, value: 70 },
                { time: timeRange.to, value: 70 },
            ]);

            this.oversoldLine.setData([
                { time: timeRange.from, value: 30 },
                { time: timeRange.to, value: 30 },
            ]);

            // Fit content
            this.chart.timeScale().fitContent();

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