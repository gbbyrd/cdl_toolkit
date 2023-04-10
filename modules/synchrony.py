import queue
import carla

class CarlaSyncMode(object):
    """Class that handles Carla Synchrony

    Args:
        world (carla world object): --
        sensors (dict): {'event_name': carla event object}
    """
    def __init__(self, world, sensors, **kwargs):
        self.world = world
        self.sensors = sensors
        self.frame = None
        self.delta_seconds = 1.0 / kwargs.get('fps', 20)
        self.max_episode_steps = kwargs.get('max_steps', 3000)
        self._queues = {}
        self._settings = None
        self.episode_steps = 0
    
    # allows the class to be used with: with ____ as ____:    
    def __enter__(self):
        self._settings = self.world.get_settings()
        self.frame = self.world.apply_settings(carla.WorldSettings(
            no_rendering_mode = False,
            synchronous_mode = True, 
            fixed_delta_seconds = self.delta_seconds
        ))
        
        # this makes queue for all events including sensors collecting data
        def make_queue(register_event, name):
            # create a q for the event to register data to
            q = queue.Queue()
            # define q.put as the function that is called when the event recieves data
            register_event(q.put)
            # add q to the list of _queues
            self._queues[name] = q
        
        # create queues for each sensor that store the data as the sensor reads it
        make_queue(self.world.on_tick, 'WORLD')
        for name, sensor in self.sensors.items():
            make_queue(sensor.listen, name)
            
        return self
    
    # call this function to step once through the simulation
    def tick(self, timeout):
        # get the next frame from the world.. this should automatically update the 
        # sensor queues as well
        self.frame = self.world.tick()
        data = {name: self._retrieve_data(name, q, timeout) for name, q in self._queues.items()}
        # ensure the data is synced
        for x in data.values():
            if x is None:
                continue
            assert x.frame == self.frame
        if self.episode_steps < self.max_episode_steps:
            data['episode_complete'] = False
        else:
            data['episode_complete'] = True
            self.episode_steps += 1
        return data
    
    def reset(self):
        pass
    
    # allows the class to be used with: with ____ as ____: 
    def __exit__(self, *args, **kwargs):
        self.world.apply_settings(self._settings)
        
    def _retrieve_data(self, sensor_name, sensor_queue, timeout):
        if sensor_queue.empty() and 'collision' in sensor_name:
            return None
        while True:
            data = sensor_queue.get(timeout=timeout)
            if data.frame == self.frame:
                return data