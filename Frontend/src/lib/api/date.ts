export async function requestDateDownload(satellite: string, startDate: string = "", endDate: string = ""): Promise<string> {
    
    if (!startDate || startDate == "Start Date not selected") {
        console.warn('No date provided, skipping date download request.');
        return 'No date provided, skipping date download request.';
    }
    const response = await fetch('http://localhost:8000/api/download_date', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', },
        body: JSON.stringify({ satellite, start_date: startDate, end_date: endDate }),
    });

    if (!response.ok) {
        throw new Error(`Failed to get the data for ${satellite} on ${startDate}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.message || 'Date Data Request sent!';
}
