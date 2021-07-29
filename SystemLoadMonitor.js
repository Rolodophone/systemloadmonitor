function handleResponse() {
    console.debug(`Response received: ${this.responseText}`)

    load = JSON.parse(this.responseText)

    const cpu_core_percents = document.getElementById("cpu_core_percents")
    if (cpu_core_percents.innerHTML == "") { //first refresh
        console.debug("Adding new CPU core percents elements.")
        for (i = 0; i < load.cpu_core_percents.length; i++) {
            cpu_core_percents.insertAdjacentHTML("beforeend",
                `<p>CPU ${i+1}: <strong><span id="cpu_core_percent${i}">${load.cpu_core_percents[i].toFixed(1)}</span>%</strong></p>`
            )
        }
    }
    else { //not first refresh
        console.debug("Refreshing CPU core percents elements.")
        for (i = 0; i < load.cpu_core_percents.length; i++) {
            document.getElementById(`cpu_core_percent${i}`).innerHTML = load.cpu_core_percents[i].toFixed(1)
        }
    }

    const memory_used = document.getElementById("memory_used")
    memory_used.innerHTML = load.memory_used

    const memory_total = document.getElementById("memory_total")
    memory_total.innerHTML = load.memory_total

    const memory_percent = document.getElementById("memory_percent")
    memory_percent.innerHTML = load.memory_percent.toFixed(1)

    console.debug("Refreshed.")
}

function sendRefreshRequest() {
    const xhttp = new XMLHttpRequest()
    xhttp.onload = handleResponse
    xhttp.open("GET", "systemload.json")
    xhttp.setRequestHeader('If-Modified-Since', null)
    xhttp.send()
    console.debug("Sent refresh request.")

    //schedule next refresh
    refresh_rate = document.getElementById("refresh_rate").value
    window.setTimeout(sendRefreshRequest, refresh_rate * 1000)
    console.debug(`Scheduled another refresh request in ${refresh_rate} second(s).`)
}

sendRefreshRequest()