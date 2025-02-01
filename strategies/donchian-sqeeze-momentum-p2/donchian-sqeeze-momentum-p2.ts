import { createChart, IChartApi, ISeriesApi, LineStyle } from 'lightweight-charts';

interface StrategyResult {
    close: number[];
    timestamps: number[];
    vf: number[];
    zscore: number[];
    squeeze_value: number[];
    squeeze_value_ma: number[];
    hypersqueeze: boolean[];
    bullish_divergence: boolean[];
    bearish_divergence: boolean[];
    underlying_momentum_bullish: boolean[];
    underlying_momentum_bearish: boolean[];
    swing_momentum_bullish: boolean[];
    swing_momentum_bearish: boolean[];
    normal_squeeze: boolean[];
    visualization: {
        colors: {
            up: string;
            down: string;
        }
    }
}

export class DonchianSqueezeMomentumP2Chart {
    private chart: IChartApi;
    private vfSeries: ISeriesApi<'Line'>;
    private zscoreSeries: ISeriesApi<'Line'>;
    private squeezeValueSeries: ISeriesApi<'Line'>;
    private bullishDivergenceSeries: ISeriesApi<'Line'>;
    private bearishDivergenceSeries: ISeriesApi<'Line'>;
    private underlyingMomentumBullishSeries: ISeriesApi<'Line'>;
    private underlyingMomentumBearishSeries: ISeriesApi<'Line'>;
    private swingMomentumBullishSeries: ISeriesApi<'Line'>;
    private swingMomentumBearishSeries: ISeriesApi<'Line'>;
    private normalSqueezeSeries: ISeriesApi<'Line'>;

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

        // VF Series
        this.vfSeries = this.chart.addLineSeries({
            color: '#2196F3',
            lineWidth: 2,
            title: 'Momentum Oscillator',
        });

        // Z-Score Series
        this.zscoreSeries = this.chart.addLineSeries({
            color: '#FF9800',
            lineWidth: 2,
            title: 'Z-Score',
        });

        // Squeeze Value Series
        this.squeezeValueSeries = this.chart.addLineSeries({
            color: '#9C27B0',
            lineWidth: 2,
            title: 'Squeeze Value',
        });

        // Divergence Series
        this.bullishDivergenceSeries = this.chart.addLineSeries({
            color: '#4CAF50',
            lineWidth: 2,
            title: 'Bullish Divergence',
            lineStyle: LineStyle.Dotted,
        });

        this.bearishDivergenceSeries = this.chart.addLineSeries({
            color: '#F44336',
            lineWidth: 2,
            title: 'Bearish Divergence',
            lineStyle: LineStyle.Dotted,
        });

        // Momentum Series
        this.underlyingMomentumBullishSeries = this.chart.addLineSeries({
            color: '#00FF00',
            lineWidth: 2,
            title: 'Underlying Momentum Bullish',
            lineStyle: LineStyle.Dotted,
        });

        this.underlyingMomentumBearishSeries = this.chart.addLineSeries({
            color: '#FF0000',
            lineWidth: 2,
            title: 'Underlying Momentum Bearish',
            lineStyle: LineStyle.Dotted,
        });

        this.swingMomentumBullishSeries = this.chart.addLineSeries({
            color: '#00FFFF',
            lineWidth: 2,
            title: 'Swing Momentum Bullish',
            lineStyle: LineStyle.Dotted,
        });

        this.swingMomentumBearishSeries = this.chart.addLineSeries({
            color: '#FF00FF',
            lineWidth: 2,
            title: 'Swing Momentum Bearish',
            lineStyle: LineStyle.Dotted,
        });

        this.normalSqueezeSeries = this.chart.addLineSeries({
            color: '#FFA500',
            lineWidth: 2,
            title: 'Normal Squeeze',
            lineStyle: LineStyle.Dotted,
        });
    }

    public async updateChart(symbol: string, timeframe: string): Promise<void> {
        try {
            const response = await fetch(`/api/donchian-sqeeze-momentum-p2?symbol=${symbol}&timeframe=${timeframe}`);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const result: StrategyResult = await response.json();

            // Update VF Series
            const vfData = result.vf.map((value, index) => ({
                time: result.timestamps[index],
                value: value,
            }));
            this.vfSeries.setData(vfData);

            // Update Z-Score Series
            const zscoreData = result.zscore.map((value, index) => ({
                time: result.timestamps[index],
                value: value,
            }));
            this.zscoreSeries.setData(zscoreData);

            // Update Squeeze Value Series
            const squeezeValueData = result.squeeze_value.map((value, index) => ({
                time: result.timestamps[index],
                value: value,
            }));
            this.squeezeValueSeries.setData(squeezeValueData);

            // Update Bullish Divergence Series
            const bullishDivergenceData = result.bullish_divergence
                .map((isDivergence, index) => 
                    isDivergence ? { 
                        time: result.timestamps[index], 
                        value: result.zscore[index] 
                    } : null
                )
                .filter(point => point !== null);
            this.bullishDivergenceSeries.setData(bullishDivergenceData);

            // Update Bearish Divergence Series
            const bearishDivergenceData = result.bearish_divergence
                .map((isDivergence, index) => 
                    isDivergence ? { 
                        time: result.timestamps[index], 
                        value: result.zscore[index] 
                    } : null
                )
                .filter(point => point !== null);
            this.bearishDivergenceSeries.setData(bearishDivergenceData);

            // Update Underlying Momentum Bullish Series
            const underlyingMomentumBullishData = result.underlying_momentum_bullish
                .map((isBullish, index) => 
                    isBullish ? { 
                        time: result.timestamps[index], 
                        value: result.vf[index] 
                    } : null
                )
                .filter(point => point !== null);
            this.underlyingMomentumBullishSeries.setData(underlyingMomentumBullishData);

            // Update Underlying Momentum Bearish Series
            const underlyingMomentumBearishData = result.underlying_momentum_bearish
                .map((isBearish, index) => 
                    isBearish ? { 
                        time: result.timestamps[index], 
                        value: result.vf[index] 
                    } : null
                )
                .filter(point => point !== null);
            this.underlyingMomentumBearishSeries.setData(underlyingMomentumBearishData);

            // Update Swing Momentum Bullish Series
            const swingMomentumBullishData = result.swing_momentum_bullish
                .map((isBullish, index) => 
                    isBullish ? { 
                        time: result.timestamps[index], 
                        value: result.zscore[index] 
                    } : null
                )
                .filter(point => point !== null);
            this.swingMomentumBullishSeries.setData(swingMomentumBullishData);

            // Update Swing Momentum Bearish Series
            const swingMomentumBearishData = result.swing_momentum_bearish
                .map((isBearish, index) => 
                    isBearish ? { 
                        time: result.timestamps[index], 
                        value: result.zscore[index] 
                    } : null
                )
                .filter(point => point !== null);
            this.swingMomentumBearishSeries.setData(swingMomentumBearishData);

            // Update Normal Squeeze Series
            const normalSqueezeData = result.normal_squeeze
                .map((isNormalSqueeze, index) => 
                    isNormalSqueeze ? { 
                        time: result.timestamps[index], 
                        value: result.squeeze_value[index] 
                    } : null
                )
                .filter(point => point !== null);
            this.normalSqueezeSeries.setData(normalSqueezeData);

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