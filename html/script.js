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
    const newElement = document.createElement('pre');
    newElement.textContent = result;
    setResultElement(element, newElement);
}

function setResultElement(element, newElement) {
    newElement.classList.add('out');
    element.parentElement.querySelector(".out").replaceWith(newElement);
}

function format_movies(element, results) {
    const newElement = document.createElement('table');
    newElement.classList.add('data-table');
    newElement.innerHTML = '<tr><th>Title</th><th>Release year</th><th>Runtime (mins)</th><th>Summary</th><th></th></tr>';
    if(results.length <= 0) {
        setResult(element, "No results found!");
    } else {
        for(const result of results) {
            const row = document.createElement('tr');
            row.dataset.titleid = result[0];
            const titleCell = document.createElement('td');
            titleCell.textContent = result[1];
            row.appendChild(titleCell);
            const releaseYearCell = document.createElement('td');
            releaseYearCell.textContent = result[2];
            row.appendChild(releaseYearCell);
            const runtimeCell = document.createElement('td');
            runtimeCell.textContent = result[3];
            row.appendChild(runtimeCell);
            const summaryCell = document.createElement('td');
            summaryCell.textContent = result[4];
            row.appendChild(summaryCell);
            newElement.appendChild(row);
        }
    }
    setResultElement(element, newElement);
}

async function query_movies(element) {
    const titleInput = document.getElementById("query_movies_title");
    const castInput = document.getElementById("query_movies_cast");
    const releaseYearInput = document.getElementById("query_movies_release_year");
    const minRuntimeInput = document.getElementById("query_movies_min_runtime");
    const maxRuntimeInput = document.getElementById("query_movies_max_runtime");
    const params = {};
    if(titleInput.value.length > 0) {
        params.title = titleInput.value;
    }
    if(castInput.value.length > 0) {
        params.cast = castInput.value;
    }
    if(releaseYearInput.value.length > 0) {
        params.releaseyear = releaseYearInput.value;
    }
    if(minRuntimeInput.value.length > 0) {
        params.minruntime = minRuntimeInput.value;
    }
    if(maxRuntimeInput.value.length > 0) {
        params.maxruntime = maxRuntimeInput.value;
    }
    setResult(element, "Loading...");
    try {
        if(Object.keys(params).length <= 0)
            throw new Error('Please use at least one filter.');
        const results = await get('/api/movies', params);
        populate_movie_dropdown(results);
        format_movies(element, results);
    } catch(e) {
        setResult(element, "Error: " + e.message);
    }
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
    for(const selector of document.getElementsByClassName("movie-selector")) {
        selector.replaceChildren(); // Clear old entries
        result.forEach((r) => {
            const option = document.createElement("option");
            option.text = r[1]
            option.value = r[0]
            selector.add(option)
        })
    }
}

async function get_personal_lists(element) {
    const token = sessionStorage.getItem("JWT_token");
    if(token != null) {
        try {
            const userid = jwt_decode(token).userid;
            const lists = await get_lists_internal(element, {userid});
            populate_list_dropdown(lists)
            format_lists(element, lists, true, false);
            return;
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
        const lists = await get_lists_internal(element, {userid: userid.value});
        format_lists(element, lists, false, false);
        return;
    } catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

async function get_lists_by_name(element) {
    const name = document.getElementById("get_lists_name");
    try {
        const lists = await get_lists_internal(element, {name: name.value});
        format_lists(element, lists, false, true);
        return;
    } catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

async function get_lists_internal(element, options) {
    const token = sessionStorage.getItem("JWT_token");
    return await get('/api/lists', { ...options, token });
}

function format_lists(element, lists, own, showOwner) {
    if(lists.length <= 0) {
        setResult(element, "No results found!");
    } else {
        const newElement = document.createElement('table');
        newElement.classList.add('data-table');
        if(showOwner) newElement.classList.add('show-owner');
        newElement.innerHTML = '<tr><th></th><th>List</th><th class="shown-owner">Creator</th><th>Titles</th></tr>';
        for(const listid of Object.keys(lists)) {
            const list = lists[listid];

            const row = document.createElement('tr');
            row.dataset.listid = listid;
            row.dataset.subscribed = list.subscribed;
            const subCell = document.createElement('td');
            if(!own) {
                const subBtn = document.createElement('button');
                subBtn.textContent = list.subscribed ? 'Unsubscribe' : 'Subscribe';
                subBtn.onclick = async () => {
                    const token = sessionStorage.getItem("JWT_token");
                    try {
                        await post('/api/subscriptions', {
                            token,
                            listid: row.dataset.listid,
                            subscribe: row.dataset.subscribed == 'false'
                        });
                    } catch(e) {
                        alert('Operation failed, error: ' + e.message);
                    }
                    get_lists(element);
                };
                subCell.appendChild(subBtn);
            }
            row.appendChild(subCell);
            const listNameCell = document.createElement('td');
            listNameCell.textContent = list.name;
            row.appendChild(listNameCell);
            const listOwnerCell = document.createElement('td');
            listOwnerCell.className = 'shown-owner';
            listOwnerCell.textContent = list.username;
            row.appendChild(listOwnerCell);
            const titlesCell = document.createElement('td');
            const titlesList = document.createElement('ul');
            for(const title of list.titles) {
                const titleElement = document.createElement('li');
                titleElement.textContent = title;
                titlesList.appendChild(titleElement);
            }
            titlesCell.appendChild(titlesList);
            row.appendChild(titlesCell);

            newElement.appendChild(row);
        }
        setResultElement(element, newElement);
    }

    /*let out = `${Object.values(lists).length} list(s) were found:\n\n`;
    for(const list of Object.values(lists)) {
        out += `${list.name} (contains ${list.titles.length} movies):\n`;
        for(const title of list.titles) {
            out += `- ${title}\n`;
        }
        out += "\n";
    }
    return out;*/
}

async function add_to_list(element) {
    const listid = document.getElementById('add_to_list_list_selector').value;
    const titleid = document.getElementById('add_to_list_movie_selector').value;
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

async function add_comment(element) {
    const comment = document.getElementById('add_comment_comment').value;
    const titleid = document.getElementById('add_comment_movie_selector').value;
    const token = sessionStorage.getItem("JWT_token");
    try {
        const result = await post('/api/comments', {
            token,
            titleid,
            comment
        });
        outText = `Added comment, ID is: ${result.commentid}`;
    }   catch(e) {
        outText = "Error: " + e.message;
    }
    setResult(element, outText);
}

async function view_comments(element) {
    const titleid = document.getElementById('view_comments_movie_selector').value;
    try {
        const comments = await get('/api/comments', { titleid });
        const newElement = document.createElement('table');
        newElement.classList.add('data-table');
        newElement.innerHTML = '<tr><th>User</th><th>Comment</th></tr>';
        if(comments.length <= 0) {
            setResult(element, "No results found!");
        } else {
            for(const result of comments) {
                const row = document.createElement('tr');
                const userCell = document.createElement('td');
                userCell.textContent = result[1];
                row.appendChild(userCell);
                const commentCell = document.createElement('td');
                commentCell.textContent = result[0];
                row.appendChild(commentCell);
                newElement.appendChild(row);
            }
        }
        setResultElement(element, newElement);
    } catch(e) {
        setResult(element, "Error: " + e.message);
    }
}

async function suggest_movie(element) {
    const movie_selector = document.getElementById('suggest_movie_genre_selector');
    const genre = movie_selector.value;
    try {
        const result = await post('/api/suggest', {genre});
        format_movies(element, [result]);
    } catch(e) {
        setResult(element, "Error: " + e.message);
    }
}

function populate_genre_selector(result) {
    for(const selector of document.getElementsByClassName("genre-selector")) {
        selector.replaceChildren(); // Clear old entries
        result.forEach((r) => {
            const option = document.createElement("option");
            option.text = r;
            option.value = r;
            selector.add(option);
        })
    }
}

async function setup_genre_selector() {
    try {
        const genres = await get('/api/genres');
        genres.sort();
        populate_genre_selector(genres);
    } catch(e) {
        alert('Error loading genres!');
        console.error('Error loading genres.', e);
    }
}

setup_genre_selector();

function checkLogin() {
    if (sessionStorage.getItem("JWT_token")) {
        console.log("yoo")
        const label = document.getElementById('signin');
        const href = document.getElementById('signin-link');
        var username = sessionStorage.getItem("username");
        label.innerHTML = `Logged in as ${username}`;
        href.removeAttribute("href");
        href.innerHTML = "Sign Out";
        href.onclick = () => {
            sessionStorage.removeItem("JWT_token");
            sessionStorage.removeItem("userid");
            sessionStorage.removeItem("username");
            window.location.replace("/home.html")
        }
        return true;
    }
    return false;
}

function deleteChild(e) {
    var child = e.lastElementChild; 
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
}

function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    console.log('Query variable %s not found', variable);
}