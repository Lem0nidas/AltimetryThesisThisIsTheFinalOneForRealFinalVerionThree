import { ncDataStore } from "$lib/stores";

export async function requestNetcdf(ncFile: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', ncFile);

    const response = await fetch('http://localhost:8000/api/viewer', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error(`Failed to get the file data.`);
    }

    const data = await response.json();
    ncDataStore.set(data);
    console.log("Fetched data:", data)
    return data;
}