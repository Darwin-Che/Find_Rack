function formatLists(elem, result, type) {
    Object.keys(result).forEach(key => {
        const div = document.createElement("div")
        div.setAttribute("id", key)
        x = ""
        for (let i = 0; i < result[key]['titles'].length; ++i) {
            x += `<li class="mvl" id="${key}-${result[key]['titles'][i]}"><a href="/movie.html?m=${result[key]['titles'][i]}">${result[key]['titlenames'][i]}</a>${type == 0 ? `<label class="btn" onclick="rmlist('${key}','${result[key]['titles'][i]}')">X</label>` : ""}</li>`
        }
        div.innerHTML = `<h3>${result[key]['name']}</h3>${
            x.length == 0 && type == 0 ? `<h5 onclick="del_list('${key}')">Delete</h5>` : ""
        }${
            type == 1 ? `<h5 onclick="unsub_list('${key}')">Unsubscribe</h5>` : ""
        }<ul>${x}</ul>`
        elem.append(div);
        console.log(result[key]['name'])
    })
};

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