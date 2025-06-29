import os
import json
import gpiozero 
class NX:
    def __init__(self):
        
        self.armed = False
        self.config = json.load(open('config.json', 'r'))
    def get_zone(self, zone: int):
        if zone <= 0: 
            return {'status': 400, 'body': 'The zone is invalid'}
        for item in self.config['zones']:
            if item['zone'] == zone:
                return {'status': 200, "body": item}
            else:
                pass
        return {'status': 400, "body": 'Zone does not exist'}
    def alertzone(self):
        zones = self.config['zones']    
    def arm(self):
        
        if self.armed:
            return {'status': 400, 'body': 'The system is already armed'}
        pass
    def disarm(self):
        if not self.armed:
            return {'status': 400, 'body': 'The system is already disarmed'}
    def codepad_send(self, codepad_interface: str, codepad_id: str | int) -> None:
        pass