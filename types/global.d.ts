// Global type declarations
declare global {
    interface CandleData {
        timestamp: number;
        open: number;
        high: number;
        low: number;
        close: number;
        volume: number;
    }

    interface Window {
        // Add any window-specific types here if needed
    }
}

export {};