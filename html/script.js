async function get(endpoint, params) {
    const result = await fetch(endpoint + '?' + new URLSearchParams(params).toString());
    if(result.ok) {
        return await result.json();
    } else if(result.status === 500 && result.headers.get('Error-Type') === 'handled') {
        throw new Error((await result.json()).error);
    } else {
        throw new Error('Bad HTTP status code!');
    }
}

async function post(endpoint, body) {
    const result = await fetch(endpoint, {
        method: 'POST', 
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(body)
    });

    if(result.ok) {
        return await result.json();
    } else if(result.status === 500 && result.headers.get('Error-Type') === 'handled') {
        throw new Error((await result.json()).error);
    } else {
        throw new Error('Bad HTTP status code!');
    }
}

function setResult(element, result) {
    element.parentElement.querySelector(".out").textContent = result;
}

async function query_movies(element) {
    const titleInput = document.getElementById("query_movies_title");
    const params = {};
    if(titleInput.value.length > 0) {
        params.title = titleInput.value;
    }
    let outText;
    try {
        const result = await get('/api/movies', params);
        outText = "Movies:\n" + result.map(it => it[1]).join('\n');
    } catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

async function query_users(element) {
    let outText;
    try {
        const result = await get('/api/users', {});
        outText = "Users:\n" + result.map(it => `userid: ${it[0]}, username: ${it[1]}`).join('\n');
    } catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

async function create_user(element) {
    const usernameInput = document.getElementById("create_user_username");
    const passwordInput = document.getElementById("create_user_password");
    let outText;
    try {
        if(usernameInput.value.length <= 0) throw new Error('Missing username!');
        if(passwordInput.value.length <= 0) throw new Error('Missing password!');
        const result = await post('/api/users', {
            username: usernameInput.value,
            password: passwordInput.value
        });
        outText = "User created, userid is: " + result.userid;
    } catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

async function login(element) {
    const usernameInput = document.getElementById("login_username");
    const passwordInput = document.getElementById("login_password");
    let outText;
    try {
        const result = await post('/api/login', {
            username: usernameInput.value,
            password: passwordInput.value
        });
        outText = "Logged in, JWT token is: " + result.token;
    } catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}
