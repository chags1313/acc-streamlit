import streamlit as st
from streamlit import components
import asyncio
import websockets
import json

# Create a list to store accelerometer data
accelerometer_data_list = []

# WebSocket server handler
async def handle_client(websocket, path):
    while True:
        try:
            # Receive accelerometer data from the client
            data = await websocket.recv()
            accelerometer_data = json.loads(data)
            
            # Append accelerometer data to the list
            accelerometer_data_list.append(accelerometer_data)
            
        except websockets.exceptions.ConnectionClosed:
            break

# Start the WebSocket server
start_server = websockets.serve(handle_client, "localhost", 8000)

# Embed the HTML file with the JavaScript code into Streamlit
components.html(
    """
    <html>
        <body>
            <script>
                // Establish WebSocket connection
                var socket = new WebSocket("ws://localhost:8000");

                // Listen for accelerometer data
                window.addEventListener('devicemotion', function(event) {
                  var accelerometerData = event.accelerationIncludingGravity;

                  // Send accelerometer data to the server
                  socket.send(JSON.stringify(accelerometerData));
                });
            </script>
        </body>
    </html>
    """,
    height=0  # Adjust the height as needed
)

# Start the Streamlit app
def main():
    # Start the WebSocket server in the background
    asyncio.ensure_future(start_server)

    # Set Streamlit app title
    st.title('Accelerometer Data')

    # Continuously display the latest accelerometer data
    while True:
        if accelerometer_data_list:
            latest_data = accelerometer_data_list[-1]
            st.write('X:', latest_data['x'])
            st.write('Y:', latest_data['y'])
            st.write('Z:', latest_data['z'])
        else:
            st.write('No accelerometer data yet.')

        # Add a button to clear the accelerometer data
        if st.button('Clear Data'):
            accelerometer_data_list.clear()

        # Sleep for a short interval
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    asyncio.run(main())


# Run the Streamlit app
if __name__ == '__main__':
    main()

