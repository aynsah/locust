from utils.config import SharedData

def log(status_code, url, error, body):
    filename = "log\err" + str(SharedData.now) + ".txt"
    f = open(filename, "a")
    f.write("=====================\n")
    f.write(str(status_code) + " => " + url + "\n")
    f.write(repr(error) + "\n")
    if status_code >= 400:
        f.write(body + "\n") 
    f.write("=====================\n\n")
    f.close()