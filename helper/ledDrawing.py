import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class LEDDrawing(Gtk.DrawingArea):
	def __init__(self, size):
		super().__init__()
		self.set_size_request(size, size)
		self.rgb_color = (128, 128, 128)  # Initial color is red (RGB)

		self.connect("draw", self.on_draw)

	def set_color(self, red, green, blue):
		self.rgb_color = (red, green, blue)
		self.queue_draw()

	def on_draw(self, widget, cr):
		allocation = self.get_allocation()
		width, height = allocation.width, allocation.height

		# Create a GdkRGBA color from the RGB values
		rgba_color = Gdk.RGBA()
		rgba_color.red = self.rgb_color[0] / 255
		rgba_color.green = self.rgb_color[1] / 255
		rgba_color.blue = self.rgb_color[2] / 255
		rgba_color.alpha = 1.0

		cr.set_source_rgba(rgba_color.red, rgba_color.green, rgba_color.blue, rgba_color.alpha)
		cr.arc(width / 2, height / 2, min(width, height) / 2 - 5, 0, 2 * 3.141592)
		cr.fill()
		
	def dimm_led(self, color="r"): 
		pointer = 0
		if color == "g":
			pointer = 1
		elif color == "b":
			pointer = 2

		colorbrightness = self.rgb_color[pointer]
		if(self.rgb_color != (128,128,128)):
			match color:
				case "r":
					self.set_color((colorbrightness-10), 0, 0)
				case "g":
					self.set_color(0, (colorbrightness-10), 0)
				case "b":
					self.set_color(0, 0, (colorbrightness-10))
		if(self.rgb_color[pointer] <= 120):
			self.set_color(128,128,128)

		return True
