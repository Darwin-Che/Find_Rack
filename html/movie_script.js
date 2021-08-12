var titleid = '';

function populateCast(cl) {
    const castlist = document.getElementById("cast-list");
    cl.forEach(cast =>  {
        const li = document.createElement("li");
        li.appendChild(document.createTextNode(`${cast[1]}: ${cast[0]}`))
        castlist.appendChild(li);
    })
}

function populateComments(cl) {
    const comment_list = document.getElementById("comments-list");
    cl.sort((a,b) => {
        return a[2] < b[2];
    })
    cl.forEach(comment =>  {
        const li = document.createElement("li");
        const cmt = document.createElement("div");
        const user = document.createElement("label");
        const body = document.createElement("p");
        user.appendChild(document.createTextNode(comment[1]));
        body.appendChild(document.createTextNode(comment[0]));
        cmt.appendChild(user);
        cmt.appendChild(body);
        cmt.appendChild(document.createElement("hr"))
        li.appendChild(cmt);
        comment_list.appendChild(li);
    })
}

async function post_comment(element) {
    const comment = document.getElementById('comment-text').value;
    document.getElementById('comment-text').value = "";
    const token = sessionStorage.getItem("JWT_token");
    try {
        if (comment.length <= 0) {
            throw new Error("Comment cannot be empty");
        }
        const result = await post('/api/comments', {
            token,
            titleid,
            comment
        });
        const li = document.createElement("li");
        const cmt = document.createElement("div");
        const user = document.createElement("label");
        const body = document.createElement("p");
        user.appendChild(document.createTextNode(sessionStorage.getItem("username")));
        body.appendChild(document.createTextNode(comment));
        cmt.appendChild(user);
        cmt.appendChild(body);
        cmt.appendChild(document.createElement("hr"))
        li.appendChild(cmt);
        const comment_list = document.getElementById("comments-list");
        console.log(comment_list.firstChild.textContent);
        comment_list.firstChild.nextSibling.after(li);
    }   catch(e) {
        alert("Error: " + e.message);
    }
}

document.addEventListener("DOMContentLoaded", async function() {
    loggedIn = checkLogin();
    titleid = getQueryVariable('m');
    const movie_info = await get("/api/movieid", {titleid: titleid});
    const cast_info = await get("/api/cast", {titleid: titleid});
    const comments = await get("/api/comments", {titleid: titleid});
    const title_elem = document.getElementById("title");
    const year_elem = document.getElementById("year");
    const runtime_elem = document.getElementById("runtime");
    const summary_elem = document.getElementById("summary");
    title_elem.innerHTML = movie_info[0][1];
    year_elem.appendChild(document.createTextNode(movie_info[0][2]));
    runtime_elem.appendChild(document.createTextNode(`${movie_info[0][3]} min`));
    summary_elem.appendChild(document.createTextNode(movie_info[0][4]));
    populateCast(cast_info);
    populateComments(comments);
});