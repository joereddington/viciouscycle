from bleak import BleakClient
from collections import deque
import asyncio
import time
import struct

def debug_flags(flags):
    """
    Debugging function to interpret and display the value of each bit in the flags field.
    
    The flags field is 1 byte (8 bits) long, and each bit represents a different piece of data.
    
    | Flag Bit | Value | Description                                  |
    |----------|-------|----------------------------------------------|
    | 0        | 0x01  | Cumulative Wheel Revolutions Present         |
    | 1        | 0x02  | Cumulative Crank Revolutions Present         |
    | 2        | 0x04  | Sensor Contact Status Supported              |
    | 3        | 0x08  | Multiple Sensor Locations Supported          |
    | 4        | 0x10  | Crank Length Supported                       |
    | 5        | 0x20  | Bike Weight Supported                        |
    | 6        | 0x40  | Power Measurement Supported                  |
    | 7        | 0x80  | Energy Expenditure Supported                 |
    
    Args:
    - flags (int): The flags byte value to be interpreted.

    Returns:
    - None
    """
    for bit in range(8):
        bit_mask = 1 << bit
        bit_value = (flags & bit_mask) >> bit
        description = ""
        
        if bit == 0:
            description = "Cumulative Wheel Revolutions Present"
        elif bit == 1:
            description = "Cumulative Crank Revolutions Present"
        elif bit == 2:
            description = "Sensor Contact Status Supported"
        elif bit == 3:
            description = "Multiple Sensor Locations Supported"
        elif bit == 4:
            description = "Crank Length Supported"
        elif bit == 5:
            description = "Bike Weight Supported"
        elif bit == 6:
            description = "Power Measurement Supported"
        elif bit == 7:
            description = "Energy Expenditure Supported"

        status = "Present" if bit_value else "Not Present"
        print(f"Bit {bit}: {status} - {description}")

# Example usage
#flags = 0b00101101  # Example flags value
#debug_flags(flags)

def print_raw_values(data):
    """
    Prints the raw values of the data bytes, including the flags field and the data fields.

    Args:
    - data (bytes): The raw measurement data as a byte array.
    
    Returns:
    - None
    """
    if not data:
        print("No data provided.")
        return

    # Print the entire data byte array in hex format
    print("Raw data (hex):", data.hex())

    # Print the flags field
    flags = data[0]
    print(f"Flags (hex): {flags:02X}")

    index = 1  # Start after the flags field

    # Determine the length of the data based on flags (for demo purposes, we print raw values)
    print("Data fields:")
    
    # Print the cumulative wheel revolutions if present
    if flags & 0x01:
        wheel_revolutions = struct.unpack_from("<I", data, index)[0]
        print(f"Cumulative Wheel Revolutions: {wheel_revolutions}")
        index += 4  # Move past this field
        last_wheel_event_time = struct.unpack_from("<H", data, index)[0]
        print(f"Last Wheel Event Time: {last_wheel_event_time}")
        index += 2  # Move past this field

    # Print the cumulative crank revolutions if present
    if flags & 0x02:
        crank_revolutions = struct.unpack_from("<H", data, index)[0]
        print(f"Cumulative Crank Revolutions: {crank_revolutions}")
        index += 2  # Move past this field
        last_crank_event_time = struct.unpack_from("<H", data, index)[0]
        print(f"Last Crank Event Time: {last_crank_event_time}")
        index += 2  # Move past this field

    # Print the sensor contact status if present
    if flags & 0x04:
        sensor_contact_status = data[index]
        print(f"Sensor Contact Status: {sensor_contact_status}")
        index += 1  # Move past this field

    # Print the crank length if present
    if flags & 0x08:
        crank_length = struct.unpack_from("<H", data, index)[0]
        print(f"Crank Length: {crank_length}")
        index += 2  # Move past this field

    # Print the bike weight if present
    if flags & 0x10:
        bike_weight = struct.unpack_from("<H", data, index)[0]
        print(f"Bike Weight: {bike_weight}")
        index += 2  # Move past this field

    # Print the power measurement if present
    if flags & 0x20:
        power_measurement = struct.unpack_from("<H", data, index)[0]
        print(f"Power Measurement: {power_measurement}")
        index += 2  # Move past this field

    # Print the energy expenditure if present
    if flags & 0x40:
        energy_expenditure = struct.unpack_from("<H", data, index)[0]
        print(f"Energy Expenditure: {energy_expenditure}")



def decode_and_handle_measurement(sender, data):
#Takes data in this format:  "022d00c1b7" and splits it into the flags and the data.  

    # Read the flags field
    flags = data[0]
    #    debug_flags(flags)
    #    print_raw_values(data)

    # Initialize variables
    cumulative_crank_revolutions = None
    last_crank_event_time = None

    index = 1  # Start after the flags field
    # Check if Crank Revolution Data is present
    if flags & 0x02:
        cumulative_crank_revolutions = struct.unpack_from("<H", data, index)[0]
        index += 2
        last_crank_event_time = struct.unpack_from("<H", data, index)[0]
        print("Cumulative crank revolutions:", cumulative_crank_revolutions)
        print("Last crank event time:", last_crank_event_time)
    else: 
        print("ERROR: probably shouldn't reach this") 
    #Then palm it off to the next place 
    return handle_measurement(cumulative_crank_revolutions,last_crank_event_time)

import time

def handle_measurement(cumulative_crank_revolutions, last_crank_event_time, n=10):
    global buffer, cadence

    # Check if valid data is provided
    if cumulative_crank_revolutions is not None and last_crank_event_time is not None:
        current_time = int(time.time())  # Get current time in seconds since epoch

        # Add the new data and current time to the buffer
        buffer.append((cumulative_crank_revolutions, last_crank_event_time, current_time))
        print("Current Buffer Values:")
        for idx, (revolutions, event_time, timestamp) in enumerate(buffer):
            print(f"Entry {idx + 1}: Crank Revolutions = {revolutions}, Event Time = {event_time}, Timestamp = {timestamp}")

        # Determine if we have enough entries for comparison
        if len(buffer) >= n:
            # Retrieve the data from n entries ago
            prev_cumulative_crank_revolutions, prev_last_crank_event_time, _ = buffer[-n]
        else:
            # Not enough data; use the oldest available data
            print("Using oldest available data")
            if len(buffer) > 1:
                prev_cumulative_crank_revolutions, prev_last_crank_event_time, _ = buffer[0]
            else:
                print("Not enough data to calculate cadence.")
                return None

        # Calculate the differences
        revolutions_diff = cumulative_crank_revolutions - prev_cumulative_crank_revolutions
        time_diff = last_crank_event_time - prev_last_crank_event_time
        print(f"Revolutions Difference: {revolutions_diff}")
        print(f"Time Difference (in 1/1024 seconds): {time_diff}")

        # Handle the case where the event time wraps around (16-bit wrap around)
        if time_diff < 0:
            time_diff += 65536  # 2^16 to handle the 16-bit wrap around
        if time_diff == 0:  # Check if time difference is zero
            print("Time difference is zero, cannot calculate cadence.")
            return None

        # Calculate cadence (RPM)
        cadence = (revolutions_diff * 1024 * 60) / time_diff
        print("Cadence (RPM):", cadence)

        # Calculate and print the separate cadence based on time
        if len(buffer) >= 2:
            prev_revolutions, prev_event_time, prev_timestamp = buffer[-2]
            time_diff_seconds = current_time - prev_timestamp
            if time_diff_seconds > 0:  # Ensure time difference is not zero
                separate_cadence = (revolutions_diff * 60) / (time_diff_seconds)
                print(f"Separate Cadence based on clock time (RPM): {separate_cadence}")

        return cadence
    else:
        print("handle_measurement was passed None values")
    return None


 
async def run(): #Only when run as main obviously
    async with BleakClient(sensor_address) as client:
        await client.start_notify(CSC_MEASUREMENT_UUID, decode_and_handle_measurement)
        print("Connected to the sensor and started notifications")
        await asyncio.sleep(60)
        await client.stop_notify(CSC_MEASUREMENT_UUID)
        print("Stopped notifications")



# Global buffer to store recent entries
buffer = deque(maxlen=10)  # Adjust maxlen as needed; here it's 10 for example
cadence=0
sensor_address = "768C9858-CC88-537E-C0B6-BA4963D060A6" #TODO read this from a file. 
CSC_MEASUREMENT_UUID = "00002a5b-0000-1000-8000-00805f9b34fb" # This says to return data in the CSC format

if __name__ == "__main__":
    asyncio.run(run())
