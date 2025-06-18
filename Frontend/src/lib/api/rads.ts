export async function requestDownload(satellite: string): Promise<string> {
    const response = await fetch(`http://localhost:8000/api/download`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({ satellite }),
    });

    if (!response.ok) {
        throw new Error(`Failed to download data for ${satellite}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.message || 'Satellite Request sent!';
}

export async function requestLatestDownload(satellite: string): Promise<string> {
    const response = await fetch(`http://localhost:8000/api/download_latest`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({ satellite }),
    });

    if (!response.ok) {
        throw new Error(`Failed to get latest data for ${satellite}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.message || 'Latest Data Request sent!';
}

export async function requestCustomDownload(satellite: string, cycle: string, pass: string = ""): Promise<string> {
    const response = await fetch('http://localhost:8000/api/download_custom', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', },
        body: JSON.stringify({ satellite, cycle_num: cycle, pass_num: pass }),
    });

    if (!response.ok) {
        throw new Error(`Failed to get the custom data for ${satellite}/c${cycle}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.message || 'Custom Data Request sent!';
}


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