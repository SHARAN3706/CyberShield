import socket

def scan_ports(host):
    open_ports = []
    ports = [21, 22, 25, 53, 80, 443, 3306, 8080]

    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex((host, port)) == 0:
            open_ports.append(port)
        s.close()

    risk_score = len(open_ports) * 12

    if risk_score > 70:
        grade = "High Risk"
    elif risk_score > 40:
        grade = "Medium Risk"
    else:
        grade = "Low Risk"

    return {
        "host": host,
        "open_ports": open_ports,
        "risk_score": risk_score,
        "grade": grade
    }
