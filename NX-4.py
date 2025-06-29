import os
import json
import gpiozero 
import threading
import time
import threading
class NX:
    def __init__(self):
        self.armed = False
        self.config = json.load(open('config.json', 'r'))
        self.zonepins = []
        for input in self.config['inputs']:
            if input['pin'] == 3:
                self.siren = gpiozero.Buzzer(input)
        for zone in self.config['zones']:
            self.zonepins.append(gpiozero.Button(zone['pin']))
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
        while True:
            for i, zone in enumerate(self.zonepins):
                if zone.is_pressed:
                    if "bypassed" in self.config['zones'][i+1]['flags'] or "partial" in self.config['zones'][i+1]['flags']:
                        print("Bypassed Zone Triggered - Ignored zone")
                    elif "entryexit" in self.config['zones'][i+1]['flags']:
                        global start_time
                        start_time = time.time()
                        self.start_exit_timer()
                        return
                    elif 'instant' in self.config['zones'][i+1]['flags']:
                        self.raise_alarm()
                        return
                else:
                    print("System is armed")
    def start_exit_timer(self):
        timeout = self.config['timeout']
        input_received = threading.Event()

        def wait_for_enter():
            input("Press Enter to simulate button press...\n")
            input_received.set()

        thread = threading.Thread(target=wait_for_enter)
        thread.daemon = True
        thread.start()

        print(f"Waiting for input (timeout = {timeout} seconds)...")
        input_received.wait(timeout)

        if input_received.is_set():
            elapsed = time.time() - start_time
            print(f"Input received after {elapsed:.2f} seconds.")
            # ✅ Input received – no action needed
        else:
            print(f"Timeout reached! No input within {timeout} seconds.")
    def raise_alarm(self):
        self.codepad_send(None, codepad_id="ALL", data={"condition": {"breach_instant"}, "codepad_text": "The system is disrupted"})
        self.siren.on()
    def arm(self):
        
        if self.armed:
            return {'status': 400, 'body': 'The system is already armed'}
        threading.Thread(target=self.alertzone).run()
    def disarm(self):
        if not self.armed:
            return {'status': 400, 'body': 'The system is already disarmed'}
    def codepad_send(self, codepad_interface: str, codepad_id: str | int, data: dict) -> None:
        print("""Not configured""")

