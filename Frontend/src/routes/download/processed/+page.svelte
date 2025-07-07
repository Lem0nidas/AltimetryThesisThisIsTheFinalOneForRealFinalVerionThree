<script lang="ts">
    import type { RADSVariable } from "$lib/data/variables";
    import type { RADSSatellite } from "$lib/data/satellites";
    import { variables } from "$lib/data/variables";
    import { satellites } from "$lib/data/satellites";
    import { X } from "@lucide/svelte";
    import Map from "$lib/components/Map.svelte";
    import { processedDownload } from "$lib";
    
    let { children } = $props()

    let selectedSatellite: RADSSatellite = $state({name: '', code: ''});
    let selectedVariable: RADSVariable | null = $state(null);
    let listBoxItems: string[] = $state([]);

    let messages = $state({
        response: '',
        error: '',
        download: '',
        custom: '',
        date: '',
    })


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

        if (!selectedSatellite) {
            messages.response = 'Please select a satellite'
        }

        try {
            messages.response = await processedDownload(selectedSatellite.code);
        } catch (err) {
            messages.error = 'Error contacting server.',
            console.log(err)
        }
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
                <option value={sat}>{sat.name}</option>
            {/each}
        </select>
    </fieldset>

    <fieldset>
        <label for="listbox">Selected Items:</label>
        <div class="listbox-wrapper">
            <ul id="listbox">
                {#each listBoxItems as items, index }
                    <li>
                        <span>{items}</span>
                        <button
                            id="removeButton"
                            onclick={() => removeFromList(index)}
                            aria-label="Remove item"
                        >
                            <X size={16} />
                        </button>
                    </li>
                {/each}
            </ul>
        </div>

        <label for="variables">Pick variables to calculate</label>
        <select name="variables" id="variables" bind:value={selectedVariable}>
            <option value={null} disabled selected>Select any amount</option>
            {#each variables as variable (variable.varName)}
                <option value={variable} onclick={addToList}>{variable.name}</option>
            {/each}
        </select>
    </fieldset>

    <fieldset>
        <button type="submit">Submit</button>
    </fieldset>
</form>

<Map />

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
        display: flex;
        flex-wrap: wrap;
        gap: 0.2em;
        max-height: 250px;
        overflow-y: auto;
        list-style: none;
        padding: 0;
        margin: 0.2rem;
    }

    ul#listbox li {
        display: flex;
        align-items: center;
        padding: 0.3rem 0.6rem;
        border: 1px solid #eee;
        border-radius: 25px;
        font-size: medium;
        width: fit-content;
    }

    ul#listbox li:hover {
        background-color: #ffffff0a;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.4);
        cursor: default;
    }

    button#removeButton {
        font-size: 1rem;
        line-height: 1;
        padding: 0;
        margin-left: 0.5rem;
        background: none;
        border: none;
        color: rgb(17, 17, 17);
        cursor: pointer;
        transition: transform 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    button#removeButton:hover {
        transform: rotate(90deg);
        color: red;
    }

    .listbox-wrapper {
        height: 270px;
        border: 1px solid #2a3140;
        border-radius: 20px;
        background-color: #1c212c;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
        margin-bottom: 1rem;
    }
</style>

{@render children?.()}