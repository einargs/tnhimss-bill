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
import Patient from "@/components/patient.tsx";
import Condition from "@/components/condition.tsx";
import Organization from "@/components/organization.tsx";
import title from '/title.jpeg';

type FormData = {
    chatInput: string;
};

type TextEntry = {
    source: 'client' | 'server',
    message: string
};

type DataEntry = {
  source: 'medicalData',
  data: any
};

type TranscriptEntry = TextEntry | DataEntry;

// ! KEEP SOCKET HERE TO PREVENT RE-CONNECTIONS
// * We use vite.config.ts to proxy the connection
const socket = io();
function useSocket(setIsSending: React.Dispatch<React.SetStateAction<boolean>>) {
    const [transcript, setTranscript] = useState<TranscriptEntry[]>([]);
    const [isConnected, setIsConnected] = useState(socket.connected);

    useEffect(() => {
        function onConnect() {
            setIsConnected(true);
        }

        function onDisconnect() {
            setIsConnected(false);
        }

        function onServerMsg(msg: any) {
           console.log("server message", msg)
               setTranscript(prev => [...prev, { message: msg, source: 'server' }])
            setIsSending(false);
        }

        function onRecords(msg: any) {
            console.log("records", msg)
            setTranscript(prev => [...prev, { data: msg, source: 'medicalData' }])
        }

        socket.on('connect', onConnect);
        socket.on('disconnect', onDisconnect);
        socket.on('server-msg', onServerMsg);
        socket.on('records', onRecords);

        console.log("connecting")

        return () => {
            console.log("Disconnecting")
            socket.off('connect', onConnect);
            socket.off('disconnect', onDisconnect);
            socket.off('server-msg', onServerMsg);
            socket.off('records', onRecords);
        };
    }, []);
    return [isConnected, transcript, setTranscript]
}

function App() {
    const [isSending, setIsSending] = useState(false);
    const [isConnected, transcript, setTranscript] = useSocket(setIsSending) as [boolean, TranscriptEntry[], React.Dispatch<React.SetStateAction<TranscriptEntry[]>>];

    function onSubmit(data: FormData) {
        setIsSending(true);
        const chatMsg = data.chatInput;
        setTranscript(prev  => [...prev, { message: chatMsg, source: 'client' }]);
        socket.emit('client-msg', chatMsg);
        form.reset({chatInput: ""});
    }

    const form = useForm<FormData>({
      defaultValues: {
        chatInput: ''
      },
    });

    return (
        <div className="h-[94vh] flex flex-col">
            <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
                <p className='hidden'>{isConnected ? "Connected" : "Not Connected"}</p>
                <div className="m-2 mt-6 pl-8">
                  <img className="h-24" src={title} alt="Logo" />
                </div>
                {/*<ScrollArea className="h-full w-full rounded-md border p-4 mb-2 text-left space-y-4">*/}
                {/*    {transcript.map((entry, idx) =>*/}
                {/*        <Card className={`p-4 m-2 w-fit ${entry.source === 'client' ? 'mr-auto' : 'ml-auto'}`} key={idx}>{entry.message}</Card>)*/}
                {/*    }*/}
                {/*</ScrollArea>*/}
                <ScrollArea className="h-full w-full rounded-md border p-4 mb-2 text-left space-y-4">
                    {transcript.map((entry, idx) => {
                        if (entry.source === 'medicalData') {
                            try {
                                console.log("entry", entry)
                                const data = entry.data;
                                switch (true) {
                                    case data.type === 'patient':
                                        return <Patient medicalData={data} key={idx} />;

                                    case data.type === 'condition':
                                        return <Condition medicalData={data} key={idx} />;

                                    case data.type === 'organization':
                                        return <Organization medicalData={data} key={idx} />;

                                    default:
                                        return <Card className="p-4 m-2 w-fit ml-auto" key={idx}>Unknown medical data</Card>;
                                }
                            } catch (error) {
                                console.error("Failed to parse JSON:", error);
                                return <Card className="p-4 m-2 w-fit ml-auto" key={idx}>Invalid JSON data</Card>;
                            }
                        } else if (entry.source === 'server') {
                            return <Card className="p-4 m-2 w-fit mr-auto" key={idx}>{entry.message}</Card>;
                        } else if (entry.source === 'client') {
                            return <Card className="p-4 m-2 w-fit ml-auto" key={idx}>{entry.message}</Card>;
                        } else {
                            return <Card className="p-4 m-2 w-fit ml-auto" key={idx}>Unknown source</Card>;
                        }
                    })}

                </ScrollArea>

                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="w-full flex flex-row space-x-2">
                        <FormField
                            control={form.control}
                            name="chatInput"
                            render={({field}) => (
                                <FormItem className="flex-grow">
                                    <FormControl className="flex-grow">
                                        <Input placeholder="Enter your message" {...field} autoComplete="off" className="flex-grow" disabled={isSending} />
                                    </FormControl>
                                </FormItem>
                            )}
                        />
                        <Button type="submit" disabled={isSending}>Submit</Button>
                    </form>
                </Form>
            </ThemeProvider>
        </div>
    );
}

export default App;
