# Raga Detector

A Python-based system for detecting and analyzing Carnatic classical music ragas from audio files using pitch extraction and pattern matching.

## Overview

This project provides tools to:
- Extract pitch contours from audio using the pYIN algorithm
- Identify the tonic (Sa) frequency
- Analyze swara (note) distributions
- Match detected patterns to known Carnatic ragas
- Generate the complete 72 Melakarta raga system programmatically

## Project Structure

```
├── raga_detector.py          # Main raga detection system
├── generate_melakartas.py    # Generates all 72 Melakarta ragas
└── requirements.txt          # Project dependencies
```

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Requirements

- librosa (>=0.10.0) - Audio analysis and pitch extraction
- soundfile (>=0.12.0) - Audio file I/O
- scipy (>=1.11.0) - Scientific computing
- numpy (>=1.24.0) - Numerical operations
- scikit-learn (>=1.3.0) - Machine learning utilities
- matplotlib (>=3.7.0) - Data visualization
- seaborn (>=0.12.0) - Statistical visualization
- tqdm (>=4.65.0) - Progress bars

## Quick Start

Run the raga detector on an audio file:
```bash
python raga_detector.py
```

Generate all 72 Melakarta ragas:
```bash
python generate_melakartas.py
```