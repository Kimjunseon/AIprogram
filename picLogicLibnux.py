import paramiko
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
from picamera import PiCamera
from time import sleep       


class Target:
    watchDir = '/home/admin/AIimage/image'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()
           
        try:
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
        
        localpath = f"C:/Users/scadaict/Desktop/sub/{file_name}"
        remotepath = f"C:/Users/khson/Desktop/images/{file_name}"

        sftp.put(localpath, remotepath)

        sftp.close()

    def on_deleted(self, event): 
        print(event)

if __name__ == '__main__':
    w = Target()
    w.run()
    
camera = PiCamera()           
camera.start_preview()        
sleep(5)                      
camera.capture('/home/admin/AIimage/image/ris.jpg')
camera.stop_preview() 


