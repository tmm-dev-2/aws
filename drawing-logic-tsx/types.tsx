export interface Point {
	x: number;
	y: number;
}

export interface AdjustmentPoint {
	x: number;
	y: number;
	type: string;
}

export interface DrawingSettings {
	lineThickness: number;
	color: string;
	backgroundColor: string;
	transparency: number;
}