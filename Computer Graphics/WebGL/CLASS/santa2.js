var gl;

var colors = [];
var  numVertices_santa=231*2;

var xDir= 1;
var xDirLoc;

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

window.onload = function init()
{
    var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

	//length_index: stars[0~47],house[+12*(4+8+4+2.5)],smoke[+12*7] //일단 vertex계산해서 써봤는데 틀린 부분 있으면
	// TODO: 맨 마지막은 smoke라고 생각하고 써야해요
	//var length = [18,15,54,6,12,36,24];
	var length = [24,36,12,6,54,15,18];
	for (var i=0; i< colorArray_santa.length; i++) {
		for (var j=0; j<length[i]; j++){
			colors.push(colorArray_santa[i]);
		}		
	}
    
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

    xDirLoc = gl.getUniformLocation(program, "xDir");
    document.getElementById( "xButton" ).onclick = function () {
        xDir=xDir*-1;
    };

    render_santa(vertex_santa);
};

function render_santa(vertex) {
	gl.uniform1f(xDirLoc, xDir);

	gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLES, 0, numVertices_santa);
    requestAnimFrame( render_santa );
}