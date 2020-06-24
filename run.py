from project import app, socketio
import os

if __name__ == "__main__":
    # os.system("project/util/start_subscribers.py")
    # from subprocess import call
    # call('python project/util/start_subscribers.py'.split())
    # exec(open('project/util/start_subscribers.py').read())
    socketio.run(app)
