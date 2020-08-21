
var gl;
var points;

var renderPolygon=false;

var colorList=[
    vec4( 0.0, 0.0, 0.0, 1.0 ),  // black
    vec4( 1.0, 0.0, 0.0, 1.0 ),  // red
    vec4( 1.0, 1.0, 0.0, 1.0 ),  // yellow
    vec4( 0.0, 1.0, 0.0, 1.0 ),  // green
    vec4( 0.0, 0.0, 1.0, 1.0 ),  // blue
    vec4( 1.0, 0.0, 1.0, 1.0 ),  // magenta
    vec4( 0.0, 1.0, 1.0, 1.0 )   // cyan
    ];
var i=0;//
var colorPick=colorList[0];
var colorMenu=document.getElementById("colorMenu");

//var x;
//var y;
//var redraw = false;
var index = 0;

window.onload = function init()
{
    var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    //mouse event
    canvas.addEventListener("mousedown", function(event){
        gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
        var t = vec2(2*event.clientX/canvas.width-1,
           2*(canvas.height-event.clientY)/canvas.height-1);
        gl.bufferSubData(gl.ARRAY_BUFFER, 8*index, flatten(t));

        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
        t = vec4(colors[(index)%7]);
        gl.bufferSubData(gl.ARRAY_BUFFER, 16*index, flatten(t));
        index++;
    } );

    
    var vertices = new Float32Array([-0.5,0.5,0.5,0.5,-0.5,-0.5,0.5,-0.5]);

    //  Configure WebGL

    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0.0, 0.0, 0.0, 1.0 );//BGcolor
    
    //  Load shaders and initialize attribute buffers
    
    var program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );
    
    // Load the data into the GPU
    
    var bufferId = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, bufferId );
    gl.bufferData( gl.ARRAY_BUFFER,vertices, gl.STATIC_DRAW );

    // Associate out shader variables with our data buffer
    
    var vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 2, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    var colorLoc = gl.getUniformLocation(program, "color");
    gl.uniform4fv(colorLoc, [0.0, 1.0, 0.0, 1.0]);//color

    render();

    //select color
    //colorMenu.addEventListener("change",pickColor);//
    //Button action
    document.getElementById("drawPolygon").addEventListener("click",pushBtn);
    //var coords=canvas.relMouseCoordinate("click");
    //canvas.addEventListener("click",canvas.relMouseCoordinate("click"));
    

    /*
    //canvas.addEventListener("click",clickCanvas);
    canvas.addEventListener("click",function(event){
        gl.bindBuffer(gl.ARRAY_BUFFER,vBuffer);
    //t=clip Coordinates
    var t=vec2(-1+2*event.clientX/canvas.width,-1+2*(canvas.height-event.clientY)/canvas.height);
    gl.bufferSubData(gl.ARRAY_BUFFER,sizeof['vec2']*index,t);
    document.getElementById("xPos").innerHTML=t;//
    //document.getElementById("yPos").innerHTML=canvasY;//
    index++;
    });*/
    

};


function render() {
    gl.clear( gl.COLOR_BUFFER_BIT );
    gl.drawArrays( gl.TRIANGLE_FAN, 0, 4 );
}
function pickColor(){
    //document.getElementById("demo").innerHTML=colorList[5];//
    switch(colorMenu.selectedIndex){
        case 0:
            colorPick=colorList[0];
            break;
        case 1:
            colorPick=colorList[1];
            break;
        case 2:
            colorPick=colorList[2];
            break;
        case 3:
            colorPick=colorList[3];
            break;
        case 4:
            colorPick=colorList[4];
            break;
        case 5:
            colorPick=colorList[5];
            break;
        case 6:
            colorPick=colorList[6];
            break;
    }
    document.getElementById("demo").innerHTML=colorPick;//
}
function pushBtn(){
    colorPick=colorList[i++];
    document.getElementById("demo").innerHTML=colorPick;
}/*
function clickCanvas(){
    gl.bindBuffer(gl.ARRAY_BUFFER,vBuffer);
    //t=clip Coordinates
    var t=vec2(-1+2*event.clientX/canvas.width,-1+2*(canvas.height-event.clientY)/canvas.height);
    gl.bufferSubData(gl.ARRAY_BUFFER,sizeof['vec2']*index,t);
    document.getElementById("xPos").innerHTML=t;//
    //document.getElementById("yPos").innerHTML=canvasY;//
    index++;
}
function relMouseCoordinate(event){
    var totalOffsetX=0;
    var totalOffsetY=0;
    var canvasX=0;
    var canvasY=0;
    var currentElement=this;
    do{
        totalOffsetX+=currentElement.offsetLeft-currentElement.scrollLeft;
        totalOffsetY+=currentElement.offsetTop-currentElement.scrollTop;
    }while(currentElement = currentElement.offsetParent)
    canvasX=event.pageX-totalOffsetX;
    canvasY=event.pageY-totalOffsetY;
    document.getElementById("xPos").innerHTML=canvasX;//
    document.getElementById("yPos").innerHTML=canvasY;//
    //return{x:canvasX,y:canvasY}
}*/