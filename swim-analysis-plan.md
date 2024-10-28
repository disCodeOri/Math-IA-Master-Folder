# Swimming Stroke Analysis Project Plan

Video: [10 Swimmer comments](https://www.youtube.com/watch?v=FpovhbAg9jk)

## Phase 1: Data Collection & Basic Analysis
### 1.1 Video Processing (Kinovea)
- Learn basic Kinovea interface
- Track key points in underwater video:
  * Hand position
  * Elbow position
  * Shoulder position
- Export tracking data as CSV/spreadsheet

### 1.2 Initial Data Processing
- Convert tracking data into coordinate points
- Create basic plots of hand movement path
- Identify one complete stroke cycle

## Phase 2: Mathematical Framework
### 2.1 Basic Analysis
- Plot x-y coordinates of hand movement
- Calculate basic metrics:
  * Stroke length
  * Stroke rate
  * Hand velocity

### 2.2 Fourier Series Introduction
- Start with simplified 2D analysis
- Break down periodic motion into components
- Apply basic Fourier series concepts:
  * Fundamental frequency
  * First few harmonics
  * Amplitude calculations

### 2.3 Multiple View Integration
- Introduce basic coordinate transformations
- Compare data from different camera angles
- Calculate error margins between views

## Phase 3: Visualization (Manim)
### 3.1 Basic Animation
```python
from manim import *

class StrokePattern(Scene):
    def construct(self):
        # Create coordinate system
        axes = Axes(
            x_range=[-5, 5],
            y_range=[-3, 3],
            axis_config={"stroke_width": 2}
        )
        
        # Plot hand trajectory
        stroke_path = ParametricFunction(
            lambda t: axes.c2p(
                # x coordinate function
                2 * np.cos(t),
                # y coordinate function
                np.sin(2*t)
            ),
            t_range=[0, TAU]
        )
        
        # Animation sequence
        self.play(Create(axes))
        self.play(Create(stroke_path))
```

### 3.2 Advanced Visualization
- Add Fourier series decomposition animation
- Show harmonic components separately
- Combine views into 3D representation

## Phase 4: Analysis & Integration
### 4.1 Pattern Analysis
- Compare your stroke pattern with ideal patterns
- Identify areas for technique improvement
- Calculate efficiency metrics

### 4.2 Documentation
- Mathematical derivations
- Visual explanations
- Technical implementation details

## Timeline
1. Phase 1: 2-3 weeks
2. Phase 2: 3-4 weeks
3. Phase 3: 2-3 weeks
4. Phase 4: 2-3 weeks

## Required Learning
1. Kinovea
   - Basic interface
   - Motion tracking
   - Data export

2. Mathematics
   - Fourier series basics
   - Coordinate transformations
   - Error analysis

3. Programming
   - Python basics
   - Manim library
   - Data processing
