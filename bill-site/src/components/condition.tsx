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
                <p><strong>Condition Code:</strong> {medicalData.description}</p>
                <p><strong>Clinical Status:</strong> {medicalData.clinical_status}</p>
                <p><strong>Recorded Date:</strong> {dayjs(medicalData.recorded_date).format('MM/DD/YYYY')}</p>
                <p><strong>Onset Date:</strong> {dayjs(medicalData.onset_date).format('MM/DD/YYYY')}</p>
            </CardContent>
            {/*<CardFooter>*/}
            {/*    <p>Condition ID: {medicalData.id}</p>*/}
            {/*</CardFooter>*/}
        </Card>
    )
}

export default Condition;
