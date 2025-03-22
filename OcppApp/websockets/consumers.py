import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from ocpp.routing import on
from ocpp.v16 import call, call_result
from ocpp.v16.enums import *

logger = logging.getLogger(__name__)

class OCPPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("Charger connected via WebSocket")

    async def disconnect(self, close_code):
        logger.info("Charger disconnected")

    async def receive(self, text_data):
        logger.info(f"Received: {text_data}")
        # Process OCPP messages here

    @on(Action.boot_notification)
    async def on_boot_notification(self, charge_point_model, **kwargs):
        logger.info(f"Boot notification from: {charge_point_model}")
        return call_result.BootNotification(
            status=RegistrationStatus.accepted,
            current_time="2025-01-01T12:00:00Z",
            interval=300,
        )
    @on(Action.heartbeat)
    async def on_heartbeat(self):
        logger.info("Received heartbeat")
        return call_result.Heartbeat(
            current_time="2025-01-01T12:00:00Z"
        )