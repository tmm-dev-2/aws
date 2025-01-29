import { createChart, LineStyle, IChartApi, ISeriesApi, Time, ChartOptions, SeriesOptionsMap } from 'lightweight-charts';

interface DiverLine {
    start_price: number;
    end_price: number;
    start_ndx: number;
    end_ndx: number;
    start_indicator: number;
    end_indicator: number;
    is_bull: boolean;
    is_hidden: boolean;
}

interface StrategyResult {
    histogram: number[];
    average: number[];
    average2: number[];
    timestamps: number[];
    pivot_highs: number[];
    pivot_lows: number[];
    divergences: {
        regular_bull: DiverLine[];
        regular_bear: DiverLine[];
        hidden_bull: DiverLine[];
        hidden_bear: DiverLine[];
    };
    tp_signals: Array<{
        type: 'buy' | 'sell';
        index: number;
        value: number;
    }>;
    status_scores: number[];
    visualization: {
        colors: {
            up: string;
            down: string;
            neutral: string;
        };
    };
}

export class DoubleHullTurboChart {
    private chart: IChartApi;
    private histogramSeries: ISeriesApi<'Histogram'>;
    private averageSeries: ISeriesApi<'Line'>;
    private average2Series: ISeriesApi<'Line'>;
    private divergenceSeries: {
        regular_bull: ISeriesApi<'Line'>;
        regular_bear: ISeriesApi<'Line'>;
        hidden_bull: ISeriesApi<'Line'>;
        hidden_bear: ISeriesApi<'Line'>;
    };
    private zeroLine: ISeriesApi<'Line'>;
    private statusLineSeries: ISeriesApi<'Line'>;

    constructor(container: HTMLElement) {
        // Initialize main chart with PineScript-like styling
        const chartOptions: ChartOptions = {
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
                scaleMargins: {
                    top: 0.3,
                    bottom: 0.3,
                },
                autoScale: true,
            },
            timeScale: {
                borderColor: '#d1d4dc',
                timeVisible: true,
            },
            width: container.clientWidth,
            height: container.clientHeight,
        };

        this.chart = createChart(container, chartOptions);

        // Histogram series (matching PineScript colors)
        this.histogramSeries = this.chart.addHistogramSeries({
            color: '#6de6f693',
            priceFormat: {
                type: 'volume',
            },
        });

        // Zero line for histogram
        this.zeroLine = this.chart.addLineSeries({
            color: '#9E9E9E',
            lineStyle: LineStyle.Dashed,
            lineWidth: 1,
        });

        // Average series (main signal line)
        this.averageSeries = this.chart.addLineSeries({
            color: '#2196F3',
            lineWidth: 2,
            priceFormat: {
                type: 'price',
                precision: 2,
                minMove: 0.01,
            },
        });

        // Average2 series (secondary smoothed line)
        this.average2Series = this.chart.addLineSeries({
            color: '#da5b52',
            lineWidth: 1,
            lineStyle: LineStyle.Dotted,
        });

        // Divergence series (matching PineScript colors)
        this.divergenceSeries = {
            regular_bull: this.chart.addLineSeries({
                color: 'white',
                lineWidth: 1,
                lineStyle: LineStyle.Solid,
            }),
            regular_bear: this.chart.addLineSeries({
                color: 'white',
                lineWidth: 1,
                lineStyle: LineStyle.Solid,
            }),
            hidden_bull: this.chart.addLineSeries({
                color: '#24baab',
                lineWidth: 1,
                lineStyle: LineStyle.Dotted,
            }),
            hidden_bear: this.chart.addLineSeries({
                color: '#f77b73',
                lineWidth: 1,
                lineStyle: LineStyle.Dotted,
            }),
        };

        // Status line series
        this.statusLineSeries = this.chart.addLineSeries({
            color: '#da5b52',
            lineWidth: 2,
        });
    }

    public async updateChart(symbol: string, timeframe: string): Promise<void> {
        try {
            const response = await fetch(`/api/double-hull-turbo-p2?symbol=${symbol}&timeframe=${timeframe}`);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const result: StrategyResult = await response.json();
            
            // Histogram data
            const histogramData = result.histogram.map((value, index) => ({
                time: result.timestamps[index] as Time,
                value: value,
                color: value >= 0 ? result.visualization.colors.up : result.visualization.colors.down,
            }));

            // Zero line data
            const zeroLineData = [
                { time: result.timestamps[0] as Time, value: 0 },
                { time: result.timestamps[result.timestamps.length - 1] as Time, value: 0 }
            ];

            // Average series data
            const averageData = result.average.map((value, index) => ({
                time: result.timestamps[index] as Time,
                value: value,
            }));

            // Average2 series data
            const average2Data = result.average2.map((value, index) => ({
                time: result.timestamps[index] as Time,
                value: value,
            }));

            // Divergence lines
            const plotDivergenceLine = (lines: DiverLine[], series: ISeriesApi<'Line'>) => {
                const divergenceData = lines.flatMap(div => [
                    { time: result.timestamps[div.start_ndx] as Time, value: div.start_price },
                    { time: result.timestamps[div.end_ndx] as Time, value: div.end_price }
                ]);
                series.setData(divergenceData);
            };

            // Plot divergence lines
            plotDivergenceLine(result.divergences.regular_bull, this.divergenceSeries.regular_bull);
            plotDivergenceLine(result.divergences.regular_bear, this.divergenceSeries.regular_bear);
            plotDivergenceLine(result.divergences.hidden_bull, this.divergenceSeries.hidden_bull);
            plotDivergenceLine(result.divergences.hidden_bear, this.divergenceSeries.hidden_bear);

            // Take profit signals as markers
const markers = result.tp_signals.map(signal => ({
    time: result.timestamps[signal.index] as Time,
    position: signal.type === 'buy' ? 'belowBar' : 'aboveBar' as 'belowBar' | 'aboveBar',
    color: signal.type === 'buy' ? '#4CAF50' : '#F44336',
    shape: signal.type === 'buy' ? 'arrowUp' : 'arrowDown' as 'arrowUp' | 'arrowDown',
    text: signal.type.toUpperCase(),
    size: 2,
}));
            // Status line data
            const statusLineData = result.status_scores.map((score, index) => ({
                time: result.timestamps[index] as Time,
                value: score === 3 ? 100 : score === 2 ? 50 : score === 1 ? 25 : 0,
            }));


            // Update series
            this.histogramSeries.setData(histogramData);
            this.zeroLine.setData(zeroLineData);
            this.averageSeries.setData(averageData);
            this.averageSeries.setMarkers(markers);
            this.average2Series.setData(average2Data);
            this.statusLineSeries.setData(statusLineData);

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