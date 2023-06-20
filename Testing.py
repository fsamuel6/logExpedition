import subprocess

def get_network_type():
    result = subprocess.run(['adb', 'shell', 'getprop', 'gsm.network.type'], capture_output=True)
    output = result.stdout.decode().strip()

    if 'lte' in output.lower():
        return '4G'
    elif '3g' in output.lower():
        return '3G'
    elif '2g' in output.lower():
        return '2G'
    elif 'nr' in output.lower():
        return '5G'