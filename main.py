import boto3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
  
class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "e:/Code/indellinent/test/"
  
    def __init__(self, handlers):
        self.observer = Observer()
        self.handlers = handlers

    def run(self):
        for handler in self.handlers:
            self.observer.schedule(handler, self.watchDirectory)

        self.observer.start()
        try:
            while self.observer.isAlive():
                self.observer.join(5)
        except KeyboardInterrupt:
            # user requested stop
            pass
        finally:
            self.observer.stop()
            self.observer.join()
            print("Observer Stopped")

class Handler(FileSystemEventHandler):

    def __init__(self, s3_client, bucket_name, target_filename):
        self.s3 = s3_client
        self.bucket_name = bucket_name
        self.target_filename = target_filename
  
    def on_any_event(self, event):

        if event.event_type == 'created' or event.event_type == 'closed' and self.target_filename in event.src_path:
            self.s3.upload_file(event.src_path, self.bucket_name, self.target_filename)
            print("Watchdog received %s event - %s." % (event.event_type, event.src_path))

  
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog="monitor-specific-file",
        description="Monitor a specific file, and upload it to a specific s3 bucket",
    )
    parser.add_argument('s3_bucket_name')
    parser.add_argument('filename')
    args = parser.parse_args()

    s3_bucket_name = args.s3_bucket_name
    filename = args.filename

    s3 = boto3.client("s3")

    test_handler = Handler(s3, s3_bucket_name, filename)

    watch = OnMyWatch([test_handler])
    watch.run()
