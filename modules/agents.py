class _Agent:
    def __init__(self, world):
        self.world = world
        print(self.world)
    
    def add_camera_rgb(self, sensor_name, location):
        pass
    
    def add_lidar(self, sensor_name, location):
        pass
    
class DQN_Agent(_Agent):
    def __init__(self, agent_name, **kwargs):
        self.name = agent_name
        print(self.world)