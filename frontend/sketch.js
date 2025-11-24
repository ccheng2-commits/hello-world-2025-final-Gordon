/**
 * IRIS#1 - Digital Biometrics
 * Main p5.js sketch: state machine, UI flow, and rendering
 */

let stateMachine;
let irisRenderer;
let lastFrameTime = 0;

// For testing: hard-coded sample latent code
const SAMPLE_LATENT_CODE = "IRIS/1?seed=2481739201&H0=212&dH=18&R0=0.41&ring=0.27&tex=0.63&λ=0.010";

function setup() {
    createCanvas(windowWidth, windowHeight);
    colorMode(HSB, 360, 100, 100);
    
    // Initialize state machine and renderer
    stateMachine = new UIStateMachine();
    irisRenderer = new DigitalIrisRenderer();
    
    // For MVP: add a sample iris to the wall
    stateMachine.digitalIrises.push(SAMPLE_LATENT_CODE);
    
    lastFrameTime = millis();
    
    console.log("IRIS#1 - Digital Biometrics initialized");
    console.log("Press SPACE to simulate capture, 'T' to test transform");
}

function draw() {
    background(0, 0, 10); // Dark background
    
    // Update state machine
    stateMachine.update();
    
    // Update iris renderer animation
    const currentTime = millis();
    const deltaTime = (currentTime - lastFrameTime) / 1000.0; // Convert to seconds
    irisRenderer.update(deltaTime);
    lastFrameTime = currentTime;
    
    // Draw based on current state
    const currentState = stateMachine.getState();
    
    switch (currentState) {
        case UI_STATE.EXHIBIT:
            drawExhibitState();
            break;
        case UI_STATE.CAPTURE:
            drawCaptureState();
            break;
        case UI_STATE.TRANSFORM:
            drawTransformState();
            break;
        case UI_STATE.DISPLAY_SINGLE:
            drawDisplaySingleState();
            break;
        case UI_STATE.UPDATE_EXHIBIT:
            drawUpdateExhibitState();
            break;
    }
}

/**
 * Draw EXHIBIT state: Digital Iris Wall (grid gallery)
 */
function drawExhibitState() {
    const irises = stateMachine.getDigitalIrises();
    const cols = 4;
    const rows = Math.ceil(irises.length / cols);
    const cellWidth = width / cols;
    const cellHeight = height / rows;
    const irisSize = min(cellWidth, cellHeight) * 0.7;
    
    // Draw grid of digital irises
    for (let i = 0; i < irises.length; i++) {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const x = col * cellWidth + cellWidth / 2;
        const y = row * cellHeight + cellHeight / 2;
        
        irisRenderer.draw(irises[i], x, y, irisSize);
    }
    
    // Title
    fill(0, 0, 100);
    textAlign(CENTER, TOP);
    textSize(24);
    text("IRIS#1 - Digital Biometrics", width / 2, 20);
    textSize(14);
    text("Press SPACE to capture", width / 2, height - 40);
}

/**
 * Draw CAPTURE state: Capturing screen
 */
function drawCaptureState() {
    fill(0, 0, 100);
    textAlign(CENTER, CENTER);
    textSize(32);
    text("CAPTURING...", width / 2, height / 2 - 50);
    
    // Simulate capture progress
    const captureTime = stateMachine.getStateTime();
    if (captureTime > 2000) {
        // After 2 seconds, simulate getting a latent code and start transform
        stateMachine.startTransform(SAMPLE_LATENT_CODE);
    }
    
    // Animated circle
    noFill();
    stroke(0, 0, 100);
    strokeWeight(3);
    const progress = min(1.0, captureTime / 2000);
    arc(width / 2, height / 2 + 50, 100, 100, 0, TWO_PI * progress);
}

/**
 * Draw TRANSFORM state: Algorithm running
 */
function drawTransformState() {
    const progress = stateMachine.getTransformProgress();
    
    // Show original iris (small, left side)
    push();
    translate(width * 0.25, height / 2);
    scale(0.3);
    irisRenderer.draw(SAMPLE_LATENT_CODE, 0, 0, 400);
    pop();
    
    // Show FFT visualization placeholder (right side)
    fill(200, 50, 50, progress * 100);
    noStroke();
    circle(width * 0.75, height / 2, 200 * progress);
    
    // Algorithm text
    fill(0, 0, 100);
    textAlign(CENTER, CENTER);
    textSize(24);
    text("TRANSFORMING...", width / 2, height / 2 - 150);
    textSize(14);
    text(`${int(progress * 100)}%`, width / 2, height / 2 + 150);
}

/**
 * Draw DISPLAY_SINGLE state: Show new visitor's Digital Iris
 */
function drawDisplaySingleState() {
    const code = stateMachine.getCurrentIrisCode();
    if (code) {
        // Draw large iris in center
        irisRenderer.draw(code, width / 2, height / 2, min(width, height) * 0.6);
        
        // Show latent code string
        fill(0, 0, 100);
        textAlign(CENTER, CENTER);
        textSize(12);
        text(code, width / 2, height - 80);
        
        textSize(18);
        text("Your Digital Iris", width / 2, 100);
    }
}

/**
 * Draw UPDATE_EXHIBIT state: Brief transition
 */
function drawUpdateExhibitState() {
    // Fade transition effect
    const progress = stateMachine.getStateTime() / stateMachine.transitionDuration;
    const alpha = 255 * (1 - progress);
    
    fill(0, 0, 0, alpha);
    rect(0, 0, width, height);
    
    fill(0, 0, 100);
    textAlign(CENTER, CENTER);
    textSize(18);
    text("Adding to Digital Iris Wall...", width / 2, height / 2);
}

/**
 * Keyboard controls for testing
 */
function keyPressed() {
    if (key === ' ') {
        // SPACE: trigger capture
        stateMachine.triggerCapture();
    } else if (key === 't' || key === 'T') {
        // T: test transform directly
        stateMachine.startTransform(SAMPLE_LATENT_CODE);
    } else if (key === 'r' || key === 'R') {
        // R: reset to exhibit
        stateMachine.setState(UI_STATE.EXHIBIT);
    }
}

/**
 * Handle window resize
 */
function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

