import asyncio
import base64
import cv2
import signal
from threading import Event, Lock
from websockets.asyncio.server import serve
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

class Detection:
    def __init__(self):
        self.__VIDEO_SOURCE = 'http://192.168.66.136:4747/video'
        self.__MODEL_PATH = 'yolov8n.pt' 
        self.__FRAME_DELAY = 0.03
        self.__RESIZE_DIM = (640, 480) 
        self.__JPEG_QUALITY = 70
        self.__SKIP_FRAME = 3
        self.__HOST = '0.0.0.0'
        self.__PORT = 8001

        self.__stop_event = Event()
        self.__lock = Lock()
        self.__cap = cv2.VideoCapture(self.__VIDEO_SOURCE)
        if not self.__cap.isOpened():
            raise Exception(f'Cannot open video source: {self.__VIDEO_SOURCE}')

        self.__model = YOLO(self.__MODEL_PATH)
        self.__frame_count = 0

    def __detect_objects(self, frame):
        results = self.__model(frame, verbose=False, agnostic_nms=True)
        annotator = Annotator(frame)

        names = self.__model.names
        boxes = results[0].boxes.xyxy.cpu()
        cls = results[0].boxes.cls.cpu()
        conf = results[0].boxes.conf.cpu()

        for box, conf, cls in zip(boxes, conf, cls):
            annotator.box_label(box, f'{names[int(cls)]} {conf.item():.2f}')
        
        return frame

    async def __video_processing(self, websocket):
        while not self.__stop_event.is_set():
            with self.__lock:
                ret, frame = self.__cap.read()
            if not ret:
                break
            
            frame = cv2.resize(frame, self.__RESIZE_DIM)

            if self.__frame_count % self.__SKIP_FRAME == 0:
                frame = self.__detect_objects(frame)
                self.__frame_count = 0 
            else:
                self.__frame_count += 1

            _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.__JPEG_QUALITY])
            data = base64.b64encode(encoded_frame.tobytes()).decode('utf-8')

            await websocket.send(data)
            await asyncio.sleep(self.__FRAME_DELAY)

    async def __handler(self, websocket):
        try:
            await self.__video_processing(websocket)
        except Exception as e:
            print(f'WebSocket Error: {e}')

    async def start(self):
        async with serve(self.__handler, self.__HOST, self.__PORT):
            await asyncio.get_running_loop().run_in_executor(None, self.__stop_event.wait)

    def stop(self):
        self.__stop_event.set()
        self.__cap.release()

    def run(self):
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            self.stop()

if __name__ == '__main__':
    detection_server = Detection()
    signal.signal(signal.SIGINT, lambda sig, frame: detection_server.stop())
    detection_server.run()