import type { SelectionBox } from "$lib/types";

export async function requestBox(selection: SelectionBox) {
    await fetch ('http://localhost:8000/api/map_info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(selection)
    });
}