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
