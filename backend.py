import socket
import threading


def scan_port(host, port, open_ports):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)

        if s.connect_ex((host, port)) == 0:
            open_ports.append(port)

        s.close()
    except:
        pass


def scan_ports(host):
    try:
        host = socket.gethostbyname(host)
    except:
        return {
            "host": host,
            "open_ports": [],
            "risk_score": 0,
            "grade": "Invalid Host"
        }

    open_ports = []
    ports = [21, 22, 25, 53, 80, 443, 3306, 8080]

    threads = []

    for port in ports:
        t = threading.Thread(target=scan_port, args=(host, port, open_ports))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

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
