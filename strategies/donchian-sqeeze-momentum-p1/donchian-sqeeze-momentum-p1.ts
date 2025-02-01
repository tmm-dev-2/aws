import { createChart, LineStyle, IChartApi, ISeriesApi, SeriesMarker, Time } from 'lightweight-charts';

interface StrategyResult {
	basis: number[];
	upper: number[];
	lower: number[];
	upper_vol: number[];
	lower_vol: number[];
	upper_inner: number[];
	lower_inner: number[];
	fu: number[];
	fl: number[];
	strong_long: number[];
	strong_short: number[];
	weak_long: number[];
	weak_short: number[];
	trend: number[];
	bullish_shift: number[];
	bearish_shift: number[];
	timestamps: number[];
	visualization: {
		colors: {
			up: string;
			down: string;
			neutral: string;
			basis_up: string;
			basis_down: string;
			cloud_up: string;
			cloud_down: string;
			cloud_neutral: string;
		};
		styles: {
			basis: { lineWidth: number };
			bands: { lineWidth: number; style: string };
			volatility: { lineWidth: number; style: string };
			signals: { size: string };
		};
	};
}

export class DonchianSqueezeMomentumChart {
	private chart: IChartApi;
	private candlestickSeries: ISeriesApi<"Candlestick">;
	private basisSeries: ISeriesApi<"Line">;
	private upperSeries: ISeriesApi<"Line">;
	private lowerSeries: ISeriesApi<"Line">;
	private upperVolSeries: ISeriesApi<"Line">;
	private lowerVolSeries: ISeriesApi<"Line">;
	private upperInnerSeries: ISeriesApi<"Line">;
	private lowerInnerSeries: ISeriesApi<"Line">;
	private fuSeries: ISeriesApi<"Line">;
	private flSeries: ISeriesApi<"Line">;
	private markerSeries: ISeriesApi<"Line">;

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
				scaleMargins: {
					top: 0.1,
					bottom: 0.1,
				},
			},
			timeScale: {
				borderColor: '#d1d4dc',
				timeVisible: true,
			
			},
		});

		// Initialize all series
		this.candlestickSeries = this.chart.createCandlestickSeries({
			upColor: '#26a69a',
			downColor: '#ef5350',
			borderVisible: false,
			wickUpColor: '#26a69a',
			wickDownColor: '#ef5350',
		});

		this.basisSeries = this.chart.addLineSeries({
			title: 'Basis',
			color: '#2196F3',
			lineWidth: 2,
		});

		this.upperSeries = this.chart.addLineSeries({
			title: 'Upper Band',
			color: '#FF4081',
			lineWidth: 1,
			lineStyle: LineStyle.Dashed,
		});

		this.lowerSeries = this.chart.addLineSeries({
			title: 'Lower Band',
			color: '#FF4081',
			lineWidth: 1,
			lineStyle: LineStyle.Dashed,
		});

		this.upperVolSeries = this.chart.addLineSeries({
			title: 'Upper Volatility',
			color: '#9C27B0',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});

		this.lowerVolSeries = this.chart.addLineSeries({
			title: 'Lower Volatility',
			color: '#9C27B0',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});

		this.upperInnerSeries = this.chart.addLineSeries({
			title: 'Upper Inner',
			color: '#7B1FA2',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});

		this.lowerInnerSeries = this.chart.addLineSeries({
			title: 'Lower Inner',
			color: '#7B1FA2',
			lineWidth: 1,
			lineStyle: LineStyle.Dotted,
		});

		this.fuSeries = this.chart.addLineSeries({
			title: 'FU Line',
			color: '#4CAF50',
			lineWidth: 1,
		});

		this.flSeries = this.chart.addLineSeries({
			title: 'FL Line',
			color: '#F44336',
			lineWidth: 1,
		});

		this.markerSeries = this.chart.addLineSeries({
			title: 'Signals',
			lineWidth: 0,
		});
	}

	public async updateChart(symbol: string, timeframe: string): Promise<void> {
		try {
			const response = await fetch(`/api/donchian-sqeeze-momentum-p1?symbol=${symbol}&timeframe=${timeframe}`);
			if (!response.ok) {
				throw new Error('Failed to fetch data');
			}
			const result: StrategyResult = await response.json();

			// Update all series
			const seriesData = this.prepareSeriesData(result);
			
			// Set data for each series
			this.basisSeries.setData(seriesData.basis);
			this.upperSeries.setData(seriesData.upper);
			this.lowerSeries.setData(seriesData.lower);
			this.upperVolSeries.setData(seriesData.upperVol);
			this.lowerVolSeries.setData(seriesData.lowerVol);
			this.upperInnerSeries.setData(seriesData.upperInner);
			this.lowerInnerSeries.setData(seriesData.lowerInner);
			this.fuSeries.setData(seriesData.fu);
			this.flSeries.setData(seriesData.fl);

			// Set markers for signals
			this.markerSeries.setMarkers(this.prepareMarkers(result));

			// Fit content
			this.chart.timeScale().fitContent();

		} catch (error) {
			console.error('Error updating chart:', error);
		}
	}

	private prepareSeriesData(result: StrategyResult) {
		const mapToTimeValue = (values: number[]) => 
			values.map((value, index) => ({
				time: result.timestamps[index],
				value: value,
			}));

		return {
			basis: mapToTimeValue(result.basis),
			upper: mapToTimeValue(result.upper),
			lower: mapToTimeValue(result.lower),
			upperVol: mapToTimeValue(result.upper_vol),
			lowerVol: mapToTimeValue(result.lower_vol),
			upperInner: mapToTimeValue(result.upper_inner),
			lowerInner: mapToTimeValue(result.lower_inner),
			fu: mapToTimeValue(result.fu),
			fl: mapToTimeValue(result.fl),
		};
	}

	private prepareMarkers(result: StrategyResult): SeriesMarker<Time>[] {
		const markers: SeriesMarker<Time>[] = [];

		for (let i = 0; i < result.timestamps.length; i++) {
			if (result.strong_long[i]) {
				markers.push({
					time: result.timestamps[i],
					position: 'belowBar',
					color: result.visualization.colors.up,
					shape: 'arrowUp',
					text: 'Strong Long',
				});
			} else if (result.strong_short[i]) {
				markers.push({
					time: result.timestamps[i],
					position: 'aboveBar',
					color: result.visualization.colors.down,
					shape: 'arrowDown',
					text: 'Strong Short',
				});
			} else if (result.weak_long[i]) {
				markers.push({
					time: result.timestamps[i],
					position: 'belowBar',
					color: result.visualization.colors.neutral,
					shape: 'circle',
					text: 'Weak Long',
				});
			} else if (result.weak_short[i]) {
				markers.push({
					time: result.timestamps[i],
					position: 'aboveBar',
					color: result.visualization.colors.neutral,
					shape: 'circle',
					text: 'Weak Short',
				});
			}
		}

		return markers;
	}

	public resize(width: number, height: number): void {
		this.chart.resize(width, height);
	}

	public remove(): void {
		this.chart.remove();
	}
}