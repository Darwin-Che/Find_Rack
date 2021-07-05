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
        populate_movie_dropdown(result);
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
        outText = "Logged in, JWT token is: " + result. token;
        sessionStorage.setItem("JWT_token", result.token);
    } catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

async function create_list(element) {
    const listname = document.getElementById("create_list_name");
    const token = sessionStorage.getItem("JWT_token");
    try {
        const result = await post('/api/lists', {
            listname: listname.value,
            token: token
        });
        outText = "Created list: " + listname.value + "\nid: " + result.listid;
    }   catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

function populate_list_dropdown(result) {
    selector = document.getElementById("list_selector")
    Object.keys(result).forEach((k) => {
        const option = document.createElement("option");
        option.text = result[k]['name']
        option.value = k
        selector.add(option)
    })
}

function populate_movie_dropdown(result) {
    selector = document.getElementById("movie_selector")
    result.forEach((r) => {
        const option = document.createElement("option");
        option.text = r[1]
        option.value = r[0]
        selector.add(option)
    })
}

async function get_personal_lists(element) {
    const token = sessionStorage.getItem("JWT_token");
    try {
        const result = await get('/api/lists', {
            token: token
        });
        populate_list_dropdown(result)
        outText = JSON.stringify(result);
    }   catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

async function add_to_list(element) {
    const listid = document.getElementById('list_selector').value;
    const titleid = document.getElementById('movie_selector').value;
    try {
        await post('/api/list-add', {
            listid: listid,
            titleid: titleid,
        });
        outText = `Added title:${titleid} to list:${listid}`;
    }   catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}
