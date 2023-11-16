import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class LEDDrawingArea(Gtk.DrawingArea):
	def __init__(self):
		super().__init__()
		self.set_size_request(50, 50)
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
