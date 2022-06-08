import React from "react";

import socketio from "socket.io-client";

const ENDPOINT = "http://localhost:5000";

export const socket = socketio.connect(ENDPOINT);
export const SocketContext = React.createContext();
