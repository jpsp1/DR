from agents import Agent, WebSearchTool, trace, Runner, function_tool
#from IPython.display import display, Markdown
from messenger import push
import statistics
import csv
from datetime import datetime, timedelta
import sys

############################


def read_recent_csv(filename,hours):
    cutoff = datetime.now() - timedelta(hours=hours)
    data = {}
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                timestamp = datetime.strptime(
                    row["timestamp"],
                    "%Y-%m-%d %H:%M:%S"
                )
            except (ValueError, KeyError):
                # Ignore rows with an invalid/missing timestamp
                continue
            # Ignore entries older than 24 hours
            if timestamp < cutoff:
                continue
            # Use timestamp as the dictionary key
            data[timestamp] = {
                "load15": float(row["load15"]),
                "cpu_used_pct": float(row["cpu_used_pct"]),
                "mem_used_pct": float(row["mem_used_pct"]),
                "disk_read_mbps": float(row["disk_read_mbps"]),
                "disk_write_mbps": float(row["disk_write_mbps"]),
                "disk_iops": int(row["disk_iops"]),
                "tcp_active": int(row["tcp_active"]),
                "tcp_established": int(row["tcp_established"]),
                "net_rx_mbps": float(row["net_rx_mbps"]),
                "net_tx_mbps": float(row["net_tx_mbps"]),
                "cpu_temp": float(
                    row["cpu_temp"]
                    .replace("'C", "")
                    .replace("°C", "")
                )
            }
    #return data
    data = dict(sorted(data.items()))
    return(data)


################################
@function_tool
def push_tool(subject: str, text_body: str) -> str:
    """
    Send out message with the given subject and body 
    
    Args:
        subject: The subject of the message
        text_body: The body of the message as plain text        
    """
    push(f"Subject: {subject}\n\n{text_body}")
    return "Message sent successfully"

#include CPU usage, memory usage, disk usage, network usage, etc.
@function_tool
def get_performance_data_tool(host: str, variable: str, time_range: int) -> list:
    """
    Get performance data about the system.

    Args:
        host: The host to get data from
        variable: The performance variable to get data for. Available variables are: load15, cpu_used_pct, mem_used_pct, disk_read_mbps, disk_write_mbps, disk_iops, tcp_active, tcp_established, net_rx_mbps,net_tx_mbps and cpu_temp. Only use these variables to call the tool.
        time_range: The time range in hours for which to get data

    Returns:
        A list containing the performance data.
    """
    # Placeholder implementation - replace with actual performance data retrieval logic
    f='/var/log/os_activity.csv'
    data = read_recent_csv(f, time_range)
    l={}
    #variable='load15'
    for timestamp, values in data.items():
        l[timestamp] = values.get(variable)
    return list(l.values())
    #datetime.datetime(2026, 10, 30, 14, 18, 26): {'load15': 0.1, 'cpu_used_


    
@function_tool
def median_tool(data: list[float]) -> [float, float]:   
    """
    Calculate the median of a list of numbers.

    Args:
        data: A list of numbers

    Returns:
        A list containing the median of the numbers and the standard deviation of the numbers. If the list is empty, returns None.
    """    
    try:
        m=statistics.median(data)
        std=statistics.stdev(data)
    except exception as e:
        print(f"Error calculating median: {e}")
        return [None, None]
    else:
        print(f"Median calculated successfully: {m}")
        return [m, std]
 
@function_tool
def daily_report_tool(host: str) -> str:
    """
    Get the JSON system daily report

    Args:
        data: host name 

    Returns:
        A JSON text containing a snapshot of the system's informatio"""
    filename='/var/log/daily-report.log'
    with open(filename) as f:
        return f.read()


#statistics.stdev([1, 3, 5, 7, 9, 11]))
########################
#from agents.model_settings import ModelSettings
#from pydantic import BaseModel, Field
#from dotenv import load_dotenv
#import asyncio
#from messenger import send_email, push
#import sys