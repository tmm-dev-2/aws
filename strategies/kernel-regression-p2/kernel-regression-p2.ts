import { createChart, LineStyle } from 'lightweight-charts';

interface StrategyResult {
	regression: number[];
	upper_band: number[];
	lower_band: number[];
	trend: number[];
	timestamps: number[];
	visualization: {
		colors: {
			regression: string;
			upper_band: string;
			lower_band: string;
			up_trend: string;
			down_trend: string;
		};
	};
}

export class KernelRegressionChart {
	private chart: any;
	private regressionSeries: any;
	private upperBandSeries: any;
	private lowerBandSeries: any;

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

		// Initialize regression line series
		this.regressionSeries = this.chart.addLineSeries({
			title: 'Kernel Regression',
			color: '#2196F3',
			lineWidth: 2,
		});

		// Initialize upper band series
		this.upperBandSeries = this.chart.addLineSeries({
			title: 'Upper Band',
			color: '#4CAF50',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});

		// Initialize lower band series
		this.lowerBandSeries = this.chart.addLineSeries({
			title: 'Lower Band',
			color: '#F44336',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});
	}

	public async updateChart(symbol: string, timeframe: string): Promise<void> {
		try {
			const response = await fetch(`/api/api-kernel-regression-p2?symbol=${symbol}&timeframe=${timeframe}`);
			if (!response.ok) {
				throw new Error('Failed to fetch data');
			}
			const result: StrategyResult = await response.json();

			// Prepare series data
			const regressionData = result.regression.map((value, index) => ({
				time: result.timestamps[index] as number,
				value: value,
				color: result.trend[index] > 0 ? result.visualization.colors.up_trend : result.visualization.colors.down_trend,
			}));

			const upperBandData = result.upper_band.map((value, index) => ({
				time: result.timestamps[index] as number,
				value: value,
			}));

			const lowerBandData = result.lower_band.map((value, index) => ({
				time: result.timestamps[index] as number,
				value: value,
			}));

			// Update series
			this.regressionSeries.setData(regressionData);
			this.upperBandSeries.setData(upperBandData);
			this.lowerBandSeries.setData(lowerBandData);

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