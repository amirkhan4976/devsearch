// Get search form and page links
let searchForm = document.getElementById("searchForm")
let pageLinks = document.getElementsByClassName("page-link")
// Ensure search form exists
if(searchForm) {
    for(let i=0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault()
            // Get the data attribute
            let page = this.dataset.page
            searchForm.innerHTML += `<input value=${page} name="page" hidden>`

            searchForm.submit()
        })
    }
}

let tags = document.getElementsByClassName('project-tag');
for (let i=0; tags.length>i; i++) {
    tags[i].addEventListener('click', (e) => {
        let tag_id = e.target.dataset.tag
        let project_id = e.target.dataset.project

        fetch('http://127.0.0.1:8000/api/remove-tag/', {
            method:'DELETE',
            headers:{
                'Content-type':'application/json'
            },
            body:JSON.stringify({
                'tag': tag_id,
                'project': project_id
            })
        })
        .then(response => response.json())
        .then(data => {
            e.target.remove();
        })
    })
}