const sendRequest = async (url, method = 'GET', body = null) => {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    }

    if (body) {
        options.body = JSON.stringify(body)
    }

    try {
        const response = await fetch(url, options)
        const result = await response.json()

        return result
    } catch (error) {
        console.log('Error:', error)
    }
}