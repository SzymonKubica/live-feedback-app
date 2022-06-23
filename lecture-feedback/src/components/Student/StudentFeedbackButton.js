import React from "react"

import { Button, Text } from "@chakra-ui/react"
import { SocketContext } from '../../context/socket'
import { getString, NilReaction } from "../Reactions"

const defaultColor = 500
const selectedColor = 900

function getColourGradient(reaction, selectedReaction) {
  if (reaction === selectedReaction) {
    return selectedColor
  }
  return defaultColor
}

const StudentFeedbackButton = ({
  title,
  color,
  reaction,
  selectedReaction,
  setSelectedReaction,
  room
}) => {

  const socket = React.useContext(SocketContext);

  function handleButton() {
    if (reaction === selectedReaction) {
      // When a button is selected and we tap it again to deselect it.
      setSelectedReaction(NilReaction)
      socket.emit("remove reaction", getString(reaction), room)
    } else if (selectedReaction === NilReaction) {
      // When nothing is selected and we press one button
      socket.emit("add reaction", getString(reaction), room)
      setSelectedReaction(reaction)
    } else {
      // When one button is selected and we press another one to change the reaction.
      socket.emit("remove reaction", getString(selectedReaction), room)
      socket.emit("add reaction", getString(reaction), room)
      setSelectedReaction(reaction)
    }
  }
  return (
    <Button
      colorScheme={color}
      bg={`${color}.${getColourGradient(reaction, selectedReaction)}`}
      onClick={handleButton}
      height="100%"
      _hover='0'
      fontSize={20}
    >
      {title}
    </Button>
  )
}

export default StudentFeedbackButton
