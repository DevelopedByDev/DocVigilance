import cv2
import numpy as np
import av
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import os
import logging
from twilio.rest import Client
import streamlit as st
import math


# logger = logging.getLogger(__name__)
alarm = False
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
face_mesh=mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5)

# Euclaidean distance 
def euclaideanDistance(point1, point2):
    x1,y1 = point1.x,point1.y
    x2,y2 = point2.x,point2.y
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def process(image):
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
        # right 145,159 bot top
        # left 374,386 bot top
        for face_landmarks in results.multi_face_landmarks:
            right_distance = euclaideanDistance(face_landmarks.landmark[145],face_landmarks.landmark[159])
            left_distance = euclaideanDistance(face_landmarks.landmark[374],face_landmarks.landmark[386])
            distance = min(right_distance,left_distance)
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style())
            if distance < 0.01:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())
    return cv2.flip(image, 1)

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def get_ice_servers():

    # Ref: https://www.twilio.com/docs/stun-turn/api
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError:
        # logger.warning(
        #     "Twilio credentials are not set. Fallback to a free STUN server from Google."  # noqa: E501
        # )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)

    token = client.tokens.create()

    return token.ice_servers

class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = process(img)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={"iceServers": get_ice_servers()},
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=VideoProcessor,
    async_processing=True,
)
