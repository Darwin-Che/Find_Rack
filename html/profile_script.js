document.addEventListener("DOMContentLoaded", async function() {
    loggedIn = checkLogin();
    userid = sessionStorage.getItem("userid");
    username = await get('/api/username', {userid})
    const lists = await get_lists_internal(null, {userid});
    const s_lists = await get_lists_internal(null, {subscribed:true});
    const subs = document.getElementById("subscribed-lists");
    const l = document.getElementById("my-lists");
    formatLists(l, lists, 0);
    formatLists(subs, s_lists, 1);
});

async function del_list(listid) {
    const token = sessionStorage.getItem("JWT_token");
    try {
        await post('/api/list-delete', { listid, token });
        document.getElementById(listid).remove();
    }   catch(e) {
        alert("Error " + e.message);
    }
}

async function unsub_list(key) {
    try {
        await post('/api/subscriptions', {
            token: sessionStorage.getItem("JWT_token"),
            listid: key,
            subscribe: false
        });
        document.getElementById(key).remove()
    } catch(e) {
        alert('Operation failed, error: ' + e.message);
    }
}

async function rmlist(key, titleid) {
    try {
        await post('/api/list-add', {
            listid: key,
            titleid: titleid,
            delete: true
        }); 
        let child = document.getElementById(`${key}-${titleid}`);
        let parent = child.parentElement;
        child.remove();
        if (!parent.hasChildNodes()) {
            let elem = document.createElement("h5");
            elem.setAttribute("onclick", `del_list('${key}')`);
            elem.innerHTML = "Delete";
            parent.replaceWith(elem);
        }
    }   catch(e) {
       alert("Error: " + e.message);
    }
}

async function create_list() {
    const listname = document.getElementById("create_list_name");
    const token = sessionStorage.getItem("JWT_token");
    try {
        const result = await post('/api/lists', {
            listname: listname.value,
            token: token
        });
        const div = document.createElement("div")
        div.setAttribute("id", result.listid)
        div.innerHTML = `<div class="mvl"><h3>${listname.value}</h3></div><h5 onclick="del_list('${result.listid}')">Delete</h5><ul></ul>`
        //outText = "Created list: " + listname.value + "\nid: " + result.listid;
        document.getElementById("my-lists").appendChild(div)
    }   catch(e) {
        alert("Error: " + e.message);
    }
}
