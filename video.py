import threading

import cv2
import streamlit as st
from matplotlib import pyplot as plt

from streamlit_webrtc import webrtc_streamer

    img = frame.to_ndarray(format="bgr24")

    results = model(img)
    output_img = np.squeeze(results.render())

    return av.VideoFrame.from_ndarray(output_img, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback)