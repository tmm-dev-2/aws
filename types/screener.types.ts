export interface ScreenerCondition {
  id: string;
  type: 'technical' | 'price' | 'volume' | 'custom';
  indicator: string;
  operator: string;
  value: number;
  timeframe?: string;
  parameter?: number; // For indicators like SMA(20), RSI(14)
}

export interface IndicatorGroup {
  name: string;
  indicators: {
    [key: string]: {
      name: string;
      parameters?: number[];
      operators: string[];
      defaultValue?: number;
    };
  };
}
