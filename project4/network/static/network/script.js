document.addEventListener('DOMContentLoaded', function() {
  const url = document.querySelector("#url_path").value
  const curr_pg = Number(document.querySelector("#page_number").innerHTML.trim())
  
  const prev = document.querySelector("#previous")
  prev.onclick = function() {
    prev.href = url.concat("", curr_pg - 1)
  };
  const next = document.querySelector("#next")
  next.onclick = function() {
    next.href = url.concat("", curr_pg + 1)
  };
})

function edit_post(id) {
  // console.time("edit_post")
  const text = document.querySelector("#post_text_" + id);
  const div = document.createElement('div')
  const textarea = document.createElement('textarea');
  const button = document.createElement('button')

  textarea.id  = 'post_text_edit_' + id;
  textarea.maxLength = 280;
  textarea.innerHTML = text.innerHTML;

  csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
  console.log(csrftoken)
  button.className = 'btn btn-primary'
  button.innerHTML = 'Save'
  button.onclick = function() {
    if (textarea.value != "") {
      fetch('/edit/' + id, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
          text: textarea.value.trim()
      }),
      credentials: 'same-origin',
      })
      .then(response => {
        response.json()
        text.innerHTML = textarea.value;
        div.parentNode.replaceChild(text, div);
        
      });}
      else {
        alert("New Post Cannot Be Empty")
      }}  
    
    
  div.append(textarea)
  div.append(document.createElement('br'))
  div.append(button)

  text.parentNode.replaceChild(div, text);
  // console.timeEnd("edit_post")
  return false;
}

function like_post(id) {
  
  const like_div = document.querySelector("#post_like_" + id)
  csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
  // console.time("like_post")
  fetch('/like/' + id, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
        liked: true,
    })
  })
  .then(response => response.json())
  .then(likes => {
    if (typeof(likes) == 'number') {
      const like_count = document.querySelector("#post_like_count_" + id)
      like_div.style.color = 'rgb(0, 123, 255)'
      like_count.innerHTML = " "+ likes
    }
  })
  // console.timeEnd("like_post")
}