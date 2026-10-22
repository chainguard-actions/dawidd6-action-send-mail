// Minimal fake SMTP server for testing. Usage: node smtp-server.cjs <port> <outdir>
// Each received message is written to <outdir>/msg-N.eml, prefixed with
// envelope lines (ENVELOPE-FROM / ENVELOPE-TO) and AUTH info if any.
const net = require("net");
const fs = require("fs");
const path = require("path");

const port = parseInt(process.argv[2] || "2525", 10);
const outDir = process.argv[3] || "/tmp/smtp-out";
fs.mkdirSync(outDir, { recursive: true });
let counter = 0;

const server = net.createServer((socket) => {
  socket.on("error", () => {});
  let buf = "";
  let mode = "cmd"; // cmd | data | authplain | authuser | authpass
  let envFrom = "";
  let envTo = [];
  let authUser = "";
  let authPass = "";
  const send = (s) => {
    try { socket.write(s + "\r\n"); } catch (e) {}
  };
  const log = (s) => fs.appendFileSync(path.join(outDir, "session.log"), s + "\n");

  send("220 localhost fake ESMTP ready");

  const handleLine = (line) => {
    log("C: " + line);
    if (mode === "authplain") {
      const parts = Buffer.from(line, "base64").toString("utf8").split("\0");
      authUser = parts[1] || "";
      authPass = parts[2] || "";
      mode = "cmd";
      fs.appendFileSync(path.join(outDir, "auth.log"), `USER=${authUser}\nPASS=${authPass}\n`);
      return send("235 2.7.0 Authentication successful");
    }
    if (mode === "authuser") {
      authUser = Buffer.from(line, "base64").toString("utf8");
      mode = "authpass";
      return send("334 UGFzc3dvcmQ6");
    }
    if (mode === "authpass") {
      authPass = Buffer.from(line, "base64").toString("utf8");
      mode = "cmd";
      fs.appendFileSync(path.join(outDir, "auth.log"), `USER=${authUser}\nPASS=${authPass}\n`);
      return send("235 2.7.0 Authentication successful");
    }
    const upper = line.toUpperCase();
    if (upper.startsWith("EHLO")) {
      socket.write("250-localhost\r\n250-8BITMIME\r\n250-SMTPUTF8\r\n250-AUTH PLAIN LOGIN\r\n250 SIZE 10485760\r\n");
      return;
    }
    if (upper.startsWith("HELO")) return send("250 localhost");
    if (upper.startsWith("AUTH PLAIN")) {
      const arg = line.slice(10).trim();
      if (arg) {
        mode = "authplain";
        return handleLine(arg);
      }
      mode = "authplain";
      return send("334 ");
    }
    if (upper.startsWith("AUTH LOGIN")) {
      const arg = line.slice(10).trim();
      if (arg) {
        authUser = Buffer.from(arg, "base64").toString("utf8");
        mode = "authpass";
        return send("334 UGFzc3dvcmQ6");
      }
      mode = "authuser";
      return send("334 VXNlcm5hbWU6");
    }
    if (upper.startsWith("MAIL FROM:")) {
      envFrom = line.slice(10).trim().split(" ")[0];
      envTo = [];
      return send("250 2.1.0 OK");
    }
    if (upper.startsWith("RCPT TO:")) {
      envTo.push(line.slice(8).trim().split(" ")[0]);
      return send("250 2.1.5 OK");
    }
    if (upper === "DATA") {
      mode = "data";
      return send("354 End data with <CR><LF>.<CR><LF>");
    }
    if (upper.startsWith("RSET")) {
      envFrom = "";
      envTo = [];
      return send("250 OK");
    }
    if (upper.startsWith("NOOP")) return send("250 OK");
    if (upper.startsWith("QUIT")) {
      send("221 Bye");
      return socket.end();
    }
    return send("502 Command not implemented");
  };

  socket.on("data", (chunk) => {
    buf += chunk.toString("utf8");
    while (true) {
      if (mode === "data") {
        let idx = buf.indexOf("\r\n.\r\n");
        let skip = 5;
        if (buf.startsWith(".\r\n")) { idx = 0; skip = 3; }
        if (idx < 0) return;
        const data = idx === 0 && skip === 3 ? "" : buf.slice(0, idx);
        buf = buf.slice(idx + skip);
        const body = data.split("\r\n").map((l) => (l.startsWith("..") ? l.slice(1) : l)).join("\n");
        counter += 1;
        const header =
          `ENVELOPE-FROM: ${envFrom}\n` +
          envTo.map((t) => `ENVELOPE-TO: ${t}\n`).join("") +
          "\n";
        fs.writeFileSync(path.join(outDir, `msg-${counter}.eml`), header + body + "\n");
        mode = "cmd";
        send("250 2.0.0 OK queued as " + counter);
        continue;
      }
      const idx = buf.indexOf("\r\n");
      if (idx < 0) return;
      const line = buf.slice(0, idx);
      buf = buf.slice(idx + 2);
      handleLine(line);
    }
  });
});

server.listen(port, "127.0.0.1", () => {
  console.log(`fake smtp listening on ${port}, writing to ${outDir}`);
});
