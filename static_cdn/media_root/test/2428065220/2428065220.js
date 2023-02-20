var width = window.innerWidth;
var height = window.innerHeight;
const showResult = document.getElementById('showResult')
var stage = new Konva.Stage({
    container: 'container',
    width: width - 500,
    height: height,
});
var layer = new Konva.Layer();
stage.add(layer);
var canvas = document.createElement('canvas');
canvas.width = stage.width();
canvas.height = stage.height();
var image = new Konva.Image({
    image: canvas,
    x: 0,
    y: 50,
});
layer.add(image);
var StartRect = new Konva.Rect({
    x: 3,
    y: 50,
    width: 25,
    height: 150,
    fill: 'green',
    shadowBlur: 3,
    cornerRadius: 5,
});

var context = canvas.getContext('2d');
context.strokeStyle = 'black';
context.lineJoin = 'round';
context.lineWidth = 2;
document.body.classList.add("custom-cursor");

StartRect.on('mousedown touchstart', function () {
    document.documentElement.requestFullscreen();
    setTimeout(function () {
        arrow.destroy();
        stage.container().style.cursor = 'pointer';
        isPaint = true;
        lastPointerPosition = stage.getPointerPosition();
        startTest()
    }, 1000);

});
// stage.on('mouseup touchend', function () {
//     isPaint = false;
// for (j = 0; j < elements.length; j++) {
//         // console.log(elements[j])
//         elements[j].off('mouseover')
//     }
// });
stage.on('mousemove touchmove', function () {
    if (!isPaint) {
        return;
    }
    context.globalCompositeOperation = 'source-over';
    context.beginPath();
    var localPos = {
        x: lastPointerPosition.x - image.x(),
        y: lastPointerPosition.y - image.y(),
    };
    context.moveTo(localPos.x, localPos.y);
    var pos = stage.getPointerPosition();
    localPos = {
        x: pos.x - image.x(),
        y: pos.y - image.y(),
    };
    context.lineTo(localPos.x, localPos.y);
    context.closePath();
    context.stroke();
    lastPointerPosition = pos;
    layer.batchDraw();
});
var isPaint = false;
var lastPointerPosition;
var mode = 'brush';
const stating_point = 30
function randomNumber(min, max) {
    return Math.random() * (max - min) + min;
}

h1 = 30
h2 = 30
yy = 150
var elements = []
for (j = 0; j < 5; j++) {
    xx = 0
    for (var i = 0; i < 33; i++) {
        let x = randomNumber(0, 125)
        if (x <= 65 && x >= 30) {
            x = x - 29
        } else if (x > 65 && x <= 100) {
            x = x + 25
        }
        // console.log( 'x is :',x)
        end = yy - x //225
        endcut = end - 25
        lastLine = [stating_point + xx, yy, stating_point + xx, end]
        comLine = [stating_point + xx, yy - 150, stating_point + xx, endcut]
        greenPoint = [stating_point + xx, endcut + 25, stating_point + xx, endcut]
        xx += 32
        this["marker" + i + j] = new Konva.Line({
            x: 0,
            y: 50,
            points: lastLine,
            tension: 0,
            strokeWidth: 1,
            hitStrokeWidth: 2,
            stroke: 'black',
        });
        layer.add(this["marker" + i + j]);

        this["2marker2" + i + j] = new Konva.Line({
            x: 0,
            y: 50,
            points: comLine,
            tension: 0,
            strokeWidth: 1,
            hitStrokeWidth: 2,
            stroke: 'black',
        });

        layer.add(this["2marker2" + i + j]);
        this["green" + i + j] = new Konva.Line({
            x: 0,
            y: 50,
            points: greenPoint,
            tension: 0,
            strokeWidth: 1,
            hitStrokeWidth: 2,
            stroke: 'white',
        });
        layer.add(this["green" + i + j]);
        elements.push(this["green" + i + j], this["2marker2" + i + j], this["marker" + i + j])
    }
    if (h1 == 0) {
        h1 = h1
        h2 = 0
    } else {
        h1 *= -1
        h2 = 30
    }
    points = [30 + h1, yy, 1080 - h2, yy]
    this["Hmarker" + i] = new Konva.Line({
        x: 0,
        y: 50,
        points: points,
        tension: 0,
        strokeWidth: 1,
        hitStrokeWidth: 2,
        stroke: 'black',
    });
    layer.add(this["Hmarker" + i]);
    yy += 150
    h1 += 30
    h2 += 30
}
rec = [0, 0, 0, 750, 1080, 750, 1080, 0, 0, 0]
var rec = new Konva.Line({
    x: 0,
    y: 50,
    points: rec,
    tension: 0,
    strokeWidth: 1,
    hitStrokeWidth: 2,
    stroke: 'black',
});
layer.add(rec);
let crossedPoints = []
let greenbar = []
function startTest() {
    for (j = 0; j < 5; j++) {
        for (var i = 0; i < 33; i++) {
            this["2marker2" + i + j].on('mouseover', function () {
                crossedPoints.push([stage.getPointerPosition().x, stage.getPointerPosition().y])
                // console.log(stage.getPointerPosition().x,event.clientX);
            });
            this["marker" + i + j].on('mouseover', function () {
                crossedPoints.push([stage.getPointerPosition().x, stage.getPointerPosition().y])
            });
            this["green" + i + j].on('mouseover', function () {
                // greenbar.push([event.clientX-160, event.clientY-30])
                greenbar.push([stage.getPointerPosition().x, stage.getPointerPosition().y])
            });
        }
    }
}

var circle = new Konva.Rect({
    x: 1075,
    y: 650,
    width: 25,
    height: 150,
    fill: 'red',
    shadowBlur: 3,
    cornerRadius: 5,
});
var text = new Konva.Text({
    text: '',
    fontFamily: 'Calibri',
    fontSize: 24,
    fill: 'black',
    x: 10,
    y: 10,
});

circle.on('click', function (evt) {
    isPaint = false;
    for (j = 0; j < elements.length; j++) {
        // console.log(elements[j])
        elements[j].off('mouseover')
    }
    calculate()
    text.text('Your Final Scroe Is ' + final_score);
});
layer.add(circle).add(text);
layer.add(StartRect)
function wrongUnique(points) {
    for (i = 0; i < points.length - 1; i++) {
        // console.log(points[i][0])
        for (j = 0; j < points.length - 1; j++) {
            // console.log(points[j][0])
            if (points[i][1] - points[j][1] <= 3) {
                points.splice(i, 1);
            }
        }
    }
}
var arrow = new Konva.Arrow({
    x: 100,
    y: 20,
    points: [40, 50, 10, 50],
    pointerLength: 20,
    pointerWidth: 40,
    fill: 'black',
    stroke: 'green',
    strokeWidth: 3,
});
layer.add(arrow);

let final_score = 0
function calculate() {
    const pointsArray = crossedPoints.map(points => {
        var ring = new Konva.Ring({
            x: points[0],
            y: points[1],
            innerRadius: 2,
            outerRadius: 6,
            fill: 'red',
            stroke: 'black',
            strokeWidth: 0.8,
        });
        layer.add(ring);
    })
    const GreenPointsArray = greenbar.map(green_points => {
        var greenRing = new Konva.Ring({
            x: green_points[0],
            y: green_points[1],
            innerRadius: 2,
            outerRadius: 6,
            fill: 'green',
            stroke: 'white',
            strokeWidth: 0.8,
        });
        layer.add(greenRing);
    })
    // console.log('greenbar.length',greenbar.length)
    correct_score = greenbar.length * 100 / 165
    wrong_score = crossedPoints.length * 100 / 165
    final_score = correct_score - wrong_score
    if (final_score < 0) {
        final_score = 0
    }
    $.ajax({
        type: 'POST',
        url: '/assessments/evaluate_psycometric_test/',
        data: {
            test_id: test_id,
            final_score: final_score,
            question_id: question_id,
        },
        headers: { 'X-CSRFToken': csrftoken },
        success: function (response) {
            console.log(question_id, final_score, test_id)
            // window.location.href = "/assessments/psycometric_test/";
            if (response.url == '/assessments') {
                window.location.href = response.url;
            } else {
                window.location.href = "/assessments/psycometric_test/";
            }
            console.log(response.url)
        },
        error: function (error) {
            console.log(error);
        }
    });
}
stage.add(layer);
var amplitude = 20;
var period = 2000;
// in ms
var centerX = 60;

var anim = new Konva.Animation(function (frame) {
    arrow.x(
        amplitude * Math.sin((frame.time * 2 * Math.PI) / period) + centerX
    );
}, layer);

anim.start();
