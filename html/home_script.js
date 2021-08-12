var loggedIn = false;

async function query_movies_fe(element) {
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
    var element = document.getElementById("movie-search");
    deleteChild(element);
    try {
        if(Object.keys(params).length <= 0)
            throw new Error('Please use at least one filter.');
        const results = await get('/api/movies', params);
        results.forEach(e => {
            var tag = document.createElement("li");
            var a = document.createElement("a");
            tag.appendChild(a);
            var text = document.createTextNode(`${e[1]} (${e[2]})`);
            a.appendChild(text);
            a.href = `/movie.html?m=${e[0]}`; 
            element.appendChild(tag);
        });
    } catch(e) {
        var tag = document.createElement("li");
        var text = document.createTextNode("Something went wrong...");
        tag.appendChild(text);
        element.appendChild(tag);
    }
}

document.addEventListener("DOMContentLoaded", function() { 
    loggedIn = checkLogin();
    if (loggedIn) {
        const a = document.createElement("a");
        a.href = "/profile.html"
        a.innerHTML = "Your Profile"
        document.getElementById("main").insertBefore(a, document.getElementById("main").children[2])
        document.getElementById("main").insertBefore(document.createElement("br"), document.getElementById("main").children[3])
    }
});
