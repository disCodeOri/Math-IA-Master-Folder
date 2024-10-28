# Mathematical Analysis of Swimming Stroke Patterns Using Fourier Series
*IB Mathematics AA HL Internal Assessment - First Draft*

## Introduction
During a break from swim training, I discovered a YouTube video showing how Fourier series could create intricate animations, including a portrait of Joseph Fourier himself emerging from mathematical equations. As a triathlete who has spent countless hours perfecting stroke techniques, the mesmerizing way these complex patterns emerged from simple trigonometric functions sparked a realization: just as Fourier series could reconstruct detailed drawings, they could potentially decompose and analyze the periodic, fluid motions of swimming strokes into their fundamental mathematical elements.

## Research Question
"How can Fourier series analysis of multi-angle video recordings be used to quantify and optimize freestyle swimming stroke patterns?"

### Aim
This exploration aims to:
1. Model the periodic motion of freestyle swimming strokes using Fourier series
2. Identify key harmonic components that contribute to efficient swimming technique
3. Develop a mathematical framework for analyzing swimming efficiency
4. Provide quantitative insights for technique optimization

## Mathematical Framework

### 1. Data Collection
My investigation will utilize three synchronized video recordings of freestyle swimming:
- Underwater orthogonal view
- Above-water side view
- Above-water front view

### 2. Motion Tracking
The analysis will employ Kinovea, a specialized sports motion tracking software, to:
- Track key anatomical points (hand, elbow, shoulder)
- Generate time-series coordinate data
- Export position data for mathematical analysis

### 3. Mathematical Analysis
The core mathematical concepts will include:

#### 3.1 Fourier Series Representation
For a periodic function f(t) with period T:
f(t) = a₀/2 + Σ(n=1 to ∞)[aₙcos(nωt) + bₙsin(nωt)]

where:
- a₀/2 represents the mean position
- ω = 2π/T is the fundamental frequency
- aₙ and bₙ are Fourier coefficients

#### 3.2 Coordinate Analysis
For each tracked point P(t):
- x(t) = Horizontal position function
- y(t) = Vertical position function
- z(t) = Depth position function (from multiple views)

### 4. Visualization
The analysis will be visualized using:
- Python's Manim library for mathematical animations
- Phase diagrams of stroke patterns
- Harmonic component breakdowns

## Expected Outcomes
1. Quantitative description of stroke patterns
2. Identification of key stroke components
3. Comparison with ideal stroke patterns
4. Recommendations for technique optimization

## Methodology

### Phase 1: Data Collection
1. Record synchronized multi-angle videos
2. Process videos through Kinovea
3. Export coordinate data

### Phase 2: Mathematical Processing
1. Apply Fourier analysis to position data
2. Calculate key stroke metrics
3. Generate mathematical models

### Phase 3: Analysis
1. Compare different stroke patterns
2. Identify efficiency factors
3. Develop optimization recommendations

## Personal Engagement
This exploration combines my passion for swimming with advanced mathematics, allowing me to:
1. Analyze my own technique scientifically
2. Develop novel approaches to stroke analysis
3. Create practical applications of mathematical concepts

## Next Steps
1. Complete video processing setup
2. Develop data processing algorithms
3. Create visualization framework
4. Begin initial data analysis

[Note: This draft outlines the intended approach and mathematical framework. Subsequent versions will include actual data analysis and results.]
