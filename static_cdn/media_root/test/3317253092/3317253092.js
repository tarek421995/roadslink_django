
var width = window.innerWidth;
var height = window.innerHeight;
document.body.classList.add("custom-cursor");

var stage = new Konva.Stage({
    container: 'container',
    width: width,
    height: height,
});
function drawCircals(x, y) {
    var circle = new Konva.Circle({
        x: x,
        y: y,
        radius: 1,
        fill: 'black',
        stroke: 'black',
        strokeWidth: 2,
    });
    layer.add(circle);
}

var layer = new Konva.Layer();
var circle = new Konva.Circle({
    x: stage.width() / 2,
    y: stage.height() / 2,
    radius: 70,
    fill: 'red',
    stroke: 'black',
    strokeWidth: 4,
});
xx = 0
correctClicks = []
wrongClicks = []
smallCircal = []
starting_points = [300, 75]
for (i = 0; i < 25; i++) {

    yy = 0
    for (j = 0; j < 25; j++) {
        let bigger = this["marker" + i + j]
        bigger = new Konva.Ellipse({
            x: starting_points[0] + xx,
            y: starting_points[1] + yy,
            radiusX: 5,
            radiusY: 10,
            stroke: 'black',
            strokeWidth: 1,
        });
        layer.add(bigger);
        let small = this["smallerMarker" + i + j]
        small = new Konva.Ellipse({
            x: starting_points[0] + xx,
            y: starting_points[1] + yy,
            radiusX: 2,
            radiusY: 6,
            stroke: 'white',
            strokeWidth: 1,
        });
        layer.add(small);
        smallCircal.push(small)
        yy += 30
        small.on('click', function () {
            // add the shape to the layer
            drawCircals(stage.getPointerPosition().x, stage.getPointerPosition().y)
            small.off('click');
            bigger.off('click');
            correctClicks.push(bigger)
            console.log('right clicks is: ', correctClicks.length)
        });
        bigger.on('click', function () {
            drawCircals(stage.getPointerPosition().x, stage.getPointerPosition().y)
            bigger.off('click');
            small.off('click');
            wrongClicks.push(bigger)
        });
    }
    xx += 20
}
var arrow = new Konva.Arrow({
    x: 20,
    y: 23,
    points: [180, 50, 210, 50],
    pointerLength: 20,
    pointerWidth: 40,
    fill: 'black',
    stroke: 'green',
    strokeWidth: 3,
});
var startingCircle = new Konva.Circle({
    x: 300,
    y: 74,
    radius: 10,
    fill: 'white',
    stroke: 'black',
    strokeWidth: 4,
});
startingCircle.on('click', function (evt) {
    startingCircle.destroy();
    arrow.destroy();

    document.documentElement.requestFullscreen();
    stage.container().style.cursor = 'pointer';
});



var circle = new Konva.Circle({
    x: 850,
    y: 800,
    radius: 20,
    fill: 'green',
    stroke: 'black',
    strokeWidth: 4,
});
var text = new Konva.Text({
    text: '',
    fontFamily: 'Calibri',
    fontSize: 24,
    fill: 'black',
    x: 10,
    y: 10,
});
function calculate() {
    for (i in smallCircal) {
        smallCircal[i].destroy()
    }
    for (i in correctClicks) {
        correctClicks[i].fill('green')
    }
    for (i in wrongClicks) {
        wrongClicks[i].fill('red')
    }

}
circle.on('click', function (evt) {
    calculate()
    corrects = correctClicks.length * 100 / 625
    wrongs = wrongClicks.length * 100 / 625
    final_score = corrects - wrongs
    if (final_score < 0) {
        final_score = 0
    }
    text.text('Your Final Scroe Is ' + final_score);
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
});
layer.add(arrow);
layer.add(startingCircle);
layer.add(circle).add(text);

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