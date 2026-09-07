#!/usr/bin/env python3
"""Simple SMTP stub server using only Python stdlib (asyncio).
Accepts all messages and prints them to stdout.
Works with Python 3.6+.
"""
import asyncio
import sys


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr}", flush=True)
    writer.write(b"220 localhost SMTP stub ready\r\n")
    await writer.drain()

    in_data = False
    data_lines = []

    while True:
        try:
            line = await asyncio.wait_for(reader.readline(), timeout=60)
        except asyncio.TimeoutError:
            break
        if not line:
            break

        if in_data:
            if line.rstrip(b"\r\n") == b".":
                in_data = False
                print(f"Message data received ({len(data_lines)} lines)", flush=True)
                writer.write(b"250 OK: Message queued\r\n")
                await writer.drain()
            else:
                # Strip leading dot-stuffing
                if line.startswith(b".."):
                    line = line[1:]
                data_lines.append(line)
            continue

        cmd = line.strip()
        print(f"C: {cmd}", flush=True)
        upper = cmd.upper()

        if upper.startswith(b"EHLO") or upper.startswith(b"HELO"):
            writer.write(b"250-localhost\r\n250 OK\r\n")
        elif upper.startswith(b"MAIL FROM"):
            writer.write(b"250 OK\r\n")
        elif upper.startswith(b"RCPT TO"):
            writer.write(b"250 OK\r\n")
        elif upper == b"DATA":
            writer.write(b"354 End data with <CR><LF>.<CR><LF>\r\n")
            in_data = True
            data_lines = []
        elif upper.startswith(b"QUIT"):
            writer.write(b"221 Bye\r\n")
            await writer.drain()
            break
        elif upper.startswith(b"RSET"):
            writer.write(b"250 OK\r\n")
        elif upper.startswith(b"NOOP"):
            writer.write(b"250 OK\r\n")
        else:
            writer.write(b"250 OK\r\n")
        await writer.drain()

    writer.close()
    try:
        await writer.wait_closed()
    except Exception:
        pass


async def run_server(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f"SMTP stub server listening on {addrs}", flush=True)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1025
    asyncio.run(run_server(host, port))
