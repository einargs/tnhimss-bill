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

type TranscriptEntry = {
    source: 'client' | 'server' | 'medicalData',
    message: string;
};
const mediacalData= {
    Condition: {
        onsetdate: "1960-10-09T06:24:57-05:00",
        pid: "urn:uuid:c698c2cc-6766-c4dd-f15a-e4b8e023c660",
        id: "4efcd5fd-e29d-85cc-30f8-0909968e140b",
        type: "Condition",
        recordeddata: "1960-10-09T06:24:57-05:00",
        verificationstatus: "confirmed",
        conditioncode: "Prediabetes",
        encref: "urn:uuid:1e8aa5b5-c92b-65cd-ff54-b893fde5410f"
    },
    Encounter: {
        provider: "urn:uuid:f569c307-dc5d-3ec7-9198-39871e1db9b1",
        encstart: "1960-10-09T06:24:57-05:00",
        encend: "1960-10-09T06:39:57-05:00",
        pid: "urn:uuid:c698c2cc-6766-c4dd-f15a-e4b8e023c660",
        id: "1e8aa5b5-c92b-65cd-ff54-b893fde5410f",
        type: "AMB",
        orgid: "urn:uuid:b8dc71b2-c5bb-3a22-845d-ec6053397e1a",
        status: "finished"
    },
    MedicationRequest: {
        requesterid: "urn:uuid:d316b4e7-87ca-3bed-8004-6521c9c6078a",
        authoredon: "1979-08-01T06:24:57-05:00",
        reasonid: "urn:uuid:b31100f3-23bd-6488-c64b-21873ba67b2c",
        codingdisplaytext: "Naproxen sodium 220 MG Oral Tablet",
        encid: "urn:uuid:8e1aab44-c0ab-e2d9-1450-be2b4f1f9599",
        pid: "urn:uuid:c698c2cc-6766-c4dd-f15a-e4b8e023c660",
        id: "0ed955c0-7b53-c827-603e-5bb146ae0267",
        codingdisplaycode: "849574",
        intent: "order",
        status: "active"
    },
    Observation: {
        obstimedate: "2010-11-28T05:24:57-06:00",
        obstext: "Body Height",
        encid: "urn:uuid:9490d6b6-7c36-0cdb-ca18-74e8d5848f46",
        obscategory: "vital-signs",
        pid: "urn:uuid:c698c2cc-6766-c4dd-f15a-e4b8e023c660",
        id: "e76733f4-0bcf-992e-01b8-d3b4442235c1",
        obscode: "cm",
        obsunit: "cm",
        obsvalue: 161.5
    },
    Organization: {
        orgtype: "Healthcare Provider",
        name: "PCP47622",
        addressState: "MA",
        id: "b8dc71b2-c5bb-3a22-845d-ec6053397e1a",
        addressLine: "161 EASTERN AVE",
        addressCity: "LYNN"
    },
    Patient: {
        zip: "01940",
        fname: "Clara",
        lname: "Carbajal",
        city: "Lynn",
        sex: "female",
        id: "c698c2cc-6766-c4dd-f15a-e4b8e023c660",
        state: "Massachusetts",
        birthDate: "1941-08-10"
    },
    Practitioner: {
        fname: "Cecilia",
        gender: "female",
        name: "Domínguez",
        id: "f569c307-dc5d-3ec7-9198-39871e1db9b1"
    },
    Procedure: {
        codingdisplaytext: "Medication Reconciliation (procedure)",
        encid: "urn:uuid:6c3ab26f-8f4e-e0ea-29cf-aeff8db30805",
        pid: "urn:uuid:c698c2cc-6766-c4dd-f15a-e4b8e023c660",
        id: "470667e4-24cc-7567-7c17-dd4bfc573b82",
        startdate: "2011-12-04T05:24:57-06:00",
        status: "completed"
    }
};


const patientIds = ['aaron-brekke']

// ! KEEP SOCKET HERE TO PREVENT RE-CONNECTIONS
// We use vite.config.ts to proxy the connection
const socket = io();

function useSocket(setIsSending: React.Dispatch<React.SetStateAction<boolean>>) {
    // const [transcript, setTranscript] = useState<string[]>([]);
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
            if (msg.type === 'medicalData') {
                setTranscript((prev) => [...prev, { message: JSON.stringify(msg, null, 2), source: 'medicalData'}])
            } else {
                console.log("server message", msg)
                setTranscript(prev => [...prev, { message: msg, source: 'server' }])
            }
            setIsSending(false);
        }


        socket.on('connect', onConnect);
        socket.on('disconnect', onDisconnect);
        socket.on('server-msg', onServerMsg)
        console.log("connecting")
        const timerId = setTimeout(() => {
            onServerMsg({
                type: 'medicalData',
                medicalData: mediacalData,
            });
        }, 2000);

        return () => {
            console.log("Disconnecting")
            socket.off('connect', onConnect);
            socket.off('disconnect', onDisconnect);
            socket.off('server-msg', onServerMsg)
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
                <ScrollArea className="h-full w-full rounded-md border p-4 mb-2 text-left space-y-4">
                    {/*{transcript.map((line, idx) =>*/}
                    {/*    <Card className={`p-4 m-2 w-fit ${idx % 2 === 0 ? 'mr-auto' : 'ml-auto'}`} key={idx}>{line}</Card>)}*/}
                    {transcript.map((entry, idx) =>
                        <Card className={`p-4 m-2 w-fit ${entry.source === 'client' ? 'mr-auto' : 'ml-auto'}`} key={idx}>{entry.message}</Card>)
                    }


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
