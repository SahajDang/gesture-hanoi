import cv2
import mediapipe as mp
import time

# Setup Mediapipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Towers represented as lists
towers = [[3, 2, 1], [], []]  # 3 disks on Tower 0 initially

selected_disk = None
source_tower = None
holding_disk = False

# Map x coordinate of hand to tower index
def get_tower_index(x, width):
    if x < width // 3:
        return 0
    elif x < 2 * width // 3:
        return 1
    else:
        return 2

# Draw towers and disks
def draw_towers(frame, holding_pos=None, holding_disk=None):
    h, w, _ = frame.shape
    tower_width = w // 3
    disk_height = 30  # Fixed height per disk
    vertical_spacing = 10  # Space between disks
    colors = [(0, 0, 255), (0, 165, 255), (0, 255, 0)]  # Disk colors

    for i in range(3):
        # Draw the tower rod
        tower_center_x = i * tower_width + tower_width // 2
        cv2.rectangle(frame, (tower_center_x - 5, h // 2),
                      (tower_center_x + 5, h), (255, 255, 255), -1)

        # Draw the disks from bottom to top
        for j, disk in enumerate(reversed(towers[i])):
            center_x = tower_center_x
            center_y = h - (j + 1) * (disk_height + vertical_spacing)

            disk_width = disk * 40
            top_left = (center_x - disk_width // 2, center_y - disk_height // 2)
            bottom_right = (center_x + disk_width // 2, center_y + disk_height // 2)

            color = colors[disk - 1] if disk <= len(colors) else (0, 255, 255)
            cv2.rectangle(frame, top_left, bottom_right, color, -1)
            
    # Draw the held disk (if any)
    if holding_pos and holding_disk:
        cx, cy = holding_pos
        disk_width = holding_disk * 40
        top_left = (cx - disk_width // 2, cy - disk_height // 2)
        bottom_right = (cx + disk_width // 2, cy + disk_height // 2)
        color = colors[holding_disk - 1] if holding_disk <= len(colors) else (255, 255, 0)
        cv2.rectangle(frame, top_left, bottom_right, color, -1)

# Main Loop
cap = cv2.VideoCapture(0)
prev_click_time = 0
click_delay = 1  # seconds

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    index_pos = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)
            index_pos = (x, y)

            cv2.circle(frame, (x, y), 10, (255, 0, 255), -1)

            current_time = time.time()
            if current_time - prev_click_time > click_delay:
                tower_idx = get_tower_index(x, w)

                if not holding_disk and towers[tower_idx]:
                    selected_disk = towers[tower_idx].pop()
                    source_tower = tower_idx
                    holding_disk = True

                elif holding_disk:
                    if not towers[tower_idx] or towers[tower_idx][-1] > selected_disk:
                        towers[tower_idx].append(selected_disk)
                    else:
                        # Invalid move, revert
                        towers[source_tower].append(selected_disk)

                    selected_disk = None
                    source_tower = None
                    holding_disk = False

                prev_click_time = current_time

    draw_towers(frame, holding_pos=index_pos if holding_disk else None,
                holding_disk=selected_disk if holding_disk else None)

    if holding_disk and selected_disk:
        cv2.putText(frame, f"Disk {selected_disk} selected", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Tower of Hanoi - Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()