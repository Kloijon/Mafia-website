<template>
  <canvas ref="canvasRef" class="fluid-smoke"></canvas>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

const canvasRef = ref<HTMLCanvasElement | null>(null);

// ----------------------------------------------
//  Реалистичные настройки с БОЛЬШИМ размером дыма
// ----------------------------------------------
const config = {
  SIM_RESOLUTION: 128,
  DYE_RESOLUTION: 528,

  DENSITY_DISSIPATION: 0.996,

  VELOCITY_DISSIPATION: 0.99,
  PRESSURE_ITERATIONS: 20, // Если компьютер мощный, можно поставить 20-30 для более плавных клубов

  // ✅ Сила выброса дыма и скорости. 250 создаст очень плотные клубы
  SPLAT_FORCE: 250,

  SPLAT_RADIUS: 0.15,
  CURL: 8, // Оставляем 12 — отличные клубы

  COLOR: { r: 0.7, g: 0.7, b: 0.7 },
};

let gl: WebGL2RenderingContext | null = null;

// ping‑pong текстуры
let density: WebGLTexture | null = null;
let densityTmp: WebGLTexture | null = null;
let velocity: WebGLTexture | null = null;
let velocityTmp: WebGLTexture | null = null;
let pressure: WebGLTexture | null = null;
let pressureTmp: WebGLTexture | null = null;
let divergence: WebGLTexture | null = null;
let curl: WebGLTexture | null = null;

let framebuffer: WebGLFramebuffer | null = null;
let framebuffer2: WebGLFramebuffer | null = null;
let screenQuad: WebGLVertexArrayObject | null = null;
let lastTime = 0;

let advectionProgram: WebGLProgram | null = null;
let pressureProgram: WebGLProgram | null = null;
let divergenceProgram: WebGLProgram | null = null;
let gradientSubtractProgram: WebGLProgram | null = null;
let vorticityProgram: WebGLProgram | null = null;
let splatProgram: WebGLProgram | null = null;
let splatVelocityProgram: WebGLProgram | null = null;
let displayProgram: WebGLProgram | null = null;
let curlProgram: WebGLProgram | null = null;

// ------------------------------------------------------------
// инициализация WebGL
// ------------------------------------------------------------
function initGL(): boolean {
  if (!canvasRef.value) return false;
  gl = canvasRef.value.getContext("webgl2", { alpha: true });
  if (!gl) {
    console.error("WebGL2 не поддерживается");
    return false;
  }
  gl.getExtension("EXT_color_buffer_float");
  gl.getExtension("OES_texture_float_linear");
  return true;
}

// ------------------------------------------------------------
// вспомогательные функции
// ------------------------------------------------------------
function createShader(source: string, type: number): WebGLShader | null {
  if (!gl) return null;
  const shader = gl.createShader(type);
  if (!shader) return null;
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error(gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
    return null;
  }
  return shader;
}

function createProgram(
  vertexSource: string,
  fragmentSource: string,
): WebGLProgram | null {
  if (!gl) return null;
  const vertexShader = createShader(vertexSource, gl.VERTEX_SHADER);
  const fragmentShader = createShader(fragmentSource, gl.FRAGMENT_SHADER);
  if (!vertexShader || !fragmentShader) return null;

  const program = gl.createProgram();
  if (!program) return null;
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error(gl.getProgramInfoLog(program));
    return null;
  }
  return program;
}

function createTexture(width: number, height: number): WebGLTexture | null {
  if (!gl) return null;
  const texture = gl.createTexture();
  if (!texture) return null;
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.texImage2D(
    gl.TEXTURE_2D,
    0,
    gl.RGBA16F,
    width,
    height,
    0,
    gl.RGBA,
    gl.FLOAT,
    null,
  );
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  return texture;
}

// ------------------------------------------------------------
// шейдеры
// ------------------------------------------------------------
function initShaders() {
  const blitVertexShader = `#version 300 es
    layout(location = 0) in vec2 aPosition;
    out vec2 vUv;
    void main() {
      vUv = aPosition * 0.5 + 0.5;
      gl_Position = vec4(aPosition, 0.0, 1.0);
    }
  `;

  const advectionFragmentShader = `#version 300 es
    precision highp float;
    uniform sampler2D uInput;
    uniform sampler2D uVelocity;
    uniform float uDt;
    uniform float uDissipation;
    uniform vec2 uTexelSize;
    in vec2 vUv;
    out vec4 fragColor;
    void main() {
      vec2 coord = vUv - uDt * texture(uVelocity, vUv).xy * uTexelSize;
      fragColor = uDissipation * texture(uInput, coord);
    }
  `;

  const divergenceFragmentShader = `#version 300 es
    precision highp float;
    uniform sampler2D uVelocity;
    uniform vec2 uTexelSize;
    in vec2 vUv;
    out vec4 fragColor;
    void main() {
      float L = texture(uVelocity, vUv - vec2(uTexelSize.x, 0.0)).x;
      float R = texture(uVelocity, vUv + vec2(uTexelSize.x, 0.0)).x;
      float T = texture(uVelocity, vUv + vec2(0.0, uTexelSize.y)).y;
      float B = texture(uVelocity, vUv - vec2(0.0, uTexelSize.y)).y;
      fragColor = vec4(0.5 * (R - L + T - B), 0.0, 0.0, 1.0);
    }
  `;

  const pressureFragmentShader = `#version 300 es
    precision highp float;
    uniform sampler2D uPressure;
    uniform sampler2D uDivergence;
    uniform vec2 uTexelSize;
    in vec2 vUv;
    out vec4 fragColor;
    void main() {
      float pL = texture(uPressure, vUv - vec2(uTexelSize.x, 0.0)).x;
      float pR = texture(uPressure, vUv + vec2(uTexelSize.x, 0.0)).x;
      float pT = texture(uPressure, vUv + vec2(0.0, uTexelSize.y)).x;
      float pB = texture(uPressure, vUv - vec2(0.0, uTexelSize.y)).x;
      float div = texture(uDivergence, vUv).x;
      fragColor = vec4((pL + pR + pT + pB - div) * 0.25, 0.0, 0.0, 1.0);
    }
  `;

  const gradientSubtractFragmentShader = `#version 300 es
    precision highp float;
    uniform sampler2D uVelocity;
    uniform sampler2D uPressure;
    uniform vec2 uTexelSize;
    in vec2 vUv;
    out vec4 fragColor;
    void main() {
      float pL = texture(uPressure, vUv - vec2(uTexelSize.x, 0.0)).x;
      float pR = texture(uPressure, vUv + vec2(uTexelSize.x, 0.0)).x;
      float pT = texture(uPressure, vUv + vec2(0.0, uTexelSize.y)).x;
      float pB = texture(uPressure, vUv - vec2(0.0, uTexelSize.y)).x;
      vec2 grad = vec2(pR - pL, pT - pB) * 0.5;
      vec2 vel = texture(uVelocity, vUv).xy;
      fragColor = vec4(vel - grad, 0.0, 1.0);
    }
  `;

  const vorticityFragmentShader = `#version 300 es
    precision highp float;
    uniform sampler2D uVelocity;
    uniform sampler2D uCurl;
    uniform float uCurlStrength;
    uniform vec2 uTexelSize;
    in vec2 vUv;
    out vec4 fragColor;
    void main() {
      float L = texture(uCurl, vUv - vec2(uTexelSize.x, 0.0)).x;
      float R = texture(uCurl, vUv + vec2(uTexelSize.x, 0.0)).x;
      float T = texture(uCurl, vUv + vec2(0.0, uTexelSize.y)).x;
      float B = texture(uCurl, vUv - vec2(0.0, uTexelSize.y)).x;
      vec2 force = 0.5 * vec2(abs(T) - abs(B), abs(R) - abs(L));
      float len = length(force);
      if (len > 0.0) force *= uCurlStrength / len;
      vec2 vel = texture(uVelocity, vUv).xy;
      vec2 noise = vec2(sin(vUv.y * 40.0), cos(vUv.x * 40.0)) * 0.003;
      fragColor = vec4(vel + force * 0.02 + noise, 0.0, 1.0);
    }
  `;

  const curlFragmentShader = `#version 300 es
    precision highp float;
    uniform sampler2D uVelocity;
    uniform vec2 uTexelSize;
    in vec2 vUv;
    out vec4 fragColor;
    void main() {
      float L = texture(uVelocity, vUv - vec2(uTexelSize.x, 0.0)).y;
      float R = texture(uVelocity, vUv + vec2(uTexelSize.x, 0.0)).y;
      float T = texture(uVelocity, vUv + vec2(0.0, uTexelSize.y)).x;
      float B = texture(uVelocity, vUv - vec2(0.0, uTexelSize.y)).x;
      fragColor = vec4(R - L - T + B, 0.0, 0.0, 1.0);
    }
  `;

  const splatFragmentShader = `#version 300 es
    precision highp float;
    uniform sampler2D uTarget;
    uniform vec2 uPoint;
    uniform vec3 uColor;
    uniform float uRadius;
    uniform float uForce;
    in vec2 vUv;
    out vec4 fragColor;
    void main() {
      vec2 coord = vUv - uPoint;
      float strength = 1.0 - smoothstep(0.0, uRadius, length(coord));
      vec4 target = texture(uTarget, vUv);
      vec3 result = target.rgb + uColor * strength * uForce;
      fragColor = vec4(result, 1.0);
    }
  `;

  const splatVelocityFragmentShader = `#version 300 es
    precision highp float;
    uniform sampler2D uTarget;
    uniform vec2 uPoint;
    uniform vec2 uColor;
    uniform float uRadius;
    uniform float uForce;
    in vec2 vUv;
    out vec4 fragColor;
    void main() {
      vec2 coord = vUv - uPoint;
      float strength = 1.0 - smoothstep(0.0, uRadius, length(coord));
      vec4 target = texture(uTarget, vUv);
      vec2 result = target.xy + uColor * strength * uForce;
      fragColor = vec4(result, 0.0, 1.0);
    }
  `;

  const displayFragmentShader = `#version 300 es
    precision highp float;
    uniform sampler2D uDensity;
    in vec2 vUv;
    out vec4 fragColor;
    void main() {
      vec3 d = texture(uDensity, vUv).rgb;
      // компрессия – дым становится более объёмным
      d = 1.0 - exp(-d * 0.8);
      vec3 color = d * 0.9;  // без экспоненциальной компрессии
			float smoke = (color.r + color.g + color.b) / 3.0;
			float alpha = clamp(smoke * 4.0, 0.0, 0.75); 
			fragColor = vec4(vec3(smoke * 0.8), alpha);
    }
  `;

  advectionProgram = createProgram(blitVertexShader, advectionFragmentShader);
  divergenceProgram = createProgram(blitVertexShader, divergenceFragmentShader);
  pressureProgram = createProgram(blitVertexShader, pressureFragmentShader);
  gradientSubtractProgram = createProgram(
    blitVertexShader,
    gradientSubtractFragmentShader,
  );
  vorticityProgram = createProgram(blitVertexShader, vorticityFragmentShader);
  splatProgram = createProgram(blitVertexShader, splatFragmentShader);
  splatVelocityProgram = createProgram(
    blitVertexShader,
    splatVelocityFragmentShader,
  );
  displayProgram = createProgram(blitVertexShader, displayFragmentShader);
  curlProgram = createProgram(blitVertexShader, curlFragmentShader);
}

// ------------------------------------------------------------
// буферы и текстуры
// ------------------------------------------------------------
function initBuffers() {
  if (!gl) return;
  const vertices = new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]);
  screenQuad = gl.createVertexArray();
  if (!screenQuad) return;
  gl.bindVertexArray(screenQuad);
  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  gl.bindVertexArray(null);
}

function initSimulation(): boolean {
  if (!gl) return false;
  const w = config.SIM_RESOLUTION;
  const h = config.SIM_RESOLUTION;
  const dw = config.DYE_RESOLUTION;
  const dh = config.DYE_RESOLUTION;

  density = createTexture(dw, dh);
  densityTmp = createTexture(dw, dh);
  velocity = createTexture(w, h);
  velocityTmp = createTexture(w, h);
  pressure = createTexture(w, h);
  pressureTmp = createTexture(w, h);
  divergence = createTexture(w, h);
  curl = createTexture(w, h);

  if (
    !density ||
    !densityTmp ||
    !velocity ||
    !velocityTmp ||
    !pressure ||
    !pressureTmp ||
    !divergence ||
    !curl
  ) {
    console.error("Failed to create textures");
    return false;
  }

  framebuffer = gl.createFramebuffer();
  framebuffer2 = gl.createFramebuffer();
  return !!(framebuffer && framebuffer2);
}

// ------------------------------------------------------------
// операции симуляции
// ------------------------------------------------------------
function splatDensity(
  x: number,
  y: number,
  color: { r: number; g: number; b: number },
  radius: number,
  force: number,
) {
  if (
    !gl ||
    !splatProgram ||
    !density ||
    !densityTmp ||
    !framebuffer2 ||
    !screenQuad
  )
    return;
  gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer2);
  gl.framebufferTexture2D(
    gl.FRAMEBUFFER,
    gl.COLOR_ATTACHMENT0,
    gl.TEXTURE_2D,
    densityTmp,
    0,
  );
  gl.viewport(0, 0, config.DYE_RESOLUTION, config.DYE_RESOLUTION);

  gl.useProgram(splatProgram);
  gl.uniform2f(gl.getUniformLocation(splatProgram, "uPoint"), x, y);
  gl.uniform3f(
    gl.getUniformLocation(splatProgram, "uColor"),
    color.r,
    color.g,
    color.b,
  );
  gl.uniform1f(gl.getUniformLocation(splatProgram, "uRadius"), radius);
  gl.uniform1f(gl.getUniformLocation(splatProgram, "uForce"), force);
  gl.uniform1i(gl.getUniformLocation(splatProgram, "uTarget"), 0);
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, density);
  gl.bindVertexArray(screenQuad);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.bindVertexArray(null);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);

  const tmp: WebGLTexture = density;
  density = densityTmp;
  densityTmp = tmp;
}

function splatVelocity(
  x: number,
  y: number,
  dirX: number,
  dirY: number,
  radius: number,
  force: number,
) {
  if (
    !gl ||
    !splatVelocityProgram ||
    !velocity ||
    !velocityTmp ||
    !framebuffer2 ||
    !screenQuad
  )
    return;
  gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer2);
  gl.framebufferTexture2D(
    gl.FRAMEBUFFER,
    gl.COLOR_ATTACHMENT0,
    gl.TEXTURE_2D,
    velocityTmp,
    0,
  );
  gl.viewport(0, 0, config.SIM_RESOLUTION, config.SIM_RESOLUTION);

  gl.useProgram(splatVelocityProgram);
  gl.uniform2f(gl.getUniformLocation(splatVelocityProgram, "uPoint"), x, y);
  gl.uniform2f(
    gl.getUniformLocation(splatVelocityProgram, "uColor"),
    dirX,
    dirY,
  );
  gl.uniform1f(gl.getUniformLocation(splatVelocityProgram, "uRadius"), radius);
  gl.uniform1f(gl.getUniformLocation(splatVelocityProgram, "uForce"), force);
  gl.uniform1i(gl.getUniformLocation(splatVelocityProgram, "uTarget"), 0);
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, velocity);
  gl.bindVertexArray(screenQuad);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.bindVertexArray(null);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);

  const tmp: WebGLTexture = velocity;
  velocity = velocityTmp;
  velocityTmp = tmp;
}

function advect(
  input: WebGLTexture,
  velocityTex: WebGLTexture,
  output: WebGLTexture,
  dissipation: number,
  texWidth: number,
  texHeight: number,
  dt: number,
) {
  if (!gl || !advectionProgram || !framebuffer || !screenQuad) return;
  gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
  gl.framebufferTexture2D(
    gl.FRAMEBUFFER,
    gl.COLOR_ATTACHMENT0,
    gl.TEXTURE_2D,
    output,
    0,
  );
  gl.viewport(0, 0, texWidth, texHeight);
  gl.useProgram(advectionProgram);
  gl.uniform1i(gl.getUniformLocation(advectionProgram, "uInput"), 0);
  gl.uniform1i(gl.getUniformLocation(advectionProgram, "uVelocity"), 1);
  gl.uniform1f(gl.getUniformLocation(advectionProgram, "uDt"), dt);
  gl.uniform1f(
    gl.getUniformLocation(advectionProgram, "uDissipation"),
    dissipation,
  );
  gl.uniform2f(
    gl.getUniformLocation(advectionProgram, "uTexelSize"),
    1.0 / texWidth,
    1.0 / texHeight,
  );
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, input);
  gl.activeTexture(gl.TEXTURE1);
  gl.bindTexture(gl.TEXTURE_2D, velocityTex);
  gl.bindVertexArray(screenQuad);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.bindVertexArray(null);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
}

function computeDivergence(velocityTex: WebGLTexture, output: WebGLTexture) {
  if (!gl || !divergenceProgram || !framebuffer || !screenQuad) return;
  gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
  gl.framebufferTexture2D(
    gl.FRAMEBUFFER,
    gl.COLOR_ATTACHMENT0,
    gl.TEXTURE_2D,
    output,
    0,
  );
  gl.viewport(0, 0, config.SIM_RESOLUTION, config.SIM_RESOLUTION);
  gl.useProgram(divergenceProgram);
  gl.uniform1i(gl.getUniformLocation(divergenceProgram, "uVelocity"), 0);
  gl.uniform2f(
    gl.getUniformLocation(divergenceProgram, "uTexelSize"),
    1.0 / config.SIM_RESOLUTION,
    1.0 / config.SIM_RESOLUTION,
  );
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, velocityTex);
  gl.bindVertexArray(screenQuad);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.bindVertexArray(null);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
}

function computePressure(
  pressureTex: WebGLTexture,
  divergenceTex: WebGLTexture,
  output: WebGLTexture,
) {
  if (!gl || !pressureProgram || !framebuffer || !screenQuad) return;
  gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
  gl.framebufferTexture2D(
    gl.FRAMEBUFFER,
    gl.COLOR_ATTACHMENT0,
    gl.TEXTURE_2D,
    output,
    0,
  );
  gl.viewport(0, 0, config.SIM_RESOLUTION, config.SIM_RESOLUTION);
  gl.useProgram(pressureProgram);
  gl.uniform1i(gl.getUniformLocation(pressureProgram, "uPressure"), 0);
  gl.uniform1i(gl.getUniformLocation(pressureProgram, "uDivergence"), 1);
  gl.uniform2f(
    gl.getUniformLocation(pressureProgram, "uTexelSize"),
    1.0 / config.SIM_RESOLUTION,
    1.0 / config.SIM_RESOLUTION,
  );
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, pressureTex);
  gl.activeTexture(gl.TEXTURE1);
  gl.bindTexture(gl.TEXTURE_2D, divergenceTex);
  gl.bindVertexArray(screenQuad);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.bindVertexArray(null);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
}

function subtractGradient(
  velocityTex: WebGLTexture,
  pressureTex: WebGLTexture,
  output: WebGLTexture,
) {
  if (!gl || !gradientSubtractProgram || !framebuffer || !screenQuad) return;
  gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
  gl.framebufferTexture2D(
    gl.FRAMEBUFFER,
    gl.COLOR_ATTACHMENT0,
    gl.TEXTURE_2D,
    output,
    0,
  );
  gl.viewport(0, 0, config.SIM_RESOLUTION, config.SIM_RESOLUTION);
  gl.useProgram(gradientSubtractProgram);
  gl.uniform1i(gl.getUniformLocation(gradientSubtractProgram, "uVelocity"), 0);
  gl.uniform1i(gl.getUniformLocation(gradientSubtractProgram, "uPressure"), 1);
  gl.uniform2f(
    gl.getUniformLocation(gradientSubtractProgram, "uTexelSize"),
    1.0 / config.SIM_RESOLUTION,
    1.0 / config.SIM_RESOLUTION,
  );
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, velocityTex);
  gl.activeTexture(gl.TEXTURE1);
  gl.bindTexture(gl.TEXTURE_2D, pressureTex);
  gl.bindVertexArray(screenQuad);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.bindVertexArray(null);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
}

function computeCurl(velocityTex: WebGLTexture, output: WebGLTexture) {
  if (!gl || !curlProgram || !framebuffer || !screenQuad) return;
  gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
  gl.framebufferTexture2D(
    gl.FRAMEBUFFER,
    gl.COLOR_ATTACHMENT0,
    gl.TEXTURE_2D,
    output,
    0,
  );
  gl.viewport(0, 0, config.SIM_RESOLUTION, config.SIM_RESOLUTION);
  gl.useProgram(curlProgram);
  gl.uniform1i(gl.getUniformLocation(curlProgram, "uVelocity"), 0);
  gl.uniform2f(
    gl.getUniformLocation(curlProgram, "uTexelSize"),
    1.0 / config.SIM_RESOLUTION,
    1.0 / config.SIM_RESOLUTION,
  );
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, velocityTex);
  gl.bindVertexArray(screenQuad);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.bindVertexArray(null);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
}

function applyVorticity(
  velocityTex: WebGLTexture,
  curlTex: WebGLTexture,
  output: WebGLTexture,
) {
  if (!gl || !vorticityProgram || !framebuffer || !screenQuad) return;
  gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
  gl.framebufferTexture2D(
    gl.FRAMEBUFFER,
    gl.COLOR_ATTACHMENT0,
    gl.TEXTURE_2D,
    output,
    0,
  );
  gl.viewport(0, 0, config.SIM_RESOLUTION, config.SIM_RESOLUTION);
  gl.useProgram(vorticityProgram);
  gl.uniform1i(gl.getUniformLocation(vorticityProgram, "uVelocity"), 0);
  gl.uniform1i(gl.getUniformLocation(vorticityProgram, "uCurl"), 1);
  gl.uniform1f(
    gl.getUniformLocation(vorticityProgram, "uCurlStrength"),
    config.CURL,
  );
  gl.uniform2f(
    gl.getUniformLocation(vorticityProgram, "uTexelSize"),
    1.0 / config.SIM_RESOLUTION,
    1.0 / config.SIM_RESOLUTION,
  );
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, velocityTex);
  gl.activeTexture(gl.TEXTURE1);
  gl.bindTexture(gl.TEXTURE_2D, curlTex);
  gl.bindVertexArray(screenQuad);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.bindVertexArray(null);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
}

// ------------------------------------------------------------
// физика
// ------------------------------------------------------------
function updatePhysics(dt: number) {
  if (
    !velocity ||
    !velocityTmp ||
    !pressure ||
    !pressureTmp ||
    !divergence ||
    !curl ||
    !density ||
    !densityTmp
  )
    return;

  computeCurl(velocity, curl);
  applyVorticity(velocity, curl, velocityTmp);
  let tmpVel: WebGLTexture = velocity;
  velocity = velocityTmp;
  velocityTmp = tmpVel;

  advect(
    velocity,
    velocity,
    velocityTmp,
    config.VELOCITY_DISSIPATION,
    config.SIM_RESOLUTION,
    config.SIM_RESOLUTION,
    dt,
  );
  tmpVel = velocity;
  velocity = velocityTmp;
  velocityTmp = tmpVel;

  computeDivergence(velocity, divergence);
  if (framebuffer) {
    gl?.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
    gl?.framebufferTexture2D(
      gl.FRAMEBUFFER,
      gl.COLOR_ATTACHMENT0,
      gl.TEXTURE_2D,
      pressure,
      0,
    );
    gl?.clearColor(0, 0, 0, 0);
    gl?.clear(gl.COLOR_BUFFER_BIT);
  }
  for (let i = 0; i < config.PRESSURE_ITERATIONS; i++) {
    computePressure(pressure, divergence, pressureTmp);
    const tmpP: WebGLTexture = pressure;
    pressure = pressureTmp;
    pressureTmp = tmpP;
  }
  subtractGradient(velocity, pressure, velocityTmp);
  tmpVel = velocity;
  velocity = velocityTmp;
  velocityTmp = tmpVel;

  advect(
    density,
    velocity,
    densityTmp,
    config.DENSITY_DISSIPATION,
    config.DYE_RESOLUTION,
    config.DYE_RESOLUTION,
    dt,
  );
  const tmpDens: WebGLTexture = density;
  density = densityTmp;
  densityTmp = tmpDens;
}

function draw() {
  if (!gl || !canvasRef.value || !displayProgram || !density || !screenQuad)
    return;

  const now = performance.now();
  let dt = Math.min(0.033, (now - lastTime) / 1000);
  if (dt <= 0) dt = 0.016;
  lastTime = now;
  const time = now / 1000;

  const emitters = [
    { baseX: 0.1, baseY: 0.05, color: { r: 0.3, g: 0.3, b: 0.3 } },
    { baseX: 0.9, baseY: 0.05, color: { r: 0.5, g: 0.5, b: 0.5 } },
    { baseX: 0.1, baseY: 0.2, color: { r: 0.7, g: 0.7, b: 0.7 } },
    { baseX: 0.9, baseY: 0.2, color: { r: 0.6, g: 0.6, b: 0.6 } },
    { baseX: 0.1, baseY: 0.4, color: { r: 0.4, g: 0.4, b: 0.4 } },
    { baseX: 0.9, baseY: 0.4, color: { r: 0.8, g: 0.8, b: 0.8 } },
  ];
  const radius = config.SPLAT_RADIUS;
  const force = config.SPLAT_FORCE * dt;

  emitters.forEach((e, i) => {
    const x = e.baseX + Math.sin(time * 0.4 + i) * 0.03;
    const y = e.baseY + Math.cos(time * 0.3 + i) * 0.005;

    const dirX = Math.sin(time * 0.4 + i) * 0.08;
    const dirY = 0.03 + Math.sin(time * 0.3 + i) * 0.1;

    splatVelocity(x, y, dirX, dirY, radius, force * 1.3);
    splatDensity(x, y, e.color, radius, force * 2.0);
  });

  updatePhysics(dt);

  const canvas = canvasRef.value;
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;
  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.disable(gl.BLEND);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  gl.useProgram(displayProgram);
  gl.uniform1i(gl.getUniformLocation(displayProgram, "uDensity"), 0);
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, density);
  gl.bindVertexArray(screenQuad);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.bindVertexArray(null);

  requestAnimationFrame(draw);
}

function handleResize() {
  if (!canvasRef.value || !gl) return;
  const canvas = canvasRef.value;
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;
  gl.viewport(0, 0, canvas.width, canvas.height);
}

onMounted(() => {
  if (!initGL()) return;
  if (canvasRef.value) {
    canvasRef.value.width = canvasRef.value.clientWidth;
    canvasRef.value.height = canvasRef.value.clientHeight;
  }
  initShaders();
  initBuffers();
  if (!initSimulation()) return;
  if (!density || !velocity || !pressure || !divergence || !curl) {
    console.error("Simulation not properly initialised");
    return;
  }
  lastTime = performance.now();
  window.addEventListener("resize", handleResize);
  draw();
  onUnmounted(() => window.removeEventListener("resize", handleResize));
});
</script>

<style scoped>
.fluid-smoke {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 400px;
  pointer-events: none;
  z-index: 1;
}
</style>
