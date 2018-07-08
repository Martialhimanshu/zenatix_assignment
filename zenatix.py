from influxdb import InfluxDBClient
from datetime import datetime
import psutil
import time

client = InfluxDBClient('127.0.0.1','8086', 'admin', 'admin', 'zenatix')

client.create_database('zenatix')

# client.create_retention_policy('awesome_policy', '3d', 3, default=True)

measurement = [{
        "measurement":"system_zenatix",
        "fields":{
            "cpu_usage":0,
            "process_running":0,
            "ports_open":0
        },
        "time": ""
    }
    ]


def cpu_stats():    
    cpu = psutil.cpu_percent(interval=0.2, percpu=False)
    """interval is configured to get cpu usage for an instance(In this example interval is 0.2 seconds)"""
    measurement[0]["fields"]["cpu_usage"] = cpu


def available_port():
    avail_port = 0
    for proc in psutil.process_iter():
        for x in proc.connections():
            if x.status == psutil.CONN_LISTEN:
                avail_port += 1
    measurement[0]["fields"]["ports_open"] = avail_port

def running_process():
    measurement[0]["fields"]["process_running"] = len(psutil.pids())

def metrix_time():
    measurement[0]["time"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

while True:
    cpu_stats()
    available_port()
    running_process()
    metrix_time()
    # print(measurement)
    time.sleep(6)

    try:
        client.write_points(measurement)
    except Exception as e:
        print(e)
