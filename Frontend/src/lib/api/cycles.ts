export async function requestCycles(satellite: string) {
    const response = await fetch ('http://localhost:8000/api/get_cycles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ satellite })
    });

    if (!response.ok) {
        throw new Error(`Failed to get the cycles for ${satellite}`);
    }

    const data = await response.json();
    return data;
}