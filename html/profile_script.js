document.addEventListener("DOMContentLoaded", async function() {
    loggedIn = checkLogin();
    userid = getQueryVariable('p');
    username = await get('/api/username', {userid})
    const uname = document.getElementById("username")
    uname.innerHTML = username[0];
    const lists = await get_lists_internal(null, {userid});
    console.log(lists);
});