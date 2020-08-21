
var gl;
var points;

window.onload = function init()
{
    var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    
    var vertices = new Float32Array([
        -0.6,1,-0.6,0,0.9,1,0.9,1,-0.6,0,0.9,0,//face
        -0.1,-0.6,-0.1,-0.8,0,-0.6,-0.1,-0.8,0,-0.6,0,-0.8,
        0.2,-0.6,0.2,-0.8,0.3,-0.6,0.2,-0.8,0.3,-0.6,0.3,-0.8,//2 legs

        //body
-0.3,0,-0.3,-0.6,0.6,0,0.6,0,-0.3,-0.6,0.6,-0.6,
//hat
-0.8,0.9,-0.8,0.8,-0.6,1,
-0.6,1,-0.8,0.8,0.9,1,
-0.8,0.8,0.9,1,0.9,0.8,

//hat_fur
-0.9,0.9,-0.9,0.8,-0.8,0.9,-0.9,0.8,-0.8,0.9,-0.8,0.8,//
-0.5,0.9,-0.5,0.7,0.8,0.9,
-0.5,0.7,0.8,0.9,0.8,0.7,//
-0.6,0.8,-0.6,0.6,-0.4,0.8,
-0.6,0.6,-0.5,0.6,-0.5,0.7,
-0.5,0.7,-0.4,0.7,-0.4,0.8,//
0.7,0.8,0.9,0.8,0.9,0.6,
0.7,0.8,0.7,0.7,0.8,0.7,
0.8,0.7,0.8,0.6,0.9,0.6,
//beard
-0.6,0.4,-0.6,0,0.9,0.4,-0.6,0,0.9,0.4,0.9,0,
-0.4,0,-0.4,-0.1,0.7,0,-0.4,-0.1,0.7,0,0.7,-0.1,
-0.2,-0.1,-0.2,-0.2,0.5,-0.1,-0.2,-0.2,0.5,-0.1,0.5,-0.2,
0,-0.2,0,-0.3,0.3,-0.2,0,-0.3,0.3,-0.2,0.3,-0.3,

//belt_buckle
0.1,-0.3,0.1,-0.6,0.4,-0.3,0.1,-0.6,0.4,-0.3,0.4,-0.6,

//eye
-0.3,0.7,-0.3,0.4,0,0.7,-0.3,0.4,0,0.7,0,0.4,
0.3,0.7,0.3,0.4,0.6,0.7,0.3,0.4,0.6,0.7,0.6,0.4,

//eye_black
-0.2,0.6,-0.2,0.4,0,0.6,-0.2,0.4,0,0.6,0,0.4,
0.4,0.6,0.4,0.4,0.6,0.6,0.4,0.4,0.6,0.6,0.6,0.4,
//mouth
0,0.3,0,0.2,0.3,0.3,0,0.2,0.3,0.3,0.3,0.2,
//belt
-0.3,-0.4,-0.3,-0.5,0.1,-0.4,-0.3,-0.5,0.1,-0.4,0.1,-0.5,
0.2,-0.4,0.2,-0.5,0.3,-0.4,0.2,-0.5,0.3,-0.4,0.3,-0.5,
0.4,-0.4,0.4,-0.5,0.6,-0.4,0.4,-0.5,0.6,-0.4,0.6,-0.5,

//boots
-0.1,-0.7,-0.1,-0.9,0,-0.7,-0.1,-0.9,0,-0.7,0,-0.9,
0,-0.8,0,-0.9,0.1,-0.8,0,-0.9,0.1,-0.8,0.1,-0.9,
0.2,-0.7,0.2,-0.9,0.3,-0.7,0.2,-0.9,0.3,-0.7,0.3,-0.9,
0.3,-0.8,0.3,-0.9,0.4,-0.8,0.3,-0.9,0.4,-0.8,0.4,-0.9
]);
    //  Configure WebGL
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0.0, 0.0, 0.0, 1.0 );
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
    gl.uniform4fv(colorLoc, [0.91, 0.76, 0.65, 1.0]);//skinColor
    gl.clear( gl.COLOR_BUFFER_BIT );
    gl.drawArrays( gl.TRIANGLES, 0, 18 );//6+12
    //render();
    
    gl.uniform4fv(colorLoc, [ 1, 0.2, 0.0, 1.0]);//red
    gl.drawArrays( gl.TRIANGLES, 18, 15 );//6+9
    //renderBodyHat();
    gl.uniform4fv(colorLoc, [1.0, 1.0, 1.0, 1.0]);//white
    gl.drawArrays( gl.TRIANGLES, 33, 54 );//6+24+24
    //renderFurBeard();
    gl.uniform4fv(colorLoc, [ 1.0, 1.0, 0.0, 1.0]);//yellow
    gl.drawArrays( gl.TRIANGLES, 87, 6 );//6
    //renderBuckle();
    gl.uniform4fv(colorLoc, [ 0.74902, 0.847059, 0.847059, 1.0]);//skyBlue
    gl.drawArrays( gl.TRIANGLES, 93, 12 );//6+6
    //renderEyes();
    gl.uniform4fv(colorLoc, [ 0.0, 0.0, 0.0, 1.0]);//black
    gl.drawArrays( gl.TRIANGLES, 105, 36 );//6+6+6+18
    //renderBlack();
    gl.uniform4fv(colorLoc, [ 0.647059, 0.164706, 0.164706, 1.0]);//brown
    gl.drawArrays( gl.TRIANGLES, 141, 24 );//12+12
    //renderBoots();

    /*
    var vertices = new Float32Array([-0.3,0,-0.3,-0.6,0.6,0,0.6,0,-0.3,-0.6,0.6,-0.6,
        -0.8,0.9,-0.8,0.8,-0.6,1,
        -0.6,1,-0.8,0.8,0.9,1,
        -0.8,0.8,0.9,1,0.9,0.8]);
    //  Configure WebGL
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );
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
    gl.uniform4fv(colorLoc, [ 1, 0.2, 0.0, 1.0]);//red
    renderBodyHat();

    var vertices = new Float32Array([-0.9,0.9,-0.9,0.8,-0.8,0.9,-0.9,0.8,-0.8,0.9,-0.8,0.8,
-0.5,0.9,-0.5,0.7,0.8,0.9,
-0.5,0.7,0.8,0.9,0.8,0.7,
-0.6,0.8,-0.6,0.6,-0.4,0.8,
-0.6,0.6,-0.5,0.6,-0.5,0.7,
-0.5,0.7,-0.4,0.7,-0.4,0.8,
0.7,0.8,0.9,0.8,0.9,0.6,
0.7,0.8,0.7,0.7,0.8,0.7,
0.8,0.7,0.8,0.6,0.9,0.6,//hat fur
-0.6,0.4,-0.6,0,0.9,0.4,
-0.6,0,0.9,0.4,0.9,0,
-0.4,0,-0.4,-0.1,0.7,0,
-0.4,-0.1,0.7,0,0.7,-0.1,
-0.2,-0.1,-0.2,-0.2,0.5,-0.1,
-0.2,-0.2,0.5,-0.1,0.5,-0.2,
0,-0.2,0,-0.3,0.3,-0.2,
0,-0.3,0.3,-0.2,0.3,-0.3]);//beard
    //  Configure WebGL
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );
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
    gl.uniform4fv(colorLoc, [1.0, 1.0, 1.0, 1.0]);//white
    renderFurBeard();

    var vertices = new Float32Array([0.1,-0.3,0.1,-0.6,0.4,-0.3,0.1,-0.6,0.4,-0.3,0.4,-0.6]);//belt buckle
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );
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
    gl.uniform4fv(colorLoc, [ 1.0, 1.0, 0.0, 1.0]);//yellow
    renderBuckle();

    var vertices = new Float32Array([-0.3,0.7,-0.3,0.4,0,0.7,-0.3,0.4,0,0.7,0,0.4,
0.3,0.7,0.3,0.4,0.6,0.7,0.3,0.4,0.6,0.7,0.6,0.4]);//left-right eyes
    //  Configure WebGL
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );
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
    gl.uniform4fv(colorLoc, [ 0.74902, 0.847059, 0.847059, 1.0]);//skyBlue
    renderEyes();

    var vertices = new Float32Array([-0.2,0.6,-0.2,0.4,0,0.6,-0.2,0.4,0,0.6,0,0.4,
0.4,0.6,0.4,0.4,0.6,0.6,0.4,0.4,0.6,0.6,0.6,0.4,
0,0.3,0,0.2,0.3,0.3,0,0.2,0.3,0.3,0.3,0.2,
-0.3,-0.4,-0.3,-0.5,0.1,-0.4,-0.3,-0.5,0.1,-0.4,0.1,-0.5,
0.2,-0.4,0.2,-0.5,0.3,-0.4,0.2,-0.5,0.3,-0.4,0.3,-0.5,
0.4,-0.4,0.4,-0.5,0.6,-0.4,0.4,-0.5,0.6,-0.4,0.6,-0.5]);//left_right eyes,mouth,belt
    //  Configure WebGL
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );
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
    gl.uniform4fv(colorLoc, [ 0.0, 0.0, 0.0, 1.0]);//black
    renderBlack();

    var vertices = new Float32Array([-0.1,-0.7,-0.1,-0.9,0,-0.7,-0.1,-0.9,0,-0.7,0,-0.9,
0,-0.8,0,-0.9,0.1,-0.8,0,-0.9,0.1,-0.8,0.1,-0.9,
0.2,-0.7,0.2,-0.9,0.3,-0.7,0.2,-0.9,0.3,-0.7,0.3,-0.9,
0.3,-0.8,0.3,-0.9,0.4,-0.8,0.3,-0.9,0.4,-0.8,0.4,-0.9]);//left_right boots
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );
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
    gl.uniform4fv(colorLoc, [ 0.647059, 0.164706, 0.164706, 1.0]);//brown
    renderBoots();*/
};


function render() {
    gl.clear( gl.COLOR_BUFFER_BIT );
    gl.drawArrays( gl.TRIANGLES, 0, 18 );//6+12
}
function renderBodyHat() {
    gl.drawArrays( gl.TRIANGLES, 0, 15 );//6+9
}
function renderFurBeard() {
    gl.drawArrays( gl.TRIANGLES, 0, 54 );//6+24+24
}
function renderBuckle() {
    gl.drawArrays( gl.TRIANGLES, 0, 6 );//6
}
function renderEyes() {
    gl.drawArrays( gl.TRIANGLES, 0, 12 );//6+6
}
function renderBlack() {
    gl.drawArrays( gl.TRIANGLES, 0, 36 );//6+6+6+18
}
function renderBoots() {
    gl.drawArrays( gl.TRIANGLES, 0, 24 );//12+12
}
