
var gl = null;
var glCanvas = null;

// Aspect ratio and coordinate system
// details

var aspectRatio;
var currentRotation = [0, 1];
var currentScale = [1.0, 1.0];

// Vertex information

var vertexArray;
var vertexBuffer;
var vertexNumComponents;
var vertexCount;

// Rendering data shared with the
// scalers.

var uScalingFactor;
var uGlobalColor;
var uRotationVector;
var aVertexPosition;

// Animation timing

var previousTime = 0.0;
var degreesPerSecond = 90.0;

window.onload = function init()
{
    /*var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    
    var triangle = new Float32Array([
        -1,-1,0,0.5,1,-1,
        -0.5,-0.25,0.5,-0.25,0,-1]);
    var vertices=[vec3(0.0,0.0,-1.0),
    vec3()];
    //  Configure WebGL
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 0.0, 0.0, 0.0, 1.0 );//black
    //  Load shaders and initialize attribute buffers
    var program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );
    // Load the data into the GPU
    var bufferId = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, bufferId );
    gl.bufferData( gl.ARRAY_BUFFER,triangle, gl.STATIC_DRAW );
    // Associate out shader variables with our data buffer
    var vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 2, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );
    var colorLoc = gl.getUniformLocation(program, "color");
    gl.uniform4fv(colorLoc, [1.0, 0.0, 0.0, 1.0]);//skinColor
    gl.clear( gl.COLOR_BUFFER_BIT );
    gl.drawArrays( gl.TRIANGLES, 0, 3 );//6 //render();

    gl.uniform4fv(colorLoc, [1.0, 1.0, 1.0, 1.0]);//skinColor
    gl.drawArrays( gl.TRIANGLES, 3, 3 );//gasket 여기까지
    */

    glCanvas = document.getElementById("glcanvas");
  gl = glCanvas.getContext("webgl");

  const shaderSet = [
    {
      type: gl.VERTEX_SHADER,
      id: "vertex-shader"
    },
    {
      type: gl.FRAGMENT_SHADER,
      id: "fragment-shader"
    }
  ];

  shaderProgram = buildShaderProgram(shaderSet);

  aspectRatio = glCanvas.width/glCanvas.height;
  currentRotation = [0, 1];
  currentScale = [1.0, aspectRatio];

  vertexArray = new Float32Array([
      -0.5, 0.5, 0.5, 0.5, 0.5, -0.5,
      -0.5, 0.5, 0.5, -0.5, -0.5, -0.5
  ]);

  vertexBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, vertexArray, gl.STATIC_DRAW);

  vertexNumComponents = 2;
  vertexCount = vertexArray.length/vertexNumComponents;

  currentAngle = 0.0;
  rotationRate = 6;

  animateScene();
  /*
    var vertices;
    var thetaMax=100;
    var dtheta=0.001;
    for(var theta=0.0;theta<thetaMax;theta+=dtheta) {
        vertices[0]=vec2(Math.sin(theta),Math.cos(theta));
        vertices[1]=vec2(Math.sin(theta),-Math.cos(theta));
        vertices[2]=vec2(-Math.sin(theta),-Math.cos(theta));
        vertices[3]=vec2(-Math.sin(theta),Math.cos(theta));
    }*/
         //  Configure WebGL

};
function buildShaderProgram(shaderInfo) {
  var program = gl.createProgram();

  shaderInfo.forEach(function(desc) {
    var shader = compileShader(desc.id, desc.type);
    if (shader) {
        gl.attachShader(program, shader);}});

  gl.linkProgram(program)

  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.log("Error linking shader program:");
    console.log(gl.getProgramInfoLog(program));
  }

  return program;
}
function compileShader(id, type) {
  var code = document.getElementById(id).firstChild.nodeValue;
  var shader = gl.createShader(type);

  gl.shaderSource(shader, code);
  gl.compileShader(shader);

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.log(`Error compiling ${type === gl.VERTEX_SHADER ? "vertex" : "fragment"} shader:`);
    console.log(gl.getShaderInfoLog(shader));
  }
  return shader;
}
function animateScene() {
  gl.viewport(0, 0, glCanvas.width, glCanvas.height);
  gl.clearColor(0.8, 0.9, 1.0, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);

  var radians = currentAngle * Math.PI / 180.0;
  currentRotation[0] = Math.sin(radians);
  currentRotation[1] = Math.cos(radians);

  gl.useProgram(shaderProgram);

  uScalingFactor =
      gl.getUniformLocation(shaderProgram, "uScalingFactor");
  uGlobalColor =
      gl.getUniformLocation(shaderProgram, "uGlobalColor");
  uRotationVector =
      gl.getUniformLocation(shaderProgram, "uRotationVector");

  gl.uniform2fv(uScalingFactor, currentScale);
  gl.uniform2fv(uRotationVector, currentRotation);
  gl.uniform4fv(uGlobalColor, [0.1, 0.7, 0.2, 1.0]);

  gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);

  aVertexPosition =
      gl.getAttribLocation(shaderProgram, "aVertexPosition");

  gl.enableVertexAttribArray(aVertexPosition);
  gl.vertexAttribPointer(aVertexPosition, vertexNumComponents,
        gl.FLOAT, false, 0, 0);

  gl.drawArrays(gl.TRIANGLES, 0, vertexCount);

  window.requestAnimationFrame(function(currentTime) {
    var deltaAngle = ((currentTime - previousTime) / 1000.0)
          * degreesPerSecond;

    currentAngle = (currentAngle + deltaAngle) % 360;

    previousTime = currentTime;
    animateScene();
  });
}

function cos(angle) {
    return Math.cos(angle);
}
function sin(angle) {
    return Math.sin(angle);
}
function render() {
    gl.clear(gl.COLOR_BUFFER_FIT);
    theta+=0.1;
    gl.uniform1f(thetaLoc,theta);
    gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
    render();//recursive
}
/*
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