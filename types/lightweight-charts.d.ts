declare module 'lightweight-charts' {
  export type Time = number | string;
  export type ColorType = string;
  export type LineStyle = number;

  export interface ChartOptions {
    layout?: {
      background?: {
        type?: string;
        color?: string;
      };
      textColor?: string;
    };
    grid?: {
      vertLines?: { color?: string };
      horzLines?: { color?: string };
    };
    width?: number;
    height?: number;
    rightPriceScale?: {
      borderColor?: string;
      scaleMargins?: {
        top?: number;
        bottom?: number;
      };
      autoScale?: boolean;
    };
    timeScale?: {
      borderColor?: string;
      timeVisible?: boolean;
      secondsVisible?: boolean;
      rightOffset?: number;
      barSpacing?: number;
      fixLeftEdge?: boolean;
      fixRightEdge?: boolean;
      lockVisibleTimeRangeOnResize?: boolean;
      minBarSpacing?: number;
    };
  }

  export interface SeriesOptions {
    upColor?: string;
    downColor?: string;
    borderVisible?: boolean;
    wickUpColor?: string;
    wickDownColor?: string;
    color?: string;
    lineWidth?: number;
    title?: string;
    lineStyle?: LineStyle;
    topColor?: string;
    bottomColor?: string;
    lineColor?: string;
    priceFormat?: {
      type?: 'price' | 'volume' | 'custom';
      precision?: number;
      minMove?: number;
      formatter?: (price: number) => string;
    };
  }

  export interface SeriesMarker<T> {
    time: T;
    position: 'aboveBar' | 'belowBar';
    color: string;
    shape: 'arrowUp' | 'arrowDown' | 'circle' | 'xcross';
    text?: string;
    size?: number;
  }

  export interface ISeriesApi<T extends SeriesType> {
    setData(data: T extends 'Area' 
      ? Array<{ time: Time; value: number; bottomValue?: number }> 
      : Array<{ time: Time; value: number; color?: string }>
    ): void;
    setMarkers(markers: SeriesMarker<Time>[]): void;
  }

  export interface ITimeScaleApi {
    fitContent(): void;
    setVisibleRange(range: { from: number; to: number }): void;
  }

  export interface IChartApi {
    applyOptions(options: ChartOptions): void;
    resize(width: number, height: number): void;
    remove(): void;
    timeScale(): ITimeScaleApi;
    addMarkers(markers: SeriesMarker<Time>[]): void;
    addLineSeries(options?: SeriesOptions): ISeriesApi<'Line'>;
    addHistogramSeries(options?: SeriesOptions): ISeriesApi<'Histogram'>;
    createCandlestickSeries(options?: SeriesOptions): ISeriesApi<'Candlestick'>;
    addCandlestickSeries(options?: SeriesOptions): ISeriesApi<'Candlestick'>;
    addAreaSeries(options?: SeriesOptions): ISeriesApi<'Area'>;
    removeSeries(series: ISeriesApi<SeriesType>): void;
  }

  export type SeriesType = 'Line' | 'Candlestick' | 'Bar' | 'Area' | 'Histogram';

  export type SeriesOptionsMap = {
    'Line': SeriesOptions;
    'Candlestick': SeriesOptions;
    'Bar': SeriesOptions;
    'Area': SeriesOptions;
    'Histogram': SeriesOptions & {
      priceFormat?: {
        type: 'volume' | 'price';
        precision?: number;
        minMove?: number;
      };
    };
  };

  export const LineStyle: {
    Solid: LineStyle;
    Dotted: LineStyle;
    Dashed: LineStyle;
  };

  export function createChart(container: HTMLElement, options?: ChartOptions): IChartApi;
}