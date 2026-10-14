# Hand Box Glitch Cam

Minimal hand-tracking script (~70 lines, 3 imports) with visible hand bone lines.

## Features
- **Bone Skeleton**: Displays the green skeleton bone lines and red joint dots on every detected hand.
- **Two-Finger Box**: Connects the **thumb (4)** and **index (8)** fingers of both hands into a camera box.
- **Glitch Filter**: Applies the chromatic aberration glitch effect **only inside that box**.
- **Keys**: Press **`q`** or **`Esc`** to quit.

## How to Run
```bash
python hand_filter_cam.py
```
