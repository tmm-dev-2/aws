class DrawingSettings:
	def __init__(self):
		self._line_thickness = 1
		self._color = "#000000"
		self._background_color = "#ffffff"
		self._transparency = 1.0

	@property
	def line_thickness(self):
		return self._line_thickness

	@line_thickness.setter
	def line_thickness(self, value):
		self._line_thickness = max(1, int(value))

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, value):
		self._color = value

	@property
	def background_color(self):
		return self._background_color

	@background_color.setter
	def background_color(self, value):
		self._background_color = value

	@property
	def transparency(self):
		return self._transparency

	@transparency.setter
	def transparency(self, value):
		self._transparency = max(0.0, min(1.0, float(value)))

	def to_dict(self):
		return {
			"line_thickness": self._line_thickness,
			"color": self._color,
			"background_color": self._background_color,
			"transparency": self._transparency
		}

	def update_from_dict(self, settings_dict):
		if "line_thickness" in settings_dict:
			self.line_thickness = settings_dict["line_thickness"]
		if "color" in settings_dict:
			self.color = settings_dict["color"]
		if "background_color" in settings_dict:
			self.background_color = settings_dict["background_color"]
		if "transparency" in settings_dict:
			self.transparency = settings_dict["transparency"]

# Global instance for shared settings
drawing_settings = DrawingSettings()