var canvas;
var gl;

var NumVertices  = 36;

var points = [];
var colors = [];

var xAxis = 0;
var yAxis = 1;
var zAxis = 2;

var axis = 0;
var theta = [ 0, 0, 0 ];

var rotVec = 1;//rotation direction
var size=1.0;
var cubeSize;//binded with size

var thetaLoc;

window.onload = function init()
{
    canvas = document.getElementById( "gl-canvas" );

    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    location=randomXYZgeneration();
    
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );

    gl.enable(gl.DEPTH_TEST);

    //  Load shaders and initialize attribute buffers
    var program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );

    var cBuffer = gl.createBuffer(); //colorBuffer
    gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW );

    var vColor = gl.getAttribLocation( program, "vColor" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor );

    var vBuffer = gl.createBuffer();//pointBuffer
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(points), gl.STATIC_DRAW );


    var vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    cubeSize=gl.getUniformLocation(program,"size");
    thetaLoc = gl.getUniformLocation(program, "theta");

    //event listeners for buttons

    document.getElementById( "xButton" ).onclick = function () {
        axis = xAxis;
    };
    document.getElementById( "yButton" ).onclick = function () {
        axis = yAxis;
    };
    document.getElementById( "zButton" ).onclick = function () {
        axis = zAxis;
    };
    document.getElementById( "toggleButton" ).onclick = function () {
        rotVec *= -1;
    };
    document.getElementById( "upButton" ).onclick = function () {
        size += 0.1;
        document.getElementById("blank").innerHTML=size;
    };
    document.getElementById( "downButton" ).onclick = function () {
        size -= 0.1;
        document.getElementById("blank").innerHTML=size;
    };

    render();
}

function colorCube()
{
    quad( 1, 0, 3, 2 );
    quad( 2, 3, 7, 6 );
    quad( 3, 0, 4, 7 );
    quad( 6, 5, 1, 2 );
    quad( 4, 5, 6, 7 );
    quad( 5, 4, 0, 1 );
}

function getRandomNum(max, min){
    return Math.random()*(max-min)+min;
}

function randomXYZgeneration(x, y, z)
{
    
    var vertices =vec3( getRandomNum(-8f,8f), getRandomNum(-8f,8f),  getRandomNum(-8f,8f)) ;// top 4 nodes

    var indices = [ a, b, c, a, c, d ];//make 2 triangles for one side

    for ( var i = 0; i < indices.length; ++i ) {
        points.push( vertices[indices[i]] );
        
        colors.push(vertexColors[a]);

    }
}

function render()
{
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    //update theta
    theta[axis] += 2.0 * rotVec;
    gl.uniform3fv(thetaLoc, theta);
    //update size
    gl.uniform1f(cubeSize,size);
    gl.drawArrays( gl.TRIANGLES, 0, NumVertices );

    requestAnimFrame( render );
}