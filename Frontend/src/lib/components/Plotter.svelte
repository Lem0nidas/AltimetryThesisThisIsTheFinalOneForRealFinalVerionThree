<script lang="ts">
    import { onMount } from "svelte";
    import Plotly from "plotly.js-dist";
    
    
    let { xTime, yData, name, units } = $props();
    let x = xTime;
    let y = yData;
    let plotDiv: HTMLDivElement;

    const layout = {
        title: name,
        xaxis: { title: 'Time' },
        yaxis: { title: `${name} (${units})` }
    }

    onMount(() => {
        Plotly.newPlot(plotDiv, [
            {
                x: x,
                y: y,
                type: "scatter",
                mode: "lines+markers",

            }
        ], layout)
    })

</script>

<div bind:this={plotDiv} style="width: 100%; height: 400px;"></div>