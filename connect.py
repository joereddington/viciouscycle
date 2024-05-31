from bleak import BleakClient
import asyncio
import struct



def handle_measurement(sender, data):
    global prev_cumulative_crank_revolutions, prev_last_crank_event_time

    # Read the flags field
    flags = data[0]

    # Initialize variables
    cumulative_wheel_revolutions = None
    last_wheel_event_time = None
    cumulative_crank_revolutions = None
    last_crank_event_time = None

    index = 1  # Start after the flags field

    # Check if Wheel Revolution Data is present
    if flags & 0x01:
        cumulative_wheel_revolutions = struct.unpack_from("<I", data, index)[0]
        index += 4
        last_wheel_event_time = struct.unpack_from("<H", data, index)[0]
        index += 2

    # Check if Crank Revolution Data is present
    if flags & 0x02:
        cumulative_crank_revolutions = struct.unpack_from("<H", data, index)[0]
        index += 2
        last_crank_event_time = struct.unpack_from("<H", data, index)[0]

    # Print the parsed values
    if cumulative_wheel_revolutions is not None:
        print("Cumulative wheel revolutions:", cumulative_wheel_revolutions)
    if last_wheel_event_time is not None:
        print("Last wheel event time:", last_wheel_event_time)
    if cumulative_crank_revolutions is not None:
        print("Cumulative crank revolutions:", cumulative_crank_revolutions)
    if last_crank_event_time is not None:
        print("Last crank event time:", last_crank_event_time)

    # Calculate cadence if crank revolution data is present
    if cumulative_crank_revolutions is not None and last_crank_event_time is not None:
        if prev_cumulative_crank_revolutions is not None and prev_last_crank_event_time is not None:
            # Calculate the differences
            revolutions_diff = cumulative_crank_revolutions - prev_cumulative_crank_revolutions
            time_diff = last_crank_event_time - prev_last_crank_event_time

            # Handle the case where the event time wraps around (CSC specification uses a 1/1024 second resolution)
            if time_diff < 0:
                time_diff += 65536  # 2^16 to handle the 16-bit wrap around

            # Calculate cadence (RPM)
            # The time difference is in 1/1024 seconds, so convert it to minutes
            cadence = (revolutions_diff * 1024 * 60) / time_diff
            print("Cadence (RPM):", cadence)

        # Update previous values
        prev_cumulative_crank_revolutions = cumulative_crank_revolutions
        prev_last_crank_event_time = last_crank_event_time
 
async def run():
    async with BleakClient(sensor_address) as client:
        await client.start_notify(CSC_MEASUREMENT_UUID, handle_measurement)
        print("Connected to the sensor and started notifications")
        
        await asyncio.sleep(60)

        await client.stop_notify(CSC_MEASUREMENT_UUID)
        print("Stopped notifications")


# TODO add main method 
# Really I want to have a customisable system were I can pass in functions for 'cadence less and x' and 'candence more than Y'
# Now, how can I do this? 
# a structure that has a 'minimum', 'maxmimum' 'name of state' 'entry function' and 'exit function' 
# For road rash that's: 
# a) Over a certain cadence the button should be held properly 
# b) at the lower end of that there should be a warning. 
# c) below that, there should be a lesser rate at which the button is held. 
# The entry and exit functions must accept the cadence 
# For a spin class that's 
# Different targets with different timings.  

# Replace this with your sensor's address
sensor_address = "768C9858-CC88-537E-C0B6-BA4963D060A6"

# CSC Measurement characteristic UUID
CSC_MEASUREMENT_UUID = "00002a5b-0000-1000-8000-00805f9b34fb"

# Initialize previous values for cadence calculation
prev_cumulative_crank_revolutions = None
prev_last_crank_event_time = None
asyncio.run(run())

