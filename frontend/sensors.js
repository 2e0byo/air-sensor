const baseUrl = new URL("https://iot.2e0byo.co.uk");
const sensorsUrl = new URL("sensors", baseUrl);
const valuesUrl = new URL("values", baseUrl);
const decimatedUrl = new URL("decimated-values", baseUrl);

const graphs = document.getElementById("graph-container");
const nav = document.getElementById("menu");
const githubMenuItem = document.getElementById("github-menu-item");

async function getSensors() {
    const resp = await fetch(sensorsUrl);
    return resp.json();
}

const canvasId = (id) => `canvas-${id}`;

const createCard = (obj, data) => {
    const section = document.createElement("section");
    const div = document.createElement("div");
    div.className = "card";
    div.id = obj.uniq_id;
    const header = `
<header>
<div class="row is-marginless">
  <div class="col-8 is marginless">
     <h4>${obj.name}</h4>
  </div>
  <div class="col-4 text-right">(${obj.uniq_id})</div>
`;
    div.innerHTML = header;

    const contents = document.createElement("div");
    const canvas = document.createElement("canvas");
    canvas.id = canvasId(obj.uniq_id);
    contents.appendChild(canvas);
    div.appendChild(contents);
    console.log(data);

    const chart = new Chart(canvas, {
        type: "line",
        data: {
            datasets: [{
                label: obj.name,
                data: data,
                parsing: {
                    xAxisKey: "timestamp",
                    yAxisKey: "value"
                }
            }]
        },
        options: {
            scales: {
                x: {
                    type: "time",
                    time: {
                    }
                }
            }
        }
    });

    section.appendChild(div);
    return section;
}

const createLink = (id, title) => {
    const a = document.createElement("a");
    a.href = `#${id}`;
    a.innerHTML = title;
    return a;
}

async function getData(sensor_id, start, end, n=100) {
    const resp = await fetch(new URL(`?sensor_id=${sensor_id}&start=${start}&end=${end}&n=${n}`, decimatedUrl));
    return resp.json();
}

async function addSection(sensor) {
    const WindowStartSeconds = 60*60*24*14;
    console.log(sensor);
    const initialData = await getData(sensor.uniq_id, Date.now() - WindowStartSeconds, Date.now());
    console.log(initialData);
    const card = createCard(sensor, initialData);
    graphs.appendChild(card);
    nav.insertBefore(createLink(sensor.uniq_id, sensor.name), githubMenuItem);
}

async function onLoad() {
    const sensors = await getSensors();
    console.log(sensors);
    await Promise.all(sensors.map(s => addSection(s)));
}

window.addEventListener("load", onLoad);
