import React, {useState, useEffect} from 'react'
import { useParams, useNavigate } from 'react-router-dom';
// import notes from '../assets/data'
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'

const NotePage = () => {

  let note_id = useParams();
  let noteID = note_id.id;
 
  let [note, setNote] = useState([])


  useEffect(() => {
    getNote()
  }, [noteID])


  let getNote = async () => {
    if (noteID === 'new') return

    let response = await fetch(`http://localhost:8000/notes/${noteID}`)
    let data = await response.json()
    setNote(data)
  }  

  let updateNote = async () => {
    await fetch(`http://localhost:8000/notes/${noteID}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({...note, 'updated': new Date()})
    })
  }

  let createNote = async () => {
    await fetch(`http://localhost:8000/notes/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({...note, 'updated': new Date()})
    })
  }

  const navigate = useNavigate();

  let deleteNote = async () => {
    await fetch(`http://localhost:8000/notes/${noteID}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    navigate(-1)
  }

  let handleSubmit = () => {

    if (noteID !== 'new' && !note.body) {
      deleteNote()
    } else if (noteID !== 'new') {
      updateNote()
      navigate(-1)
    } else if (noteID === 'new' && note.body) {
      createNote()
      navigate(-1)
    } else {
      navigate(-1)
    }

    
  }

  return (
    
    <div className='note'>
      <div className='note-header'>

        <h3>
            <ArrowLeft onClick={handleSubmit}/>
        </h3>


        {noteID !== 'new' ? (
          <button onClick={deleteNote}>Delete</button>
        ) : (
          <button onClick={handleSubmit}>Done</button>
        )}


      </div>
      <textarea onChange={(e)=> {setNote({...note, 'body':e.target.value})}} value={note.body}>

      </textarea>
    </div>
  )
}

export default NotePage