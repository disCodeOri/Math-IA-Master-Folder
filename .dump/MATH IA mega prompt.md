I need to make my Math IA's Draft, and here's the structure that I am gonna follow for the IA.

```
1. Introduction, Purpose, ...
2. Research Question
3. Rationale (Everything about the process which you are going to follow)
4. Research and Data Collection
5. All the graphs (using tools) along with the video snippets pictures (reference: video links), the csv data in table for noise cancellation process and then the reference to the code that generates the and the graphs in main part.
6. Now the corrected CSV (amplitude with respect to time) data table along with its Mathematical explanation from FFT.
7. Statistical analysis for Comparison- between 2 different years for Bolt and then between Bolt and Justin
2016.
(2008 and 2016 for Bolt and 2016 for Justin G)
8. Result...
```

Additional notes:

Purpose:
Identifying the differences in stride patterns in Usain Bolt's 2008 and 2016 olympic performance and the differences in stride of usain bolt and Justin gatlin in the 2016 Olympics. for the final 100mtr sprint event.

For the statistical analysis my teacher told me something about the pearson correlation coefficient. And she is yet to teach me about that, so yeah. and i'm not so aware of what the process really is for the statistical analysis.

For the data collection I used kinovea to extract points of motion of Usain bolt's and Gatlin's ankles, with their hips being the point of origin for their own respective motion. And the y axis being aligned with their torso.

And I used FFT from Sci py to remove any noise that was generated due to camera motion, and that was actually done by separately tracking the motion of the hip and then using the FFT algorithm in scipy to remove the noise. I have attached the code.

```py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from matplotlib.widgets import RadioButtons
from scipy.signal import savgol_filter

# Load data and drop rows with missing values
df = pd.read_csv("Bolt ankles vertical position graph values.csv").dropna()
time = df["Time (ms)"].values / 1000  # Convert ms to seconds
ankle1 = df["Ankle 1"].values
ankle2 = df["Ankle 2"].values
hip = df["2008 hip"].values

def remove_camera_shake(ankle_signal, hip_signal):
    # The hip should ideally have minimal vertical movement
    # So we can treat hip motion as camera shake
    # Simply subtract the hip motion to stabilize the view
    stabilized_motion = ankle_signal - hip_signal

    # Optional: Smooth out any high-frequency noise
    window = 11  # Smaller window to preserve more detail
    stabilized_smooth = savgol_filter(stabilized_motion, window, 3) #Savitzky-Golay filter, performs smoothing on data points to increase the signal-to-noise ratio without greatly distorting the signal. It fits successive sub-sets of adjacent data points with a low-degree polynomial using linear least squares.

    return stabilized_smooth

# Apply to both ankles
ankle1_cleaned = remove_camera_shake(ankle1, hip)
ankle2_cleaned = remove_camera_shake(ankle2, hip)

# Create a DataFrame with the cleaned data
cleaned_data = pd.DataFrame({
    'Time (s)': time,
    'Cleaned Ankle 1': ankle1_cleaned,
    'Cleaned Ankle 2': ankle2_cleaned,
    'Original Ankle 1': ankle1,
    'Original Ankle 2': ankle2,
    'Hip Position': hip
})

# Export to a new CSV file
output_filepath = "cleaned_ankle_data.csv"
cleaned_data.to_csv(output_filepath, index=False)
print(f"Cleaned data saved to: {output_filepath}")

# Create figure and subplots
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(left=0.3)  # Make room for radio buttons

# Calculate frequency domain data for both ankles
freq = np.fft.fftfreq(len(time), d=(time[1]-time[0]))
ankle1_fft_clean = fft(ankle1_cleaned)
ankle2_fft_clean = fft(ankle2_cleaned)
power_clean1 = np.abs(ankle1_fft_clean)**2
power_clean2 = np.abs(ankle2_fft_clean)**2

# Create radio buttons for domain selection
rax1 = plt.axes([0.05, 0.7, 0.2, 0.15])
radio_domain = RadioButtons(rax1, ('Time Domain', 'Frequency Domain'))

# Create radio buttons for ankle selection
rax2 = plt.axes([0.05, 0.4, 0.2, 0.15])
radio_ankle = RadioButtons(rax2, ('Ankle 1', 'Ankle 2'))

def update_plot():
    ax.clear()
    domain = radio_domain.value_selected
    ankle = radio_ankle.value_selected

    if domain == 'Time Domain':
        if ankle == 'Ankle 1':
            ax.plot(time, ankle1, 'b', alpha=0.5, label="Raw Ankle 1")
            ax.plot(time, ankle1_cleaned, 'r', label="Cleaned Ankle 1")
        else:
            ax.plot(time, ankle2, 'b', alpha=0.5, label="Raw Ankle 2")
            ax.plot(time, ankle2_cleaned, 'r', label="Cleaned Ankle 2")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Position")
        ax.set_title(f"{ankle}: Raw vs. Cleaned")
        ax.legend()
    else:
        if ankle == 'Ankle 1':
            ax.plot(freq[:len(freq)//2], power_clean1[:len(freq)//2], 'g')
        else:
            ax.plot(freq[:len(freq)//2], power_clean2[:len(freq)//2], 'g')
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Power")
        ax.set_title(f"{ankle} Power Spectrum")
    fig.canvas.draw_idle()

# Initial plot
update_plot()

# Connect radio button events
radio_domain.on_clicked(lambda x: update_plot())
radio_ankle.on_clicked(lambda x: update_plot())

plt.show()
```

I need to write up a draft until the 6th point since stats hasn't been covered yet.

Additional notes:
I don't have any hypotheses. Real world significance: I dunno maybe better analysis methods for people with lower end equipment for sports with periodic motion.
I'm gonna take stride freq. and stride length for specific metrics to choose.
Why compare Bolt’s 2008 vs. 2016? cuz simply comparing justing and bolt would be too less content to talk about.
Why Bolt vs. Gatlin in 2016? Cuz that was the only video I found of those two in the same single race.
Why use Kinovea and FFT? Cuz that was the first thing I found, I didn't really dive too deep into it.
How did I track hips/ankles in Kinovea? A mix of manual and automated tracking. Frame rate is at 29.97. I do have some level of noise in the terms of zooming and the player drifting across the screen, but I only fixed the drifting part and left the zooming problem unsolved, but it doesn't seem to be posing a large issue here.
What graphs will you include? I wil be including both the raw and the filtered graphs and also show the process behind the denoising along with the math for it. I will try to include as much as I can to meet that 2000 word mark. But I can't go beyond that mark.

Now I simply want you to just help me make the drafts itself. I will always specify clearly what I need. Also I need that section in coherent paragraphs. The examiners look down upon listing.

Here's what I cooked up for the introduction part.

```md
The biomechanics of sprinting, particularly stride patterns, play a critical role in athletic performance. This investigation compares the stride dynamics of Usain Bolt (2008 vs. 2016 Olympics) and Bolt vs. Justin Gatlin (2016 Olympics) during the 100m final. The purpose is to demonstrate accessible methods for motion analysis using low-cost tools (Kinovea) and signal processing (FFT). Aiding coaches and sports persons of sports involving periodic motion to be able to analyse their performance and chart their course of improvement accordingly. All without the need to spend on expensive equipment.
Personally, as a triathlete, the result of this investigation will help me in improving my own stride patterns in Swimming, Cycling and especially Running.
The thought of this investigation sprouted when I was unable to collaborate with my coach in improving my running stride as he lives far away and so he usually assigns me the workouts through online messaging and video calls. But making sure that I was able to perform the proper technique was always a monumental question. Hence this investigation to lay the groundwork for a system to allow cost-efficient analysis.

The reason why I chose the specific configuration of comparing Usian Bolt's own performance in 2008 and 2016 and also comparing the 2016 performance with the performance of Justin Gatlin in the same year is that the camera motion in all the footages contain a considerable amount of noise, which is a common issue in sports analysis, and generally to mitigate that issue the analysers try to keep the camera stationary and this requires a large resolution, resulting in expensive apparatus and furthermore, this limits the analysis as it is harder to spot issues in a footage where the player is not stationary, and is, what I call, "drifting across the screen". Such footage gravely hinders the coach's ability to spot any issues where the runner's legs may be deviating from the ideal technique. And so this investigation utilises footage that is ideal for proper analysis, which is a side view footage. And to tackle the challenge of any noise in the data that is obtained.

I would like to specifically investigate the differences in stride length and the stride frequency. As they are the most essential metric for measuring improvements in performance and also simultaneously provide a strong standpoint for technique improvement.

The stride length of a runner in this investigation is the maximum distance that the heel of a runner deviates from the Y-axis, where the Y-axis is aligned to the runner's torso. Generally speaking, the ideal stride length of a runner depends on the body of the runner. The shorter the body of the runner the shorter the ideal stride length, and vice versa. Any deviation from this ideal stride length causes significant loss in performance, hence it is imperative for a runner to maintain a consistent stride length.

The stride frequency of a runner is the no. of strides per unit time. This is also an important metric in running, as a higher stride frequency means that the runner is able put in more net force upon the ground per unit time to accelerate forward. Which also helps in overcoming the loss in speed caused by drag that slows down the runner.
```

Here's the RQ:

```md
How do Usain Bolt’s stride patterns (stride length and frequency) differ between the 2008 and 2016 Olympic 100m finals, and how do they compare to Justin Gatlin’s in the 2016 final?
```

Here's the rationale section so far:

```md
Rationale
My approach to this will involve the use of side view footage from the 2008 and 2016 Olympics, the specific event being the final 100 meter sprint.

<sample snapshot from video showing the runners>

To perform the analysis I will be using an existing software that is widely used by many coaches for basic video analysis, called Kinovea. This software will allow me to track the joints of the runners and obtain a position-against-time graph for their motion. It will also allow me to align the coordinate plane's y-axis with the runner’s torso, and also set the origin point of the coordinate plane to the runner’s hip. This will allow me to mitigate the aforementioned issue of “drifting” reducing a significant amount to noise generated.

The tracking process in Kinovea combines both manual and automated tracking at 29.97 frames per second. While the software's automated tracking helps maintain consistency, manual corrections are sometimes necessary to ensure accuracy, especially during rapid movements. For each runner, I track three key points: the hip joint which serves as the origin point and helps account for lateral movement, and the ankle joint which is critical for measuring stride length and frequency.

Despite setting the coordinate system relative to the runner's body, some noise remains in the data due to camera movement and zoom variations. To address this, I implement a Fast Fourier Transform (FFT) algorithm using Python's SciPy library. The FFT is particularly suitable because it can separate periodic motion (the runner's natural stride) from random noise (camera shake), while preserving the important frequency components of the stride pattern and allowing for selective filtering of unwanted frequency components.

The data processing follows a comprehensive workflow. Initially, I export position-time data from Kinovea as CSV files. This data is then processed using Python to remove camera motion. The process treats hip movement as a reference for camera shake, subtracting this motion from ankle motion measurements. A Savitzky-Golay filter is then applied to smooth any remaining high-frequency noise. This processing allows me to generate both raw and filtered graphs for analysis. From this cleaned data, I can calculate the crucial stride metrics: stride length, measured as maximum horizontal displacement of ankle from vertical axis, and stride frequency, computed from the time domain signal using FFT analysis.

This methodology enables meaningful comparison between different races while accounting for variations in video quality and camera movement. The approach is intentionally designed to work with readily available footage and tools, making it accessible for broader application in sports analysis. The selection of stride length and frequency as key metrics is based on their fundamental role in sprint performance and their measurability using this technique. These parameters directly influence a sprinter's velocity and can reveal changes in technique between performances.
```

I can get screenshots of the two runners with the noisy graphs and tracking paths and also the cleaned data's graphs, so you can go all out on the diagrams but don't make it super excessive.

Here's the 4th, 5th and 6th section so far:

```md
Research and Data Collection - Mathematical Framework

The analysis of stride patterns requires robust mathematical processing to extract meaningful data from video footage. This section details the mathematical principles and algorithms employed in the investigation, with implementation details available in Appendix A.

Signal Processing Fundamentals

The raw positional data obtained from Kinovea contains both the desired stride pattern signals and unwanted noise components. The vertical position of an ankle joint $y(t)$ can be mathematically represented as:

$y(t) = s(t) + n(t) + c(t)$

where $s(t)$ represents the actual stride motion, $n(t)$ represents random noise, and $c(t)$ represents systematic camera motion.

<note>Diagram 1: A visual representation showing the decomposition of the raw signal into its components: stride motion, random noise, and camera motion. This could be three separate wave patterns that sum to create the observed signal.</note>

Fast Fourier Transform (FFT)

The Fast Fourier Transform is fundamental to our noise reduction process. The FFT converts our time-domain signal into the frequency domain, expressing the signal as a sum of sinusoidal components:

$Y(f) = \int_{-\infty}^{\infty} y(t)e^{-2\pi ift}dt$

where $Y(f)$ represents the frequency components of our signal. In discrete implementation, this becomes:

$Y[k] = \sum_{n=0}^{N-1} y[n]e^{-2\pi ikn/N}$

<note>Diagram 2: Side-by-side comparison of a time-domain signal and its frequency-domain representation after FFT, highlighting the periodic components of stride patterns versus noise.</note>

Camera Motion Compensation

To address camera motion, we utilize the hip position as a reference point. The hip's vertical motion $h(t)$ primarily reflects camera movement since the actual vertical hip motion during sprinting is relatively minimal. The stabilized ankle position $y_{stable}(t)$ is computed as:

$y_{stable}(t) = y(t) - h(t)$

This subtraction effectively removes the camera motion component $c(t)$ from our signal.

Savitzky-Golay Filtering

After camera motion compensation, we apply a Savitzky-Golay filter to smooth remaining high-frequency noise while preserving the important characteristics of the stride pattern. This filter fits successive windows of data points to a polynomial of degree $n$:

$p(t) = \sum_{k=0}^{n} a_k t^k$

For our analysis, we use a window size of 11 points and a polynomial degree of 3, providing optimal balance between noise reduction and signal preservation. The coefficients $a_k$ are determined through least squares minimization:

$\min \sum_{i=-m}^{m} (y_i - p(i))^2$

where $m$ represents the half-width of the window.

<note>Diagram 3: Before and after comparison showing the effect of Savitzky-Golay filtering on a noisy signal, demonstrating how it preserves the shape of stride patterns while removing noise.</note>

Stride Metrics Calculation

From the processed data, we calculate two key metrics:

1. Stride Length:
   The maximum horizontal displacement from the vertical axis, calculated as:

$L_{stride} = \max_{t}|x(t)|$

where $x(t)$ represents the horizontal position relative to the hip.

2. Stride Frequency:
   Calculated from the frequency domain representation after FFT:

$f_{stride} = \argmax_f |Y(f)|$

where $|Y(f)|$ represents the magnitude spectrum of the processed signal.

<note>Diagram 4: Annotated graph showing how stride length and frequency are measured from the processed data, with clear labels indicating the metrics.</note>

Signal Quality Assessment

To validate our processing, we calculate the signal-to-noise ratio (SNR) before and after filtering:

$SNR = 10\log_{10}\left(\frac{P_{signal}}{P_{noise}}\right)$

where $P_{signal}$ and $P_{noise}$ represent the power of the signal and noise components respectively.

The implementation of these mathematical concepts in Python code can be found in Appendix A, which utilizes the SciPy library's FFT and signal processing modules. The code applies these mathematical principles to transform raw tracking data into clean, analyzable stride patterns, enabling precise comparison between different performances.

Data Analysis and Visual Results

The application of our mathematical framework to the video footage yields several key visualizations that illuminate the differences in stride patterns. Let's examine the data processing stages and their results.

Raw Data Collection

<note>Diagram 5: Side-by-side screenshots from Kinovea showing the tracking points for both Bolt (2008 and 2016) and Gatlin (2016). Each screenshot should highlight the hip reference point and ankle tracking points with their respective coordinate systems aligned to the torso.</note>

The initial tracking data from Kinovea reveals the inherent challenges in our analysis. The raw position-time graphs for each athlete show significant noise from camera movement:

<note>Diagram 6: Raw position-time graphs for:

1. Bolt 2008 - showing both ankles' vertical position with visible camera shake
2. Bolt 2016 - same format
3. Gatlin 2016 - same format
   Each graph should include the hip position line to illustrate the camera motion component.</note>

Noise Reduction Results

After applying our FFT-based noise reduction algorithm, we observe a marked improvement in signal clarity. The processed data reveals the true stride patterns:

<note>Diagram 7: Processed position-time graphs (same format as Diagram 6, but showing cleaned data). Include a zoomed-in section showing how the noise has been removed while preserving the stride pattern characteristics.</note>

The effectiveness of our noise reduction approach is particularly evident in the frequency domain representation:

<note>Diagram 8: Power spectrum plots showing:

1. Original signal with noise
2. Cleaned signal with clear stride frequency peaks
   Label the primary stride frequency peaks for each athlete.</note>

Stride Pattern Analysis

From the cleaned data, we can extract precise measurements of stride characteristics. The vertical position graphs reveal clear periodic patterns:

For Bolt's 2008 performance:

- Average stride length: [Your measured value] meters
- Stride frequency: [Your measured value] Hz
- Pattern consistency: [Observed variation in stride metrics]

For Bolt's 2016 performance:

- Average stride length: [Your measured value] meters
- Stride frequency: [Your measured value] Hz
- Pattern consistency: [Observed variation in stride metrics]

For Gatlin's 2016 performance:

- Average stride length: [Your measured value] meters
- Stride frequency: [Your measured value] Hz
- Pattern consistency: [Observed variation in stride metrics]

<note>Diagram 9: Composite graph showing overlaid cleaned stride patterns for all three performances, color-coded for easy comparison. Include annotations highlighting key differences in stride length and frequency.</note>

Data Validation

To verify the reliability of our analysis, we performed several validation checks:

1. Signal-to-Noise Ratio Improvement:
   Before cleaning: [SNR value] dB
   After cleaning: [SNR value] dB

2. Stride Pattern Consistency:
   Standard deviation in stride length and frequency for each athlete, demonstrating the stability of their technique throughout the analyzed portion of the race.

3. Processing Artifacts:
   Careful examination of the cleaned signals confirms that our noise reduction process preserved the authentic stride characteristics while removing unwanted artifacts.

<note>Diagram 10: Quality control visualization showing:

1. Original vs. cleaned signal overlay
2. Residual plot (difference between original and cleaned signals)
3. SNR improvement visualization</note>

These results provide a solid foundation for our subsequent statistical analysis, offering clear evidence of both the differences and similarities in stride patterns between the performances. The cleaned data reveals subtle technical variations that were obscured in the raw footage, demonstrating the effectiveness of our analytical approach.
```

-

Don't redescribe the stuff that has already been covered in the previous sections.
