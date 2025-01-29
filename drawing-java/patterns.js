class XABCDPattern {
    constructor(x, a, b, c, d) {
        this.x = x;
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
        this.adjustmentPointers = this.createAdjustmentPoints();
    }

    createAdjustmentPoints() {
        return [
            { ...this.x, type: 'adjustment' },
            { ...this.a, type: 'adjustment' },
            { ...this.b, type: 'adjustment' },
            { ...this.c, type: 'adjustment' },
            { ...this.d, type: 'adjustment' }
        ];
    }

    isValid() {
        const xa = Math.sqrt((this.a.x - this.x.x) ** 2 + (this.a.y - this.x.y) ** 2);
        const ab = Math.sqrt((this.b.x - this.a.x) ** 2 + (this.b.y - this.a.y) ** 2);
        const bc = Math.sqrt((this.c.x - this.b.x) ** 2 + (this.c.y - this.b.y) ** 2);
        const cd = Math.sqrt((this.d.x - this.c.x) ** 2 + (this.d.y - this.c.y) ** 2);

        const abRetracement = ab / xa;
        if (!(0.382 <= abRetracement && abRetracement <= 0.886)) {
            return false;
        }

        const bcRetracement = bc / ab;
        if (!(0.382 <= bcRetracement && bcRetracement <= 0.886)) {
            return false;
        }

        const cdExtension = cd / bc;
        if (!(1.272 <= cdExtension && cdExtension <= 1.618)) {
            return false;
        }

        return true;
    }
}

class CypherPattern {
    constructor(x, a, b, c, d) {
        this.x = x;
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
        this.adjustmentPointers = this.createAdjustmentPoints();
    }

    createAdjustmentPoints() {
        return [
            { ...this.x, type: 'adjustment' },
            { ...this.a, type: 'adjustment' },
            { ...this.b, type: 'adjustment' },
            { ...this.c, type: 'adjustment' },
            { ...this.d, type: 'adjustment' }
        ];
    }
}

class HeadAndShouldersPattern {
    constructor(leftShoulder, head, rightShoulder, necklineStart, necklineEnd) {
        this.leftShoulder = leftShoulder;
        this.head = head;
        this.rightShoulder = rightShoulder;
        this.necklineStart = necklineStart;
        this.necklineEnd = necklineEnd;
        this.adjustmentPointers = this.createAdjustmentPoints();
    }

    createAdjustmentPoints() {
        return [
            { ...this.leftShoulder, type: 'adjustment' },
            { ...this.head, type: 'adjustment' },
            { ...this.rightShoulder, type: 'adjustment' },
            { ...this.necklineStart, type: 'adjustment' },
            { ...this.necklineEnd, type: 'adjustment' }
        ];
    }
}

class ABCDPattern {
    constructor(a, b, c, d) {
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
        this.adjustmentPointers = this.createAdjustmentPoints();
    }

    createAdjustmentPoints() {
        return [
            { ...this.a, type: 'adjustment' },
            { ...this.b, type: 'adjustment' },
            { ...this.c, type: 'adjustment' },
            { ...this.d, type: 'adjustment' }
        ];
    }
}

class TrianglePattern {
    constructor(start, top, bottom) {
        this.start = start;
        this.top = top;
        this.bottom = bottom;
        this.adjustmentPointers = this.createAdjustmentPoints();
    }

    createAdjustmentPoints() {
        return [
            { ...this.start, type: 'adjustment' },
            { ...this.top, type: 'adjustment' },
            { ...this.bottom, type: 'adjustment' }
        ];
    }
}

class ThreeDrivesPattern {
    constructor(start, drive1, drive2, drive3, end) {
        this.start = start;
        this.drive1 = drive1;
        this.drive2 = drive2;
        this.drive3 = drive3;
        this.end = end;
        this.adjustmentPointers = this.createAdjustmentPoints();
    }

    createAdjustmentPoints() {
        return [
            { ...this.start, type: 'adjustment' },
            { ...this.drive1, type: 'adjustment' },
            { ...this.drive2, type: 'adjustment' },
            { ...this.drive3, type: 'adjustment' },
            { ...this.end, type: 'adjustment' }
        ];
    }
}

export { 
    XABCDPattern, 
    CypherPattern, 
    HeadAndShouldersPattern, 
    ABCDPattern, 
    TrianglePattern, 
    ThreeDrivesPattern 
};
