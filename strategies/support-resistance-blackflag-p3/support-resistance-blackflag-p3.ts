import { createChart, LineStyle } from 'lightweight-charts';

interface StrategyResult {
    open: number[];
    high: number[];
    low: number[];
    close: number[];
    volume: number[];
    mfi: number[];
    clusters: {
        overbought: number;
        neutral: number;
        oversold: number;
    };
    position_between_bands: number[];
    val: number[];
    standard_deviation: number;
    trend: string;
    timestamps: number[];
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
    atr: number[];
    volatility: number[];
    is_volatile: boolean[];
    trend_strength: number[];
    trend_reversal_signal: boolean;
    visualization: {
        colors: {
            up: string;
            down: string;
            neutral: string;
        };
    };
}

export class SupportResistanceBlackflagP3Chart {
    private chart: any;
    private mfiSeries: any;
    private neutralLine: any;
    private overboughtLine: any;
    private oversoldLine: any;
    private rsiSeries: any;
    private macdSeries: any;
    private volatilitySeries: any;

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

        // MFI Series
        this.mfiSeries = this.chart.addLineSeries({
            color: '#2196F3',
            lineWidth: 2,
            title: 'MFI',
        });

        // Horizontal Lines
        this.neutralLine = this.chart.addLineSeries({
            color: '#808080',
            lineWidth: 1,
            lineStyle: LineStyle.Dashed,
            title: 'Neutral Line',
        });

        this.overboughtLine = this.chart.addLineSeries({
            color: '#FF0000',
            lineWidth: 1,
            lineStyle: LineStyle.Dashed,
            title: 'Overbought Line',
        });

        this.oversoldLine = this.chart.addLineSeries({
            color: '#00FF00',
            lineWidth: 1,
            lineStyle: LineStyle.Dashed,
            title: 'Oversold Line',
        });

        // Additional Indicator Series
        this.rsiSeries = this.chart.addLineSeries({
            color: '#FF9800',
            lineWidth: 1,
            title: 'RSI',
        });

        this.macdSeries = this.chart.addLineSeries({
            color: '#9C27B0',
            lineWidth: 1,
            title: 'MACD',
        });

        this.volatilitySeries = this.chart.addLineSeries({
            color: '#795548',
            lineWidth: 1,
            title: 'Volatility',
        });
    }

    public async updateChart(symbol: string, timeframe: string): Promise<void> {
        try {
            const response = await fetch(`/api/support-resistance-blackflag-p3?symbol=${symbol}&timeframe=${timeframe}`);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const result: StrategyResult = await response.json();

            // Update MFI series
            const mfiData = result.mfi.map((value, index) => ({
                time: result.timestamps[index],
                value: value,
            }));
            this.mfiSeries.setData(mfiData);

            // Update horizontal lines
            const timeRange = {
                from: result.timestamps[0],
                to: result.timestamps[result.timestamps.length - 1],
            };

            this.neutralLine.setData([
                { time: timeRange.from, value: result.clusters.neutral },
                { time: timeRange.to, value: result.clusters.neutral },
            ]);

            this.overboughtLine.setData([
                { time: timeRange.from, value: result.clusters.overbought },
                { time: timeRange.to, value: result.clusters.overbought },
            ]);

            this.oversoldLine.setData([
                { time: timeRange.from, value: result.clusters.oversold },
                { time: timeRange.to, value: result.clusters.oversold },
            ]);

            // Update RSI series
            const rsiData = result.rsi.map((value, index) => ({
                time: result.timestamps[index],
                value: value,
            }));
            this.rsiSeries.setData(rsiData);

            // Update MACD series
            const macdData = result.macd.line.map((value, index) => ({
                time: result.timestamps[index],
                value: value,
            }));
            this.macdSeries.setData(macdData);

            // Update Volatility series
            const volatilityData = result.volatility.map((value, index) => ({
                time: result.timestamps[index],
                value: value,
            }));
            this.volatilitySeries.setData(volatilityData);

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