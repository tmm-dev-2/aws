import { createChart, LineStyle } from 'lightweight-charts';

interface StrategyResult {
	average: number[];
	timestamps: number[];
	volatile: boolean[];
	muted: boolean[];
	visualization: {
		colors: {
			up: string;
			down: string;
			neutral: string;
		};
	};
}

export class RSIVolatilityBandsChart {
	private chart: any;
	private averageSeries: any;
	private zeroLine: any;

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

		// Initialize average series
		this.averageSeries = this.chart.addLineSeries({
			title: 'Average Volatility',
			color: '#2196F3',
			lineWidth: 2,
			priceFormat: {
				type: 'custom',
				minMove: 0.1,
				formatter: (price: number) => price.toFixed(1),
			},
		});

		// Initialize zero line
		this.zeroLine = this.chart.addLineSeries({
			title: 'Zero Line',
			color: '#9E9E9E',
			lineWidth: 1,
			lineStyle: LineStyle.Dashed,
		});
	}

	public async updateChart(symbol: string, timeframe: string): Promise<void> {
		try {
			const response = await fetch(`/api/rsi-volatility-bands-p2?symbol=${symbol}&timeframe=${timeframe}`);
			if (!response.ok) {
				throw new Error('Failed to fetch data');
			}
			const result: StrategyResult = await response.json();
			
			// Prepare average series data with colors
			const averageData = result.average.map((value, index) => {
				const color = value > 0 ? 
					(value > (result.average[index - 1] || 0) ? result.visualization.colors.up : result.visualization.colors.down) :
					result.visualization.colors.neutral;
				
				return {
					time: result.timestamps[index] as number,
					value: value,
					color: color,
				};
			});

			// Update series
			this.averageSeries.setData(averageData);

			// Set zero line
			const timeRange = {
				from: Math.min(...result.timestamps),
				to: Math.max(...result.timestamps),
			};

			this.zeroLine.setData([
				{ time: timeRange.from, value: 0 },
				{ time: timeRange.to, value: 0 },
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