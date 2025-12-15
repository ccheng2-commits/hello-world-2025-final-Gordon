graph TD
    %% --- Phase 1: Capture (Physical Input) ---
    User((User)) -->|Gaze & Chin Rest| Camera["📷 Camera\nCanon 5D / A7R2"]
    Camera -->|USB Tethering| Incoming[📂 Folder: /incoming]

    %% --- Phase 2: Python Backend (The Brain) ---
    subgraph "🐍 Python Backend (The Brain)"
        Incoming -.->|Watchdog Detects| Watcher{{Watcher Script}}
        Watcher -->|Trigger| Processor["⚙️ Image Processor\nOpenCV"]
        
        %% OpenCV Logic
        Processor -->|Grayscale & Blur| PreOp(Pre-processing)
        PreOp -->|Find Darkest Blob| PupilDet(Pupil Detection)
        PupilDet -->|Dynamic Masking| Donut["🍩 Donut Masking\n(Safe Zone Extraction)"]
        Donut -->|Crop 1000x1000| CropImg(Processed Iris Image)

        %% Analysis Logic
        CropImg -->|Pass Image| Analyzer["📊 FFT Analyzer\nNumPy"]
        Analyzer -->|FFT Transform| Spectrum(2D Spectrum)
        Spectrum -->|Radial Avg| Waveform(1D Waveform Array)
        Spectrum -->|Hash Pixels| Seed(Unique Seed ID)
        
        %% Latent Code Generation
        CropImg -->|Extract Features| CodeGen["🔑 Latent Code Generator\nlatent_code.py"]
        Spectrum -->|FFT Features| CodeGen
        CodeGen -->|Generate| LatentCode["📝 Latent Code\nIRIS/I?SEED=...GHO=..."]
    end

    %% --- Phase 3: Data Handoff (Data Exchange) ---
    CropImg -->|Save .jpg| OutFolder[📂 Folder: /processed]
    Waveform & Seed -->|Save .json| OutFolder
    LatentCode -->|Save .txt/.json| CodesFolder[📂 Folder: /codes]

    %% --- Phase 4: Frontend (Visual Presentation) ---
    subgraph "🎨 p5.js Frontend (The Face)"
        LiveServer(Live Server / Localhost) -->|Hosts| Sketch(sketch.js)
        OutFolder -.->|loadJSON & loadImage| Sketch
        CodesFolder -.->|load Latent Code| Sketch
        Sketch -->|Parse Code| Renderer["🎨 Iris Renderer\niris_renderer.js"]
        Renderer -->|Map Parameters| Visual(Generative Iris)
        Visual -->|Render| Screen["🖥️ Digital Wall / Monitor"]
    end

    %% Styles
    style Incoming fill:#f9f,stroke:#333,stroke-width:2px
    style OutFolder fill:#f9f,stroke:#333,stroke-width:2px
    style Donut fill:#ff9,stroke:#f66,stroke-width:2px,stroke-dasharray: 5 5
    style Analyzer fill:#ccf,stroke:#333,stroke-width:2px
    style CodeGen fill:#9cf,stroke:#333,stroke-width:2px
    style CodesFolder fill:#f9f,stroke:#333,stroke-width:2px