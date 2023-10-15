import React, {useEffect, useState} from 'react';
import {useForm} from 'react-hook-form';
import './App.css';
import {io} from 'socket.io-client';

import {Button} from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
} from "@/components/ui/form"
import {Input} from "@/components/ui/input"
import {ThemeProvider} from "@/components/theme-provider.jsx";
import {ScrollArea} from "@/components/ui/scroll-area"
import {Card} from "@/components/ui/card.jsx";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select.jsx";

type FormData = {
    chatInput: string;
};

const patientIds = ['aaron-brekke']

const URL = "http://localhost:5000";
// ! KEEP SOCKET HERE TO PREVENT RE-CONNECTIONS
const socket = io(URL);

function useSocket(setIsSending: React.Dispatch<React.SetStateAction<boolean>>) {
    const [transcript, setTranscript] = useState<string[]>([]);
    const [isConnected, setIsConnected] = useState(socket.connected);

    useEffect(() => {
        function onConnect() {
            setIsConnected(true);
        }

        function onDisconnect() {
            setIsConnected(false);
        }

        function onServerMsg(msg: any) {
            setTranscript(prev => [...prev, msg])
            setIsSending(false);

        }

        socket.on('connect', onConnect);
        socket.on('disconnect', onDisconnect);
        socket.on('server-msg', onServerMsg)

        return () => {
            socket.off('connect', onConnect);
            socket.off('disconnect', onDisconnect);
            socket.off('server-msg', onServerMsg)
        };
    }, []);
    return [isConnected, transcript, setTranscript]
}

function App() {
    const [isSending, setIsSending] = useState(false);
    const [selectedPatient, setSelectedPatient] = useState<string | null>(null);
    const [isChatStarted, setIsChatStarted] = useState(false);
    const [isConnected, transcript, setTranscript] = useSocket(setIsSending) as [boolean, string[], React.Dispatch<React.SetStateAction<string[]>>];

    function startChat(patientId: string) {
        setSelectedPatient(patientId);
        socket.emit('start-chat', patientId);
        setIsChatStarted(true);
    }

    function onSubmit(data: FormData) {
        setIsSending(true);
        const chatMsg = data.chatInput;
        setTranscript(prev => [...prev, chatMsg]);
        socket.emit('client-msg', chatMsg);
        form.reset({chatInput: ""});
    }

    const form = useForm<FormData>();

    return (
        <div className="h-[94vh] flex flex-col">
            <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
                <p>{isConnected ? "Connected" : "Not Connected"}</p>
                <p>{isChatStarted ? "Chat Started" : "Chat Not Started"}</p>
                <ScrollArea className="h-full w-full rounded-md border p-4 mb-2 text-left space-y-4">
                    {transcript.map((line, idx) =>
                        <Card className='p-4' key={idx}>{line}</Card>)}
                </ScrollArea>
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="w-full flex flex-row space-x-2">
                        <FormField
                            control={form.control}
                            name="chatInput"
                            render={({field}) => (
                                <FormItem>
                                    <Select defaultValue={field.value} onValueChange={(e) => startChat(e.valueOf())}
                                    >
                                        <FormControl>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select a patient"/>
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent>
                                            {patientIds.map((id, idx) =>
                                                <SelectItem key={idx} value={id}>{id}</SelectItem>)
                                            }
                                        </SelectContent>
                                    </Select>
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="chatInput"
                            render={({field}) => (
                                <FormItem className="flex-grow">
                                    <FormControl className="flex-grow">
                                        <Input placeholder="Enter your message" {...field} className="flex-grow" disabled={isSending || !selectedPatient} />
                                    </FormControl>
                                </FormItem>
                            )}
                        />
                        <Button type="submit" disabled={isSending || !selectedPatient}>Submit</Button>
                    </form>
                </Form>
            </ThemeProvider>
        </div>
    );
}

export default App;
