# Python code for Streamlit app with accelerometer data and WebSocket server

import streamlit as st
import asyncio
import websockets
import json

# Function to handle incoming accelerometer data
async def handle_accelerometer_data(websocket, path):
    while True:
        # Receive accelerometer values from the WebSocket server
        data = await websocket.recv()
        accelerometer_data = json.loads(data)
        x = accelerometer_data['x']
        y = accelerometer_data['y']
        z = accelerometer_data['z']

        # Process the accelerometer values as desired
        # ...

        # Display the accelerometer values using Streamlit
        st.write(f'x: {x}, y: {y}, z: {z}')

# Start the Streamlit app
def main():
    st.title('Accelerometer Data')

    # Display the accelerometer values in Streamlit
    st.write('Listening to accelerometer data...')

    # JavaScript code to read accelerometer values and send them to WebSocket
    js_code = """
    <script>
    const socket = new WebSocket('ws://localhost:8000');

    socket.onopen = function () {
      console.log('WebSocket connection established');
    };

    socket.onerror = function (error) {
      console.error('WebSocket error:', error);
    };

    function handleAccelerometerData(event) {
      const acceleration = event.accelerationIncludingGravity;
      const x = acceleration.x;
      const y = acceleration.y;
      const z = acceleration.z;

      socket.send(JSON.stringify({ x, y, z }));
    }

    function startAccelerometer() {
      window.addEventListener('devicemotion', handleAccelerometerData);
    }

    function stopAccelerometer() {
      window.removeEventListener('devicemotion', handleAccelerometerData);
    }

    startAccelerometer();
    </script>
    """

    # Display the JavaScript code
    st.markdown(js_code, unsafe_allow_html=True)

    # Start the WebSocket server
    start_server = websockets.serve(handle_accelerometer_data, 'localhost', 8000)

    # Run the WebSocket server in the background
    asyncio.ensure_future(start_server)

# Run the Streamlit app
if __name__ == '__main__':
    main()
