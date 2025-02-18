const url = 'http://localhost:5000/login'
const login = document.getElementById('login')
const username = document.getElementById('username')
const password = document.getElementById('password')
const toggle = document.getElementById('toggle')

login.addEventListener('submit', async (e) => {
    e.preventDefault()

    const data = {
        username: username.value,
        password: password.value
    }

    const result = await sendRequest(url, 'POST', data)
    if (result.message == 'success'){
        window.location.href = 'homepage.html'
    }
})

toggle.addEventListener('click', ()=>{
    if(password.type == 'password'){
        password.type = 'text'
        toggle.textContent = 'hide password'
    } else {
        password.type = 'password'
        toggle.textContent = 'show password'
    }
})
