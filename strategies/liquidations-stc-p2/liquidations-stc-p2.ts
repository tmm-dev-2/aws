import { IChartApi, createChart, LineStyle } from 'lightweight-charts';

declare global {
	interface Window {
		eel: {
			calculate_stc: (data: { close: number[], high: number[], low: number[] }, 
						  params: STCParams) => Promise<{
				stcValue: number[];
				macdValue: number[];
				crossovers: Array<{ position: number, type: string }>;
				histogram_colors: string[];
			}>;
		}
	}
}

interface PythonFunctions {
	calculateSTC: (data: { close: number[], high: number[], low: number[] }, params: STCParams) => Promise<{
		stcValue: number[];
		macdValue: number[];
		crossovers: Array<{ position: number, type: string }>;
		histogram_colors: string[];
	}>;
}

interface STCParams {
	length: number;
	stcLength: number;
	smoothingFactor: number;
	fastLength: number;
	slowLength: number;
	upColor: string;
	downColor: string;
}

interface CandleData {
	time: number;
	open: number;
	high: number;
	low: number;
	close: number;
}

export class LiquidationsSTCP2 {
	private params: STCParams;
	private chart: IChartApi | null = null;
	private stcSeries: any | null = null;
	private macdHistogram: any | null = null;
	private pythonFunctions: PythonFunctions | null = null;
	private isCalculating: boolean = false;

	constructor(params: Partial<STCParams> = {}) {
		this.params = {
			length: 55,
			stcLength: 12,
			smoothingFactor: 0.45,
			fastLength: 26,
			slowLength: 50,
			upColor: '#6f6f6f',
			downColor: '#ff0000',
			...params
		};
		this.setPythonFunctions();
	}

	public setPythonFunctions(): void {
		if (typeof window !== 'undefined' && window.eel) {
			this.pythonFunctions = {
				calculateSTC: async (data, params) => {
					try {
						// Call the Python function directly without the bridge
						const result = await window.eel.calculate_stc(data, params)();
						if (!result) {
							throw new Error('Failed to get result from Python');
						}
						return result;
					} catch (error) {
						console.error('Error calling Python function:', error);
						throw error;
					}
				}
			};
		} else {
			console.error('Eel is not initialized');
		}
	}

	public initializeChart(container: HTMLElement): void {
		this.chart = createChart(container, {
			layout: {
				background: { color: '#131722' },
				textColor: '#d1d4dc',
			},
			grid: {
				vertLines: { color: '#1e222d' },
				horzLines: { color: '#1e222d' },
			},
			width: container.clientWidth,
			height: 300
		});

		// Create STC line series
		this.stcSeries = this.chart.addLineSeries({
			color: this.params.upColor,
			lineWidth: 2,
		});

		// Create MACD histogram series
		this.macdHistogram = this.chart.addHistogramSeries({
			color: this.params.upColor,
			priceFormat: { type: 'volume' },
		});

		// Add horizontal lines
		[-60, -25, 0, 25, 60].forEach(level => {
			this.chart.addLineSeries({
				color: 'gray',
				lineWidth: 1,
				lineStyle: LineStyle.Dotted,
			}).setData([{ time: 0, value: level }]);
		});
	}

	public async updateChart(data: CandleData[]): Promise<void> {
		if (!this.stcSeries || !this.macdHistogram || !this.pythonFunctions) {
			console.error('Chart components not initialized');
			return;
		}

		try {
			this.isCalculating = true;
			const results = await this.pythonFunctions.calculateSTC({
				close: data.map(d => d.close),
				high: data.map(d => d.high),
				low: data.map(d => d.low)
			}, this.params);

			// Update STC line with error checking
			const stcData = data.map((candle, i) => ({
				time: candle.time,
				value: results.stcValue[i] ?? 0,
				color: (results.stcValue[i] ?? 0) > (results.stcValue[i-1] ?? 0) ? 
					this.params.upColor : this.params.downColor
			}));

			// Update MACD histogram with error checking
			const macdData = data.map((candle, i) => ({
				time: candle.time,
				value: results.macdValue[i] ?? 0,
				color: results.histogram_colors[i] ?? this.params.downColor
			}));

			this.stcSeries.setData(stcData);
			this.macdHistogram.setData(macdData);
		} catch (error) {
			console.error('Error updating chart:', error);
		} finally {
			this.isCalculating = false;
		}
	}
}
