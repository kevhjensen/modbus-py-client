import ctypes
import os

class pyZerovaChgrModbus:
    def __init__(self) -> None:
        self.modbus_dll = None
        self.load_modbus_dll()

    def load_modbus_dll(self):
        try:
            # Load the DLL (you might need to adjust the path if necessary)
            dll_path = os.path.join(os.getcwd(), 'modbus.dll')

            # Check if DLL exists
            if not os.path.exists(dll_path):
                raise FileNotFoundError(f"modbus.dll not found at {dll_path}")

            # Load the DLL using ctypes.CDLL with Cdecl calling convention
            self.modbus_dll = ctypes.CDLL(dll_path, ctypes.CDLL)

            print("modbus.dll loaded successfully.")
        except Exception as e:
            print(f"Failed to load modbus.dll: {e}")

    def modbus_set_slave(self, ctx, slave):
        try:
            # Define the function signature for modbus_set_slave
            modbus_set_slave = self.modbus_dll.modbus_set_slave
            modbus_set_slave.argtypes = [ctypes.c_void_p, ctypes.c_int]
            modbus_set_slave.restype = ctypes.c_int

            # Call the function
            result = modbus_set_slave(ctx, slave)
            return result
        except Exception as e:
            print(f"Error calling modbus_set_slave: {e}")
            return None

    def modbus_connect(self, ctx):
        try:
            # Define the function signature for modbus_connect
            modbus_connect = self.modbus_dll.modbus_connect
            modbus_connect.argtypes = [ctypes.c_void_p]
            modbus_connect.restype = ctypes.c_int

            # Call the function
            result = modbus_connect(ctx)
            return result
        except Exception as e:
            print(f"Error calling modbus_connect: {e}")
            return None

    def modbus_new_tcp(self, ip_address, port):
        try:
            # Define the function signature for modbus_new_tcp
            modbus_new_tcp = self.modbus_dll.modbus_new_tcp
            modbus_new_tcp.argtypes = [ctypes.c_char_p, ctypes.c_int]
            modbus_new_tcp.restype = ctypes.c_void_p

            # Call the function
            ctx = modbus_new_tcp(ip_address.encode('utf-8'), port)
            return ctx
        except Exception as e:
            print(f"Error calling modbus_new_tcp: {e}")
            return None

    # Add more functions as needed, based on the C# signatures.

# Example usage
if __name__ == "__main__":
    modbus_client = pyZerovaChgrModbus()
    
    # Create a new Modbus TCP context
    ctx = modbus_client.modbus_new_tcp("192.168.10.155", 502)
    if ctx:
        print("TCP context created.")
        
        # Set the slave ID
        result = modbus_client.modbus_set_slave(ctx, 1)
        print(f"Set slave result: {result}")

        # Connect to the Modbus server
        result = modbus_client.modbus_connect(ctx)
        print(f"Connect result: {result}")
