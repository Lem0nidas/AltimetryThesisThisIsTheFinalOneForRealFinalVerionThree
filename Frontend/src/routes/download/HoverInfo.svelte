<!-- TODO Update the Hover Info for each button. Add images -->
<script lang="ts">
    import { fade } from "svelte/transition";

    let { currentInfo } = $props();

    const rawText = `
        Lorem ipsum dolor sit, amet consectetur adipisicing elit. 
        Provident id, corrupti quisquam consequuntur obcaecati et libero temporibus, 
        consectetur necessitatibus harum placeat, 
        voluptate qui ratione illum ab ea impedit molestiae alias.
    `;

    const processedText = `
        Lorem ipsum dolor sit, amet consectetur adipisicing elit. 
        Provident id, corrupti quisquam consequuntur obcaecati et libero temporibus, 
        consectetur necessitatibus harum placeat, 
        voluptate qui ratione illum ab ea impedit molestiae alias.
    `;
</script>

<div class="info-box">
    {#if currentInfo === 'raw'}
        <div class="info-text-wrapper" transition:fade={{ duration: 500 }}>
            <h2>Raw altimetry Data</h2>
            <p>{rawText}</p>
        </div>
    {:else if currentInfo === 'processed'}
        <div class="info-text-wrapper" transition:fade={{ duration: 500 }}>
            <h2>Processed Alitimetry Data</h2>
            <p>{processedText}</p>
        </div>
    {/if}
</div>

<style>
    .info-box {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .info-text-wrapper {
        width: 50%;
        margin-top: 0.5rem;
        padding: 0.5rem 1rem;
        background-color: #1c1f26;
        border-radius: 4px;
        font-size: 0.9rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }

    h2 {
        text-align: center;
    }

    p {
        text-align: center;
        font-style: italic;
        color: white
    }
</style>