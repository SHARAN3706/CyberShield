import socket
import threading


PORTS_TO_SCAN = [21, 22, 25, 53, 80, 443, 3306, 8080]

PORT_LABELS = {
    21:   "FTP",
    22:   "SSH",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    443:  "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Alt",
}


def scan_port(host: str, port: int, open_ports: list, lock: threading.Lock) -> None:
    """Attempt a TCP connection to host:port with a short timeout.
    Appends the port to open_ports (thread-safe) if the connection succeeds.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.1)
            result = sock.connect_ex((host, port))
            if result == 0:
                with lock:
                    open_ports.append(port)
    except (socket.error, OSError):
        pass


def scan_ports(target: str) -> dict:
    """Resolve *target* to an IP, scan all PORTS_TO_SCAN in parallel,
    and return a result dictionary.

    Returns
    -------
    dict with keys:
        host        – resolved IP address string
        open_ports  – sorted list of open port numbers
        risk_score  – integer (open ports × 12)
        grade       – "High Risk" | "Medium Risk" | "Low Risk"

    Raises
    ------
    ValueError  – if the host cannot be resolved
    """
    # Resolve domain → IP
    try:
        host = socket.gethostbyname(target.strip())
    except socket.gaierror:
        raise ValueError(f"Invalid website or IP address: '{target}'")

    open_ports: list = []
    lock = threading.Lock()
    threads = []

    for port in PORTS_TO_SCAN:
        t = threading.Thread(
            target=scan_port,
            args=(host, port, open_ports, lock),
            daemon=True,
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join(timeout=1.0)   # guard: never block longer than 1 s per thread

    open_ports.sort()

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
        "grade": grade,
    }
