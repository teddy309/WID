var canvas;
var gl;



var maxNumTriangles = 200;
var maxNumVertices  = 3 * maxNumTriangles;
var index = 0;
//var From=[];
//var To=[];
var colors = [
    vec4( 0.0, 0.0, 0.0, 1.0 ),  // black
    vec4( 1.0, 0.0, 0.0, 1.0 ),  // red
    vec4( 1.0, 1.0, 0.0, 1.0 ),  // yellow
    vec4( 0.0, 1.0, 0.0, 1.0 ),  // green
    vec4( 0.0, 0.0, 1.0, 1.0 ),  // blue
    vec4( 1.0, 0.0, 1.0, 1.0 ),  // magenta
    vec4( 0.0, 1.0, 1.0, 1.0 )   // cyan
];

var mouse=[];
var mouseLoc;
var vTrans=[];
var vTransLoc;
var currentValue=[];
var iterNum;


window.onload = function init() {
    canvas = document.getElementById( "gl-canvas" );

    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    //canvas.addEventListener("mousedown", function(){
    canvas.addEventListener("mousedown", function(event){
        gl.bindBuffer( gl.ARRAY_BUFFER, eventBuffer );
        var t = vec2(2*event.clientX/canvas.width-1,
           2*(canvas.height-event.clientY)/canvas.height-1);
        gl.bufferSubData(gl.ARRAY_BUFFER, 8*index, flatten(t));

        vTrans=vec2(t[0]-mouse[0],t[1]-mouse[1]);
        //document.getElementById("blank").innerHTML=index+":"+t;//지우기
        document.getElementById("vector").innerHTML="from/to:"+mouse+"/"+t+"->"+vTrans;
        currentValue=mouse;
        iterNum=0;
        //document.getElementById("blank").innerHTML=iterNum+":"+currentValue;
        mouse=t;
        if(currentValue[0]<mouse[0]){
        document.getElementById("check").innerHTML="go right";
    }
    else{
        document.getElementById("check").innerHTML="go left";
    }


        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
        t = vec4(colors[(index)%7]);
        gl.bufferSubData(gl.ARRAY_BUFFER, 16*index, flatten(t));
        index++;
    } );


    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0.5, 0.5, 0.5, 1.0 );


    //
    //  Load shaders and initialize attribute buffers
    //
    var program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );


    var eventBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, eventBuffer);
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

    var vTransLoc = gl.getUniformLocation( program, "vTrans" );
/*
    var vFromBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, eventBuffer);
    gl.bufferData( gl.ARRAY_BUFFER, 8*maxNumVertices, gl.STATIC_DRAW );
    var vToBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, eventBuffer);
    gl.bufferData( gl.ARRAY_BUFFER, 8*maxNumVertices, gl.STATIC_DRAW );
    for(var i;i<index.length;i++){

        if(i%2==0){

        }
    }*/

    render();

}


function render() {
    var ifIter=false;
    gl.clear( gl.COLOR_BUFFER_BIT );
    gl.drawArrays( gl.POINTS, 0, index );
    if(Math.abs(mouse[0]-currentValue[0])>0.1){
        currentValue[0]+=0.05*vTrans[0];
        ifIter=true;
    }
    if(Math.abs(mouse[1]-currentValue[1])>0.1){
        currentValue[1]+=0.05*vTrans[1];
        ifIter=true;
    }
    if(ifIter==true){
        iterNum++;
    }
    document.getElementById("blank").innerHTML=iterNum+":"+currentValue;
    document.getElementById("vtran").innerHTML="index:"+index;
    //gl.uniform4fv(vTransLoc,currentValue-vTrans);
    sleep(100);
    /*if(Math.abs(mouse[0]-currentValue[0])<0.05 && Math.abs(mouse[1]-currentValue[1])<0.05){
        if(mouse[])currentValue=vec2(currentValue[0]+0.1*vTrans[0],currentValue[1]+0.1*vTrans[1]);
        document.getElementById("blank").innerHTML=currentValue;
        sleep(1000);
        //setTimeout(execute(),1000);
    }*/
    window.requestAnimFrame(render);//0.5sec delay
}
function sleep(delay) {
    var start=new Date().getTime();
    while(new Date().getTime()<start+delay);
}/*
function execute() {
    alert("hellow world");
}*/