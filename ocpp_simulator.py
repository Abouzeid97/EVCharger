import asyncio
import logging
import websockets
from ocpp.v16 import call
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

    

async def main():
    uri = "ws://localhost:8000/ws/ocpp/charger123/"
    
    async with websockets.connect(uri) as ws:
        charge_point = ChargePointClient("test_charger_01", ws)

        # Start listening in the background
        asyncio.create_task(charge_point.start()) 

        await asyncio.sleep(2)  

        # Register charger with CSMS
        await charge_point.send_boot_notification()
        
        # Send periodic messages
        while True:
            await charge_point.send_heartbeat()
            await asyncio.sleep(10) 

if __name__ == "__main__":
    asyncio.run(main())
