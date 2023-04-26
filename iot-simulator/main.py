# The following code block is used to run three separate Python scripts in parallel and wait for them to complete.

# Import the `subprocess` module to run external commands
import subprocess

# Use the `subprocess.Popen` method to create three separate processes for each Python script
# Each process is created by passing a list containing the command to be executed (i.e., the Python executable and the name of the script)
# For each process, the `Popen` method returns a subprocess object that can be used to control and interact with the process.
proc1 = subprocess.Popen(["python", "temperature_sensor.py"])
proc2 = subprocess.Popen(["python", "smart_electricity_meter.py"])
proc3 = subprocess.Popen(["python", "garage_door.py"])

# Use the `wait()` method to block the execution of the main program until each subprocess has completed
# The `wait()` method waits for the subprocess to terminate and returns the exit code of the process.
# By calling `wait()` for each process in sequence, the main program waits for all subprocesses to finish before terminating.
proc1.wait()
proc2.wait()
proc3.wait()

# Print a message to indicate that the simulation has finished running
print("End of IOT device simulator run")