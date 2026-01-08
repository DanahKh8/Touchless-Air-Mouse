# 👆🖱️ Touchless Air Mouse

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat&logo=python)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Computer%20Vision-orange?style=flat&logo=google)
![OpenCV](https://img.shields.io/badge/OpenCV-Image%20Processing-green?style=flat&logo=opencv)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-red?style=flat)

> **"The ultimate tool for multitasking."**
> A contact-free controller designed for sanitary and seamless browsing, allowing you to scroll and click without ever touching a device.

## Demo Preview
**Real-Time Hand Tracking & Cursor Control**
![Demo Preview](demo_preview.gif)

---

## How It Works
This tool leverages **Google MediaPipe**, a high-fidelity hand-tracking solution.
1.  **Landmark Detection:** The app captures video input and detects 21 distinct 3D landmarks on the user's hand in real-time.
2.  **Coordinate Scaling:** It tracks the Index Finger (Landmark 8) and maps its position from the camera frame to the computer screen using linear interpolation.
3.  **Gesture Recognition:**
    * **Movement:** A virtual "mousepad" box reduces arm fatigue by amplifying small movements.
    * **Clicking:** Calculates the Euclidean distance between the Thumb and Index finger; a "pinch" triggers a click.
    * **Scrolling:** Detects when the hand enters the top or bottom 10% of the frame to trigger dynamic scrolling.

## Technical Stack
* **Language:** Python
* **ML Framework:** MediaPipe Hands
* **Image Processing:** OpenCV
* **Automation:** PyAutoGUI & Ctypes (Windows API)

## Local Installation
If you want to run this locally on your machine:

```bash
# 1. Clone the repository
git clone [https://github.com/DanahKh8/Touchless-Air-Mouse.git](https://github.com/DanahKh8/Touchless-Air-Mouse.git)
cd Touchless-Air-Mouse

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python Touchless_Controller.py
