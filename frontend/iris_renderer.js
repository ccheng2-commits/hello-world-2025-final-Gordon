/**
 * IRIS#1 - Digital Biometrics
 * Generative Digital Iris renderer that takes a latent code and renders
 * a looping, animated, circular pattern.
 */

/**
 * Parse a latent code string into parameters
 * Format: IRIS/1?seed=2481739201&H0=212&dH=18&R0=0.41&ring=0.27&tex=0.63&λ=0.010
 */
function parseLatentCode(latentCode) {
    const params = {};
    
    // Extract seed
    const seedMatch = latentCode.match(/seed=(\d+)/);
    if (seedMatch) {
        params.seed = parseInt(seedMatch[1]);
    }
    
    // Extract other parameters
    const paramPatterns = {
        'H0': /H0=(\d+)/,
        'dH': /dH=(\d+)/,
        'R0': /R0=([\d.]+)/,
        'ring': /ring=([\d.]+)/,
        'tex': /tex=([\d.]+)/,
        'λ': /λ=([\d.]+)/
    };
    
    for (const [key, pattern] of Object.entries(paramPatterns)) {
        const match = latentCode.match(pattern);
        if (match) {
            params[key] = parseFloat(match[1]);
        }
    }
    
    // Set defaults if missing
    params.seed = params.seed || 1000000000;
    params.H0 = params.H0 || 128;
    params.dH = params.dH || 50;
    params.R0 = params.R0 || 0.5;
    params.ring = params.ring || 0.5;
    params.tex = params.tex || 0.5;
    params['λ'] = params['λ'] || 0.5;
    
    return params;
}

/**
 * Seeded random number generator (for deterministic patterns)
 */
function seededRandom(seed) {
    let value = seed;
    return function() {
        value = (value * 9301 + 49297) % 233280;
        return value / 233280;
    };
}

/**
 * Render a Digital Iris from a latent code
 * This creates a generative, animated circular pattern
 */
class DigitalIrisRenderer {
    constructor() {
        this.time = 0;
    }
    
    /**
     * Update animation time
     */
    update(deltaTime) {
        this.time += deltaTime;
    }
    
    /**
     * Draw the Digital Iris
     * @param {string} latentCode - The latent code string
     * @param {number} x - Center X position
     * @param {number} y - Center Y position
     * @param {number} size - Diameter of the iris
     */
    draw(latentCode, x, y, size) {
        const params = parseLatentCode(latentCode);
        const rand = seededRandom(params.seed);
        
        push();
        translate(x, y);
        
        const radius = size / 2;
        const centerBrightness = params.H0;
        const contrast = params.dH;
        const radialStrength = params.R0;
        const ringPattern = params.ring;
        const texture = params.tex;
        const frequency = params['λ'];
        
        // Draw concentric circles with animated patterns
        for (let r = radius; r > 0; r -= 2) {
            const normalizedR = r / radius;
            
            // Base color from brightness and contrast
            const baseBrightness = centerBrightness + (normalizedR - 0.5) * contrast;
            
            // Radial pattern (R0)
            const radial = sin(normalizedR * PI * radialStrength * 2) * 0.5 + 0.5;
            
            // Ring pattern
            const ring = sin(normalizedR * PI * 10 * ringPattern + this.time * 0.5) * 0.3 + 0.7;
            
            // Texture/noise
            const noiseValue = noise(normalizedR * texture * 10, this.time * 0.1) * 0.2;
            
            // Frequency-based pattern (λ)
            const freqPattern = sin(normalizedR * PI * frequency * 20 + this.time) * 0.2 + 0.8;
            
            // Combine all patterns
            const brightness = baseBrightness * radial * ring * (1 + noiseValue) * freqPattern;
            const brightnessClamped = constrain(brightness, 0, 255);
            
            // Color mapping (can be customized)
            const hue = map(normalizedR, 0, 1, 200, 280); // Blue-purple range
            const saturation = map(brightnessClamped, 0, 255, 30, 80);
            const lightness = map(brightnessClamped, 0, 255, 20, 80);
            
            fill(hue, saturation, lightness);
            noStroke();
            circle(0, 0, r * 2);
        }
        
        // Add some radial lines for structure
        stroke(255, 20);
        strokeWeight(1);
        for (let angle = 0; angle < TWO_PI; angle += PI / 8) {
            const lineLength = radius * (0.3 + ringPattern * 0.4);
            line(
                cos(angle) * radius * 0.2,
                sin(angle) * radius * 0.2,
                cos(angle) * lineLength,
                sin(angle) * lineLength
            );
        }
        
        pop();
    }
}

