var width = window.innerWidth;
var height = window.innerHeight * 3;
cent = 10
var yy = 150
var FirstX = 100
var SecondX = width - 100
var stage = new Konva.Stage({
    container: 'container',
    width: width,
    height: height,
});
var layer = new Konva.Layer();
var group1 = new Konva.Group();
layer.add(group1);
var group2 = new Konva.Group();
layer.add(group2);
var group3 = new Konva.Group();
layer.add(group3);
var imageObj = new Image();
imageObj.onload = function () {
    var yoda = new Konva.Image({
        x: 102,
        y: 120,
        image: imageObj,
        width: width - 200,
        height: 1500,
    });
    group1.add(yoda);
};
imageObj.src = './visualAttention.svg';
rectBox = []
rightAnswar = [1, 3, 29, 13, 35, 20, 28, 7, 16, 32, 18, 6, 8, 11, 40, 23, 12, 5, 36, 2, 39, 31, 24, 21, 9, 10, 15, 38, 25, 37, 4, 14, 17, 19, 22, 26, 27, 30, 34, 33]
rightAnswar1 = [1, 20, 2, 31, 18, 12, 8, 13, 25, 26, 14, 17, 4, 32, 27, 9, 33, 11, 34, 6, 24, 35, 16, 23, 29, 36, 37, 7, 3, 38, 22, 10, 40, 39, 5, 19, 30, 28, 21, 15]
pair = []
for (let i = 0; i < 40; i++) {
    if (i >= 9) {
        cent = 6
    }
    this['rect' + i] = new Konva.Rect({
        x: FirstX + 23,
        y: yy,
        width: 40,
        height: 25,
        fill: 'white',
        shadowBlur: 3,
        cornerRadius: 10,
    });

    group2.add(this['rect' + i])
    this['text1' + i] = new Konva.Text({
        x: FirstX + 30,
        y: yy + 4,
        text: i + 1,
        fontSize: 20,
        fontFamily: 'Calibri',
        fill: 'black',
        wrap: 'word',
        align: 'center',
    });
    group2.add(this['text1' + i])
    this['text' + i] = new Konva.Text({
        x: SecondX + 10,
        y: yy + 4,
        text: rightAnswar1[i],
        fontSize: 20,
        fontFamily: 'Calibri',
        fill: 'black',
        wrap: 'word',
        align: 'center',
    });

    this['rect2' + i] = new Konva.Rect({
        x: SecondX,
        y: yy,
        width: 40,
        height: 25,
        _id: rightAnswar[i],
        fill: 'white',
        shadowBlur: 3,
        cornerRadius: 10,
    });
    rectBox.push([this['rect' + i], this['rect2' + i], rightAnswar1[i], rightAnswar[i], this['text' + i],this['text1' + i]])
    group2.add(this['rect2' + i])
    if (i > 15 && i < 25) {
        yy = yy + 35
    } else if (i >= 25) {
        yy = yy + 36
    } else {
        yy = yy + 36
    }
}
// console.log(rectBox)

var arrow = new Konva.Arrow({
    x: 5,
    y: 112,
    points: [5, 50,50, 50],
    pointerLength: 15,
    pointerWidth: 20,
    fill: 'black',
    stroke: 'green',
    strokeWidth: 3,
});

var StartRect = new Konva.Rect({
    x: FirstX+23,
    y: 150,
    width: 40,
    height: 25,
    fill: 'green',
    shadowBlur: 3,
    cornerRadius: 10,
});

StartRect.on('click', function (evt) {
    StartRect.destroy();
    arrow.destroy();
    document.documentElement.requestFullscreen();
    stage.container().style.cursor = 'pointer';
})

var rightRect = 0

function checkRight(rect, index, r) {

    for (let i = 0; i < rectBox.length; i++) {
        let rect1 = rectBox[i][1]
        rect1.on('click', function (evt) {
            let click = rectBox[i][3]
            let click1 = rectBox[i][2]
            let text = rectBox[i][4]
            let text1 = rectBox[i][5]
            text1.fill('white')
            text.fill('white')
            console.log('r:', r, ' click', click, ' click1: ', click1)
            if (r == rightAnswar1[click1 - 1]) {
                rect.fill('green');
                rect1.fill('green');
                group3.add(text)
                rightRect += 1
            } else {
                rect.fill('red');
                rect1.fill('red')
            }
            // group3.add(text)
            rect1.off('click')
            for (let i = 0; i < rectBox.length; i++) {
                let rect1 = rectBox[i][1]
                rect1.off('click')
            }

            rectTrigger(index)
        });
    }
}
function rectTrigger(id = 0) {
    var index = id
    // console.log('index: ',index)
    let rect = rectBox[index][0]
    let r = rectBox[index][2]
    rect.on('click', function (evt) {
        // console.log('clicked') 
        index++
        rect.fill('yellow');
        checkRight(rect, index, r);
        // pair.push(rectBox[index][2])
        rect.off('click')
    });
}
rectTrigger()
var circle = new Konva.Circle({
    x: SecondX -50,
    y: 1700,
    radius: 20,
    fill: 'green',
    stroke: 'black',
    strokeWidth: 4,
});
group2.add(circle)
circle.on('click', function (evt) {
    finalScore()
});
function finalScore() {
    final = rightRect * 100 / 40
    console.log(final)
    let complexText = new Konva.Text({
        x: 1000,
        y: 1650,
        text: 'Your Final Score is: ' + final + ' %',
        fontSize: 20,
        fontFamily: 'Calibri',
        fill: '#555',
        wrap: 'word',
        align: 'center',
    });
    $.ajax({
        type: 'POST',
        url: '/assessments/evaluate_psycometric_test/',
        data: {
            test_id: test_id,
            final_score: final,
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

    group2.add(complexText)
}
layer.add(StartRect);
layer.add(arrow);

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