async function create_user_fe(element) {
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
        alert(outText);
    } catch(e) {
        alert("Error: " + e.message);
    }
}

async function login_fe(element) {
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
        sessionStorage.setItem("username", usernameInput.value);
        sessionStorage.setItem("userid", jwt_decode(token).userid);
        window.location.assign("/home.html");
    } catch(e) {
        alert("Error: " + e.message);
    }
}
