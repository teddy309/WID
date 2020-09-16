
var gl;
var points;

window.onload = function init()//When brower opened
{
    var canvas = document.getElementById( "gl-canvas" );//reference canvas at html File
    
    gl = WebGLUtils.setupWebGL( canvas );//interface to OpenGL graphic rendering context on HTML canvas
    if ( !gl ) { alert( "WebGL isn't available" ); }

    //clipsace=-1~1
    var vertices = [ //3개 vertex 좌표 사용.
    vec2(0,0.5),
    vec2(-0.5,-0.5),
    vec2(0.5,-0.5)
    ];

    var colors=[ //R,G,B
    vec4(1.0,0.0,0.0,1.0),
    vec4(0.0,1.0,0.0,1.0),
    vec4(0.0,0.0,1.0,1.0)
    ];

    //  Configure WebGL(setting)
    gl.viewport( 0, 0, canvas.width, canvas.height );//match canvas-GPU
    gl.clearColor( 0.0, 0.0, 0.0, 1.0 );//canvas color: black
    
    //  Load shaders and initialize attribute buffers
    var program = initShaders( gl, "vertex-shader", "fragment-shader" );
    //make WebGL to run Shader program
    gl.useProgram( program );

    
    // Load the data into the GPU
    var vertexPositionBufferId = gl.createBuffer();//Load data onto GPU(buffer object on GPU)
    gl.bindBuffer( gl.ARRAY_BUFFER, vertexPositionBufferId );//bind 2 points
    gl.bufferData( gl.ARRAY_BUFFER,flatten(vertices), gl.STATIC_DRAW );
    //copy data to &bufferId on GPU. 
    //flatten(JS array->array float32) to readable for GPU
    //how to use data. here data is static.

    // Associate out shader variables with our data buffer
    var vPosition = gl.getAttribLocation( program, "vPosition" );
    //connect variables in shader and program
    gl.vertexAttribPointer( vPosition, 2, gl.FLOAT, false, 0, 0 );
    //how to get data from buffer(location,size,type,normalize,stride,offset)
    gl.enableVertexAttribArray( vPosition );


    var vertexColorBufferId=gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER,vertexColorBufferId);
    gl.bufferData(gl.ARRAY_BUFFER,flatten(colors),gl.STATIC_DRAW);

    var vColor = gl.getAttribLocation( program, "vColor" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor );

    render();
};

function render() {
    gl.clear( gl.COLOR_BUFFER_BIT );
    gl.drawArrays( gl.TRIANGLE_FAN, 0, 3 );//(primitiveType,offset,count)
}
