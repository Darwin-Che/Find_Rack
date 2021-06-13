async function get(endpoint, params) {
    const result = await fetch(endpoint + '?' + new URLSearchParams(params).toString());
    if(result.ok) {
        return await result.json();
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

    return await result.json();
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
    let outText;
    try {
        if(usernameInput.value.length <= 0) throw new Error('Missing username!');
        const result = await post('/api/users', {username: usernameInput.value});
        if(result.ok) {
            outText = "User created, userid is: " + result.userid;
        } else {
            throw new Error('Bad HTTP status code!');
        }
    } catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}
