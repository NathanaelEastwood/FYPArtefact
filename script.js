document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('graphForm');
    const graphType = document.getElementById('graphType');
    const dataInput = document.getElementById('data');
    const graphOutput = document.getElementById('graphOutput');

    // Update placeholder based on graph type
    graphType.addEventListener('change', () => {
        if (graphType.value === 'scatter_graph') {
            dataInput.placeholder = 'Enter x,y pairs (one per line)\nExample:\n1,2\n2,4\n3,6';
        } else {
            dataInput.placeholder = 'For 1D: Enter comma-separated numbers\nExample: 1,2,3,4,5';
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        try {
            const type = graphType.value;
            const endpoint = type === 'scatter_graph' ? '/graph/get2d' : '/graph/get1d';
            
            // Parse data based on graph type
            let data;
            if (type === 'scatter_graph') {
                data = document.getElementById('data').value
                    .split('\n')
                    .filter(line => line.trim())
                    .map(line => {
                        const [x, y] = line.split(',').map(num => parseFloat(num.trim()));
                        return [x, y];
                    });
            } else {
                data = document.getElementById('data').value
                    .split(',')
                    .map(num => parseFloat(num.trim()));
            }

            // Prepare the request body
            const requestBody = {
                type: type,
                data: data,
                width: parseInt(document.getElementById('width').value),
                height: parseInt(document.getElementById('height').value),
                line_name: "something",
                configuration: {
                    x_axis_size: parseInt(document.getElementById('xAxisSize').value),
                    y_axis_size: parseInt(document.getElementById('yAxisSize').value),
                    labels: document.getElementById('labels').value
                        .split(',')
                        .map(label => label.trim())
                }
            };

            // Show loading state
            graphOutput.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';

            // Make the API call
            const response = await fetch(`http://13.41.196.253:8000${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            // Get the SVG content directly from the response
            const svgText = await response.text();
            
            // Display the SVG
            graphOutput.innerHTML = svgText;

        } catch (error) {
            console.error('Error:', error);
            graphOutput.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        }
    });
});
