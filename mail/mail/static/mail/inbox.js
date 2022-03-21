document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  console.log(mailbox)
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  localStorage.clear()

  fetch('/emails/'+ mailbox)
    .then(response => response.json())
    .then(emails => {return read_email_data(emails, mailbox)})
}

function send_email() {

  // Post email to API route
  fetch('/emails' , {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value,
      read: false,
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    localStorage.clear();
    load_mailbox('sent');
  });  
  return false;
}

function read_email_data(emails, mailbox) {
  for(let i = 0; i < emails.length; i++) {
    const div = document.createElement('div');
    if (emails[i].read == true && mailbox != 'sent') {
      div.style.background = 'gray'
    }
    div.id = "email_" + [i];
    div.style.border = '1px solid black';
    div.style.paddingBottom = '10px';
    div.style.boxShadow = '0px 0px 1px 0.5px';
    div.onclick = function () {load_email(emails[i], mailbox)}

    const span1 = document.createElement('span');
    const span2 = document.createElement('span');
    const span3 = document.createElement('span');
    if (mailbox == sent) {
      span1.innerHTML = emails[i]['recipients']
    } else {
      span1.innerHTML = emails[i]['sender']
    }
    span1.style.fontWeight = 'bold';

    span2.innerHTML = emails[i]['subject']
    span2.style.paddingLeft = '10px';
    
    span3.innerHTML = emails[i]['timestamp']
    span3.style.display = 'inline-block';
    span3.style.float = 'right';

    div.append(span1);
    div.append(span2);
    div.append(span3);
  
    document.querySelector("#emails-view").append(div);
  }
  return document.querySelector("#emails-view")
}

function load_email(email, mailbox) {
  console.log("test" + email.id)
  fetch('/emails/' + email.id, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
  document.querySelector("#emails-view").innerHTML = '';
  
  const span1 = document.createElement('div');
  const span2 = document.createElement('div');
  const span3 = document.createElement('div');
  const span4 = document.createElement('div');
  const button = document.createElement('button');
  const button1 = document.createElement('button');
  const body = document.createElement('p');

  span1.innerHTML = '<b>' + "From: " + '</b>'+ email.sender;
  document.querySelector("#emails-view").append(span1);
  span2.innerHTML = '<b>' + "To: " + '</b>'+ email.recipients;
  document.querySelector("#emails-view").append(span2);
  span3.innerHTML = '<b>' + "Subject: " + '</b>'+ email.subject;
  document.querySelector("#emails-view").append(span3);
  span4.innerHTML = '<b>' + "Timestamp: " + '</b>'+ email.timestamp;
  document.querySelector("#emails-view").append(span4);

  button.innerHTML = "Reply"
  button.className = "btn btn-sm btn-outline-primary"
  button.onclick = function () {reply(email)}
  
  if (email.archived == false) {
    button1.innerHTML = "Archive"
    button1.onclick = function () {
      fetch('/emails/' + email.id, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
      fetch('/emails/archive')
      .then(response => response.json())
      .then(emails => {return load_mailbox('archive');
    })}
  } else {
    button1.innerHTML = "Unarchive"
    button1.onclick = function () {
      fetch('/emails/' + email.id, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
      fetch('/emails/inbox')
      .then(response => response.json())
      .then(emails => {return load_mailbox('inbox');
    })}
  }
  button1.className = "btn btn-sm btn-outline-primary"
  console.log("mailbox:" + mailbox)
  if (mailbox != 'sent') {
  document.querySelector("#emails-view").append(button);
  document.querySelector("#emails-view").append(button1);
  }
  document.querySelector("#emails-view").append(document.createElement('hr'))
  
  body.innerHTML = email.body
  document.querySelector("#emails-view").append(body);
}
function reply(email) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = ''+ email.sender;
  document.querySelector('#compose-subject').value = 'Re:'+ email.subject;
  document.querySelector('#compose-body').value = email.timestamp + ' ' + email.sender + ' wrote: ' + email.body;
}