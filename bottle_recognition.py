import paramiko
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
from picamera import PiCamera
from time import sleep       
import uuid

class Target:
    watchDir = '/home/admin/AIimage/image'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()
           
        try:
            url = "http://192.168.0.35:45226/prediction"
            camera = PiCamera()
            camera.resolution = (600, 600)
            camera.framerate = 15          
            camera.start_preview()
            for i in range(6):
                random_name = uuid.uuid1()
                time.sleep(2)                      
                camera.capture(f'/home/admin/AIimage/image/{random_name}.jpg')        
                form_data = {
                    'trainid': 'onnx',
                    'device_name': 'cpu',
                    'imagePath': 'C:/Users/khson/Desktop/new/sampleimage'
                }
                response = requests.get(url, params=form_data, data = form_data)
                if response.status_code == 200:
                    print('success')
                    print('respone:', response.text)
                else:
                    print('fail:', response.status_code)
                    print('respone:', response.text)
               
            camera.stop_preview()
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("System off")
            self.observer.join()

class Handler(FileSystemEventHandler):
    def on_created(self, event): 
        
        file_name = os.path.basename(event.src_path)
        host = "192.168.0.35"
        port = 22 
        transprot = paramiko.transport.Transport(host,port)
        userId = "desktop"
        password = "1234"

        transprot.connect(username = userId, password = password)
        sftp = paramiko.SFTPClient.from_transport(transprot)
        
        localpath = f"/home/admin/AIimage/image/{file_name}"
        remotepath = f"C:/Users/khson/Desktop/new/sampleimage/{file_name}"

        sftp.put(localpath, remotepath)

        sftp.close()

    def on_deleted(self, event): 
        print(event)

if __name__ == '__main__':
    w = Target()
    w.run()
    