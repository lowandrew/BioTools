import subprocess


def run_subprocess(command):
    """
    command is the command to run, as a string.
    runs a subprocess, returns stdout and stderr from the subprocess as strings.
    """
    x = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = x.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if x.returncode != 0:
        print('STDERR from called program: {}'.format(err))
        raise subprocess.CalledProcessError(x.returncode, command)
    return out, err
