from bleak import BleakClient
from viciouscycle import Zone
import asyncio
import viciouscycle
import bleak

def zone1(sender, data): 
    print("Here")
    cadence=viciouscycle.decode_and_handle_measurement(sender,data) 
    if cadence is None:
        print("None") 
        return
    if cadence > 60: 
        if cadence <150: 
            print("Doing great!")         
    else:
        print("No, do better") 

def zone2(sender, data): 
    print("Here")
    cadence=viciouscycle.decode_and_handle_measurement(sender,data) 
    if cadence is None:
        print("None") 
        return
    if cadence > 120: 
        if cadence <150: 
            print("Doing great!")         
    else:
        print("No, do better") 
    


async def warmup():
    async with BleakClient(viciouscycle.sensor_address) as client:
        print("Start a warmup!") 
        print("60 Seconds at 60 rmp") 
        await client.start_notify(viciouscycle.CSC_MEASUREMENT_UUID, zone1)
        await asyncio.sleep(60)
        await client.stop_notify(viciouscycle.CSC_MEASUREMENT_UUID)
        print("Now two minutes Seconds at 120 rmp") 
        await client.start_notify(viciouscycle.CSC_MEASUREMENT_UUID, zone2)
        await asyncio.sleep(120)
        await client.stop_notify(viciouscycle.CSC_MEASUREMENT_UUID)
        # now do the next section 
        print("Stopped notifications")


if __name__ == "__main__":
# TODO - make this into a proper gygame interface 
    print("Entering Warm up") 
    print("Seeking Sensor")  
    try: 
        asyncio.run(warmup())
    except bleak.exc.BleakDeviceNotFoundError: 
        print("Device was NOT found")  
