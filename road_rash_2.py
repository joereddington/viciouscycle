from bleak import BleakClient
import asyncio
import viciouscycle
import keyboard
import bleak

def go_forward(sender, data): 
    cadence = viciouscycle.decode_and_handle_measurement(sender, data)
    if cadence is None:
        print("Cadence data is None")
        return
    
    print(f"Cadence: {cadence}")
    if 80 < cadence < 150: 
        print("Doing great!")
        keyboard.hold_key('z',1.5)
    else:
        print(f"Cadence is only {cadence}")

async def play():
    try:
        async with BleakClient(viciouscycle.sensor_address) as client:
            print("Connected to device")
            await client.start_notify(viciouscycle.CSC_MEASUREMENT_UUID, go_forward)
            print("We have reached the sleep point")
            await asyncio.sleep(3600)  # Adjust this duration as needed
            print("Okay, stopping") 
            await client.stop_notify(viciouscycle.CSC_MEASUREMENT_UUID)
            print("We have stopped")
    except bleak.exc.BleakDeviceNotFoundError:
        print("Device NOT found")
    except Exception as e:
        print(f"An error occurred: {e}")

def hello(): 
    import pyfiglet
    figlet = pyfiglet.Figlet(font='slant')
    # Generate the ASCII art for "Vicious Cycle"
    ascii_art = figlet.renderText('Vicious Cycle')

    # Print the ASCII art
    print(ascii_art)


if __name__ == "__main__":
    hello()
    print("Searching for sensor...")
    print("Stay on this window until the first keyDown event") 
    try:
        asyncio.run(play())
    except KeyboardInterrupt:
        print("Program interrupted by user")

