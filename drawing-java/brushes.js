class Brush {
    constructor(settings) {
        this.points = [];
        this.settings = settings;
    }

    addPoint(point) {
        this.points.push(point);
    }

    draw(context) {
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

class Highlighter extends Brush {
    draw(context) {
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

class Brushes {
    constructor() {
        this.brushes = new Map();
        this.currentBrush = null;
        this.currentHighlighter = null;
    }

    createBrush(settings) {
        const brush = new Brush(settings);
        this.brushes.set('brush', brush);
        this.currentBrush = brush;
    }

    createHighlighter(settings) {
        const highlighter = new Highlighter(settings);
        this.brushes.set('highlighter', highlighter);
        this.currentHighlighter = highlighter;
    }

    addPoint(point) {
        if (this.currentBrush) {
            this.currentBrush.addPoint(point);
        }
        if (this.currentHighlighter) {
            this.currentHighlighter.addPoint(point);
        }
    }

    draw(context) {
        if (this.currentBrush) {
            this.currentBrush.draw(context);
        }
        if (this.currentHighlighter) {
            this.currentHighlighter.draw(context);
        }
    }

    clearPoints() {
        this.currentBrush = null;
        this.currentHighlighter = null;
        this.brushes.clear();
    }
}

export { Brush, Highlighter, Brushes };
