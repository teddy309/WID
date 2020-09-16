var gl;

var colors = [];
var  numVertices_santa=165;//231;
var  numVertices_rudolf=102;

var xDir= 1;
var xDirLoc;
var vTrans=[];
var vTransLoc;

var mouse=[];
var mouseLoc;

//vertex,color for house
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

var vertex_rudolf = new Float32Array([
//// rodulf ////
      0.58, -0.605, 0.6, -0.605, 0.58, -0.625, //left black eye
        0.6, -0.605, 0.58, -0.625, 0.6, -0.625,

        0.65, -0.605, 0.67, -0.605, 0.65, -0.625, //right black eye
        0.67, -0.605, 0.65, -0.625, 0.67, -0.625,

        0.525, -0.5925, 0.55, -0.5925, 0.55, -0.61, //left pink ear

        0.7, -0.5925, 0.725, -0.5925, 0.7, -0.61, //right pink ear

        0.6075, -0.68, 0.6425, -0.68, 0.625, -0.69, //tongue

      0.57, -0.6, 0.61, -0.6, 0.57, -0.63, //left white eye
        0.61, -0.6, 0.57, -0.63, 0.61, -0.63,

        0.64, -0.6, 0.68, -0.6, 0.64, -0.63, //right white eye
        0.68, -0.6, 0.64, -0.63, 0.68, -0.63,

        0.61, -0.64, 0.64, -0.64, 0.61, -0.665, //nose
        0.64, -0.64, 0.61, -0.665, 0.64, -0.665,

        0.59, -0.67, 0.66, -0.67, 0.625, -0.69, //mouth

      0.55, -0.575, 0.7, -0.575, 0.55, -0.7, //face
        0.7, -0.575, 0.55, -0.7, 0.7, -0.7,
      
      0.625, -0.7, 0.875, -0.7, 0.625, -0.8, //body
        0.875, -0.7, 0.625, -0.8, 0.875, -0.8,

      0.875, -0.68, 0.915, -0.68, 0.875, -0.72, //tail
        0.915, -0.68, 0.875, -0.72, 0.915, -0.72,
   
      0.625, -0.8, 0.65, -0.8, 0.625, -0.9, //front leg
        0.65, -0.8, 0.675, -0.8, 0.65, -0.9,

      0.825, -0.8, 0.85, -0.8, 0.825, -0.9, //rear leg 
        0.85, -0.8, 0.875, -0.8, 0.85, -0.9,

      0.5, -0.575, 0.55, -0.575, 0.55, -0.61, //left ear

        0.7, -0.575, 0.75, -0.575, 0.7, -0.61, //right ear

      0.565, -0.45, 0.6, -0.45, 0.565, -0.575, //left horn
        0.6, -0.45, 0.565, -0.575, 0.6, -0.575,

        0.65, -0.45, 0.685, -0.45, 0.65, -0.575, //right horn
        0.685, -0.45, 0.65, -0.575, 0.685, -0.575,

        0.53, -0.485, 0.565, -0.485, 0.53, -0.52, //left small horn
        0.565, -0.485, 0.53, -0.52, 0.565, -0.52,

        0.685, -0.485, 0.72, -0.485, 0.685, -0.52, //right small horn
        0.72, -0.485, 0.685, -0.52, 0.72, -0.52
    ]);
var colorArray_rudolf = [
    /*[0.6, 0.27, 0, 1],//face
    [0.3, 0.15, 0, 1],//left horn
    [0.3, 0.15, 0, 1],//right horn
    [0.3, 0.15, 0, 1],//left small horn
    [0.3, 0.15, 0, 1],//right small horn
    [0.6, 0.27, 0, 1],//ear
    [1, 1, 1, 1],//left white eye
    [1, 1, 1, 1],//right white eye
    [1, 0, 0, 1],//red nose
    [0.9, 0.9, 0.9, 1],//mouth
    [0, 0, 0, 1],//black eye
    [1, 0.5, 0.5, 1],//pink ear, tongue
    [0.6, 0.27, 0, 1]//body & leg & tail*/
    [0, 0, 0, 1], //black eye
    [1, 0.5, 0.5, 1], //pink ear, tongue
    [1, 1, 1, 1], //white eye
    [1, 0, 0, 1], //red nose
    [0.9, 0.9, 0.9, 1], //mouth
    [0.6, 0.27, 0, 1], //face & body
    [0.3, 0.15, 0, 1], //horn
    ];
var length_rudolf = [12, 9, 12, 6, 3, 36, 24];//[6,6,6,6,6,6,6,6,6,6,12,9,24];//
for (var i=0; i< colorArray_santa.length; i++) {
    for (var j=0; j<length_rudolf[i]; j++){
        colors.push(colorArray_rudolf[i]);
    }       
}
//resize and relocation to rudolf
    /*for (var i = 0; i < vertex_rudolf.length; i++) {
        if (i % 2 == 0) {// x
            vertex_rudolf[i] += 0.2;
        }
        else { //y
            vertex_rudolf[i] += -0.3;
        }
    }*/

window.onload = function init()
{
    var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    /*canvas.addEventListener("mousedown", function(event){
        gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );//
        var t = vec2(2*event.clientX/canvas.width-1,
           2*(canvas.height-event.clientY)/canvas.height-1);
        gl.bufferSubData(gl.ARRAY_BUFFER, 8*index, flatten(t));

        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
        t = vec4(colors[(index)%7]);
        gl.bufferSubData(gl.ARRAY_BUFFER, 16*index, flatten(t));
        index++;
    } );*/
    
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
	gl.bufferData(gl.ARRAY_BUFFER, vertex_santa, gl.STATIC_DRAW);

    // Associate out shader variables with our data buffer   	
	// attribute variable
    var vPosition = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray( vPosition );  

    vTransLoc = gl.getUniformLocation( program, "vTrans" );
    xDirLoc = gl.getUniformLocation(program, "xDir");
    document.getElementById( "xButton" ).onclick = function () {
        xDir=xDir*-1;
        vTrans=vec2(0.1,0.1);//
        document.getElementById("blank").innerHTML="color array size: "+colors.length;
    };

    

    render_santa(vertex_santa);
    //render_rudolf(vertex_rudolf);
};

function render_santa(vertex) {
	gl.uniform1f(xDirLoc, xDir);
    gl.uniform2fv(vTransLoc,vTrans);

	gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLES, 0, numVertices_santa);
    requestAnimFrame( render_santa );
}
function render_rudolf(vertex) {

    //gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLES, numVertices_santa, numVertices_rudolf);
    requestAnimFrame( render_rudolf );
}