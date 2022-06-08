import React, {useState, useEffect} from "react";
import socketIOClient from "socket.io-client";
import { socket } from "../context/socket";


export const SocketCounter = (props) => {
    const [counter, setCounter] = useState(0);

    useEffect(() => {
        socket.on("update " + props.reaction, data => {
            setCounter(data.count)

        });

        // Disconnect when unmounts
        return () => socket.off("fromApi");
        //

    }, [])

    return (
    <div>
        <p>{props.reaction}: {counter}</p>
    </div>
    );
}