import cv2
import mediapipe as mp
import numpy as np
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

cTime = 0
pTime = 0

# TO MAKE EACH VIDEO RECORDING UNIQUE PATIENT ID IS NEEDED
# patient_id = int(input("Enter patient ID: "))

width = int(cap.get(3))
height = int(cap.get(4))

size = (width, height)

# RECORDING VIDEO
# result = cv2.VideoWriter(f'{patient_id}.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)


frames = []
frame_counter = 0 # TODO: incremenet this at the end


while True:

    if frame_counter != 5:
        success, img = cap.read()

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        start_time = time.time()
        stop_time = 0.0
        time_diff = 0.0

        frame_row = [start_time, stop_time, time_diff]

        hand_results = hands.process(imgRGB)

        if hand_results.multi_hand_landmarks:
            for handLms in hand_results.multi_hand_landmarks:
                # handLms.landmark is the Python list of all hand landmarks observed in one frame
                for lmk in handLms.landmark:
                    current_landmark = np.array([(lmk.x)*width, (lmk.y)*height])
                    frame_row.append(current_landmark)
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        stop_time = time.time()
        frame_row[1] = stop_time
        time_diff = stop_time - start_time
        frame_row[2] = time_diff

        # # VIDEO WRITING, VIDEO VARIABLE NAME IS result
        if len(frame_row) == 24:
            frames.append(frame_row)
        # result.write(img) 

        frame_counter += 1    

        # FPS CALCULATION AND DISPLAY
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 10)

    else:
        frame_counter = 0

        # CALCULATING DISTANCES
        n = 60
        last_n_frames = frames[-n::] # last 5 frame_rows; each frame_row = [start_time, stop_time, time_diff, 21*[x, y, z for each hand landmark]]

        current_distances = []
        current_velocities = []

        last_n_distances = []
        last_n_velocities = []

        # 5 frames -> 4 distances -> 3 velocities -> 2 accelerations

        if (len(last_n_frames) == n):
            for i in range(1, len(last_n_frames)):
                # excluding start_time, stop_time and time_diff from each frame_row
                current_distances.append(np.array(last_n_frames[i][3:]) - np.array(last_n_frames[i-1][3:]))
                current_velocities.append((np.array(last_n_frames[i][3:]) - np.array(last_n_frames[i-1][3:]))/last_n_frames[i][2])

                last_n_distances.append(current_distances)
                last_n_velocities.append(current_velocities)
                current_distances = []
                current_velocities = []
        
            # print(len(last_n_velocities))

        if len(last_n_velocities) == n-1:
            cumulative_velocity = last_n_velocities[0]
            for i in last_n_velocities[1::]:
                cumulative_velocity = np.add(cumulative_velocity, i)
            avg_velocity = cumulative_velocity/len(last_n_velocities)
            
            print(avg_velocity[0][8][0])
            # print("done")

            cumulative_avg_velocity = avg_velocity[0][0]
            for j in range(1, len(avg_velocity[0])):
                cumulative_avg_velocity = np.add(cumulative_avg_velocity, j)
            final_avg_velocity = cumulative_avg_velocity/len(avg_velocity[0])

            if ((abs(avg_velocity[0][8][0]) > 32) and (abs(avg_velocity[0][8][0]) < 52)) or ((abs(avg_velocity[0][8][1]) > 32) and (abs(avg_velocity[0][8][1]) < 52)):
                # cv2.putText(img, "SHAKING", (500, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 10)
                # # time.sleep(0.5)
                print("SHAKING")

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
# result.release()
cv2.destroyAllWindows()