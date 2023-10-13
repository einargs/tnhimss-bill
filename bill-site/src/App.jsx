import {useEffect, useState} from 'react';
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


const patientIds = ['Aaron Brekke']


const URL = "http://localhost:5000";
// ! KEEP SOCKET HERE TO PREVENT RE-CONNECTIONS
const socket = io(URL);

function useSocket() {
    const [transcript, setTranscript] = useState([])
    const [isConnected, setIsConnected] = useState(socket.connected);

    useEffect(() => {
            console.log("test");
        function onConnect() {
            setIsConnected(true);
        }

        function onDisconnect() {
            setIsConnected(false);
        }

        function onServerMsg(msg) {
            setTranscript(prev => [...prev, msg])
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
    const [isChatStarted, setIsChatStarted] = useState(false);
    const [isConnected, transcript, setTranscript] = useSocket();
    const [message, setMessage] = useState("");

    function startChat() {
        socket.emit('start-chat', "aaron-brekke");
        setIsChatStarted(true);
    }

    function onSubmit(data) {
        const chatMsg = data.chatInput;
        setTranscript(prev => [...prev, chatMsg]);
        socket.emit('client-msg', chatMsg);
        setMessage("");  // Clear the message state here
    }

    const form = useForm()

    return (
        <div className="h-[94vh] flex flex-col">
            <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
                <h1>Simple frontend to test responses</h1>
                <p>{isConnected ? "Connected" : "Not Connected"}</p>
                <p>{isChatStarted ? "Chat Started" : "Chat Not Started"}</p>
                <div className="card">
                    <Button onClick={startChat}>
                        Start Chat
                    </Button>
                </div>


                <ScrollArea className="h-full w-full rounded-md border p-4 mb-2 text-left space-y-4">
                    {transcript.map((line, idx) =>
                        <Card className='p-4' key={idx}>{line}</Card>)}
                </ScrollArea>


                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="w-full flex flex-row space-x-2">
                        <FormField
                            control={form.control}
                            name="email"
                            render={({field}) => (
                                <FormItem>
                                    <Select defaultValue={field.value}>
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
                            className="flex-grow"
                            name="chatInput"
                            render={({field}) => (
                                <FormItem className="flex-grow">
                                    <FormControl className="flex-grow">
                                        <Input placeholder="Enter your message" {...field} className="flex-grow"/>
                                    </FormControl>
                                </FormItem>
                            )}
                        />
                        <Button type="submit">Submit</Button>
                    </form>
                </Form>

            </ThemeProvider>
        </div>
    );
}

export default App;
