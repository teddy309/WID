
var gl;
var points;

window.onload = function init()
{
    var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    
    var vertices = new Float32Array([
        -0.5,0.5,0.5,0.5,0.5,-0.5,0.5,-0.5,-0.5,0.5,-0.5,-0.5//square
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
    gl.drawArrays( gl.TRIANGLES, 0, 6 );//6//render();
    
    //randomRender();

    /*
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
    //renderBoots();*/
};


function render() {
    gl.clear( gl.COLOR_BUFFER_BIT );
    gl.drawArrays( gl.TRIANGLES, 0, 6 );//6+12
}/*
function setRectangle(model,a,b,c,d) {
    var vertices = new Float32Array([
        -1*a,b,c,d,c,-1*d, -1*a,b,c,-d,-1*a,-1*b//square
        ]);
    var size = Math.random();
    for (var i = 0; i <6; i++) {
        vertices[i] *= size;
        if (i % 2 == 0) {// x
            vertices[i] += Math.random();
        }
        else { //y
            vertices[i] += Math.random();

        }
    }
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
}
function randomRender() {
    for (var i=0;i<50;++i){
        setRactangle(gl,Math.random(),Math.random(),Math.random(),Math.random());//set 2angles,size random
        var colorLoc = gl.getUniformLocation(program, "color");
        gl.uniform4fv(colorLoc,[Math.random(),Math.random(),Math.random(),1.0]);//set RGB random
        var primitiveType=gl.TRIANGLES;
        var offset=0;
        car count=6;
        gl.drawArrays(primitiveType,offset,count);
    }
}*/