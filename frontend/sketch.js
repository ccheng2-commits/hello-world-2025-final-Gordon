/**
 * IRIS#1 - Digital Biometrics
 * Main p5.js sketch: state machine, UI flow, and rendering
 */

let stateMachine;
let irisRenderer;
let lastFrameTime = 0;

// Codes loaded from backend
let loadedCodes = [];
let codesLoadTime = 0;
const CODES_REFRESH_INTERVAL = 5000; // Refresh every 5 seconds
// Try multiple paths for compatibility with different server setups
const CODES_INDEX_URLS = [
    '/data/codes_index.json',        // Server root (start_server.py)
    '../data/codes_index.json',      // Relative from frontend/ (Live Server)
    'data/codes_index.json'          // Same directory (fallback)
];
let currentUrlIndex = 0;

// For generating random test codes (fallback)
let currentCodeIndex = 0;

function setup() {
    console.log("✓ p5.js setup() called");
    createCanvas(windowWidth, windowHeight);
    colorMode(HSB, 360, 100, 100);
    
    // Initialize state machine and renderer
    try {
        stateMachine = new UIStateMachine();
        irisRenderer = new DigitalIrisRenderer();
        console.log("✓ State machine and renderer initialized");
    } catch (e) {
        console.error("✗ Error initializing:", e);
    }
    
    // Load codes from backend
    loadCodesFromBackend();
    
    lastFrameTime = millis();
    codesLoadTime = millis();
    
    console.log("IRIS#1 - Digital Biometrics initialized");
    console.log("Press SPACE to simulate capture, 'T' to test transform, 'R' to reset");
}

/**
 * Load latent codes from backend JSON index file
 */
function loadCodesFromBackend() {
    if (currentUrlIndex >= CODES_INDEX_URLS.length) {
        console.warn("⚠ All code index URLs failed, using fallback");
        useFallbackCodes();
        return;
    }
    
    const url = CODES_INDEX_URLS[currentUrlIndex];
    
    loadJSON(url, function(data) {
        if (data && data.codes && Array.isArray(data.codes)) {
            loadedCodes = data.codes.map(item => item.code);
            stateMachine.digitalIrises = [...loadedCodes];
            codesLoadTime = millis();
            console.log(`✓ Loaded ${loadedCodes.length} Digital Irises from backend (${url})`);
            currentUrlIndex = 0; // Reset on success
        } else {
            console.warn(`⚠ Could not parse codes index from ${url}, trying next...`);
            currentUrlIndex++;
            loadCodesFromBackend(); // Try next URL
        }
    }, function(error) {
        console.warn(`⚠ Could not load codes from ${url}, trying next...`);
        currentUrlIndex++;
        if (currentUrlIndex >= CODES_INDEX_URLS.length) {
            console.log("All URLs failed, using fallback codes");
            useFallbackCodes();
        } else {
            loadCodesFromBackend(); // Try next URL
        }
    });
}

/**
 * Use fallback sample codes if backend is unavailable
 */
function useFallbackCodes() {
    const fallbackCodes = [
        "IRIS/I?SEED=4821640GHO=67GDH=83GRO=1.023GRING=0.500GTEX=0.015G/1=0.010",
        "IRIS/I?SEED=635037019GHO=34GDH=55GRO=1.054GRING=0.500GTEX=0.002G/1=0.010",
        "IRIS/I?SEED=926357696GHO=47GDH=61GRO=1.336GRING=0.500GTEX=0.002G/1=0.010"
    ];
    loadedCodes = fallbackCodes;
    stateMachine.digitalIrises = [...fallbackCodes];
}

function draw() {
    background(0, 0, 10); // Dark background (very dark gray in HSB)
    
    // Check if state machine and renderer are initialized
    if (!stateMachine || !irisRenderer) {
        fill(0, 0, 100); // White text
        textAlign(CENTER, CENTER);
        textSize(18);
        text("Initializing...", width / 2, height / 2);
        console.log("draw: Waiting for initialization");
        return;
    }
    
    // Debug: Log draw calls occasionally
    if (frameCount % 60 === 0) {
        console.log(`draw: Frame ${frameCount}, State: ${stateMachine.getState()}, Irises: ${stateMachine.getDigitalIrises().length}`);
    }
    
    // Auto-refresh codes from backend periodically
    const currentTime = millis();
    if (currentTime - codesLoadTime > CODES_REFRESH_INTERVAL) {
        loadCodesFromBackend();
    }
    
    // Update state machine
    try {
        stateMachine.update();
    } catch (e) {
        console.error("Error updating state machine:", e);
    }
    
    // Update iris renderer animation
    try {
        const deltaTime = (currentTime - lastFrameTime) / 1000.0; // Convert to seconds
        irisRenderer.update(deltaTime);
        lastFrameTime = currentTime;
    } catch (e) {
        console.error("Error updating renderer:", e);
    }
    
    // Draw based on current state
    try {
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
            default:
                fill(0, 0, 100);
                textAlign(CENTER, CENTER);
                textSize(18);
                text(`Unknown state: ${currentState}`, width / 2, height / 2);
        }
    } catch (e) {
        console.error("Error drawing:", e);
        fill(0, 0, 100);
        textAlign(CENTER, CENTER);
        textSize(18);
        text("Error: " + e.message, width / 2, height / 2);
    }
}

/**
 * Draw EXHIBIT state: Digital Iris Wall (grid gallery)
 */
function drawExhibitState() {
    // Ensure we have a state machine
    if (!stateMachine || !irisRenderer) {
        fill(0, 0, 100);
        textAlign(CENTER, CENTER);
        textSize(24);
        text("Loading...", width / 2, height / 2);
        console.log("drawExhibitState: stateMachine or irisRenderer not ready");
        return;
    }
    
    const irises = stateMachine.getDigitalIrises();
    console.log(`drawExhibitState: Drawing ${irises ? irises.length : 0} irises`);
    
    // Show message if no irises loaded yet
    if (!irises || irises.length === 0) {
        fill(0, 0, 100);
        textAlign(CENTER, CENTER);
        textSize(18);
        text("Loading Digital Irises...", width / 2, height / 2);
        textSize(14);
        text("(If this persists, check browser console)", width / 2, height / 2 + 30);
        return;
    }
    
    const cols = 4;
    const rows = Math.ceil(irises.length / cols);
    const cellWidth = width / cols;
    const cellHeight = height / rows;
    const irisSize = min(cellWidth, cellHeight) * 0.7;
    
    console.log(`drawExhibitState: Grid ${cols}x${rows}, irisSize=${irisSize}, canvas=${width}x${height}`);
    
    // Draw grid of digital irises
    for (let i = 0; i < irises.length; i++) {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const x = col * cellWidth + cellWidth / 2;
        const y = row * cellHeight + cellHeight / 2;
        
        try {
            console.log(`Drawing iris ${i} at (${x}, ${y}) with size ${irisSize}`);
            irisRenderer.draw(irises[i], x, y, irisSize);
        } catch (e) {
            console.error(`Error drawing iris ${i}:`, e);
            // Draw a placeholder circle if render fails
            fill(200, 50, 50);
            circle(x, y, irisSize * 0.5);
        }
    }
    
    // Title - make sure it's visible
    fill(0, 0, 100); // White text
    textAlign(CENTER, TOP);
    textSize(24);
    text("IRIS#1 - Digital Biometrics", width / 2, 20);
    textSize(14);
    text(`Loaded ${irises.length} Digital Irises | Press SPACE to capture`, width / 2, height - 40);
    
    // Debug: Draw a test circle to verify rendering works
    fill(180, 100, 100); // Bright cyan
    circle(50, 50, 30);
    fill(0, 0, 100);
    textSize(12);
    textAlign(LEFT, TOP);
    text("TEST", 35, 40);
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
        // After 2 seconds, generate a new unique code and start transform
        const newCode = generateNewLatentCode();
        stateMachine.startTransform(newCode);
    }
    
    // Animated circle
    noFill();
    stroke(0, 0, 100);
    strokeWeight(3);
    const progress = min(1.0, captureTime / 2000);
    arc(width / 2, height / 2 + 50, 100, 100, 0, TWO_PI * progress);
}

/**
 * Generate a new unique latent code (simulates backend processing)
 */
function generateNewLatentCode() {
    // Generate random seed
    const seed = Math.floor(Math.random() * 4294967295);
    
    // Generate random features within realistic ranges
    const GHO = Math.floor(Math.random() * 100 + 20);  // 20-120
    const GDH = Math.floor(Math.random() * 60 + 30);   // 30-90
    const GRO = (Math.random() * 1.5 + 0.5).toFixed(3);  // 0.5-2.0
    const GRING = (Math.random() * 0.5 + 0.3).toFixed(3); // 0.3-0.8
    const GTEX = (Math.random() * 0.03 + 0.002).toFixed(3); // 0.002-0.032
    const G1 = "0.010";  // Fixed frequency parameter
    
    return `IRIS/I?SEED=${seed}GHO=${GHO}GDH=${GDH}GRO=${GRO}GRING=${GRING}GTEX=${GTEX}G/1=${G1}`;
}

/**
 * Draw TRANSFORM state: Algorithm running
 */
function drawTransformState() {
    const progress = stateMachine.getTransformProgress();
    const currentCode = stateMachine.getCurrentIrisCode();
    
    // Show preview of generating iris (small, left side)
    if (currentCode) {
        push();
        translate(width * 0.25, height / 2);
        scale(0.3);
        irisRenderer.draw(currentCode, 0, 0, 400);
        pop();
    }
    
    // Show FFT visualization placeholder (right side) - growing circle effect
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
        // T: test transform directly with a new generated code
        const testCode = generateNewLatentCode();
        console.log("Testing transform with:", testCode);
        stateMachine.startTransform(testCode);
    } else if (key === 'r' || key === 'R') {
        // R: reset to exhibit
        stateMachine.setState(UI_STATE.EXHIBIT);
    } else if (key === 'c' || key === 'C') {
        // C: reload codes from backend
        loadCodesFromBackend();
        stateMachine.setState(UI_STATE.EXHIBIT);
        console.log("Reloaded codes from backend");
    }
}

/**
 * Handle window resize
 */
function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

