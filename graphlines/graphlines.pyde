"""Processing.py sketch to graph multiple lines.

This sketch reads multiple numbers from a serial port and draws line
graphs from that data. The format of a line should correspond to the
regex '^(\d+ )*\d+$' ended by a linefeed (ASCII 10).
"""

add_library('serial')

# SKETCH CONFIGURATION ---
DISPLAY_SIZE = (1280, 720)  # display size (in pixels)
SCALING_ENABLED = False  # whether to scale values to fit the display
LINES_ALLOWED = 6  # number of lines to draw (must be <= len(COLORS))
BG_COLOR = 255  # background color (in grayscale)
# ---

# GRAPH CONFIGURATION ---
X_START = 0  # begin graph at this distance from the y-axis
Y_START = 10  # begin graph at this distance from the x-axis
X_SPACING = 50  # length of 1 unit (in pixels) on the x-axis
MIN_Y = 0  # minimum possible value of y
MAX_Y = 10000  # maximum possible value of y
# ---

# CONSTANTS ---
RED = '#FF0000'
GREEN = '#00FF00'
BLUE = '#0000FF'
CYAN = '#00FFFF'
MAGENTA = '#FF00FF'
YELLOW = '#FFFF00'
COLORS = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW]
LF = 10  # ASCII code for linefeed
# ---

# GLOBAL VARIABLES
xpos = [X_START] * LINES_ALLOWED
ypos = [Y_START] * LINES_ALLOWED
data = [Y_START] * LINES_ALLOWED
# ---


def setup():
    size(*DISPLAY_SIZE)
    reset_background()
    configure_serial_port()
    noLoop()  # disable continuous drawing


def draw():
    strokeWeight(2)  # set the line thickness to double
    stroke(0)  # set default line color to black

    global xpos, ypos

    # Graph the lines
    for i in range(LINES_ALLOWED):
        draw_line(
            xpos[i], ypos[i],
            xpos[i] + X_SPACING, data[i],
            COLORS[i]
        )

    off_display = False  # flag to set if graph goes off-display

    # Update the coordinates
    for i in range(LINES_ALLOWED):
        xpos[i] += X_SPACING
        ypos[i] = data[i]

        # Flag and make adjustments if off-display
        if xpos[i] >= width - X_START:
            off_display = True
            xpos[i] = X_START

    if off_display:
        reset_background()


def configure_serial_port():
    """Set up the serial port connection."""
    port_name = Serial.list()[0]  # get the port's name
    port = Serial(this, port_name)  # open a connection at 9600 bps (default)
    port.bufferUntil(LF)  # set serialEvent() to be called when '\n' is read
    port.clear()  # clear any data from the serial port


def draw_line(x1, y1, x2, y2, color):
    """Draw a colored line on the Cartesian plane."""
    stroke(color)  # set the line's color
    y1 = height - Y_START - y1
    y2 = height - Y_START - y2
    line(x1, y2, x2, y2)


def reset_background():
    """Clear the display."""
    background(BG_COLOR)


def serialEvent(port):
    """Process new data and update the graph.

    This is a Processing function called automatically whenever data is
    available to be read from the serial port (which is specified in the
    parameter).
    """
    # Read a string from the serial port
    input = port.readStringUntil(LF)

    if input and len(input) > 0:
        # Convert data into numbers
        values = input.strip().split()
        values = [float(x) for x in values]

        # Scale and update the graph data
        update_data(values)

        # Update the graph
        redraw()


def update_data(values):
    """Update the graph data with scaled values."""
    global data
    # Note: 'map' here is a Processing function that scales data
    data = [
        map(v, MIN_Y, MAX_Y, Y_START, height - Y_START)
        if SCALING_ENABLED else v
        for v in values
    ]
    data = [int(v) for v in data]
    print_data()


def print_data():
    """Print graph data for debugging purposes."""
    println(data)
