import { createChart, LineStyle } from 'lightweight-charts';

interface CandleData {
	time: number;
	open: number;
	high: number;
	low: number;
	close: number;
	volume?: number;
}

interface Level {
	price: number;
	grade: number;
	breaks: number;
	bar_index: number;
}

interface StrategyResult {
	support_levels: Level[];
	resistance_levels: Level[];
	sma_values: Record<string, number[]>;
	bb_values: Record<string, {upper: number[], lower: number[]}>;
	timestamps: number[];
	candles: {
		open: number[];
		high: number[];
		low: number[];
		close: number[];
		volume: number[];
		time: number[];
	};
	visualization: {
		colors: {
			up: string;
			down: string;
			neutral: string;
		};
	};
}

export class SupportResistanceChart {
	private chart: any;
	private candleSeries: any;
	private supportLines: any[] = [];
	private resistanceLines: any[] = [];
	private smaLines: any[] = [];
	private bbLines: any[] = [];

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

		this.candleSeries = this.chart.addCandlestickSeries({
			upColor: '#26a69a',
			downColor: '#ef5350',
			borderVisible: false,
			wickUpColor: '#26a69a',
			wickDownColor: '#ef5350',
		});
	}

	private createSupportResistanceLine(price: number, color: string, grade: number): any {
		return this.chart.addLineSeries({
			color: color,
			lineWidth: 2,
			lineStyle: LineStyle.Dashed,
			priceLineVisible: false,
			lastValueVisible: false,
			crosshairMarkerVisible: false,
			autoscaleInfoProvider: () => ({
				priceRange: {
					minValue: price - 1,
					maxValue: price + 1,
				},
			}),
		});
	}

	public async updateChart(symbol: string, timeframe: string): Promise<void> {
		try {
			const response = await fetch(`/api/support-resistance-blackflag-p1?symbol=${symbol}&timeframe=${timeframe}`);
			if (!response.ok) {
				throw new Error('Failed to fetch data');
			}
			const result: StrategyResult = await response.json();

			// Transform candle data to the format expected by lightweight-charts
			const candleData: CandleData[] = result.candles.time.map((time, i) => ({
				time: time,
				open: result.candles.open[i],
				high: result.candles.high[i],
				low: result.candles.low[i],
				close: result.candles.close[i],
				volume: result.candles.volume[i]
			}));

			// Update candlestick series
			this.candleSeries.setData(candleData);

			// Clear existing lines
			this.supportLines.forEach(line => this.chart.removeSeries(line));
			this.resistanceLines.forEach(line => this.chart.removeSeries(line));
			this.smaLines.forEach(line => this.chart.removeSeries(line));
			this.bbLines.forEach(line => this.chart.removeSeries(line));

			// Plot support levels
			result.support_levels.forEach(level => {
				const line = this.createSupportResistanceLine(
					level.price,
					result.visualization.colors.up,
					level.grade
				);
				this.supportLines.push(line);
				line.setData([
					{ time: result.candles.time[0], value: level.price },
					{ time: result.candles.time[result.candles.time.length - 1], value: level.price },
				]);
			});

			// Plot resistance levels
			result.resistance_levels.forEach(level => {
				const line = this.createSupportResistanceLine(
					level.price,
					result.visualization.colors.down,
					level.grade
				);
				this.resistanceLines.push(line);
				line.setData([
					{ time: result.candles.time[0], value: level.price },
					{ time: result.candles.time[result.candles.time.length - 1], value: level.price },
				]);
			});

			// Plot SMAs and Bollinger Bands
			Object.entries(result.sma_values).forEach(([key, values]) => {
				const smaLine = this.chart.addLineSeries({
					color: '#2196F3',
					lineWidth: 1,
					title: `SMA ${key}`,
				});
				this.smaLines.push(smaLine);
				smaLine.setData(
					values.map((value, i) => ({
						time: result.candles.time[i],
						value: value,
					}))
				);
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