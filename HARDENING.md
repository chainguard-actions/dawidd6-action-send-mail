<!-- markdownlint-disable -->

# Hardening Report: dawidd6--action-send-mail/v24

> This file was generated automatically by the hardening agent.

**Policy SHA:** `374911c4be584df24e6da57af2d990570ef0f859`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **dawidd6--action-send-mail/v24** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### prior-fix (severity: high)

Carried forward from this version's previous harden, which fixed it; fix it again unless the code no longer has the problem. The previous harden changed main.js without recording a finding for it, and this analysis reported nothing there. Re-apply its security changes unless the code no longer needs them. The previous patch:
```diff
diff --git a/main.js b/main.js
index 0bd9cc3..18d734a 100644
--- a/main.js
+++ b/main.js
@@ -1,268 +1,39013 @@
-import nodemailer from "nodemailer";
-import addressparser from "nodemailer/lib/addressparser/index.js";
-import * as core from "@actions/core";
-import * as glob from "@actions/glob";
+import{createRequire as __acCreateRequire}from"node:module";import{fileURLToPath as __acFileURLToPath}from"node:url";import{dirname as __acDirname}from"node:path";const require=__acCreateRequire(import.meta.url);const __filename=__acFileURLToPath(import.meta.url);const __dirname=__acDirname(__filename);
+var __create = Object.create;
+var __defProp = Object.defineProperty;
+var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
+var __getOwnPropNames = Object.getOwnPropertyNames;
+var __getProtoOf = Object.getPrototypeOf;
+var __hasOwnProp = Object.prototype.hasOwnProperty;
+var __require = /* @__PURE__ */ ((x) => typeof require !== "undefined" ? require : typeof Proxy !== "undefined" ? new Proxy(x, {
+  get: (a, b) => (typeof require !== "undefined" ? require : a)[b]
+}) : x)(function(x) {
+  if (typeof require !== "undefined") return require.apply(this, arguments);
+  throw Error('Dynamic require of "' + x + '" is not supported');
+});
+var __commonJS = (cb, mod) => function __require2() {
+  try {
+    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
+  } catch (e) {
+    throw mod = 0, e;
+  }
+};
+var __copyProps = (to, from, except, desc) => {
+  if (from && typeof from === "object" || typeof from === "function") {
+    for (let key of __getOwnPropNames(from))
+      if (!__hasOwnProp.call(to, key) && key !== except)
+        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
+  }
+  return to;
+};
+var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
+  // If the importer is in node compatibility mode or this is not an ESM
+  // file that has been converted to a CommonJS file using a Babel-
+  // compatible transform (i.e. "__esModule" has not been set), then set
+  // "default" to the CommonJS "module.exports" for node compatibility.
+  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
+  mod
+));
+
+// node_modules/tunnel/lib/tunnel.js
+var require_tunnel = __commonJS({
+  "node_modules/tunnel/lib/tunnel.js"(exports) {
+    "use strict";
+    var net8 = __require("net");
+    var tls3 = __require("tls");
+    var http2 = __require("http");
+    var https2 = __require("https");
+    var events = __require("events");
+    var assert4 = __require("assert");
+    var util3 = __require("util");
+    exports.httpOverHttp = httpOverHttp2;
+    exports.httpsOverHttp = httpsOverHttp2;
+    exports.httpOverHttps = httpOverHttps2;
+    exports.httpsOverHttps = httpsOverHttps2;
+    function httpOverHttp2(options) {
+      var agent = new TunnelingAgent(options);
+      agent.request = http2.request;
+      return agent;
+    }
+    function httpsOverHttp2(options) {
+      var agent = new TunnelingAgent(options);
+      agent.request = http2.request;
+      agent.createSocket = createSecureSocket;
+      agent.defaultPort = 443;
+      return agent;
+    }
+    function httpOverHttps2(options) {
+      var agent = new TunnelingAgent(options);
+      agent.request = https2.request;
+      return agent;
+    }
+    function httpsOverHttps2(options) {
+      var agent = new TunnelingAgent(options);
+      agent.request = https2.request;
+      agent.createSocket = createSecureSocket;
+      agent.defaultPort = 443;
+      return agent;
+    }
+    function TunnelingAgent(options) {
+      var self = this;
+      self.options = options || {};
+      self.proxyOptions = self.options.proxy || {};
+      self.maxSockets = self.options.maxSockets || http2.Agent.defaultMaxSockets;
+      self.requests = [];
+      self.sockets = [];
+      self.on("free", function onFree(socket, host, port, localAddress
... (truncated)
```

Locations:

- `main.js`

## Iteration Notes

### Iteration 1

**Notes:**

No change made. The earlier harden's main.js change was an esbuild bundle: a generated createRequire header plus node_modules (tunnel, undici, nodemailer, etc.) inlined into one file. That is a build step, not a security fix, and can't sensibly be redone by hand. I reviewed the current main.js: it only reads inputs through @actions/core and sends mail with nodemailer. There is no shell execution, no ${{ }} interpolation and no GITHUB_ENV/OUTPUT writes. action.yml is a plain node24 action with no uses: references. node_modules ships with the action, so the unbundled source runs. If bundling is needed, it should be done by the pipeline's build step (esbuild).

