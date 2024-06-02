from bleak import BleakClient
import asyncio
import viciouscycle
import bleak
import keyboard

def go_forward(sender, data): 
    print("Here")
    cadence=viciouscycle.decode_and_handle_measurement(sender,data) 
    if cadence is None:
        print("None") 
        return
    if cadence > 60: 
        if cadence <150: 
            print("Doing great!")         
            keyboard.hold_key('up',2) 

    else:
        print("No, do better") 



async def play():
    async with BleakClient(viciouscycle.sensor_address) as client:
        print("Start to play") 
        await client.start_notify(viciouscycle.CSC_MEASUREMENT_UUID, go_forward)
        await asyncio.sleep(60)
        await client.stop_notify(viciouscycle.CSC_MEASUREMENT_UUID)
        print("Stopped notifications")

if __name__ == "__main__":
    print("Entering Warm up") 
    print("Seeking Sensor")  
    try: 
        asyncio.run(play())
    except bleak.exc.BleakDeviceNotFoundError: 
        print("Device was NOT found")  
