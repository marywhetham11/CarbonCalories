var percentColors = [
    { pct: 0.0, color: { r: 0xff, g: 0x00, b: 0 } },
    { pct: 0.5, color: { r: 0xff, g: 0xff, b: 0 } },
    { pct: 1.0, color: { r: 0x00, g: 0xff, b: 0 } }
];

function chooseColour(pct, targetElement, radius) {
    pct /= 10;
    for (var i = 1; i < percentColors.length - 1; i++) {
        if (pct < percentColors[i].pct) {
            break;
        }
    }
    var lower = percentColors[i - 1];
    var upper = percentColors[i];
    var range = upper.pct - lower.pct;
    var rangePct = (pct - lower.pct) / range;
    var pctLower = 1 - rangePct;
    var pctUpper = rangePct;
    var color = {
        r: Math.floor(lower.color.r * pctLower + upper.color.r * pctUpper),
        g: Math.floor(lower.color.g * pctLower + upper.color.g * pctUpper),
        b: Math.floor(lower.color.b * pctLower + upper.color.b * pctUpper)
    };
    var colour = 'rgb(' + [color.r, color.g, color.b].join(',') + ')';
    document.getElementById(targetElement).style.stroke = colour;

    document.getElementById(targetElement).style.strokeDashoffset = 2 * 3.14 * radius * 0.25;
    console.log("'" + (2 * 3.14 * radius * 0.25) + "'");
    document.getElementById(targetElement).style.strokeDasharray = (2 * 3.14 * radius * pct) + " " + (2 * 3.14 * radius * (1 - pct));
    // or output as hex if preferred
};