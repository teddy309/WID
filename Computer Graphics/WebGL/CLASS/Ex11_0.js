
var gl = null;
var glCanvas = null;

var renderPolygon=false;

var myButton=document.getElementById("drawPolygon");
myButton.addEventListener("click",function(){
  renderPolygon=!renderPolygon;
});

/*var colorPick=[
[0.0,0.0,0.0,1.0],
[1.0,0.0,0.0,1.0],
[0.0,1.0,1.0,1.0],
[0.0,1.0,0.0,1.0],
[0.0,0.0,1.0,1.0],
[0.0,0.0,0.0,1.0],
[0.0,0.0,0.0,1.0]];
var colorMenu=document.getElementById("colorPick");
colorMenu.addEventListener("click",function(){
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
  }
});*/

window.onload = function init()
{
   var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    
    var vertices = new Float32Array([-0.5, 0.5, 0, 1, 0.5, 0.5]);

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
    gl.uniform4fv(colorLoc, [0.0, 1.0, 0.0, 1.0]);

    render();

};//end window.onload()

function cos(angle) {
    return Math.cos(angle);
}
function sin(angle) {
    return Math.sin(angle);
}
function render() {
  
  gl.clear( gl.COLOR_BUFFER_BIT );
  gl.drawArrays( gl.TRIANGLES, 0, 3);
}
function renderPolygon(num){
  if(renderPolygon){
    //draw
  }
  gl.drawArrays( gl.TRIANGLES, 0, 9 );
}