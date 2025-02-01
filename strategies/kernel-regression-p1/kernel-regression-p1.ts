import { createChart, LineStyle } from 'lightweight-charts';

interface StrategyResult {
	wave: number[];
	upper_band1: number[];
	lower_band1: number[];
	upper_band2: number[];
	lower_band2: number[];
	mid_line: number[];
	trend_up: boolean[];
	trend_down: boolean[];
	timestamps: number[];
}

class KernelRegressionCalculator {
    private bandwidth = 45;
    private width = 2.0;
    private sd_lookback = 150;
    private sd_mult = 3.0;
    private min_wave_change = 0.001;
    private signal_smoothing = 3;

    constructor(bandwidth: number = 45, width: number = 2.0, sd_lookback: number = 150, sd_mult: number = 3.0, min_wave_change: number = 0.001, signal_smoothing: number = 3) {
        this.bandwidth = bandwidth;
        this.width = width;
        this.sd_lookback = sd_lookback;
        this.sd_mult = sd_mult;
        this.min_wave_change = min_wave_change;
        this.signal_smoothing = signal_smoothing;
    }

    private gaussianKernel(x: number[]): number[] {
        return x.map(val => Math.exp(-0.5 * val ** 2) / Math.sqrt(2 * Math.PI));
    }

    private epanechnikovKernel(x: number[]): number[] {
        return x.map(val => Math.abs(val) <= 1 ? 3 / 4 * (1 - val ** 2) : 0);
    }

    private logisticKernel(x: number[]): number[] {
        return x.map(val => 1 / (Math.exp(val) + 2 + Math.exp(-val)));
    }

    private waveKernel(x: number[]): number[] {
        return x.map(val => Math.abs(val) <= 1 ? (1 - val ** 2) * Math.sin(1 / (1 - val ** 2)) : 0);
    }

    private kernelRegression(data: number[], kernelType: string): number[] {
        const n = data.length;
        const yPred = new Array(n).fill(0);

        for (let i = 0; i < n; i++) {
            let weights = new Array(n).fill(0);
            for (let j = 0; j < n; j++) {
                const x = (i - j) / this.bandwidth;
                if (kernelType === 'Epanechnikov') {
                    weights[j] = this.epanechnikovKernel([x])[0];
                } else if (kernelType === 'Logistic') {
                    weights[j] = this.logisticKernel([x])[0];
                } else if (kernelType === 'Gaussian') {
                    weights[j] = this.gaussianKernel([x])[0];
                } else {
                    weights[j] = this.waveKernel([x])[0];
                }
            }
            const sumWeights = weights.reduce((a, b) => a + b, 0);
            weights = weights.map(w => w / sumWeights);
            yPred[i] = weights.reduce((acc, w, k) => acc + w * data[k], 0);
        }
        return yPred;
    }

    private calculateWave(data: number[]): number[] {
        const scaledData = data.map(val => val * this.width);
        return this.kernelRegression(scaledData, 'Wave');
    }

    private calculateStdBands(data: number[], lookback: number, multiplier: number): [number[], number[], number[]] {
        const series = data;
        const rollingMean = series.map((_, i) => {
            if (i < lookback - 1) return NaN;
            let sum = 0;
            for (let j = i - lookback + 1; j <= i; j++) {
                sum += series[j];
            }
            return sum / lookback;
        });
        const rollingStd = series.map((_, i) => {
            if (i < lookback - 1) return NaN;
            let sum = 0;
            const mean = rollingMean[i];
            for (let j = i - lookback + 1; j <= i; j++) {
                sum += (series[j] - mean) ** 2;
            }
            return Math.sqrt(sum / lookback);
        });

        const upperBand = rollingMean.map((mean, i) => mean + rollingStd[i] * multiplier);
        const lowerBand = rollingMean.map((mean, i) => mean - rollingStd[i] * multiplier);

        return [rollingMean.filter(x => !isNaN(x)), upperBand.filter(x => !isNaN(x)), lowerBand.filter(x => !isNaN(x))];
    }

    private calculateMomentum(wave: number[]): number[] {
        const momentum = new Array(wave.length).fill(0);
        for (let i = 1; i < wave.length; i++) {
            momentum[i] = wave[i] - wave[i - 1];
        }
        return momentum;
    }

    private calculateVolatility(data: number[]): number[] {
        const series = data;
        return series.map((_, i) => {
            if (i < this.sd_lookback - 1) return NaN;
            let sum = 0;
            for (let j = i - this.sd_lookback + 1; j <= i; j++) {
                sum += (series[j] - this.calculateStdBands(data, this.sd_lookback, this.sd_mult)[0][i - this.sd_lookback + 1]) ** 2;
            }
            return Math.sqrt(sum / this.sd_lookback);
        }).filter(x => !isNaN(x));
    }

    public calculateStrategy(data: { close: number[], high: number[], low: number[], time: number[] }): StrategyResult {
        const closes = data.close;
        const highs = data.high;
        const lows = data.low;
        const timestamps = data.time;

        const wave = this.calculateWave(closes);
        const epSignal = this.kernelRegression(closes, 'Epanechnikov');
        const logSignal = this.kernelRegression(closes, 'Logistic');
        const waveSignal = this.kernelRegression(closes, 'Wave');
        const gaussSignal = this.kernelRegression(closes, 'Gaussian');

        const avgSignal = closes.map((close, i) => (epSignal[i] + logSignal[i] + waveSignal[i] + gaussSignal[i]) / 4 + close);

        const momentum = this.calculateMomentum(wave);
        const volatility = this.calculateVolatility(closes);

        const [mid, upper1, lower1] = this.calculateStdBands(avgSignal, this.sd_lookback, this.sd_mult / 2);
        const [, upper2, lower2] = this.calculateStdBands(avgSignal, this.sd_lookback, this.sd_mult);

        const trendUp = new Array(wave.length).fill(false);
        const trendDown = new Array(wave.length).fill(false);

        for (let i = 2; i < wave.length; i++) {
            trendUp[i] = (wave[i] > wave[i - 1] &&
                !(wave[i - 1] > wave[i - 2]) &&
                momentum[i] > this.min_wave_change);
            trendDown[i] = (wave[i] < wave[i - 1] &&
                !(wave[i - 1] < wave[i - 2]) &&
                momentum[i] < -this.min_wave_change);
        }

        return {
            wave: wave,
            upper_band1: upper1,
            lower_band1: lower1,
            upper_band2: upper2,
            lower_band2: lower2,
            mid_line: mid,
            trend_up: trendUp,
            trend_down: trendDown,
            timestamps: timestamps.slice(this.sd_lookback - 1)
        };
    }
}


export class KernelRegressionChart {
	private chart: any;
	private waveSeries: any;
	private upperBand1: any;
	private lowerBand1: any;
	private upperBand2: any;
	private lowerBand2: any;
	private midLine: any;
	private markers: any;
    private calculator: KernelRegressionCalculator;

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

		this.waveSeries = this.chart.addLineSeries({
			title: 'Wave Signal',
			color: '#2196F3',
			lineWidth: 2,
		});

		this.upperBand1 = this.chart.addLineSeries({
			title: 'Upper Band 1',
			color: '#FF4081',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});

		this.lowerBand1 = this.chart.addLineSeries({
			title: 'Lower Band 1',
			color: '#00E676',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});

		this.upperBand2 = this.chart.addLineSeries({
			title: 'Upper Band 2',
			color: '#FF4081',
			lineWidth: 1,
		});

		this.lowerBand2 = this.chart.addLineSeries({
			title: 'Lower Band 2',
			color: '#00E676',
			lineWidth: 1,
		});

		this.midLine = this.chart.addLineSeries({
			title: 'Mid Line',
			color: '#9E9E9E',
			lineWidth: 1,
			lineStyle: LineStyle.Dashed,
		});
        this.calculator = new KernelRegressionCalculator();
	}

	public async updateChart(symbol: string, timeframe: string): Promise<void> {
		try {
            const response = await fetch(`/api/fetch_candles?symbol=${symbol}&timeframe=${timeframe}`);
            if (!response.ok) {
                throw new Error('Failed to fetch candle data');
            }
            const candleData = await response.json();
            const data = {
                close: candleData.map((candle: any) => candle.close),
                high: candleData.map((candle: any) => candle.high),
                low: candleData.map((candle: any) => candle.low),
                time: candleData.map((candle: any) => candle.time),
            };
            const result = this.calculator.calculateStrategy(data);


			const seriesData = result.wave.map((value, index) => ({
				time: result.timestamps[index] as number,
				value: value,
			}));

			const upperBand1Data = result.upper_band1.map((value, index) => ({
				time: result.timestamps[index] as number,
				value: value,
			}));

			const lowerBand1Data = result.lower_band1.map((value, index) => ({
				time: result.timestamps[index] as number,
				value: value,
			}));

			const upperBand2Data = result.upper_band2.map((value, index) => ({
				time: result.timestamps[index] as number,
				value: value,
			}));

			const lowerBand2Data = result.lower_band2.map((value, index) => ({
				time: result.timestamps[index] as number,
				value: value,
			}));

			const midLineData = result.mid_line.map((value, index) => ({
				time: result.timestamps[index] as number,
				value: value,
			}));

			this.waveSeries.setData(seriesData);
			this.upperBand1.setData(upperBand1Data);
			this.lowerBand1.setData(lowerBand1Data);
			this.upperBand2.setData(upperBand2Data);
			this.lowerBand2.setData(lowerBand2Data);
			this.midLine.setData(midLineData);

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