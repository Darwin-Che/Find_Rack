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
    const castInput = document.getElementById("query_movies_cast");
    const params = {};
    if(titleInput.value.length > 0) {
        params.title = titleInput.value;
    }
    if(castInput.value.length > 0) {
        params.cast = castInput.value;
    }
    let outText;
    setResult(element, "Loading...");
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
        const token = result.token;
        outText = `Logged in, JWT token is: ${token}, user id: ${jwt_decode(token).userid}`;
        sessionStorage.setItem("JWT_token", token);
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
    for(const selector of document.getElementsByClassName("list-selector")) {
        selector.replaceChildren(); // Clear old entries
        Object.keys(result).forEach((k) => {
            const option = document.createElement("option");
            option.text = result[k]['name']
            option.value = k
            selector.add(option)
        })
    }
}

function populate_movie_dropdown(result) {
    selector = document.getElementById("movie_selector")
    selector.replaceChildren(); // Clear old entries
    result.forEach((r) => {
        const option = document.createElement("option");
        option.text = r[1]
        option.value = r[0]
        selector.add(option)
    })
}

async function get_personal_lists(element) {
    const token = sessionStorage.getItem("JWT_token");
    if(token != null) {
        try {
            const userid = jwt_decode(token).userid;
            const lists = await get_lists_internal(element, userid);
            populate_list_dropdown(lists)
            outText = format_lists(lists);
        } catch(e) {
            outText = "Error: " + e.message;
        }
    } else {
        outText = "You must be logged in!";
    }
    setResult(element, outText);
}

async function get_lists(element) {
    const userid = document.getElementById("get_lists_userid");
    try {
        const lists = await get_lists_internal(element, userid.value);
        outText = format_lists(lists);
    } catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

async function get_lists_internal(element, userid) {
    return await get('/api/lists', { userid });
}

function format_lists(lists) {
    let out = `${Object.values(lists).length} list(s) were found:\n\n`;
    for(const list of Object.values(lists)) {
        out += `${list.name} (contains ${list.titles.length} movies):\n`;
        for(const title of list.titles) {
            out += `- ${title}\n`;
        }
        out += "\n";
    }
    return out;
}

async function add_to_list(element) {
    const listid = document.getElementById('add_to_list_list_selector').value;
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

async function delete_list(element) {
    const listid = document.getElementById('delete_list_list_selector').value;
    const token = sessionStorage.getItem("JWT_token");
    try {
        await post('/api/list-delete', { listid, token });
        outText = `Deleted list: ${listid}`;
    }   catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}
