export interface MarketData {
    open: number[];
    high: number[];
    low: number[];
    close: number[];
    volume: number[];
    timestamp: string[];
}

export interface SegmentData {
    country: string;
    segment: string;
    exchanges: string[];
    data: Record<string, MarketData>;
}

export declare function fetchSegmentData(country: string, segment: string, timeframe: string): Promise<SegmentData>;
export declare function getCurrentSegmentData(): SegmentData | null;
export declare function screenSegmentData(formula: string): Promise<string[]>;
