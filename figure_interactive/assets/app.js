"use strict";

const X_COUNT = 72;
const THETA_COUNT = 64;
const REGION_COLOR = "#498FFF";
const AXIS_COLOR = "#858585";
const LABEL_COLOR = "#4F4F4F";
const X_AXIS_RANGE = [-0.5, 2.0];
const RADIAL_AXIS_RANGE = [-1.25, 1.25];
const TICK_SIZE = 0.035;

const graph = document.getElementById("region-graph");
const slider = document.getElementById("alpha-slider");
const alphaInput = document.getElementById("alpha-input");

function sequence(start, stop, count) {
  const step = (stop - start) / (count - 1);
  return Array.from({ length: count }, (_, index) => start + index * step);
}

function tickSequence(start, stop) {
  const ticks = [];
  for (let value = start; value <= stop + 1e-9; value += 0.25) {
    const rounded = Math.round(value * 100) / 100;
    if (rounded !== 0) ticks.push(rounded);
  }
  return ticks;
}

function radiusProfile(xValues, alpha) {
  const lower = new Float64Array(xValues.length);
  const upper = new Float64Array(xValues.length).fill(1);
  const exponent = alpha / 2;

  for (let iteration = 0; iteration < 36; iteration += 1) {
    for (let index = 0; index < xValues.length; index += 1) {
      const x = xValues[index];
      const radius = (lower[index] + upper[index]) / 2;
      const value =
        Math.pow(x * x + radius * radius, exponent) +
        Math.pow((1 - x) * (1 - x) + radius * radius, exponent);
      if (value <= 1) lower[index] = radius;
      else upper[index] = radius;
    }
  }
  return lower;
}

function regionMesh(alpha) {
  const xValues = sequence(0, 1, X_COUNT);
  const thetaValues = sequence(0, 2 * Math.PI, THETA_COUNT);
  const radii = radiusProfile(xValues, alpha);
  const x = [];
  const y = [];
  const z = [];

  for (const theta of thetaValues) {
    const xRow = [];
    const yRow = [];
    const zRow = [];
    for (let index = 0; index < xValues.length; index += 1) {
      xRow.push(xValues[index]);
      yRow.push(radii[index] * Math.cos(theta));
      zRow.push(radii[index] * Math.sin(theta));
    }
    x.push(xRow);
    y.push(yRow);
    z.push(zRow);
  }
  return { x, y, z };
}

function coordinateFrameTraces() {
  const xTicks = tickSequence(...X_AXIS_RANGE);
  const radialTicks = tickSequence(...RADIAL_AXIS_RANGE);
  const positiveRadialTicks = radialTicks.filter((tick) => tick > 0);
  const tickX = [];
  const tickY = [];
  const tickZ = [];

  for (const tick of xTicks) {
    tickX.push(tick, tick, null);
    tickY.push(-TICK_SIZE, TICK_SIZE, null);
    tickZ.push(0, 0, null);
  }
  for (const tick of radialTicks) {
    tickX.push(-TICK_SIZE, TICK_SIZE, null, -TICK_SIZE, TICK_SIZE, null);
    tickY.push(tick, tick, null, 0, 0, null);
    tickZ.push(0, 0, null, tick, tick, null);
  }

  return [
    {
      type: "scatter3d",
      x: [X_AXIS_RANGE[0], X_AXIS_RANGE[1], null, 0, 0, null, 0, 0],
      y: [0, 0, null, RADIAL_AXIS_RANGE[0], RADIAL_AXIS_RANGE[1], null, 0, 0],
      z: [0, 0, null, 0, 0, null, RADIAL_AXIS_RANGE[0], RADIAL_AXIS_RANGE[1]],
      mode: "lines",
      line: { color: AXIS_COLOR, width: 3 },
      hoverinfo: "skip",
      showlegend: false,
    },
    {
      type: "scatter3d",
      x: tickX,
      y: tickY,
      z: tickZ,
      mode: "lines",
      line: { color: AXIS_COLOR, width: 2 },
      hoverinfo: "skip",
      showlegend: false,
    },
    {
      type: "scatter3d",
      x: [
        ...xTicks,
        ...positiveRadialTicks.map(() => -0.07),
        ...positiveRadialTicks.map(() => -0.07),
      ],
      y: [
        ...xTicks.map(() => 0.06),
        ...positiveRadialTicks,
        ...positiveRadialTicks.map(() => 0.06),
      ],
      z: [
        ...xTicks.map(() => 0.06),
        ...positiveRadialTicks.map(() => 0.06),
        ...positiveRadialTicks,
      ],
      mode: "text",
      text: [...xTicks, ...positiveRadialTicks, ...positiveRadialTicks].map(String),
      textfont: { color: "#717784", size: 9 },
      hoverinfo: "skip",
      showlegend: false,
    },
    {
      type: "scatter3d",
      x: [1.92, 0, 0],
      y: [0, 1.18, 0],
      z: [0, 0, 1.18],
      mode: "text",
      text: ["x", "y", "z"],
      textfont: { color: LABEL_COLOR, size: 15 },
      hoverinfo: "skip",
      showlegend: false,
    },
  ];
}

function formatAlpha(alpha) {
  return Number(alpha.toPrecision(4)).toString();
}

function figureData(alpha) {
  const mesh = regionMesh(alpha);
  return [
    {
      type: "surface",
      x: mesh.x,
      y: mesh.y,
      z: mesh.z,
      surfacecolor: mesh.z,
      cmin: -1,
      cmax: 1,
      colorscale: [
        [0, "#2E73DE"],
        [0.5, REGION_COLOR],
        [1, "#82B4FF"],
      ],
      opacity: 0.58,
      showscale: false,
      hoverinfo: "skip",
      lighting: { ambient: 1, diffuse: 0, specular: 0, roughness: 1, fresnel: 0 },
    },
    ...coordinateFrameTraces(),
    {
      type: "scatter3d",
      x: [0, 1],
      y: [0, 0],
      z: [0, 0],
      mode: "lines+markers+text",
      line: { color: "#111111", width: 5 },
      marker: { color: "#111111", size: 5 },
      text: ["0", "e₁"],
      textposition: ["bottom left", "top right"],
      hoverinfo: "skip",
      showlegend: false,
    },
  ];
}

function figureLayout(alpha) {
  return {
    title: {
      text: `K<sub>SS,α</sub>, α = ${formatAlpha(alpha)}`,
      x: 0.5,
      y: 0.97,
      font: { family: "Georgia, Times New Roman, serif", size: 22, color: "#172033" },
    },
    margin: { l: 0, r: 0, t: 52, b: 8 },
    paper_bgcolor: "white",
    font: { color: LABEL_COLOR },
    showlegend: false,
    uirevision: "stepping-stone-camera",
    scene: {
      bgcolor: "white",
      xaxis: { range: X_AXIS_RANGE, visible: false },
      yaxis: { range: RADIAL_AXIS_RANGE, visible: false },
      zaxis: { range: RADIAL_AXIS_RANGE, visible: false },
      aspectmode: "cube",
      camera: { eye: { x: 0.25, y: -1.23, z: 0.62 } },
    },
  };
}

const plotConfig = {
  displaylogo: false,
  responsive: true,
  scrollZoom: true,
  modeBarButtonsToRemove: ["select3d", "lasso3d"],
};

function render(alpha) {
  Plotly.react(graph, figureData(alpha), figureLayout(alpha), plotConfig);
}

function updateSliderProgress() {
  const progress = (Number(slider.value) / 2) * 100;
  slider.style.setProperty("--slider-progress", `${progress}%`);
}

let pendingFrame = null;
function scheduleRender(alpha) {
  if (pendingFrame !== null) cancelAnimationFrame(pendingFrame);
  pendingFrame = requestAnimationFrame(() => {
    render(alpha);
    pendingFrame = null;
  });
}

slider.addEventListener("input", () => {
  const alpha = Math.pow(10, Number(slider.value));
  alphaInput.value = formatAlpha(alpha);
  updateSliderProgress();
  scheduleRender(alpha);
});

alphaInput.addEventListener("change", () => {
  const alpha = Number(alphaInput.value);
  if (!Number.isFinite(alpha) || alpha <= 0) {
    alphaInput.setCustomValidity("Enter a positive alpha value.");
    alphaInput.reportValidity();
    return;
  }
  alphaInput.setCustomValidity("");
  if (alpha >= 1 && alpha <= 100) {
    slider.value = Math.log10(alpha);
    updateSliderProgress();
  }
  scheduleRender(alpha);
});

updateSliderProgress();
render(Number(alphaInput.value));
