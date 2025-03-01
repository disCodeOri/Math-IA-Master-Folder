- Savitzky-golay fliter cleaning for 2008 data only
- Data scaling for all the data to resolve zooming issue for all 3 data sets.
  (Used 2016 Usain bolt data as the reference point for which to scale up or down to).
  - Method: Set/calibrated the in-video height of 2016 usain bolt as 195cm (real height of usain bolt {but that number is arbitrary}), then I measured the heights of the 2008 bolt and Gatlin. once I got that I plugged into the scaling script {refer to Qwen2.5Max chat: https://chat.qwen.ai/c/912326d1-085e-40e8-bafc-62577c049c99}
  - I didn't scale up or down the 2008 vertical data as the current data somehow didn't have that issue.

Will perform:

- Pearson's Correlation Coefficient

In video heights after calibration:

- Gatlin: 138.72
- Bolt (2008): 241.17
