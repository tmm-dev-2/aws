import { IChartApi, LineStyle, ColorType } from 'lightweight-charts';

interface StrategyResult {
    hma1: number[];
    hma2: number[];
    crossover: number[];
    crossunder: number[];
    index: number[];
    valley_formation: boolean[];
    candle_direction: number[];
    candle_length: number[];
    box_data: Array<{
        time_index: number;
        high: number;
        low: number;
        color: string;
        transparency: number;
        extend: string;
    }>;
    timestamps: number[];
    visualization: {
        colors: {
            hma1_up: string;
            hma1_down: string;
            hma2_up: string;
            hma2_down: string;
        };
        transparency: number;
        box_color: string;
    };
    hma1Conditions: number[];
    hma2Conditions: number[];
}

export class DoubleHullTurboP1Chart {
    private chart: IChartApi;
    private hma1Series: any;
    private hma2Series: any;
    private indexSeries: any;
    private boxSeries: any;

    constructor(chart: IChartApi) {
        if (!chart) {
            throw new Error('Chart instance is required');
        }
        
        this.chart = chart;
        this.initializeSeries();
    }

    private initializeSeries(): void {
        // Initialize series after chart is created
        this.hma1Series = this.chart.addLineSeries({
            title: 'HMA1',
            color: '#2196F3',
            lineWidth: 2,
            priceFormat: {
                type: 'price',
                precision: 5,
                minMove: 0.00001,
            },
        });

        // Initialize HMA2 series
        this.hma2Series = this.chart.addLineSeries({
            title: 'HMA2',
            color: '#FF9800',
            lineWidth: 2,
            priceFormat: {
                type: 'price',
                precision: 5,
                minMove: 0.00001,
            },
        });

        // Initialize Index series
        this.indexSeries = this.chart.addLineSeries({
            title: 'Index',
            color: '#4CAF50',
            lineWidth: 1,
            priceFormat: {
                type: 'price',
                precision: 2,
                minMove: 0.01,
            },
        });

        // Initialize Box series for valley formations
        this.boxSeries = this.chart.addCandlestickSeries({
            upColor: 'transparent',
            downColor: 'transparent',
            borderVisible: true,
            
        });
    }


    private calculateWMA(data: number[], length: number): number[] {
        const weights = Array.from({length: length}, (_, i: number) => i + 1);
        const wma = new Array(data.length).fill(0);
        const weightSum = weights.reduce((a: number, b: number) => a + b, 0);
        
        for (let i = length - 1; i < data.length; i++) {
            const window = data.slice(i - length + 1, i + 1);
            wma[i] = weights.reduce((sum: number, weight: number, idx: number) => sum + weight * window[idx], 0) / weightSum;
        }
        
        return wma;
    }

    private calculateHMA(data: number[], length: number): number[] {
        const halfLength = Math.floor(length / 2);
        const sqrtLength = Math.floor(Math.sqrt(length));
        
        const wmaHalf = this.calculateWMA(data, halfLength);
        const wmaFull = this.calculateWMA(data, length);
        
        const wmaf = wmaHalf.map((value: number, i: number) => 2 * value - (wmaFull[i] || 0));
        return this.calculateWMA(wmaf, sqrtLength);
    }

    private calculateFirstDerivative(data: number[], length: number): number[] {
        const derivative = new Array(data.length).fill(0);
        const sma = this.calculateSMA(data, length);
        
        for (let i = 1; i < data.length; i++) {
            derivative[i] = sma[i] - sma[i-1];
        }
        
        return derivative;
    }

    private calculateSMA(data: number[], length: number): number[] {
        const sma = new Array(data.length).fill(0);
        let sum = 0;
        
        for (let i = 0; i < data.length; i++) {
            sum += data[i];
            if (i >= length) {
                sum -= data[i - length];
            }
            sma[i] = i < length - 1 ? 0 : sum / length;
        }
        
        return sma;
    }

    private checkDerivativeConditions(data: number[], length: number): number[] {
        const derivative = this.calculateFirstDerivative(data, length);
        return derivative.map(value => value > 0 ? 1 : value < 0 ? -1 : 0);
    }

    private calculatePVINVI(closes: number[], volumes: number[]): [number[], number[]] {
        const pvi = new Array(closes.length).fill(1000);
        const nvi = new Array(closes.length).fill(1000);
        
        for (let i = 1; i < closes.length; i++) {
            const priceChange = (closes[i] - closes[i-1]) / closes[i-1];
            if (volumes[i] > volumes[i-1]) {
                pvi[i] = pvi[i-1] * (1 + priceChange);
                nvi[i] = nvi[i-1];
            } else {
                nvi[i] = nvi[i-1] * (1 + priceChange);
                pvi[i] = pvi[i-1];
            }
        }
        
        return [pvi, nvi];
    }

    private calculateRSI(data: number[], period: number): number[] {
        const rsi = new Array(data.length).fill(0);
        const gains = new Array(data.length).fill(0);
        const losses = new Array(data.length).fill(0);
        
        // Calculate gains and losses
        for (let i = 1; i < data.length; i++) {
            const diff = data[i] - data[i-1];
            gains[i] = diff > 0 ? diff : 0;
            losses[i] = diff < 0 ? -diff : 0;
        }
        
        // Calculate average gains and losses
        let avgGain = gains.slice(1, period + 1).reduce((a, b) => a + b) / period;
        let avgLoss = losses.slice(1, period + 1).reduce((a, b) => a + b) / period;
        
        rsi[period] = 100 - (100 / (1 + avgGain / avgLoss));
        
        // Calculate RSI
        for (let i = period + 1; i < data.length; i++) {
            avgGain = (avgGain * (period - 1) + gains[i]) / period;
            avgLoss = (avgLoss * (period - 1) + losses[i]) / period;
            rsi[i] = 100 - (100 / (1 + avgGain / avgLoss));
        }
        
        return rsi;
    }

    private calculateBoxData(highs: number[], lows: number[], valleyFormation: boolean[]): Array<{
        time_index: number;
        high: number;
        low: number;
        color: string;
        transparency: number;
        extend: string;
    }> {
        const boxData: Array<{
            time_index: number;
            high: number;
            low: number;
            color: string;
            transparency: number;
            extend: string;
        }> = [];
        
        for (let i = 0; i < highs.length; i++) {
            if (valleyFormation[i]) {
                const lookback = Math.max(0, i - 20);
                const localHigh = Math.max(...highs.slice(lookback, i + 1));
                const localLow = Math.min(...lows.slice(lookback, i + 1));
                
                boxData.push({
                    time_index: i,
                    high: localHigh,
                    low: localLow,
                    color: '#00FFB3',
                    transparency: 99,
                    extend: 'both'
                });
            }
        }
        
        return boxData;
    }

    private calculateStrategy(data: {
        close: number[];
        open: number[];
        high: number[];
        low: number[];
        volume: number[];
        time: number[];
    }): StrategyResult {
        const length1 = 20;
        const length2 = 198;
        const indexPeriod = 25;
        const volumeFlowPeriod = 14;
        const normalizationPeriod = 500;
        
        const closes = data.close;
        const opens = data.open;
        const highs = data.high;
        const lows = data.low;
        const volumes = data.volume;
        
        // Calculate HMAs with derivatives
        const hma1 = this.calculateHMA(closes, length1);
        const hma2 = this.calculateHMA(closes, length2);
        const hma1Conditions = this.checkDerivativeConditions(hma1, 1);
        const hma2Conditions = this.checkDerivativeConditions(hma2, 1);
        
        // Calculate PVI and NVI
        const [pvi, nvi] = this.calculatePVINVI(closes, volumes);
        const pviEma = this.calculateEMA(pvi, 255);
        const nviEma = this.calculateEMA(nvi, 255);
        
        // Calculate money flow indicators
        const dumb = pvi.map((value, i) => value - pviEma[i]);
        const smart = nvi.map((value, i) => value - nviEma[i]);
        const drsi = this.calculateRSI(dumb, volumeFlowPeriod);
        const srsi = this.calculateRSI(smart, volumeFlowPeriod);
        
        // Calculate ratio and index
        const ratio = srsi.map((value, i) => drsi[i] !== 0 ? value / drsi[i] : 0);
        const sums = this.calculateSMA(ratio, indexPeriod);
        const peak = this.calculateRollingMax(sums, normalizationPeriod);
        const index = sums.map((value, i) => peak[i] !== 0 ? value / peak[i] : 0);
        
        // Calculate patterns
        const candleDirection = closes.map((value, i) => value > opens[i] ? 1 : -1);
        const candleLength = closes.map((value, i) => Math.abs(value - opens[i]));
        const valleyFormation = hma1.map((value, i) => value > hma2[i]);
        
        // Calculate box data
        const boxData = this.calculateBoxData(highs, lows, valleyFormation);
        
        // Detect crossovers
        const crossover = new Array(closes.length).fill(0);
        const crossunder = new Array(closes.length).fill(0);
        
        for (let i = 1; i < closes.length; i++) {
            if (hma1[i] > hma2[i] && hma1[i-1] <= hma2[i-1] && hma1Conditions[i] > 0) {
                crossover[i] = 1;
            }
            if (hma1[i] < hma2[i] && hma1[i-1] >= hma2[i-1] && hma1Conditions[i] < 0) {
                crossunder[i] = 1;
            }
        }
        
        return {
            hma1,
            hma2,
            crossover,
            crossunder,
            index,
            valley_formation: valleyFormation,
            candle_direction: candleDirection,
            candle_length: candleLength,
            box_data: boxData,
            timestamps: data.time,
            visualization: {
                colors: {
                    hma1_up: '#00FF00',
                    hma1_down: '#FF0000',
                    hma2_up: '#00FF00',
                    hma2_down: '#FF0000'
                },
                transparency: 99,
                box_color: '#00FFB3'
            },
            hma1Conditions,
            hma2Conditions
        };
    }

    private calculateEMA(data: number[], period: number): number[] {
        const ema = new Array(data.length).fill(0);
        const multiplier = 2 / (period + 1);
        
        ema[0] = data[0];
        for (let i = 1; i < data.length; i++) {
            ema[i] = (data[i] - ema[i-1]) * multiplier + ema[i-1];
        }
        
        return ema;
    }

    private calculateRollingMax(data: number[], period: number): number[] {
        const result = new Array(data.length).fill(0);
        
        for (let i = 0; i < data.length; i++) {
            const start = Math.max(0, i - period + 1);
            result[i] = Math.max(...data.slice(start, i + 1));
        }
        
        return result;
    }

    private async fetchCandleData(symbol: string, timeframe: string): Promise<{
        close: number[];
        open: number[];
        high: number[];
        low: number[];
        volume: number[];
        time: number[];
    }> {
        try {
            const response = await fetch(
                `http://localhost:5000/fetch_candles?symbol=${symbol}&timeframe=${timeframe}`
            );

            if (!response.ok) {
                throw new Error('Failed to fetch candle data');
            }

            const rawData = await response.json();
            const candles = rawData || [];

            return {
                open: candles.map((c: any) => c.open),
                high: candles.map((c: any) => c.high),
                low: candles.map((c: any) => c.low),
                close: candles.map((c: any) => c.close),
                volume: candles.map((c: any) => c.volume),
                time: candles.map((c: any) => c.time)
            };
        } catch (error) {
            console.error('Error fetching candle data:', error);
            throw error;
        }
    }


    public async updateChart(symbol: string, timeframe: string): Promise<void> {
        try {
            const candleData = await this.fetchCandleData(symbol, timeframe);
            const result = this.calculateStrategy(candleData);


            const hma1Data = result.hma1.map((value, index) => ({
                time: result.timestamps[index] as number,
                value: value,
                color: result.hma1Conditions[index] > 0 ? 
                    result.visualization.colors.hma1_up : 
                    result.visualization.colors.hma1_down,
            }));

            // Prepare HMA2 data with colors
            const hma2Data = result.hma2.map((value, index) => ({
                time: result.timestamps[index] as number,
                value: value,
                color: result.hma2Conditions[index] > 0 ? 
                    result.visualization.colors.hma2_up : 
                    result.visualization.colors.hma2_down,
            }));

            // Prepare Index data
            const indexData = result.index.map((value, index) => ({
                time: result.timestamps[index] as number,
                value: value,
            }));

            // Prepare box data for valley formations
            const boxData = result.box_data.map(box => ({
                time: result.timestamps[box.time_index] as number,
                open: box.high,
                high: box.high,
                low: box.low,
                close: box.low,
                borderColor: box.color,
                borderVisible: true,
                wickVisible: false,
            }));

            // Update series
            this.hma1Series.setData(hma1Data);
            this.hma2Series.setData(hma2Data);
            this.indexSeries.setData(indexData);
            this.boxSeries.setData(boxData);

            // Add markers for crossovers and crossunders
            const markers = [];
            for (let i = 0; i < result.crossover.length; i++) {
                if (result.crossover[i]) {
                    markers.push({
                        time: result.timestamps[i],
                        position: 'belowBar',
                        color: '#2196F3',
                        shape: 'arrowUp',
                        text: 'BUY',
                    });
                }
                if (result.crossunder[i]) {
                    markers.push({
                        time: result.timestamps[i],
                    });
                }
            }
            this.hma1Series.setMarkers(markers);

            // Set box series options
            this.boxSeries.applyOptions({
                lastValueVisible: false,
                priceLineVisible: false,
                extendLines: true  // This mimics PineScript's extend.both
            });

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