<script lang="ts">
    import type { RADSVariable } from "$lib/data/variables";
    import { variables } from "$lib/data/variables";

    let selectedSatellite = $state('');
    let listBoxItems: string[] = $state([]);
    let selectedVariable: RADSVariable | null = $state(null);

    let messages = $state({
        response: '',
        error: '',
        download: '',
        custom: '',
        date: '',
    })

    const satellites = [
		{ name: 'Geosat', code: 'gs' },
		{ name: 'ERS-1', code: 'e1' },
		{ name: 'TOPEX', code: 'tx' },
		{ name: 'Poseidon', code: 'pn' },
		{ name: 'ERS-2', code: 'e2' },
		{ name: 'GFO', code: 'g1' },
		{ name: 'Jason-1', code: 'j1' },
		{ name: 'Envisat', code: 'n1' },
		{ name: 'Jason-2', code: 'j2' },
		{ name: 'CryoSat-2', code: 'c2' },
		{ name: 'SARAL', code: 'sa' },
		{ name: 'Jason-3', code: 'j3' },
		{ name: 'Sentinel-3A', code: '3a' },
		{ name: 'Sentinel-3B', code: '3b' },
		{ name: 'Sentinel-6A', code: '6a' },
		{ name: 'SWOT nadir', code: 'sw' }
    ];


    function addToList() {
        if (selectedVariable && !listBoxItems.includes(selectedVariable.name)) {
            listBoxItems = [...listBoxItems, selectedVariable.name]
        }
    }

    function removeFromList(index: number) {
        listBoxItems = listBoxItems.filter((_, i) => i !== index)
    }


    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault()
    }
</script>




<h1>
    Welcome to Download Processed Data page
</h1>

<form onsubmit={handleSubmit}>
    <fieldset>
        <label for="satellite">Choose a satellite</label>
        <select id="satellite" bind:value={selectedSatellite}>
            <option value="" disabled selected>Select one</option>
            {#each satellites as sat}
                <option value={sat.code}>{sat.name}</option>
            {/each}
        </select>
    </fieldset>

    <fieldset>
        <label for=""></label>
    </fieldset>

    <fieldset>
        <label for="listbox">Selected Items:</label>
        <ul id="listbox" style="max-height: 8rem; overflow-y: auto;">
            {#each listBoxItems as items, index }
                <li style="display: flex; align-items: center; justify-content: space-between;">
                    <span>{items}</span>
                    <button
                        onclick={() => removeFromList(index)}
                        style="margin-left: 0.5rem; background: none; border: none; color: red; cursor: pointer;" 
                        aria-label="Remove item"
                    >
                        &times;
                    </button>
                </li>
            {/each}
        </ul>

        <label for="variables">Pick variables to calculate</label>
        <select name="variables" id="variables" bind:value={selectedVariable}>
            <option value={null} disabled selected>Select any amount</option>
            {#each variables as variable (variable.varName)}
                <option value={variable} onclick={addToList}>{variable.name}</option>
            {/each}
        </select>
        
    </fieldset>
</form>




<style>
    form {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        border-radius: 10px;
        background-color: #1c1f26;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
    }

    h1 {
        text-align: center;
        margin-top: 1.5rem;
        color: white;
    }

    fieldset {
        border: none;
        margin-bottom: 1.5rem;
    }

    ul#listbox {
        list-style: none;
        padding: 0;
        margin: 0.5rem 0;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    ul#listbox li {
        padding: 0.3rem 0.6rem;
        border-bottom: 1px solid #eee;
    }
    ul#listbox li:last-child {
        border-bottom: none;
    }

</style>