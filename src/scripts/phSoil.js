const url = 'http://localhost:5000/data'
const soil = document.getElementById('soil')
const ph = document.getElementById('ph')

const data = async ()=>{
    const result = await sendRequest(url)

    soil.textContent = result.humidity
    ph.textContent = result.ph
}

setInterval(data, 1000)