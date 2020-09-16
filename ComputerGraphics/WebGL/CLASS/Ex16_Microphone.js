"use strict";

var canvas;
var gl;

var NumVertices  = 36*1000;//12;

var points = [];
var colors = [];

var xAxis = 0;
var yAxis = 1;
var zAxis = 2;

var direction=1;

var axis = 0;
var theta = [ 0, 0, 0 ];

var thetaLoc;

var flag=false;//

window.onload = function init()
{
    canvas = document.getElementById( "gl-canvas" );

    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }
    
    //Sphere
    var mySphere=sphere();
    mySphere.scale(0.6,0.6,0.6);
    mySphere.rotate(0.0,[1,1,1]);
    mySphere.translate(0.0,-0.3,0.5);

    points=points.concat(mySphere.TriangleVertices);
    colors=colors.concat(mySphere.TriangleVertexColors);
    
    //Cylinder
    var myCylinder=cylinder(36,1,true);
    myCylinder.scale(0.3,0.7,0.3);
    myCylinder.rotate(0.0,[1,1,1]);
    myCylinder.translate(0.0,0.6,0.5);

    points=points.concat(myCylinder.TriangleVertices);
    colors=colors.concat(myCylinder.TriangleVertexColors);

    /*
    //colorCube();
    var myCube=cube(0.5);
    myCube.rotate(45,[1,1,1]);
    myCube.translate(0.5,0.5,0.0);
    colors=myCube.TriangleVertexColors;
    points=myCube.TriangleVertices;*/

    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );

    gl.enable(gl.DEPTH_TEST);

    //
    //  Load shaders and initialize attribute buffers
    //
    var program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );

    var cBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW );

    var vColor = gl.getAttribLocation( program, "vColor" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor );

    var vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(points), gl.STATIC_DRAW );


    var vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

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
        direction=direction*(-1);
    };

    render();
}

function render()
{
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    theta[axis] += 2.0*direction;
    gl.uniform3fv(thetaLoc, theta);

    gl.drawArrays( gl.TRIANGLES, 0, NumVertices );

    requestAnimFrame( render );
}