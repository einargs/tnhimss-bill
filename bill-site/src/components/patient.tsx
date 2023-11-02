import {Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle} from "@/components/ui/card.tsx";
import dayjs from "dayjs";

function Patient({ medicalData }: any) {
    console.log("patient", medicalData)
    return (
        <Card className='w-[370px]'>
        <CardHeader>
                <CardTitle>Patient Information</CardTitle>
                {/*<CardDescription>{`${medicalData.fname} ${medicalData.lname}`}</CardDescription>*/}
            </CardHeader>
            <CardContent>
                <p><strong>Name:</strong> {`${medicalData.fname} ${medicalData.lname}`}</p>
                <p><strong>Birth Date:</strong> {dayjs(medicalData.birthDate).format('MM/DD/YYYY')}</p>
                <p><strong>Gender:</strong> {medicalData.sex}</p>
                <p><strong>City:</strong> {medicalData.city}</p>
                <p><strong>State:</strong> {medicalData.state}</p>
                <p><strong>ZIP:</strong> {medicalData.zip}</p>
            </CardContent>
            {/*<CardFooter>*/}
            {/*    <p>Patient ID: {medicalData.id}</p>*/}
            {/*</CardFooter>*/}
        </Card>
    )
}

export default Patient
