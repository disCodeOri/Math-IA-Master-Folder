# Analyzing Swim Stroke Patterns Using Fourier Series
*IB Mathematics AA HL Internal Assessment*

## Introduction
During a break from swim training, I discovered a YouTube video showing how Fourier series could create intricate animations, including a portrait of Joseph Fourier himself emerging from mathematical equations. As a triathlete who has spent countless hours perfecting stroke techniques, the mesmerizing way these complex patterns emerged from simple trigonometric functions sparked a realization: just as Fourier series could reconstruct detailed drawings, they could potentially decompose and analyze the periodic, fluid motions of swimming strokes into their fundamental mathematical elements.

### Research Question
How can Fourier series be applied to analyze and optimize swim stroke patterns in freestyle swimming, and what insights can this mathematical analysis provide for technique improvement?

### Aim
This exploration aims to:
1. Model the periodic motion of freestyle swimming strokes using Fourier series
2. Identify key harmonic components that contribute to efficient swimming technique
3. Develop a mathematical framework for analyzing swimming efficiency
4. Provide quantitative insights for technique optimization

## Mathematical Framework

### 1. Fourier Series Fundamentals
A Fourier series represents a periodic function f(t) as an infinite sum of sine and cosine terms:

f(t) = a₀/2 + Σ(n=1 to ∞)[aₙcos(nωt) + bₙsin(nωt)]

where:
- a₀/2 is the mean value of the function over its period
- ω = 2π/T is the fundamental frequency (T is the period)
- aₙ and bₙ are the Fourier coefficients

The Fourier coefficients are calculated using:

aₙ = (2/T)∫[f(t)cos(nωt)]dt from -T/2 to T/2
bₙ = (2/T)∫[f(t)sin(nωt)]dt from -T/2 to T/2

### 2. Application to Swim Stroke Analysis
In freestyle swimming, the stroke pattern can be broken down into several key components:

1. **Vertical Hand Movement**
   y(t) = Σ[Aₙsin(nωt + φₙ)]
   where:
   - Aₙ represents amplitude of each harmonic
   - φₙ represents phase shift
   - n represents harmonic number

2. **Horizontal Hand Movement**
   x(t) = Σ[Bₙcos(nωt + θₙ)]
   where:
   - Bₙ represents amplitude of each harmonic
   - θₙ represents phase shift

### 3. Data Collection Methodology
To analyze actual swim strokes, I will:
1. Record video footage of freestyle swimming from side and top views
2. Track hand positions using motion tracking software
3. Convert position data into time series
4. Apply Fourier analysis to the time series data

### 4. Initial Analysis Plan
1. Extract position coordinates (x,y) at regular time intervals
2. Calculate Fourier coefficients for both x(t) and y(t)
3. Determine significant harmonics
4. Compare coefficients between different skill levels

## Preliminary Work Required
1. **Data Collection Setup**
   - Camera positioning
   - Motion tracking calibration
   - Sampling rate determination

2. **Mathematical Tools**
   - Fourier coefficient calculation methods
   - Error analysis framework
   - Graphical representation techniques

3. **Software Requirements**
   - Video analysis software
   - Mathematical computation tools
   - Data visualization packages

## Next Steps
1. Begin data collection with multiple swimmers
2. Develop computational methods for Fourier analysis
3. Create visualization tools for results
4. Establish criteria for pattern evaluation

[Note: This draft will be expanded with actual data analysis, results, and detailed mathematical work in subsequent revisions.]

## Personal Engagement
My experience as a triathlete has given me unique insights into the importance of swimming technique. This exploration combines my passion for swimming with advanced mathematical concepts, allowing me to:
1. Better understand the mechanics of my own swimming
2. Develop quantitative methods for technique analysis
3. Contribute to the broader understanding of swimming biomechanics

## Expected Challenges
1. Accurate data collection underwater
2. Dealing with noise in motion tracking
3. Determining appropriate number of harmonics
4. Interpreting results in practical context