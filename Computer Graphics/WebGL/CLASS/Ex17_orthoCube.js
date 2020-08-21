"use strict";

var canvas;
var gl;

var numVertices  = 72;//org:36

var pointsArray = [];
var colorsArray = [];
/*
var vertices = [
        vec4( -0.5, -0.5,  0.5, 1.0 ),
        vec4( -0.5,  0.5,  0.5, 1.0 ),
        vec4( 0.5,  0.5,  0.5, 1.0 ),
        vec4( 0.5, -0.5,  0.5, 1.0 ),
        vec4( -0.5, -0.5, -0.5, 1.0 ),
        vec4( -0.5,  0.5, -0.5, 1.0 ),
        vec4( 0.5,  0.5, -0.5, 1.0 ),
        vec4( 0.5, -0.5, -0.5, 1.0 ),
    ];

var vertexColors = [
        vec4( 0.0, 0.0, 0.0, 1.0 ),  // black
        vec4( 1.0, 0.0, 0.0, 1.0 ),  // red
        vec4( 1.0, 1.0, 0.0, 1.0 ),  // yellow
        vec4( 0.0, 1.0, 0.0, 1.0 ),  // green
        vec4( 0.0, 0.0, 1.0, 1.0 ),  // blue
        vec4( 1.0, 0.0, 1.0, 1.0 ),  // magenta
        vec4( 0.0, 1.0, 1.0, 1.0 ),  // cyan
        vec4( 1.0, 1.0, 1.0, 1.0 ),  // white
    ];*/
var vertices = [
        vec4( -1.0, -1.0,  0.5, 1.0 ),//top left:0,1,2,3
        vec4( -1.0,  1.0,  0.5, 1.0 ),
        vec4(  0.0,  1.0,  0.5, 1.0 ),
        vec4(  0.0, -1.0,  0.5, 1.0 ),
        vec4(  0.0,  0.0,  0.5, 1.0 ),//top right:4,5,6,7
        vec4(  0.0,  1.0,  0.5, 1.0 ),
        vec4(  1.0,  1.0,  0.5, 1.0 ),
        vec4(  1.0,  0.0,  0.5, 1.0 ),
        vec4( -1.0, -1.0, -0.5, 1.0 ),//bottom left:8,9,10,11
        vec4( -1.0,  1.0, -0.5, 1.0 ),
        vec4(  0.0,  1.0, -0.5, 1.0 ),
        vec4(  0.0, -1.0, -0.5, 1.0 ),
        vec4(  0.0,  0.0, -0.5, 1.0 ),//bottom right:12,13,14,15
        vec4(  0.0,  1.0, -0.5, 1.0 ),
        vec4(  1.0,  1.0, -0.5, 1.0 ),
        vec4(  1.0,  0.0, -0.5, 1.0 ),
    ];

var vertexColors = [
        [ 0.0, 0.0, 0.0, 1.0 ],  // black
        [ 0.0, 0.0, 0.0, 1.0 ],  // black
        [ 0.0, 0.0, 0.0, 1.0 ],  // black
        [ 0.0, 0.0, 1.0, 1.0 ],  // blue 3
        [ 1.0, 1.0, 0.0, 1.0 ],  // yellow 4
        [ 0.0, 0.0, 0.0, 1.0 ],  // black
        [ 1.0, 1.0, 0.0, 1.0 ],  // yellow 6
        [ 0.0, 0.0, 1.0, 1.0 ],  // blue 7
        [ 0.0, 1.0, 0.0, 1.0 ],  // green 8
        [ 0.0, 1.0, 1.0, 1.0 ],  // cyan 9
        [ 0.0, 0.0, 0.0, 1.0 ],  // black
        [ 1.0, 0.0, 1.0, 1.0 ],  // magenta 11
        [ 0.0, 1.0, 0.0, 1.0 ],  // green 12
        [ 0.0, 0.0, 0.0, 1.0 ],  // black
        [ 1.0, 0.0, 0.0, 1.0 ],  // red 14
        [ 1.0, 0.0, 1.0, 1.0 ],  // magenta 15
    ];

var near = -1;
var far = 1;
var radius = 1.0;
var theta  = 0.0;
var phi    = 0.0;
var dr = 5.0 * Math.PI/180.0;//direction

var left = -1.0;
var right = 1.0;
var ytop = 1.0;
var bottom = -1.0;


var modelViewMatrix, projectionMatrix;
var modelViewMatrixLoc, projectionMatrixLoc;
var eye;

const at = vec3(0.0, 0.0, 0.0);
const up = vec3(0.0, 1.0, 0.0);

// quad uses first index to set color for face

window.onload = function init() {
    canvas = document.getElementById( "gl-canvas" );

    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    colorCube();
    /*
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );
    gl.enable(gl.DEPTH_TEST);

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
    */
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
    gl.bufferData( gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW );

    var vColor = gl.getAttribLocation( program, "vColor" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor);

    var vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(pointsArray), gl.STATIC_DRAW );

    var vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    modelViewMatrixLoc = gl.getUniformLocation( program, "modelViewMatrix" );
    projectionMatrixLoc = gl.getUniformLocation( program, "projectionMatrix" );

// buttons to change viewing parameters

    document.getElementById("Button1").onclick = function(){
        near  *= 1.1; far *= 1.1;};//increase Z
    document.getElementById("Button2").onclick = function(){
        near *= 0.9; far *= 0.9;};//decrease Z
    document.getElementById("Button3").onclick = function(){
        radius *= 1.1;};//increase R
    document.getElementById("Button4").onclick = function(){
        radius *= 0.9;};//decrease R
    document.getElementById("Button5").onclick = function(){
        theta += dr;};//increase theta
    document.getElementById("Button6").onclick = function(){
        theta -= dr;};//decrease theta
    document.getElementById("Button7").onclick = function(){
        phi += dr;};//increase phi
    document.getElementById("Button8").onclick = function(){
        phi -= dr;};//decrease phi

    render();
}

function quad(a, b, c, d) {
    var indices = [ a, b, c, a, c, d ];
    for ( var i = 0; i < indices.length; ++i ) {
        points.push( vertices[indices[i]] );
        colors.push(vertexColors[d]);
    }

    /*
    pointsArray.push(vertices[a]);
     colorsArray.push(vertexColors[a]);
     pointsArray.push(vertices[b]);
     colorsArray.push(vertexColors[a]);
     pointsArray.push(vertices[c]);
     colorsArray.push(vertexColors[a]);
     pointsArray.push(vertices[a]);
     colorsArray.push(vertexColors[a]);
     pointsArray.push(vertices[c]);
     colorsArray.push(vertexColors[a]);
     pointsArray.push(vertices[d]);
     colorsArray.push(vertexColors[a]);*/
}

// Each face determines two triangles
function colorCube()
{
    quad( 0, 1, 2, 3 );//top
    quad( 4, 5, 6, 7 );
    quad( 8, 9, 10, 11 );//bottom
    quad( 12, 13, 14, 15 );
    quad( 1, 0, 8, 9 );//side
    quad( 0, 3, 11, 8);
    quad( 12, 11, 3, 4);
    quad( 4, 7, 15, 12);
    quad( 14, 15, 7, 6);
    quad( 6, 1, 9, 14);
    /*
    quad( 1, 0, 3, 2 );
    quad( 2, 3, 7, 6 );
    quad( 3, 0, 4, 7 );
    quad( 6, 5, 1, 2 );
    quad( 4, 5, 6, 7 );
    quad( 5, 4, 0, 1 );*/
}



var render = function() {
        gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

        eye = vec3(radius*Math.sin(phi), radius*Math.sin(theta),
             radius*Math.cos(phi));

        modelViewMatrix = lookAt(eye, at , up);
        projectionMatrix = ortho(left, right, bottom, ytop, near, far);

        gl.uniformMatrix4fv( modelViewMatrixLoc, false, flatten(modelViewMatrix) );
        gl.uniformMatrix4fv( projectionMatrixLoc, false, flatten(projectionMatrix) );

        gl.drawArrays( gl.TRIANGLES, 0, numVertices );
        requestAnimFrame(render);
    }