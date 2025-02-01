import { Point, DrawingSettings } from './types';

export class Brush {
	private points: Point[] = [];
	private settings: DrawingSettings;

	constructor(settings: DrawingSettings) {
		this.settings = settings;
	}

	addPoint(point: Point): void {
		this.points.push(point);
	}

	draw(context: CanvasRenderingContext2D): void {
		if (this.points.length > 1) {
			context.beginPath();
			context.strokeStyle = this.settings.color;
			context.lineWidth = this.settings.lineThickness;
			context.moveTo(this.points[0].x, this.points[0].y);
			
			for (let i = 1; i < this.points.length; i++) {
				context.lineTo(this.points[i].x, this.points[i].y);
			}
			
			context.stroke();
		}
	}
}

export class Highlighter extends Brush {
	draw(context: CanvasRenderingContext2D): void {
		if (this.points.length > 1) {
			context.beginPath();
			context.globalAlpha = this.settings.transparency;
			context.strokeStyle = this.settings.color;
			context.lineWidth = this.settings.lineThickness;
			context.moveTo(this.points[0].x, this.points[0].y);
			
			for (let i = 1; i < this.points.length; i++) {
				context.lineTo(this.points[i].x, this.points[i].y);
			}
			
			context.stroke();
			context.globalAlpha = 1.0;
		}
	}
}

export class Brushes {
	private brushes: Map<string, Brush> = new Map();
	private currentBrush: Brush | null = null;
	private currentHighlighter: Highlighter | null = null;

	createBrush(settings: DrawingSettings): void {
		const brush = new Brush(settings);
		this.brushes.set('brush', brush);
		this.currentBrush = brush;
	}

	createHighlighter(settings: DrawingSettings): void {
		const highlighter = new Highlighter(settings);
		this.brushes.set('highlighter', highlighter);
		this.currentHighlighter = highlighter;
	}

	addPoint(point: Point): void {
		if (this.currentBrush) {
			this.currentBrush.addPoint(point);
		}
		if (this.currentHighlighter) {
			this.currentHighlighter.addPoint(point);
		}
	}

	draw(context: CanvasRenderingContext2D): void {
		if (this.currentBrush) {
			this.currentBrush.draw(context);
		}
		if (this.currentHighlighter) {
			this.currentHighlighter.draw(context);
		}
	}

	clearPoints(): void {
		this.currentBrush = null;
		this.currentHighlighter = null;
		this.brushes.clear();
	}
}