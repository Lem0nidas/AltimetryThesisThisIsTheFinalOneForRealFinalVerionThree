export async function processedDownload(satellite: string): Promise<string> {
    const response = await fetch(`http://localhost:8000/api/download_processed`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ satellite }),
    });

    if (!response.ok) {
        throw new Error(`Failed to download data for ${satellite}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.message || 'Satellite Request sent!';
}