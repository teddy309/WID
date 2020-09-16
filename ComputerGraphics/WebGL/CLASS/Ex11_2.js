var canvas;
var gl;


var maxNumTriangles = 200;
var maxNumVertices  = 3 * maxNumTriangles;
var index = 0;
var vertices = 0;
var count = 0;

var colors = [
    vec4( 0.0, 0.0, 0.0, 1.0 ),  // black
    vec4( 1.0, 0.0, 0.0, 1.0 ),  // red
    vec4( 1.0, 1.0, 0.0, 1.0 ),  // yellow
    vec4( 0.0, 1.0, 0.0, 1.0 ),  // green
    vec4( 0.0, 0.0, 1.0, 1.0 ),  // blue
    vec4( 1.0, 0.0, 1.0, 1.0 ),  // magenta
    vec4( 0.0, 1.0, 1.0, 1.0 )   // cyan
];

var i=0;//
var colorPick=colors[0];
var colorMenu=document.getElementById("colorMenu");


window.onload = function init() {
    canvas = document.getElementById( "gl-canvas" );

    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    //canvas.addEventListener("mousedown", function(){
    canvas.addEventListener("mousedown", function(event){
        //vertexBuffer
        gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
        var t = vec2(2*event.clientX/canvas.width-1,
           2*(canvas.height-event.clientY)/canvas.height-1);
        gl.bufferSubData(gl.ARRAY_BUFFER, 8*index, flatten(t));
        //colorBuffer
        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
        t = vec4(colors[colorPick]);
        t=vec4(colors[i]);
        gl.bufferSubData(gl.ARRAY_BUFFER, 16*index, flatten(t));
        //document.getElementById("xPos").innerHTML=;
        index++;
    } );


    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0.5, 0.5, 0.5, 1.0 );


    //
    //  Load shaders and initialize attribute buffers
    //
    var program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );


    var vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData( gl.ARRAY_BUFFER, 8*maxNumVertices, gl.STATIC_DRAW );

    var vPosition = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);

    var cBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, 16*maxNumVertices, gl.STATIC_DRAW );

    var vColor = gl.getAttribLocation( program, "vColor" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor );

    render();

    //select color
    //colorMenu.addEventListener("change",pickColor);//
    //Button action
    document.getElementById("drawPolygon").addEventListener("click",pushBtn);

}


function render() {
    gl.clear( gl.COLOR_BUFFER_BIT );
    //gl.drawArrays( gl.POINTS, 0, index );
    gl.drawArrays( gl.TRIANGLE_FAN, count, 8*index );
    index=0;
    //window.requestAnimFrame(render);

}
function pickColor(){
    //document.getElementById("demo").innerHTML=colorMenu.options[colorMenu.selectedIndex].value;//
    switch(colorMenu.options[colorMenu.selectedIndex].value){
        case 0:
            colorPick=colors[0];
            break;
        case 1:
            colorPick=colors[1];
            break;
        case 2:
            colorPick=colors[2];
            break;
        case 3:
            colorPick=colors[3];
            break;
        case 4:
            colorPick=colors[4];
            break;
        case 5:
            colorPick=colors[5];
            break;
        case 6:
            colorPick=colors[6];
            break;
    }
    document.getElementById("demo").innerHTML=colorPick;//
}
function pushBtn(){
    //colorPick=colors[i++];
    document.getElementById("demo").innerHTML=colorPick;
    window.requestAnimFrame(render);//

}