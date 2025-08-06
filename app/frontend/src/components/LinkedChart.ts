import { LitElement, html, css } from 'lit';
import {Chart} from "chart.js";

class LinkedCharts extends LitElement {
  static styles = css`
    .chart-container {
      display: flex;
      flex-direction: column;
      gap: 2rem;
      max-width: 100%;
    }
    canvas {
      max-width: 100%;
      height: 300px;
    }
  `;

  constructor() {
    super();
    this.chart1 = null;
    this.chart2 = null;
    this.chartData = [];
  }

  render() {
    return html`
      <div class="chart-container">
        <canvas id="chart1"></canvas>
        <canvas id="chart2"></canvas>
      </div>
    `;
  }

  async firstUpdated() {
    // Fetch data from backend API
    try {
      const response = await fetch('/data/');
      this.chartData = await response.json();
    } catch (err) {
      console.error('Error fetching chart data', err);
      return;
    }
    // Prepare data for Chart.js (labels and values)
    const labels = this.chartData.map(dp => new Date(dp.timestamp));
    const values = this.chartData.map(dp => dp.value);
    // Base Chart.js configuration (line chart with one dataset)
    const config = {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Wartość',
          data: values,
          fill: false,
          borderColor: 'blue',
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'time',
            time: { unit: 'day' },
            title: { display: true, text: 'Data' }
          },
          y: {
            title: { display: true, text: 'Wartość' }
          }
        },
        plugins: {
          zoom: {
            pan: { enabled: true, mode: 'x' },
            zoom: {
              wheel: { enabled: true },
              pinch: { enabled: true },
              mode: 'x',
              onZoomComplete: ({chart}) => {
                // Sync zoom range between charts
                try {
                  const meta = chart.scales.x;
                  const min = meta.min;
                  const max = meta.max;
                  if (chart === this.chart1 && this.chart2) {
                    this.chart2.config.options.scales.x.min = min;
                    this.chart2.config.options.scales.x.max = max;
                    this.chart2.update('none');
                  } else if (chart === this.chart2 && this.chart1) {
                    this.chart1.config.options.scales.x.min = min;
                    this.chart1.config.options.scales.x.max = max;
                    this.chart1.update('none');
                  }
                } catch(e) {
                  console.error('Zoom sync error:', e);
                }
              }
            }
          }
        }
      }
    };
    // Initialize two Chart.js instances
    const ctx1 = this.renderRoot.getElementById('chart1').getContext('2d');
    const ctx2 = this.renderRoot.getElementById('chart2').getContext('2d');
    this.chart1 = new Chart(ctx1, config);
    // Deep clone config for second chart to avoid shared state
    const config2 = JSON.parse(JSON.stringify(config));
    this.chart2 = new Chart(ctx2, config2);
  }
}
customElements.define('linked-charts', LinkedCharts);
