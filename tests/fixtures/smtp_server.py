#!/usr/bin/env python3
"""Tiny SMTP sink used by the tests.

Usage: smtp_server.py PORT OUTDIR

Accepts connections sequentially, supports EHLO/HELO, AUTH PLAIN/LOGIN,
MAIL, RCPT, DATA, RSET, NOOP, QUIT. Each received message is written to
OUTDIR/msg-N.eml, prefixed with X-Test-Envelope-From / X-Test-Envelope-To /
X-Test-Auth lines describing the SMTP session.
"""
import base64
import os
import socket
import sys

port = int(sys.argv[1])
outdir = sys.argv[2]
os.makedirs(outdir, exist_ok=True)


def b64d(value):
    try:
        return base64.b64decode(value).decode("utf-8", "replace")
    except Exception:
        return value


def handle(conn, counter):
    f = conn.makefile("rb")

    def send(text):
        conn.sendall(text.encode("utf-8"))

    def readline():
        line = f.readline()
        if not line:
            raise EOFError()
        return line.decode("utf-8", "replace").rstrip("\r\n")

    send("220 localhost ESMTP test sink\r\n")
    mail_from = ""
    rcpts = []
    auth = ""
    while True:
        try:
            line = readline()
        except EOFError:
            return counter
        cmd = line.split(" ", 1)[0].upper()
        if cmd == "EHLO":
            send("250-localhost\r\n250-AUTH PLAIN LOGIN\r\n250-8BITMIME\r\n250 SIZE 10485760\r\n")
        elif cmd == "HELO":
            send("250 localhost\r\n")
        elif cmd == "AUTH":
            parts = line.split()
            mech = parts[1].upper() if len(parts) > 1 else ""
            if mech == "PLAIN":
                if len(parts) > 2:
                    data = parts[2]
                else:
                    send("334 \r\n")
                    data = readline()
                decoded = b64d(data).split("\x00")
                if len(decoded) >= 3:
                    auth = decoded[1] + ":" + decoded[2]
                else:
                    auth = ":".join(decoded)
                send("235 2.7.0 Authentication successful\r\n")
            elif mech == "LOGIN":
                if len(parts) > 2:
                    user = b64d(parts[2])
                else:
                    send("334 VXNlcm5hbWU6\r\n")
                    user = b64d(readline())
                send("334 UGFzc3dvcmQ6\r\n")
                pw = b64d(readline())
                auth = user + ":" + pw
                send("235 2.7.0 Authentication successful\r\n")
            else:
                send("504 Unrecognized authentication type\r\n")
        elif cmd == "MAIL":
            mail_from = line[5:].strip()
            rcpts = []
            send("250 OK\r\n")
        elif cmd == "RCPT":
            rcpts.append(line[5:].strip())
            send("250 OK\r\n")
        elif cmd == "DATA":
            send("354 End data with <CR><LF>.<CR><LF>\r\n")
            lines = []
            while True:
                raw = f.readline()
                if not raw:
                    return counter
                text = raw.decode("utf-8", "replace").rstrip("\r\n")
                if text == ".":
                    break
                if text.startswith(".."):
                    text = text[1:]
                lines.append(text)
            counter += 1
            path = os.path.join(outdir, "msg-%d.eml" % counter)
            with open(path, "w") as out:
                out.write("X-Test-Envelope-From: %s\n" % mail_from)
                for r in rcpts:
                    out.write("X-Test-Envelope-To: %s\n" % r)
                out.write("X-Test-Auth: %s\n" % auth)
                out.write("\n".join(lines))
                out.write("\n")
            print("stored %s" % path, flush=True)
            send("250 OK queued\r\n")
        elif cmd == "RSET":
            mail_from = ""
            rcpts = []
            send("250 OK\r\n")
        elif cmd == "NOOP":
            send("250 OK\r\n")
        elif cmd == "QUIT":
            send("221 Bye\r\n")
            return counter
        else:
            send("502 Command not implemented\r\n")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", port))
sock.listen(5)
print("listening on %d" % port, flush=True)
count = 0
while True:
    conn, _ = sock.accept()
    try:
        count = handle(conn, count)
    except Exception as exc:  # keep serving
        print("error: %s" % exc, flush=True)
    finally:
        try:
            conn.close()
        except Exception:
            pass
