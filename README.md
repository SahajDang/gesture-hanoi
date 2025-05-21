# 🧠 Tower of Hanoi - Hand Gesture Control

An interactive and intuitive implementation of the classic **Tower of Hanoi** puzzle using real-time **hand gesture control** with **MediaPipe** and **OpenCV**.

> 🎯 Move disks between towers using just your index finger — no mouse, no keyboard!

---

## 🚀 Features

- 🎮 Control the Tower of Hanoi puzzle using your **hand gestures**.
- ✋ Uses **MediaPipe** for accurate fingertip tracking.
- 🔴🟠🟢 Disks are color-coded and dynamically rendered.
- ⛔ Prevents invalid moves (can’t place larger disk on a smaller one).
- 🕹️ Fully interactive in real time using your webcam.

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV** – for video capture and rendering
- **MediaPipe** – for hand and fingertip landmark detection
- **Numpy** – for efficient frame handling (implicitly through OpenCV)

---

## 📦 Requirements

Install dependencies using pip:

pip install opencv-python mediapipe

---
▶️ How to Run
1. Clone this repository:

git clone https://github.com/YOUR-USERNAME/gesture-hanoi.git


cd gesture-hanoi

2. Run the script:
   
python hanoi_gesture_control.py


3. Allow camera access. The game will start using your webcam input.


4. Use your index finger to hover over the towers:
   
<ul> Pick a disk by hovering for a second. </ul>

<ul> Move and drop it on a valid tower. </ul>

<ul> Solve the puzzle just like in classic Tower of Hanoi! </ul>

---
### 🧠 Game Rules (Quick Refresher)

Only one disk can be moved at a time.

Only the top disk on any rod can be moved.

A larger disk may not be placed on top of a smaller disk.

Objective: Move all disks from Tower 1 to Tower 3.


--- 
✅ Future Improvements

Visual highlighting for hovered towers

Move counter and timer for gamification

Sound effects and winning animation

Difficulty levels (4+ disks)

Add support for voice commands or gesture clicks

---

🙌 Acknowledgments

MediaPipe by Google

OpenCV

---

📄 License

This project is licensed under the MIT License.
