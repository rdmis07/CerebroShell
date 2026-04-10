import subprocess

def execute_command(cmd):
    try:
        if isinstance(cmd, str):
            cmd = cmd.replace('"', '\\"') 
            cmd = f'cmd /c "{cmd}"'
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        return stdout, stderr
    except Exception as e:
        return "", str(e)