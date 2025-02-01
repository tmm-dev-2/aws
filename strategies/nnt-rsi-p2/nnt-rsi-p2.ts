import { createChart } from 'lightweight-charts';

interface ChartData {
	time: number;
	value: number;
}

export const plotNNTRSIP2 = async (
	container: HTMLElement,
	symbol: string,
	timeframe: string
) => {
	try {
		// Fetch data from API
		const response = await fetch(`/api/api-nnt-rsi-p2?symbol=${symbol}&timeframe=${timeframe}`);
		if (!response.ok) {
			throw new Error('Failed to fetch data');
		}
		const indicators = await response.json();

		// Create chart
		const chart = createChart(container, {
			width: container.clientWidth,
			height: 500,
			layout: {
				background: { type: 'solid', color: '#131722' },
				textColor: '#d1d4dc',
			},
			grid: {
				vertLines: { color: '#1e222d' },
				horzLines: { color: '#1e222d' },
			}
		});

		// Add EMA lines
		const ema1Series = chart.addLineSeries({
			color: '#00ffbb',
			lineWidth: 2,
			title: 'EMA1'
		});
		const ema2Series = chart.addLineSeries({
			color: '#ff1100',
			lineWidth: 2,
			title: 'EMA2'
		});
		const ema3Series = chart.addLineSeries({
			color: '#ffbb00',
			lineWidth: 2,
			title: 'EMA3'
		});

		// Convert indicators to chart data format
		const emaData1: ChartData[] = indicators.ema1.map((value: number, index: number) => ({
			time: indicators.timestamps[index],
			value: value
		}));
		const emaData2: ChartData[] = indicators.ema2.map((value: number, index: number) => ({
			time: indicators.timestamps[index],
			value: value
		}));
		const emaData3: ChartData[] = indicators.ema3.map((value: number, index: number) => ({
			time: indicators.timestamps[index],
			value: value
		}));

		// Set EMA data
		ema1Series.setData(emaData1);
		ema2Series.setData(emaData2);
		ema3Series.setData(emaData3);

		// Add markers for signals
		const markers = indicators.timestamps.map((time: number, index: number) => {
			if (indicators.long_signals[index]) {
				return {
					time: time,
					position: 'belowBar',
					color: '#00ffbb',
					shape: 'arrowUp',
					text: 'LONG'
				};
			}
			if (indicators.short_signals[index]) {
				return {
					time: time,
					position: 'aboveBar',
					color: '#ff1100',
					shape: 'arrowDown',
					text: 'SHORT'
				};
			}
			return null;
		}).filter(marker => marker !== null);

		// Add markers to the chart
		const markersSeries = chart.addLineSeries({
			lineVisible: false,
			lastValueVisible: false,
		});
		markersSeries.setMarkers(markers);

		// Handle window resize
		window.addEventListener('resize', () => {
			chart.resize(container.clientWidth, 500);
		});

		return chart;
	} catch (error) {
		console.error('Error plotting chart:', error);
		throw error;
	}
};
