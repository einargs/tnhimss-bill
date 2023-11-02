import dayjs from 'dayjs';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card.tsx";

function Condition({ medicalData }: any ) {
    console.log("condition", medicalData)

    return (
        <Card className='w-[370px]'>
            <CardHeader>
                <CardTitle>Condition Information</CardTitle>
                {/*<CardDescription>{medicalData.conditioncode}</CardDescription>*/}
            </CardHeader>
            <CardContent>
                <p><strong>Condition Code:</strong> {medicalData.conditioncode}</p>
                {/*<p><strong>Type:</strong> {medicalData.type}</p>*/}
                <p><strong>Recorded Date:</strong> {dayjs(medicalData.recordeddata).format('MM/DD/YYYY')}</p>
                <p><strong>Verification Status:</strong> {medicalData.verificationstatus}</p>
                <p><strong>Onset Date:</strong> {dayjs(medicalData.onsetdate).format('MM/DD/YYYY')}</p>
            </CardContent>
            {/*<CardFooter>*/}
            {/*    <p>Condition ID: {medicalData.id}</p>*/}
            {/*</CardFooter>*/}
        </Card>
    )
}

export default Condition;
