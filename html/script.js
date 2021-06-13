async function query_movie(element) {
    const titleInput = document.getElementById("query_movie_title");
    const params = {};
    if(titleInput.value.length > 0) {
        params.title = titleInput.value;
    }
    let outText;
    try {
        const result = await fetch('/api/movies?' + new URLSearchParams(params).toString());
        if(result.ok) {
            outText = "Movies:\n" + (await result.json()).map(it => it[1]).join('\n')
        } else {
            throw new Error('Bad HTTP status code!');
        }
    } catch(e) {
        outText = "Error: " + e.message;
    }
    element.parentElement.querySelector(".out").textContent = outText;
}

async function create_user(element) {
    const usernameInput = document.getElementById("create_user_username");
    let outText;
    try {
        if(usernameInput.value.length <= 0) throw new Error('Missing username!');
        const result = await fetch('/api/users', {
            method: 'POST', 
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                username: usernameInput.value
            }
        )});
        if(result.ok) {
            outText = "User created, userid is: " + (await result.json()).userid;
        } else {
            throw new Error('Bad HTTP status code!');
        }
    } catch(e) {
        outText = "Error: " + e.message;
    }
    element.parentElement.querySelector(".out").textContent = outText;
}
