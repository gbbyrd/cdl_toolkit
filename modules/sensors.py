class SensorType:
    def __init__(self):
        self.camera = 'sensor.camera.rgb'

class Camera_RGB:
    
    def __init__(self, blueprint_library, sensor_name, **kwargs):
        # identifiers
        self.name = sensor_name
        self.type = 'sensor.camera.rgb'
        
        self.bp = blueprint_library.find(self.type)
        self.bp.set_attribute("image_size_x", f"{kwargs.get('IM_HEIGHT', 480)}")
        self.bp.set_attribute("image_size_y", f"{kwargs.get('IM_WIDTH', 640)}")
        self.bp.set_attribute("fov", f"{kwargs.get('fov', 110)}")
        
class Lidar:
    
    def __init__(self, blueprint_library, sensor_name, **kwargs):
        # identifiers
        self.name = sensor_name
        self.type = ''