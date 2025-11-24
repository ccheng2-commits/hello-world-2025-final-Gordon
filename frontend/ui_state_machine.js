/**
 * IRIS#1 - Digital Biometrics
 * State machine for UI flow: EXHIBIT -> CAPTURE -> TRANSFORM -> DISPLAY_SINGLE -> UPDATE_EXHIBIT
 */

// State constants
const UI_STATE = {
    EXHIBIT: 'EXHIBIT',              // Shows Digital Iris Wall (gallery)
    CAPTURE: 'CAPTURE',              // Capturing screen
    TRANSFORM: 'TRANSFORM',          // Algorithm running (shows iris + FFT)
    DISPLAY_SINGLE: 'DISPLAY_SINGLE', // Shows new visitor's Digital Iris
    UPDATE_EXHIBIT: 'UPDATE_EXHIBIT'  // Brief transition to add to wall
};

/**
 * State Machine class to manage UI states and transitions
 */
class UIStateMachine {
    constructor() {
        this.currentState = UI_STATE.EXHIBIT;
        this.stateStartTime = 0;
        this.transitionDuration = 2000; // 2 seconds for transitions
        
        // State data
        this.digitalIrises = []; // Array of latent codes for the wall
        this.currentIrisCode = null; // Current visitor's latent code
        this.transformProgress = 0; // 0-1 for TRANSFORM animation
    }
    
    /**
     * Change to a new state
     */
    setState(newState) {
        if (this.currentState !== newState) {
            console.log(`State transition: ${this.currentState} -> ${newState}`);
            this.currentState = newState;
            this.stateStartTime = millis();
            this.transformProgress = 0;
        }
    }
    
    /**
     * Get current state
     */
    getState() {
        return this.currentState;
    }
    
    /**
     * Get time elapsed in current state (milliseconds)
     */
    getStateTime() {
        return millis() - this.stateStartTime;
    }
    
    /**
     * Update state machine logic (called every frame)
     */
    update() {
        const stateTime = this.getStateTime();
        
        switch (this.currentState) {
            case UI_STATE.TRANSFORM:
                // Animate transform progress
                this.transformProgress = min(1.0, stateTime / 3000); // 3 second transform
                if (this.transformProgress >= 1.0 && this.currentIrisCode) {
                    this.setState(UI_STATE.DISPLAY_SINGLE);
                }
                break;
                
            case UI_STATE.DISPLAY_SINGLE:
                // Show single iris for 5 seconds, then update exhibit
                if (stateTime > 5000) {
                    this.setState(UI_STATE.UPDATE_EXHIBIT);
                }
                break;
                
            case UI_STATE.UPDATE_EXHIBIT:
                // Brief transition, then go back to exhibit
                if (stateTime > this.transitionDuration) {
                    // Add current iris to the wall
                    if (this.currentIrisCode) {
                        this.digitalIrises.push(this.currentIrisCode);
                        this.currentIrisCode = null;
                    }
                    this.setState(UI_STATE.EXHIBIT);
                }
                break;
        }
    }
    
    /**
     * Trigger capture flow (simulate new visitor)
     * For MVP: can be triggered by keyboard or button
     */
    triggerCapture() {
        if (this.currentState === UI_STATE.EXHIBIT) {
            this.setState(UI_STATE.CAPTURE);
        }
    }
    
    /**
     * Start transform with a latent code
     */
    startTransform(latentCode) {
        this.currentIrisCode = latentCode;
        this.setState(UI_STATE.TRANSFORM);
    }
    
    /**
     * Get all digital irises for the wall
     */
    getDigitalIrises() {
        return this.digitalIrises;
    }
    
    /**
     * Get current visitor's iris code
     */
    getCurrentIrisCode() {
        return this.currentIrisCode;
    }
    
    /**
     * Get transform progress (0-1)
     */
    getTransformProgress() {
        return this.transformProgress;
    }
}

