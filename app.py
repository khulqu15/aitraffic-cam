import cv2
from aiohttp import web
from aiohttp.web_middlewares import middleware
from aiortc import RTCPeerConnection, VideoStreamTrack, RTCSessionDescription
from aiortc.contrib.media import MediaRelay
from av import VideoFrame
import asyncio

pcs = set()
relay = MediaRelay()

@middleware
async def cors_middleware(request, handler):
    response = await handler(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

async def options_handler(request):
    return web.Response(status=204)

class CameraStream(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = VideoFrame.from_ndarray(frame, format='rgb24')
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    local_video = CameraStream()
    pc.addTrack(local_video)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })

app = web.Application(middlewares=[cors_middleware])
app.router.add_post("/offer", offer)
app.router.add_options("/offer", options_handler)
web.run_app(app, port=8080)