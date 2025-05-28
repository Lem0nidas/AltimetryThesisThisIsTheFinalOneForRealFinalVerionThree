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
