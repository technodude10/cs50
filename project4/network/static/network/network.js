
// get csrftoken

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const profile_id = JSON.parse(document.getElementById('profile_id').textContent);

let isfollowing = JSON.parse(document.getElementById('is_following').textContent);
;

function like_click(clicked_id) {

  fetch(`/like/${clicked_id}`, {
        method: 'PUT',
        headers:{'X-CSRFToken':csrftoken},
        body: JSON.stringify({
            like: `like`,
        })
    })
    .then((response) => response.json())
    .then((result) => {
      // Print result
      console.log(result.like);

      fetch(`/like/${clicked_id}`)
      .then((response) => response.json())
      .then((likecount) => {
        // like color change
        if (result.like === true) {
          var likeclr = document.getElementById(`l${clicked_id}`).nextSibling;
          likeclr.style.color = "red";
        } else {
          var likeclr = document.getElementById(`l${clicked_id}`).nextSibling;
          likeclr.style.color = "";
        }
        // like count change
        if (likecount.likecount > 0) {
          var div = document.getElementById(`l${clicked_id}`);
          div.innerHTML = likecount.likecount;
        } else {
          var div = document.getElementById(`l${clicked_id}`);
          div.innerHTML = "";
        }
        
    });
  })
}

// edit content function
function reply_click(clicked_id)
  {
    // 
    fetch(`/editpost/${clicked_id}`)
    .then((response) => response.json())
    .then((editpost) => {
      document.querySelector("#editcontent").value = editpost.content;

      document.querySelector("#compose-form").onsubmit = () => {
        const content = document.querySelector("#editcontent").value;
        document.querySelector("#editcontent").value = "";

        
        // submit edited details via post
        fetch(`/editpost/${editpost.id}`, {
          method: "POST",
          headers:{'X-CSRFToken':csrftoken},
          body: JSON.stringify({
            id: editpost.id,
            content: content,
          }),
        })
          .then((response) => response.json())
          .then((result) => {
            // Print result
            console.log(result);
            if (result.message === "error") {
              var msg = document.getElementById(`poor_mans_msg`);
              msg.innerHTML = `<div class="alert alert-danger text-center" role="alert">Edited post cannot be blank</div>`;
            } else {
              var msg = document.getElementById(`poor_mans_msg`);
              msg.innerHTML = "";
              var div = document.getElementById(`c${editpost.id}`);
              div.innerHTML = content;
            }
            

          });

        var myModalEl = document.getElementById('editModal');
        var modal = bootstrap.Modal.getInstance(myModalEl)
        modal.hide();

        return false;
        
        };
    })
  }

  // follow profile function 

  function App() {

const [count, setCount] = React.useState(0);

function putdetails(arg) {
    fetch(`/follow/${profile_id}`, {
        method: 'PUT',
        headers:{'X-CSRFToken':csrftoken},
        body: JSON.stringify({
            follow: arg,
        })
    })
    .then((response) => response.json())
    .then((result) => {
      // Print result
      console.log(result);
      fetch(`/updatefollow/${profile_id}`)
        .then((response) => response.json())
        .then((followercount) => {

        var div = document.getElementById(`followercount`);
        div.innerHTML = followercount.followercount;
    });
  });

    
}


function onCount() {
  setCount(2);
  putdetails(true)
}

function offCount() {
  setCount(1);
  putdetails(false)
}

let button = "";

if (isfollowing) {
  button = (<button id="followbtn" onClick={offCount} type="button" class="btn btn-outline-primary btn-sm">Unfollow</button>);
} else {
  button = (<button id="followbtn" onClick={onCount} type="button" class="btn btn-primary btn-sm">Follow</button>);
}

if (count === 2) {
  button = (<button id="followbtn" onClick={offCount} type="button" class="btn btn-outline-primary btn-sm">Unfollow</button>);
} else if (count === 1) {
  button = (<button id="followbtn" onClick={onCount} type="button" class="btn btn-primary btn-sm">Follow</button>);
}


return (
  <div>
      {button}
  </div>
);
}

ReactDOM.render(<App />, document.querySelector("#follow_button"));