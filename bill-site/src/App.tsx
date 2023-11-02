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
import Patient from "@/components/patient.tsx";
import Condition from "@/components/condition.tsx";
import Organization from "@/components/organization.tsx";

type FormData = {
    chatInput: string;
};

type TranscriptEntry = {
    source: 'client' | 'server' | 'medicalData',
    message: string;
};

const condition = {
    onsetdate: "1960-10-09T06:24:57-05:00",
    pid: "urn:uuid:c698c2cc-6766-c4dd-f15a-e4b8e023c660",
    id: "4efcd5fd-e29d-85cc-30f8-0909968e140b",
    type: "condition",
    recordeddata: "1960-10-09T06:24:57-05:00",
    verificationstatus: "confirmed",
    conditioncode: "Prediabetes",
    encref: "urn:uuid:1e8aa5b5-c92b-65cd-ff54-b893fde5410f"
};

const patient = {
    zip: "01940",
    fname: "Clara",
    type: "patient",
    lname: "Carbajal",
    city: "Lynn",
    sex: "female",
    id: "c698c2cc-6766-c4dd-f15a-e4b8e023c660",
    state: "Massachusetts",
    birthDate: "1992-06-12T06:24:57-05:00"
};

const organization = {
    orgtype: "Healthcare Provider",
    name: "PCP47622",
    type: "organization",
    addressState: "MA",
    id: "b8dc71b2-c5bb-3a22-845d-ec6053397e1a",
    addressLine: "161 EASTERN AVE",
    addressCity: "LYNN"
};


const patientIds = ['aaron-brekke']

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
            // Array of the objects
            const objects = [condition, patient, organization];

            // Select a random object from the array
            const randomObj = objects[Math.floor(Math.random() * objects.length)];

            console.log("records", msg)
            setTranscript(prev => [...prev, { message: JSON.stringify(randomObj, null, 2), source: 'medicalData' }])
        }

        socket.on('connect', onConnect);
        socket.on('disconnect', onDisconnect);
        socket.on('server-msg', onServerMsg);
        socket.on('records', onRecords);

        console.log("connecting")

            const timerId = setTimeout(() => {
                const objects = [condition, patient, organization];
                const randomObj = objects[Math.floor(Math.random() * objects.length)];
                console.log("sending", randomObj)
                onRecords({
                    type: 'medicalData',
                    message: randomObj,
                });
            }, 2000);

        return () => {
            console.log("Disconnecting")
            socket.off('connect', onConnect);
            socket.off('disconnect', onDisconnect);
            socket.off('server-msg', onServerMsg);
            socket.off('records', onRecords);
            clearTimeout(timerId);
        };
    }, []);
    return [isConnected, transcript, setTranscript]
}

function App() {
    const [isSending, setIsSending] = useState(false);
    const [selectedPatient, setSelectedPatient] = useState<string | null>(null);
    const [isChatStarted, setIsChatStarted] = useState(false);
    const [isConnected, transcript, setTranscript] = useSocket(setIsSending) as [boolean, TranscriptEntry[], React.Dispatch<React.SetStateAction<TranscriptEntry[]>>];
    function startChat(patientId: string) {
        setSelectedPatient(patientId);
        socket.emit('start-chat', patientId);
        console.log("selected", patientId)
        setIsChatStarted(true);
    }

    function onSubmit(data: FormData) {
        setIsSending(true);
        const chatMsg = data.chatInput;
        setTranscript(prev  => [...prev, { message: chatMsg, source: 'client' }]);
        socket.emit('client-msg', chatMsg);
        form.reset({chatInput: ""});
    }

    const form = useForm<FormData>();

    return (
        <div className="h-[94vh] flex flex-col">
            <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
                <p className='hidden'>{isConnected ? "Connected" : "Not Connected"}</p>
                <p className='hidden'>{isChatStarted ? "Chat Started" : "Chat Not Started"}</p>
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
                                const data = JSON.parse(entry.message);
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
