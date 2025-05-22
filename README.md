# 3D-Reconstruction-Demo

This is a demo web application for 3D reconstruction from photographs using OpenMVG and OpenMVS.

# 🔧 Project Overview
The pipeline takes a set of photos of an object or scene and reconstructs a textured 3D model using structure-from-motion (SfM) and multi-view stereo (MVS) techniques. The system runs in a containerized environment built with Docker to simplify the setup of legacy dependencies.

## Project Structure

```
3D-Reconstruction-Demo/
├── app/                          # Flask application
│   ├── static/                   # Static assets (images, results, etc.)
│   │   ├── reconstruction_sequential/  # Temporary folder for 3D reconstruction
│   │   └── .gitkeep              # Placeholder to keep directory in Git
│   ├── templates/                # HTML templates
│   │   └── index.html
│   ├── main.py                    # Main Flask server
│   └── utils.py                   # Main Function Realization
├── uploads/                      # Temporary folder for uploaded image sets
│   └── .gitkeep
├── Dockerfile                    # Docker image definition
├── docker-compose.yml           # Docker Compose configuration
├── .gitignore                   # Git ignore rules
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies
```

# 🧱 Core Tools
- **OpenMVG**: Structure-from-Motion (SfM) for sparse point cloud and camera pose estimation
- **OpenMVS**: Multi-View Stereo (MVS) for dense reconstruction and mesh generation
- **Docker**: Containerized environment for reproducibility and simplified setup
- **Flask + Web UI**: Lightweight interface to trigger the pipeline and preview results

# 🚀 How It Works
1. Upload a set of photos (10–30 images taken around the object)

2. The system performs feature extraction, matching, SfM, MVS, and mesh texturing

3. A downloadable 3D model (.ply format) is generated for preview or further use

# How to Run

## Prerequisites
- Make sure you have [Docker](https://www.docker.com/get-started) installed on your machine.

## Steps
- Build and run the Docker containers

```docker-compose up --build```

- Open your browser and go to `http://localhost:5000`
