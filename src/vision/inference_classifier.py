import pickle
import cv2
import mediapipe as mp
import numpy as np
import threading
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent / ""

class HandGestureClassifier:
    def __init__(self):
        # Load the trained model
        model_dict = pickle.load(open(BASE_DIR / "model.p", 'rb'))
        self.model = model_dict['model']

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, model_complexity=1, min_detection_confidence=0.7)

        # Define labels dictionary
        self.labels_dict = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E',
            5: 'F', 6: 'G', 7: 'H', 8: 'I',
            9: 'K', 10: 'L', 11: 'M', 12: 'N', 13: 'O',
            14: 'P', 15: 'Q', 16: 'R', 17: 'S', 18: 'T',
            19: 'U', 20: 'V', 21: 'W', 22: 'X', 23: 'Y'
        }

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)
        self.predicted_character = ""
        self.stop_thread = False
        self.thread = threading.Thread(target=self.run_inference, daemon=True)
        self.thread.start()

    def run_inference(self):
        while not self.stop_thread:
            ret, frame = self.cap.read()
            if not ret:
                continue

            data_aux = []
            x_ = []
            y_ = []

            H, W, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                    # Ensure data_aux has exactly 42 features
                    if len(data_aux) != 42:
                        continue

                    prediction = self.model.predict([np.asarray(data_aux)])
                    self.predicted_character = self.labels_dict[int(prediction[0])]

            time.sleep(1)  # to reduce CPU usage

    def get_prediction(self):
        return self.predicted_character
 
    def release(self):
        self.stop_thread = True
        self.thread.join()
        self.cap.release()
        cv2.destroyAllWindows()


# For testing purposes
if __name__ == "__main__":
    classifier = HandGestureClassifier()
    try:
        while True:
            ret, frame = classifier.cap.read()
            if not ret:
                break

            # Display the predicted character on the frame
            cv2.putText(frame, f'Prediction: {classifier.get_prediction()}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Hand Gesture Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass

    finally:
        classifier.release()
        cv2.destroyAllWindows()
