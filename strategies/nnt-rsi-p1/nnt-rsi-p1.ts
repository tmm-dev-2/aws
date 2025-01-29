import { createChart, ColorType, LineStyle } from 'lightweight-charts';

interface NNTRSIData {
	nn_output: number[];
	ha_candles: {
		open: number[];
		high: number[];
		low: number[];
		close: number[];
	};
	upper_band: number[];
	lower_band: number[];
	mean_line: number[];
}

class NNTRSIChart {
	private chart: any;
	private mainSeries: any;
	private upperBandSeries: any;
	private lowerBandSeries: any;
	private meanLineSeries: any;
	private haCandles: any;

	constructor(container: HTMLElement) {
		this.chart = createChart(container, {
			layout: {
				background: { color: '#253248' },
				textColor: '#DDD',
			},
			grid: {
				vertLines: { color: '#334158' },
				horzLines: { color: '#334158' },
			},
			
			rightPriceScale: {
				borderColor: '#485c7b',
			},
			timeScale: {
				borderColor: '#485c7b',
			},
		});

		// Initialize series
		this.initializeSeries();
	}

	private initializeSeries() {
		// Main NNT RSI line
		this.mainSeries = this.chart.addLineSeries({
			color: '#2196F3',
			lineWidth: 2,
			title: 'NNT RSI',
		});

		// Upper band
		this.upperBandSeries = this.chart.addLineSeries({
			color: '#FF4444',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
			title: 'Upper Band',
		});

		// Lower band
		this.lowerBandSeries = this.chart.addLineSeries({
			color: '#4CAF50',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
			title: 'Lower Band',
		});

		// Mean line
		this.meanLineSeries = this.chart.addLineSeries({
			color: '#FFD700',
			lineWidth: 1,
			title: 'Mean Line',
		});

		// Heikin-Ashi candles
		this.haCandles = this.chart.addCandlestickSeries({
			upColor: '#4CAF50',
			downColor: '#FF4444',
			borderVisible: false,
			wickUpColor: '#4CAF50',
			wickDownColor: '#FF4444',
		});
	}

	public updateData(data: NNTRSIData, timestamps: number[]) {
		// Update main NNT RSI line
		const mainData = timestamps.map((time, i) => ({
			time,
			value: data.nn_output[i],
		}));
		this.mainSeries.setData(mainData);

		// Update bands
		const upperBandData = timestamps.map((time, i) => ({
			time,
			value: data.upper_band[i],
		}));
		this.upperBandSeries.setData(upperBandData);

		const lowerBandData = timestamps.map((time, i) => ({
			time,
			value: data.lower_band[i],
		}));
		this.lowerBandSeries.setData(lowerBandData);

		// Update mean line
		const meanLineData = timestamps.map((time, i) => ({
			time,
			value: data.mean_line[i],
		}));
		this.meanLineSeries.setData(meanLineData);

		// Update Heikin-Ashi candles
		const haData = timestamps.map((time, i) => ({
			time,
			open: data.ha_candles.open[i],
			high: data.ha_candles.high[i],
			low: data.ha_candles.low[i],
			close: data.ha_candles.close[i],
		}));
		this.haCandles.setData(haData);
	}

	public resize(width: number, height: number) {
		this.chart.applyOptions({
			width,
			height,
		});
	}
}

// Initialize chart when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
	const container = document.getElementById('chart');
	if (!container) return;

	const chart = new NNTRSIChart(container);

	// Handle window resize
	window.addEventListener('resize', () => {
		chart.resize(container.clientWidth, container.clientHeight);
	});

	// Example of fetching and updating data
	async function updateChart() {
		try {
			// @ts-ignore (eel is injected globally)
			const data = await eel.calculate_indicators({
				open: [], // Add your data here
				high: [], // Add your data here
				low: [],  // Add your data here
				close: [] // Add your data here
			})();

			const timestamps = Array.from(
				{ length: data.nn_output.length },
				(_, i) => Math.floor(Date.now() / 1000) - (data.nn_output.length - i) * 60
			);

			chart.updateData(data, timestamps);
		} catch (error) {
			console.error('Error updating chart:', error);
		}
	}

	// Initial update
	updateChart();

	// Update periodically (e.g., every minute)
	setInterval(updateChart, 60000);
});