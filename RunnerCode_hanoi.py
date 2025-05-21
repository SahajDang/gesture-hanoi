import cv2
import mediapipe as mp
import time

# Setup Mediapipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Towers represented as lists
towers = [[3, 2, 1], [], []]  # 3 disks initially on Tower 0

selected_disk = None
source_tower = None

# Recursive Tower of Hanoi Solver (for reference)
def solve_hanoi(n, source, helper, target):
    if n > 0:
        solve_hanoi(n - 1, source, target, helper)
        print(f"Move disk from {source} to {target}")
        solve_hanoi(n - 1, helper, source, target)

# Function to draw towers and disks
def draw_towers(frame):
    h, w, c = frame.shape
    tower_width = w // 3
    for i in range(3):
        cv2.rectangle(frame, (i*tower_width + tower_width//2 - 5, h//2), 
                      (i*tower_width + tower_width//2 + 5, h), (255, 255, 255), -1)
        for j, disk in enumerate(reversed(towers[i])):
            radius = disk * 20
            center_x = i * tower_width + tower_width // 2
            center_y = h - (j+1)*40
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), -1)

# Map x coordinate of hand to tower index
def get_tower_index(x, width):
    if x < width // 3:
        return 0
    elif x < 2 * width // 3:
        return 1
    else:
        return 2

# Main Loop
cap = cv2.VideoCapture(0)

prev_click_time = 0
click_delay = 1  # seconds

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            x = int(hand_landmarks.landmark[8].x * w)  # Index finger tip
            y = int(hand_landmarks.landmark[8].y * h)

            # Draw a circle at index finger tip
            cv2.circle(frame, (x, y), 10, (255, 0, 255), -1)

            current_time = time.time()
            if current_time - prev_click_time > click_delay:
                tower_idx = get_tower_index(x, w)
                if selected_disk is None and towers[tower_idx]:
                    selected_disk = towers[tower_idx].pop()
                    source_tower = tower_idx
                elif selected_disk is not None:
                    # Check if move is valid
                    if not towers[tower_idx] or towers[tower_idx][-1] > selected_disk:
                        towers[tower_idx].append(selected_disk)
                    else:
                        # Invalid move, put disk back
                        towers[source_tower].append(selected_disk)
                    selected_disk = None
                    source_tower = None
                prev_click_time = current_time

    draw_towers(frame)

    if selected_disk:
        cv2.putText(frame, f"Disk {selected_disk} selected", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Tower of Hanoi - Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
