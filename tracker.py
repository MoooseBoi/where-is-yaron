import cv2
import mediapipe as mp


def capture_thread(shared, width, height):
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray_frame, 1.1, 4)

        try:
            x, y, w, h = faces[0]
        except IndexError:
            continue



        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if not landmark_points:
            continue

        landmarks = landmark_points[0].landmark

        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            if id == 1:
                screen_x = width * landmark.x
                screen_y = height * landmark.y

                shared.put((screen_x, screen_y))
