var gl;

var colors = [];
var  numVertices=231;

var vertex = [
    //santa
    -0.6, 1, -0.6, 0, 0.9, 1, 0.9, 1, -0.6, 0, 0.9, 0,//face
    -0.1, -0.6, -0.1, -0.8, 0, -0.6, -0.1, -0.8, 0, -0.6, 0, -0.8,
    0.2, -0.6, 0.2, -0.8, 0.3, -0.6, 0.2, -0.8, 0.3, -0.6, 0.3, -0.8,//2 legs

    //body
    -0.3, 0, -0.3, -0.6, 0.6, 0, 0.6, 0, -0.3, -0.6, 0.6, -0.6,
    //hat
    -0.8, 0.9, -0.8, 0.8, -0.6, 1,
    -0.6, 1, -0.8, 0.8, 0.9, 1,
    -0.8, 0.8, 0.9, 1, 0.9, 0.8,

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

        //belt_buckle
    0.1, -0.3, 0.1, -0.6, 0.4, -0.3, 0.1, -0.6, 0.4, -0.3, 0.4, -0.6,

    //eye
    -0.3, 0.7, -0.3, 0.4, 0, 0.7, -0.3, 0.4, 0, 0.7, 0, 0.4,
    0.3, 0.7, 0.3, 0.4, 0.6, 0.7, 0.3, 0.4, 0.6, 0.7, 0.6, 0.4,

    //eye_black
    -0.2, 0.6, -0.2, 0.4, 0, 0.6, -0.2, 0.4, 0, 0.6, 0, 0.4,
    0.4, 0.6, 0.4, 0.4, 0.6, 0.6, 0.4, 0.4, 0.6, 0.6, 0.6, 0.4,
    //mouth
    0, 0.3, 0, 0.2, 0.3, 0.3, 0, 0.2, 0.3, 0.3, 0.3, 0.2,
    //belt
    -0.3, -0.4, -0.3, -0.5, 0.1, -0.4, -0.3, -0.5, 0.1, -0.4, 0.1, -0.5,
    0.2, -0.4, 0.2, -0.5, 0.3, -0.4, 0.2, -0.5, 0.3, -0.4, 0.3, -0.5,
    0.4, -0.4, 0.4, -0.5, 0.6, -0.4, 0.4, -0.5, 0.6, -0.4, 0.6, -0.5,

        //boots
    -0.1, -0.7, -0.1, -0.9, 0, -0.7, -0.1, -0.9, 0, -0.7, 0, -0.9,
    0, -0.8, 0, -0.9, 0.1, -0.8, 0, -0.9, 0.1, -0.8, 0.1, -0.9,
    0.2, -0.7, 0.2, -0.9, 0.3, -0.7, 0.2, -0.9, 0.3, -0.7, 0.3, -0.9,
    0.3, -0.8, 0.3, -0.9, 0.4, -0.8, 0.3, -0.9, 0.4, -0.8, 0.4, -0.9
];

var colorArray=[
    [0.91, 0.76, 0.65, 1.0],//skinColor
    [1, 0.2, 0.0, 1.0],//red
    [1.0, 1.0, 1.0, 1.0],//white
    [1.0, 1.0, 0.0, 1.0],//yellow
    [0.74902, 0.847059, 0.847059, 1.0],//skyBlue
    [0.0, 0.0, 0.0, 1.0],//black
    [0.647059, 0.164706, 0.164706, 1.0]//brown
];

window.onload = function init()
{
    var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    var length = [18,15,54,6,12,36,24];
    for (var i=0; i< colorArray.length; i++) {
        for (var j=0; j<length[i]; j++){
            colors.push(colorArray[i]);
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
    gl.bufferData(gl.ARRAY_BUFFER, vertex, gl.STATIC_DRAW);

    // Associate out shader variables with our data buffer      
    // attribute variable
    var vPosition = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray( vPosition );  

    render());
};

function render() {
    // clear buffer bit
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLES, 0, numVertices);
    requestAnimFrame( render_house );
    /*
    gl.uniform4f(vColor, 0.91, 0.76, 0.65, 1.0);//skinColor
    gl.drawArrays(gl.TRIANGLES, 0, 18);//6+12

    gl.uniform4f(vColor, 1, 0.2, 0.0, 1.0);//red
    gl.drawArrays(gl.TRIANGLES, 18, 15);//6+9
    //renderBodyHat();
    gl.uniform4f(fColor, 1.0, 1.0, 1.0, 1.0);//white
    gl.drawArrays(gl.TRIANGLES, 33, 54);//6+24+24
    //renderFurBeard();
    gl.uniform4f(fColor,1.0, 1.0, 0.0, 1.0);//yellow
    gl.drawArrays(gl.TRIANGLES, 87, 6);//6
    //renderBuckle();
    gl.uniform4f(fColor, 0.74902, 0.847059, 0.847059, 1.0);//skyBlue
    gl.drawArrays(gl.TRIANGLES, 93, 12);//6+6
    //renderEyes();
    gl.uniform4f(fColor, 0.0, 0.0, 0.0, 1.0);//black
    gl.drawArrays(gl.TRIANGLES, 105, 36);//6+6+6+18
    //renderBlack();
    gl.uniform4f(fColor, 0.647059, 0.164706, 0.164706, 1.0);//brown
    gl.drawArrays(gl.TRIANGLES, 141, 24);//12+12
    */
}
