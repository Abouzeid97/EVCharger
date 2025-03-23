import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from ocpp.routing import on
from ocpp.v16 import call_result, call
from ocpp.v16 import ChargePoint as OcppChargePoint
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus, Reason
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class CustomChargePoint(OcppChargePoint):
    """ Custom ChargePoint class to handle OCPP messages """

    @on(Action.boot_notification)
    async def on_boot_notification(self, charge_point_model, **kwargs):
        """ Handle BootNotification message """
        logger.info(f"Boot notification received from: {charge_point_model}")
        return call_result.BootNotification(
            status=RegistrationStatus.accepted,
            current_time= datetime.now(timezone.utc).isoformat(),
            interval=300,
        )

    @on(Action.heartbeat)
    async def on_heartbeat(self):
        """ Handle Heartbeat message """
        logger.info("Received heartbeat")
        return call_result.Heartbeat(
            current_time="2025-01-01T12:00:00Z"
        )
    @on(Action.authorize)
    async def on_authorize(self, id_tag, **kwargs):
        """ Handle Authorize request from charge point """
        logger.info(f"Authorize request received for idTag: {id_tag}")

        # Simulating authorization (you can add real logic here)
        authorized_tags = {"12345", "67890"}  # Example valid RFID tags
        status = AuthorizationStatus.accepted if id_tag in authorized_tags else AuthorizationStatus.invalid

        logger.info(f"Authorization result for {id_tag}: {status}")

        return call_result.Authorize(id_tag_info={"status": status})
    
    @on(Action.start_transaction)
    async def on_start_transaction(self, connector_id, id_tag, meter_start, timestamp, reservation_id=None, **kwargs):
        """ Handle StartTransaction request from charge point """
        logger.info(f"StartTransaction received for idTag {id_tag} on connector {connector_id}")

        # Simulating a successful transaction start
        transaction_id = 1234  # In a real scenario, this should be generated dynamically

        logger.info(f"Transaction started: {transaction_id}")

        return call_result.StartTransaction(
            transaction_id=transaction_id,
            id_tag_info={"status": AuthorizationStatus.accepted},
        )

    @on(Action.stop_transaction)
    async def on_stop_transaction(self, transaction_id, meter_stop, timestamp, reason, **kwargs):
        """ Handle StopTransaction request from charge point """
        logger.info(f"StopTransaction received for transaction {transaction_id}")
    
        return call_result.StopTransaction(
            id_tag_info={"status": AuthorizationStatus.accepted},
        )
class OCPPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ WebSocket connection handler """
        self.charger_id = self.scope["url_route"]["kwargs"]["charger_id"]
        self.charge_point = CustomChargePoint(self.charger_id, self) 

        await self.accept()
        logger.info(f"Charger {self.charger_id} connected via WebSocket")

    async def disconnect(self, close_code):
        """ WebSocket disconnection handler """
        logger.info(f"Charger {self.charger_id} disconnected")

    async def receive(self, text_data):
        """ Route incoming OCPP messages to appropriate handlers """
        logger.info(f"DEBUG: Received message: {text_data}")
        await self.charge_point.route_message(text_data) 
