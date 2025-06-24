export async function requestDownload(satellite: string, cycle: string, pass: string): Promise<string> {
    const response = await fetch(`http://localhost:8000/api/download`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({ satellite, cycle_num: cycle , pass_num: pass }),
    });

    if (!response.ok) {
        throw new Error(`Failed to download data for ${satellite}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.message || 'Satellite Request sent!';
}

