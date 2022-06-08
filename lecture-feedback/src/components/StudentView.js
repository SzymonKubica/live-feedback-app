import React, {useState, useEffect} from "react";
import { Button, ButtonGroup } from '@chakra-ui/react'
import { socket, SocketContext } from "../context/socket";
import { SocketButton } from "./SocketButton";
import { ToggleButton } from "./ToggleButton";
import { ConfusedButton } from "./ConfusedButton";

import {
  ChakraProvider,
  Box,
  Grid,
  theme,
} from '@chakra-ui/react';
import { ColorModeSwitcher } from '../ColorModeSwitcher';

export const StudentView = () => {
    return(
        <ChakraProvider theme={theme}>
            <Box textAlign="center" fontSize="xl">
            <Grid minH="100vh" p={3}>
                <ColorModeSwitcher justifySelf="flex-end" />
            <SocketContext.Provider value={socket}>
                <ToggleButton reaction="good"/>            
                <ToggleButton reaction="confused"/>            
                <ToggleButton reaction="too fast"/>            
                <ToggleButton reaction="chilling"/>            
            </SocketContext.Provider>
            </Grid>
            </Box>
        </ChakraProvider>
    )
}