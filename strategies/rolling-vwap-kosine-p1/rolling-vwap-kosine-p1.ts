import { createChart, LineStyle } from 'lightweight-charts';

interface StrategyResult {
	vwap: number[];
	upper_band1: number[];
	lower_band1: number[];
	upper_band2: number[];
	lower_band2: number[];
	upper_band3: number[];
	lower_band3: number[];
	buy_signals: boolean[];
	sell_signals: boolean[];
	timestamps: number[];
	visualization: {
		colors: {
			up: string;
			down: string;
			neutral: string;
		};
	};
}

export class RollingVWAPKosineChart {
	private chart: any;
	private vwapSeries: any;
	private upperBand1: any;
	private lowerBand1: any;
	private upperBand2: any;
	private lowerBand2: any;
	private upperBand3: any;
	private lowerBand3: any;
	private markerSeries: any;

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
			width: container.clientWidth,
			height: container.clientHeight,
		});

		// Initialize VWAP line
		this.vwapSeries = this.chart.addLineSeries({
			title: 'VWAP',
			color: '#2196F3',
			lineWidth: 2,
		});

		// Initialize bands
		this.upperBand1 = this.chart.addLineSeries({
			title: 'Upper Band 1',
			color: '#c22ed0',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});

		this.lowerBand1 = this.chart.addLineSeries({
			title: 'Lower Band 1',
			color: '#5ffae0',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});

		// Initialize other bands similarly
		this.upperBand2 = this.chart.addLineSeries({
			title: 'Upper Band 2',
			color: '#c22ed0',
			lineWidth: 1,
			lineStyle: LineStyle.Dashed,
		});

		this.lowerBand2 = this.chart.addLineSeries({
			title: 'Lower Band 2',
			color: '#5ffae0',
			lineWidth: 1,
			lineStyle: LineStyle.Dashed,
		});

		this.upperBand3 = this.chart.addLineSeries({
			title: 'Upper Band 3',
			color: '#c22ed0',
			lineWidth: 1,
		});

		this.lowerBand3 = this.chart.addLineSeries({
			title: 'Lower Band 3',
			color: '#5ffae0',
			lineWidth: 1,
		});

		// Initialize marker series for signals
		this.markerSeries = this.chart.addLineSeries({
			title: 'Signals',
			lineWidth: 0,
		});
	}

	public async updateChart(symbol: string, timeframe: string): Promise<void> {
		try {
			const response = await fetch(`/api/rolling-vwap-kosine-p1?symbol=${symbol}&timeframe=${timeframe}`);
			if (!response.ok) {
				throw new Error('Failed to fetch data');
			}
			const result: StrategyResult = await response.json();

			// Update VWAP
			this.vwapSeries.setData(
				result.vwap.map((value, index) => ({
					time: result.timestamps[index],
					value: value,
				}))
			);

			// Update bands
			this.upperBand1.setData(
				result.upper_band1.map((value, index) => ({
					time: result.timestamps[index],
					value: value,
				}))
			);

			this.lowerBand1.setData(
				result.lower_band1.map((value, index) => ({
					time: result.timestamps[index],
					value: value,
				}))
			);

			// Update other bands similarly
			this.upperBand2.setData(
				result.upper_band2.map((value, index) => ({
					time: result.timestamps[index],
					value: value,
				}))
			);

			this.lowerBand2.setData(
				result.lower_band2.map((value, index) => ({
					time: result.timestamps[index],
					value: value,
				}))
			);

			this.upperBand3.setData(
				result.upper_band3.map((value, index) => ({
					time: result.timestamps[index],
					value: value,
				}))
			);

			this.lowerBand3.setData(
				result.lower_band3.map((value, index) => ({
					time: result.timestamps[index],
					value: value,
				}))
			);

			// Update signals
			const markers = [];
			for (let i = 0; i < result.timestamps.length; i++) {
				if (result.buy_signals[i]) {
					markers.push({
						time: result.timestamps[i],
						position: 'belowBar',
						color: result.visualization.colors.up,
						shape: 'arrowUp',
						text: 'Buy',
					});
				}
				if (result.sell_signals[i]) {
					markers.push({
						time: result.timestamps[i],
						position: 'aboveBar',
						color: result.visualization.colors.down,
						shape: 'arrowDown',
						text: 'Sell',
					});
				}
			}
			this.markerSeries.setMarkers(markers);

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