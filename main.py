import os
import time
import boto3
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
  
s3_bucket_name = ""
filename = ""
  
class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "e:/Code/indellinent/test/"
  
    def __init__(self):
        self.observer = Observer()
  
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
  
        self.observer.join()
  
  
class Handler(FileSystemEventHandler):
  
    @staticmethod
    def on_any_event(event):

        if event.event_type == 'created' and filename in event.src_path :
            s3 = boto3.client(
                's3',
                region_name = os.environ['AWS_REGION'],
                aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']            
            )

            s3.upload_file(event.src_path, s3_bucket_name, filename)
            print("Watchdog received created event - % s." % event.src_path)
        elif event.event_type == 'modified' and filename in event.src_path :
            s3 = boto3.client(
                's3',
                region_name = os.environ['AWS_REGION'],
                aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']            
            )
            
            s3.upload_file(event.src_path, s3_bucket_name, filename)
            print("Watchdog received modified event - % s." % event.src_path)
        else:
            return None
              
  
if __name__ == '__main__':

    #Set global variables as data that's passed from command line
    s3_bucket_name = sys.argv[1]
    filename = sys.argv[2]

    watch = OnMyWatch()
    watch.run()