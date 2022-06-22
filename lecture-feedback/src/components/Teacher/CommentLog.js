import React, { useState, useEffect } from "react"
import { SocketContext } from '../../context/socket'


import { Flex, Switch } from '@chakra-ui/react'

import Messages from "./Messages"

export default function CommentLog({room}) {
    const [commentsAllowed, setCommentsAllowed] = useState(false)
    
    const [comments, setComments] = useState([])
    const socket = React.useContext(SocketContext);    
  
    useEffect(() => {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({"room": room}),
      }  

      socket.on("update comments", () => {
          
          fetch('/api/get-comments', requestOptions)
          .then(res => res.json())
          .then(data => {
            setComments(data.comments)
          })
        })

        fetch('/api/get-comments', requestOptions)
        .then(res => res.json())
        .then(data => {
          setComments(data.comments)
        })
        
        // Disconnect when unmounts
        return () => socket.off("update comments")
      }, [])
  

    return (    
    <Flex w="100%" h="100%" justify="center" align="center">
      <Flex w={["100%", "100%", "40%"]} h="90%" flexDir="column">
      <Switch isChecked = {commentsAllowed} onChange = {e => setCommentsAllowed(!commentsAllowed)}>Comments</Switch>
      {commentsAllowed ? 
            <Messages h="calc(40vh)" messages={comments} />
            : null}

      </Flex>
    </Flex>
    )
}
