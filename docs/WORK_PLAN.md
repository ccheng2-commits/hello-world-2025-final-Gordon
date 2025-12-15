# IRIS#1 Work Plan - Frontend & Backend Breakdown

## 📋 Project Understanding: Frontend vs Backend

### 🔧 Backend - "The Factory"
**Role:** Process photos, generate data  
**Language:** Python  
**Location:** `backend/` folder  
**Runs on:** Mac mini (local computer)

**Workflow:**
```
Photo → Crop → FFT Analysis → Extract Features → Generate Code
```

### 🎨 Frontend - "The Gallery"
**Role:** Display interface, render visual effects  
**Language:** JavaScript (p5.js)  
**Location:** `frontend/` folder  
**Runs on:** Web browser

**Workflow:**
```
Read Code → Parse Parameters → Render Digital Iris → Display on Screen
```

---

## 🔗 How Frontend & Backend Connect

```
Backend generates code → Saves to file → Frontend reads file → Displays effect
```

**Data Flow:**
1. Backend saves code to `data/codes/` folder (JSON or TXT file)
2. Frontend periodically reads the latest file from this folder
3. Frontend parses the code and renders it as visual effect

---

## ✅ Completed Work

### Backend ✅
- [x] `config.py` - Configuration file
- [x] `iris_processor.py` - Photo cropping
- [x] `fft_pipeline.py` - FFT computation
- [x] `latent_code.py` - Code generation (format updated)
- [x] `watch_folder.py` - Auto monitoring

### Frontend ✅
- [x] `index.html` - Main page
- [x] `sketch.js` - Main controller
- [x] `ui_state_machine.js` - State management
- [x] `iris_renderer.js` - Renderer (needs format update)

---

## 🚧 Next Steps

### 🔧 Backend Tasks

#### 1. Test Backend Functionality ⚠️ Priority
**Goal:** Ensure all tools work correctly

**Tasks:**
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Prepare test photo: Place an iris photo in `data/incoming/`
- [ ] Test cropping: Run `python -m backend.iris_processor`
- [ ] Test FFT: Run `python -m backend.fft_pipeline`
- [ ] Test code generation: Run `python -m backend.latent_code`
- [ ] Verify generated code format is correct

**Expected Results:**
- Cropped photos in `data/processed/`
- FFT visualization images in `data/fft/`
- Code files in `data/codes/` (format: `IRIS/I?SEED=...GHO=...`)

#### 2. Improve Pupil Detection 🔄 Future Enhancement
**Goal:** Upgrade from simple center crop to automatic pupil detection

**Tasks:**
- [ ] Research OpenCV pupil detection methods (HoughCircles or deep learning)
- [ ] Modify `iris_processor.py` to add detection
- [ ] Test detection under different lighting conditions

#### 3. Optimize Feature Extraction 🔄 Future Enhancement
**Goal:** Extract more accurate feature values

**Tasks:**
- [ ] Analyze feature differences between different irises
- [ ] Adjust feature extraction algorithm
- [ ] Ensure each iris generates a unique code

---

### 🎨 Frontend Tasks

#### 1. Update Code Parser ⚠️ Priority
**Goal:** Make frontend read the new code format

**Tasks:**
- [ ] Modify `parseLatentCode()` function in `iris_renderer.js`
- [ ] Update parameter names: `GHO`, `GDH`, `GRO`, `GRING`, `GTEX`, `G/1`
- [ ] Update parameter usage in `draw()` function
- [ ] Test parsing is correct

**Changes Needed:**
```javascript
// Old format: H0, dH, R0, ring, tex, λ
// New format: GHO, GDH, GRO, GRING, GTEX, G/1
```

#### 2. Connect Frontend & Backend ⚠️ Priority
**Goal:** Make frontend automatically read backend-generated codes

**Tasks:**
- [ ] Add file reading functionality to `sketch.js`
- [ ] Periodically check `data/codes/` folder for latest file
- [ ] Parse code and trigger state machine
- [ ] Test complete flow: backend generates → frontend displays

**Implementation Options:**
- **Option A:** Frontend reads local files with JavaScript (requires special permissions)
- **Option B:** Create simple HTTP server, frontend gets data via API

#### 3. Optimize Visual Effects 🔄 Ongoing
**Goal:** Make Digital Iris more beautiful

**Tasks:**
- [ ] Adjust color scheme
- [ ] Optimize animation effects
- [ ] Improve gallery wall layout
- [ ] Add transition animations

#### 4. Enhance State Machine 🔄 Future
**Goal:** Make interactions smoother

**Tasks:**
- [ ] Optimize state transition animations
- [ ] Add sound effects (optional)
- [ ] Improve user instruction text

---

## 📊 Priority Levels

### 🔴 High Priority (Must Do First)
1. **Test backend functionality** - Ensure basic tools work
2. **Update frontend code parser** - Match new format
3. **Connect frontend & backend** - Make system fully functional

### 🟡 Medium Priority (Important but not urgent)
4. **Optimize visual effects** - Make display more beautiful
5. **Improve pupil detection** - Increase accuracy

### 🟢 Low Priority (Nice to have)
6. **Add sound effects** - Enhance experience
7. **Optimize feature extraction** - More precise

---

## 🎯 This Week's Goals (Suggested)

### Step 1: Test Backend (1-2 hours)
```
1. Install dependencies
2. Prepare test photo
3. Test each tool one by one
4. Check output results
```

### Step 2: Update Frontend (1 hour)
```
1. Modify code parser
2. Test frontend displays correctly
```

### Step 3: Connect System (2-3 hours)
```
1. Implement file reading functionality
2. Test complete flow
3. Debug issues
```

### Step 4: Optimize Visuals (Ongoing)
```
1. Adjust colors and animations
2. Improve layout
3. Test different parameters
```

---

## 💡 How to Get Started?

### You can do now:
1. **Ask me:** "Help me test backend functionality"
2. **Or:** "Help me update frontend code parser"
3. **Or:** "I want to see what the backend-generated code looks like first"

### When you need help:
- **Backend issues:** "This Python code has an error, help me check"
- **Frontend issues:** "This visual effect is wrong, help me adjust"
- **Connection issues:** "How do frontend and backend connect?"

---

## 📝 Notes

1. **Test backend first, then connect frontend** - Ensure data is correct
2. **Test after every code change** - Avoid accumulating errors
3. **Save work progress** - Commit code with Git
4. **Ask questions when stuck** - Don't get stuck for too long

---

## 🔄 Suggested Workflow

```
1. Choose a task (backend/frontend)
2. Tell me what you want to do
3. I help you implement or guide you
4. Test functionality
5. Adjust and optimize
6. Continue to next task
```

