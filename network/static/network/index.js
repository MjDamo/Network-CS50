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


