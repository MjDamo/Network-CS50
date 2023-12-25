function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) return parts.pop().split(';').shift();
}

function submitChange(id) {
    const newContent = document.getElementById(`textarea_${id}`).value
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

}


