document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";

  document.querySelector("#compose-form").onsubmit = () => {
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        // Print result
        console.log(result);
        load_mailbox("sent");
      });
    return false;
  };
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views

  document.querySelector("#email").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#emails-view").style.display = "block";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((email) => {
        const element = document.createElement("div");
        if (email.read === true) {
          element.className =
            "border rounded border-dark bg-secondary text-dark  p-2";
        } else {
          element.className = "border rounded border-dark text-dark p-2";
        }
        element.setAttribute("id", `id${email.id}`);
        element.innerHTML = `<p style="display:inline" class="font-weight-bold mr-3">${email.sender}</p><p style="display:inline" class="mr-3" >${email.subject}</p><small style="float:right;" class="font-weight-light text-end">${email.timestamp}</small>`;

        element.addEventListener("click", function () {
          console.log("This element has been clicked!");

          fetch(`/emails/${email.id}`, {
            method: "PUT",
            body: JSON.stringify({
              read: true,
            }),
          }).then(() => {
            load_email(mailbox, email.id);
          });
        });
        document.querySelector("#emails-view").append(element);
      });
    });
}

function load_email(mailbox, email_id) {
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email").style.display = "block";

  // document.querySelector("#email").innerHTML = '<h3>Email</h3>';
  document.querySelector("#email").innerHTML = "";

  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      // Print email
      console.log(email);

      const element = document.createElement("div");
      element.setAttribute("id", `emailid${email.id}`);
      element.innerHTML = `<h3>${email.subject}</h3>
      <p style="padding: 0;" class="mt-4"><strong>From: </strong>${email.sender}
      <br><strong>To: </strong>${email.recipients}
      <br><strong>Timestamp: </strong>${email.timestamp}</p>
      <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
      <hr><p>${email.body}</p>`;

      

      // Archive/Unarchive button
      const archive = document.createElement("div");
      let archived_or_not = true;

      if (mailbox === "inbox") {
        archive.innerHTML = `<button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>`;
        archived_or_not = true;
      } else if (mailbox === "archive") {
        archive.innerHTML = `<button class="btn btn-sm btn-outline-primary" id="archive">Unarchive</button>`;
        archived_or_not = false;
      } else {
        archive.innerHTML = '';
      }
      document.querySelector("#email").append(element, archive);

      // Reply button function
      document.querySelector("#reply").addEventListener("click", () => load_reply(mailbox, email.id));

      // Archive/Unarchive function
      document.querySelector("#archive").addEventListener("click", () => {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: archived_or_not
          })
        })
        .then(() => {
          load_mailbox("inbox");
        })
      });
    });
}

function load_reply(mailbox, email_id) {


}
