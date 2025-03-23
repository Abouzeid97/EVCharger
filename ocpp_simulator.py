import asyncio
import logging
import websockets
from ocpp.v16 import call
from ocpp.v16.enums import Reason
from ocpp.v16 import ChargePoint as cp

logging.basicConfig(level=logging.INFO)

class ChargePointClient(cp):
    async def send_boot_notification(self):
        """ Send a BootNotification message to the CSMS """
        logging.info("DEBUG: Sending BootNotification...")
        request = call.BootNotification(
            charge_point_model="TestModel",
            charge_point_vendor="TestVendor",
        )
        response = await self.call(request)
        logging.info(f"BootNotification response: {response}")

    async def send_heartbeat(self):
        """ Send a Heartbeat message """
        logging.info("DEBUG: Sending Heartbeat...")
        request = call.Heartbeat()
        response = await self.call(request)
        logging.info(f"Heartbeat response: {response}")
    
    async def send_authorize(self, id_tag):
        """ Send an Authorize request to CSMS """
        logging.info(f"DEBUG: Sending Authorize request for idTag {id_tag}")
        request = call.Authorize(id_tag=id_tag)
        response = await self.call(request)
        logging.info(f"Authorize response: {response}")

    async def send_start_transaction(self, id_tag, connector_id=1, meter_start=0, reservation_id=None):
        """ Start a charging session """
        logging.info("DEBUG: Sending StartTransaction...")
        request = call.StartTransaction(
            connector_id=connector_id,
            id_tag=id_tag,
            meter_start=meter_start,
            timestamp="2025-01-01T12:00:00Z",
            reservation_id=reservation_id,
        )
        response = await self.call(request)
        logging.info(f"StartTransaction response: {response}")
        return response.transaction_id
    
    async def send_stop_transaction(self, transaction_id, meter_stop=100):
        """ Stop a charging session """
        logging.info("DEBUG: Sending StopTransaction...")
        request = call.StopTransaction(
            transaction_id=transaction_id,
            meter_stop=meter_stop,
            timestamp="2025-01-01T12:00:00Z",
            reason=Reason.local,
        )
        response = await self.call(request)
        logging.info(f"StopTransaction response: {response}")

    

async def main():
    uri = "ws://localhost:8000/ws/ocpp/charger123/"
    
    async with websockets.connect(uri) as ws:
        charge_point = ChargePointClient("test_charger_01", ws)

        # Start listening in the background
        asyncio.create_task(charge_point.start())  

        await asyncio.sleep(2)

        try:
            
            await charge_point.send_boot_notification()

            await charge_point.send_authorize("12345")
            
            transaction_id = await charge_point.send_start_transaction("12345")
            
            await asyncio.sleep(5)
            
            await charge_point.send_stop_transaction(transaction_id)

        except Exception as e:
            logging.error(f"Error during BootNotification, Authorization, or Transactions: {e}")
            return  

        # Step 6: Keep sending heartbeat every 10 seconds
        while True:
            try:
                await charge_point.send_heartbeat()
            except Exception as e:
                logging.error(f"Heartbeat failed: {e}")

            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
