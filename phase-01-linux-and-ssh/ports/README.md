# Ports and Network Sockets

## What I learned

A port is a numbered network endpoint used to reach a specific service on a machine.

Examples:

- SSH commonly uses port 22
- HTTP commonly uses port 80
- HTTPS commonly uses port 443

A listening port means a process is waiting for incoming network communication on that port.

## Inspecting sockets

Linux provides the `ss` command for inspecting network sockets.

Example:

```bash
ss -tulpn
```

Important fields in the output include:

- protocol: TCP or UDP
- state: such as `LISTEN`
- Local Address:Port
- Peer Address:Port
- process name
- PID

## TCP and UDP

TCP establishes a connection and provides reliable, ordered delivery.

UDP does not use the same connection model and does not guarantee delivery or ordering.

## Socket vs port

A port is only a number.

A socket is a communication endpoint used by a process.

Example:

```text
127.0.0.1:39013
```

Here:

- `127.0.0.1` is the local address
- `39013` is the port

## Local and peer endpoints

`Local Address:Port` represents this machine's side of the socket.

`Peer Address:Port` represents the other endpoint.

For a listening socket:

```text
0.0.0.0:*
```

in the peer column means there is no specific peer connected yet.

## Binding addresses

```text
127.0.0.1:39013
```

means the socket is available only through the local machine.

```text
0.0.0.0:PORT
```

in the local-address column means the socket is bound to all local IPv4 interfaces.

`0.0.0.0` is not the machine's real IP address.

## Real output practiced

I inspected real `ss` output from my Fedora machine.

I identified:

```text
VS Code → TCP
Chrome  → UDP
```

I also identified the process PID and distinguished the process ID from the network port.

## Current understanding

I can explain:

- port
- listening port
- TCP vs UDP
- socket vs port
- Local Address:Port
- Peer Address:Port
- `127.0.0.1`
- `0.0.0.0`
- process PID in `ss` output