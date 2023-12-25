function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) return parts.pop().split(';').shift();
}

function submitChange(id) {
    const newContent = document.getElementById(`textarea_${id}`).value;
    const content = document.getElementById(`content_${id}`);
    const modal = document.getElementById(`staticBackdrop_${id}`);
    fetch(`/edit/${id}`,{
        method: 'POST',
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            content: newContent
        })
    })
        .then(response => response.json())
        .then(result => {
            content.innerHTML = result.data;
            modal.classList.remove('show');
            modal.setAttribute('aria-hidden', 'true');
            modal.setAttribute('style', 'display: none');

            const back = document.querySelectorAll('.modal-backdrop');
            for (let i = 0; i < back.length; i++){
                document.body.removeChild(back[i]);
            }
        })
}


function likeUnlike(post_id, user_likes) {
    const likeUnlikeBtn = document.getElementById(`${post_id}`);
    likeUnlikeBtn.classList.remove('bi-heart-fill')
    likeUnlikeBtn.classList.remove('bi-heart')
    let likeFlag = false;
    if (user_likes.indexOf(post_id) >= 0) {
        likeFlag = true
    }
    if (likeFlag){
        fetch(`/unlike_post/${post_id}`)
            .then(response => response.json)
            .then(result => {
                likeUnlikeBtn.add('bi-heart')
            })
    } else {
        fetch(`/like_post/${post_id}`)
            .then(response => response.json)
            .then(result => {
                likeUnlikeBtn.add('bi-heart-fill')
            })
    }
    likeFlag = !likeFlag
}

