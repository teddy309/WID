var gl;

var colors = [];
var  numVertices_santa=165;

var maxNumTriangles = 200;//
var maxNumVertices  = 3 * maxNumTriangles;
var index = 0;

var xDir= 1;
var xDirLoc;

var mouse=vec2(0.0,0.0);
var mouseLoc;
var vTrans=vec2(0.0,0.0);
var vTransLoc;

var translation=vec2(0.0,0.0);
var offset=vec2(0.0,0.0);
var currentValue=vec2(0.0,0.0);
var iterNum=0;//

var vertex_santa = new Float32Array([
//santa
    //boots
    -0.1, -0.7, -0.1, -0.9, 0, -0.7, -0.1, -0.9, 0, -0.7, 0, -0.9,
    0, -0.8, 0, -0.9, 0.1, -0.8, 0, -0.9, 0.1, -0.8, 0.1, -0.9,
    0.2, -0.7, 0.2, -0.9, 0.3, -0.7, 0.2, -0.9, 0.3, -0.7, 0.3, -0.9,
    0.3, -0.8, 0.3, -0.9, 0.4, -0.8, 0.3, -0.9, 0.4, -0.8, 0.4, -0.9,

    //belt
    -0.3, -0.4, -0.3, -0.5, 0.1, -0.4, -0.3, -0.5, 0.1, -0.4, 0.1, -0.5,
    0.2, -0.4, 0.2, -0.5, 0.3, -0.4, 0.2, -0.5, 0.3, -0.4, 0.3, -0.5,
    0.4, -0.4, 0.4, -0.5, 0.6, -0.4, 0.4, -0.5, 0.6, -0.4, 0.6, -0.5,

    //eye_black
    -0.2, 0.6, -0.2, 0.4, 0, 0.6, -0.2, 0.4, 0, 0.6, 0, 0.4,
    0.4, 0.6, 0.4, 0.4, 0.6, 0.6, 0.4, 0.4, 0.6, 0.6, 0.6, 0.4,
    //mouth
    0, 0.3, 0, 0.2, 0.3, 0.3, 0, 0.2, 0.3, 0.3, 0.3, 0.2,
    //eye
    -0.3, 0.7, -0.3, 0.4, 0, 0.7, -0.3, 0.4, 0, 0.7, 0, 0.4,
    0.3, 0.7, 0.3, 0.4, 0.6, 0.7, 0.3, 0.4, 0.6, 0.7, 0.6, 0.4,

    //belt_buckle
    0.1, -0.3, 0.1, -0.6, 0.4, -0.3, 0.1, -0.6, 0.4, -0.3, 0.4, -0.6,

    //hat_fur
    -0.9, 0.9, -0.9, 0.8, -0.8, 0.9, -0.9, 0.8, -0.8, 0.9, -0.8, 0.8,//
    -0.5, 0.9, -0.5, 0.7, 0.8, 0.9,
    -0.5, 0.7, 0.8, 0.9, 0.8, 0.7,//
    -0.6, 0.8, -0.6, 0.6, -0.4, 0.8,
    -0.6, 0.6, -0.5, 0.6, -0.5, 0.7,
    -0.5, 0.7, -0.4, 0.7, -0.4, 0.8,//
    0.7, 0.8, 0.9, 0.8, 0.9, 0.6,
    0.7, 0.8, 0.7, 0.7, 0.8, 0.7,
    0.8, 0.7, 0.8, 0.6, 0.9, 0.6,
    //beard
    -0.6, 0.4, -0.6, 0, 0.9, 0.4, -0.6, 0, 0.9, 0.4, 0.9, 0,
    -0.4, 0, -0.4, -0.1, 0.7, 0, -0.4, -0.1, 0.7, 0, 0.7, -0.1,
    -0.2, -0.1, -0.2, -0.2, 0.5, -0.1, -0.2, -0.2, 0.5, -0.1, 0.5, -0.2,
    0, -0.2, 0, -0.3, 0.3, -0.2, 0, -0.3, 0.3, -0.2, 0.3, -0.3,

    //body
    -0.3, 0, -0.3, -0.6, 0.6, 0, 0.6, 0, -0.3, -0.6, 0.6, -0.6,
    //hat
    -0.8, 0.9, -0.8, 0.8, -0.6, 1,
    -0.6, 1, -0.8, 0.8, 0.9, 1,
    -0.8, 0.8, 0.9, 1, 0.9, 0.8,

    -0.6, 1, -0.6, 0, 0.9, 1, 0.9, 1, -0.6, 0, 0.9, 0,//face
    -0.1, -0.6, -0.1, -0.8, 0, -0.6, -0.1, -0.8, 0, -0.6, 0, -0.8,
    0.2, -0.6, 0.2, -0.8, 0.3, -0.6, 0.2, -0.8, 0.3, -0.6, 0.3, -0.8//2 legs
    ]);
var colorArray_santa = [
    [0.647059, 0.164706, 0.164706, 1.0],//brown
    [0.0, 0.0, 0.0, 1.0],//black
    [0.74902, 0.847059, 0.847059, 1.0],//skyBlue
    [1.0, 1.0, 0.0, 1.0],//yellow
    [1.0, 1.0, 1.0, 1.0],//white
    [1, 0.2, 0.0, 1.0],//red
    [0.91, 0.76, 0.65, 1.0],//skinColor
	];
var length_santa = [24,36,12,6,54,15,18];
for (var i=0; i< colorArray_santa.length; i++) {
    for (var j=0; j<length_santa[i]; j++){
        colors.push(colorArray_santa[i]);
    }       
}



window.onload = function init()
{
    var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    canvas.addEventListener("mousedown", function(event){
        gl.bindBuffer( gl.ARRAY_BUFFER, eventBuffer );
        var t = vec2(2*event.clientX/canvas.width-1,
           2*(canvas.height-event.clientY)/canvas.height-1);
        gl.bufferSubData(gl.ARRAY_BUFFER, 8*index, flatten(t));

        translation=vec2(t[0]-currentValue[0],t[1]-currentValue[1]);
        
        mouse=t;
        //document.getElementById("blank").innerHTML=index+":"+t;//지우기
        document.getElementById("vector").innerHTML="from:"+currentValue+"/to:"+t+"->offset:"+translation;
        //currentValue[0]+=vTrans[0];//mouse;
        //currentValue[1]+=vTrans[1];

        //Initializing offset values
        //vTrans=vec2(0,0);
        iterNum=0;
        if(currentValue[0]<=mouse[0]){
            xDir=1;//go right
        }else{
            xDir=-1;//go left
        }
        index++;
    } );

    //  Configure WebGL  
    gl.viewport( 0, 0, canvas.width, canvas.height);
    gl.clearColor( 0.184314, 0.184314, 0.309804, 1.0 );    
    
    gl.enable(gl.DEPTH_TEST);
    
    //  Load shaders and initialize 
    var program = initShaders( gl, "vertex-shader", "fragment-shader" );
	gl.useProgram( program );   
	
    var cBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW );

    var vColor = gl.getAttribLocation( program, "vColor" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor );

    // create a buffer on gpu and bind point    
    var bufferId = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, bufferId);
	gl.bufferData(gl.ARRAY_BUFFER, vertex_santa, gl.STATIC_DRAW);//

    var vPosition = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray( vPosition );  

    var eventBuffer = gl.createBuffer();//
    gl.bindBuffer( gl.ARRAY_BUFFER, eventBuffer);
    gl.bufferData( gl.ARRAY_BUFFER, 8*maxNumVertices, gl.STATIC_DRAW );

    vTransLoc = gl.getUniformLocation( program, "vTrans" );
    xDirLoc = gl.getUniformLocation(program, "xDir");


    render_santa(vertex_santa);
};

function render_santa(vertex) {
    var ifIter=false;//
    /*if(Math.abs(mouse[0]-currentValue[0])>0.3){
        vTrans[0]+=0.01*translation[0];//currentValue[0]+=0.05*vTrans[0];
        //currentValue[0]+=vTrans[0];
        ifIter=true;
    }
    if(Math.abs(mouse[1]-currentValue[1])>0.3){
        vTrans[1]+=0.01*translation[1];//currentValue[1]+=0.05*vTrans[1];
        //currentValue[1]+=vTrans[1];
        ifIter=true;
    }*/
    /*if(vTrans[0]<translation[0]){
        vTrans[0]+=0.05*translation[0];//currentValue[0]+=0.05*vTrans[0];
        currentValue[0]+=0.05*translation[0];//vTrans[0];
        ifIter=true;
    }
    if(vTrans[1]<translation[1]){
        vTrans[1]+=0.05*translation[1];//currentValue[1]+=0.05*vTrans[1];
        currentValue[1]+=0.05*translation[1];//vTrans[1];
        ifIter=true;
    }*/
    if(Math.abs(offset[0])<Math.abs(translation[0] && iterNum<20)){
        offset[0]+=0.05*translation[0];//currentValue[0]+=0.05*vTrans[0];
        currentValue[0]+=0.05*translation[0];//vTrans[0];
        ifIter=true;
    }
    else{
        ifIter=false;
    }
    if(Math.abs(offset[1])<Math.abs(translation[1] && iterNum<20)){
        offset[1]+=0.05*translation[1];//currentValue[1]+=0.05*vTrans[1];
        currentValue[1]+=0.05*translation[1];//vTrans[1];
        ifIter=true;
    }else{
        ifIter=false;
    }

    if(ifIter==true){
        iterNum++;//
        //vTrans=currentValue;
    }
    else if (ifIter==false){
        vTrans=currentValue;//
        offset=vec2(0.0,0.0);
    }

    gl.uniform1f(xDirLoc, xDir);
    gl.uniform2fv(vTransLoc,vTrans);

    document.getElementById("blank").innerHTML=iterNum+":"+vTrans;//currentValue;
    sleep(100);

	gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLES, 0, numVertices_santa);
    requestAnimFrame( render_santa );
}
function sleep(delay) {
    var start=new Date().getTime();
    while(new Date().getTime()<start+delay);
}