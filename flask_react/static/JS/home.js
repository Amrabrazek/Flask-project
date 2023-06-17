

function checkRadio() {
    var publicid = document.getElementById("publicid");
    var friends_onlyid = document.getElementById("friends_onlyid");
    var only_meid = document.getElementById("only_meid");

    var public_container = document.getElementById("public_posts_container")
    var friends_only_container = document.getElementById("friends_only_post_container")
    var only_me_container = document.getElementById("only_me_posts_container")

    if (publicid.checked) {
        console.log("public")
        only_me_container.classList.add('d-none');
        friends_only_container.classList.add('d-none');
        public_container.classList.remove('d-none');

    } else if (friends_onlyid.checked) {
        console.log("friends")
        only_me_container.classList.add('d-none');
        friends_only_container.classList.remove('d-none');
        public_container.classList.add('d-none');

    } else {
        only_me_container.classList.remove('d-none');
        friends_only_container.classList.add('d-none');
        public_container.classList.add('d-none');
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Add smooth scrolling behavior
    });

    const input = document.getElementsByClassName('input_x')[0];
    input.focus();
}

console.log("hello")



function openEditForm(postId) {
    // fetch('/edit_post/' + postId)
    //     .then(response => response.json())
    //     .then(data => {
    //     // Populate form fields with data
    //     document.getElementById('title').value = data.title;
    //     document.getElementById('content').value = data.content;
    //     // Show edit form
    //     document.getElementById('edit-form').style.display = 'block';
    // });

    console.log(postId)
}