import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card.tsx";

function Organization({ medicalData }: any) {

    console.log("org", medicalData)
    return (
        <Card className='w-[370px]'>
            <CardHeader>
                <CardTitle>Organization Information</CardTitle>
                {/*<CardDescription>{medicalData.name}</CardDescription>*/}
            </CardHeader>
            <CardContent>
                <p><strong>Name:</strong> {medicalData.name}</p>
                <p><strong>Organization:</strong> {medicalData.orgtype}</p>
                {/*<p><strong>Type:</strong> {medicalData.type}</p>*/}
                <p><strong>City:</strong> {medicalData.addressCity}</p>
                <p><strong>State:</strong> {medicalData.addressState}</p>
                <p><strong>ZIP:</strong> {medicalData.addressLine}</p>
            </CardContent>
            {/*<CardFooter>*/}
                {/*<p>Organization ID: {medicalData.id}</p>*/}
            {/*</CardFooter>*/}
        </Card>
    )
}

export default Organization;