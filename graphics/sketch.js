let note = "Waiting...";
let targetColor;
let currentColor;
let pulse = 0;
let pulseSpeed = 0.05;
let glowSize = 20;
let orbitron;

let colors = {
  "C3": "#e6194b", "D3": "#3cb44b", "E3": "#ffe119", "F3": "#4363d8", "G3": "#f58231", "A3": "#911eb4", "B3": "#46f0f0",
  "C4": "#f032e6", "D4": "#bcf60c", "E4": "#fabebe", "F4": "#008080", "G4": "#e6beff", "A4": "#9a6324", "B4": "#fffac8",
  "C5": "#800000", "D5": "#aaffc3", "E5": "#808000", "F5": "#ffd8b1", "G5": "#000075", "A5": "#808080", "B5": "#ffffff"
};

function preload() {
  orbitron = loadFont('Orbitron-VariableFont_wght.ttf'); // Use relative path
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  textFont(orbitron);
  textAlign(CENTER, CENTER);
  textSize(80);
  currentColor = color(100);
  targetColor = currentColor;
  setInterval(fetchNote, 2000);
}

function draw() {
  background(20);
  let radius = 100 + sin(pulse) * 20;
  pulse += pulseSpeed;

  currentColor = lerpColor(currentColor, targetColor, 0.05);

  noStroke();
  drawingContext.shadowBlur = glowSize;
  drawingContext.shadowColor = currentColor.toString();
  fill(currentColor);
  ellipse(width / 2, height / 2, radius * 2);

  drawingContext.shadowBlur = 0;

  let floatY = sin(frameCount * 0.05) * 10;
  fill(255);
  text(note, width / 2, height / 2 + floatY);
}

function fetchNote() {
    fetch("note.txt?nocache=" + new Date().getTime())
      .then(res => res.text())
      .then(text => {
        let newNote = text.trim();
        if (newNote !== note) {
          note = newNote;
          targetColor = color(colors[note] || "#ffffff");
        }
      })
      .catch(err => {
        note = "???";
        targetColor = color(100);
      });
  }