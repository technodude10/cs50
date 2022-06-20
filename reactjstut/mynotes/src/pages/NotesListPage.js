import React from 'react'
import notes from '../assets/data'

const NotesListPage = () => {
  return (
    <div>
        <div className='notes-list'>
            {notes.map(note => (
                <p>{note.body}</p>
            ))}
        </div>
    </div>
  )
}

export default NotesListPage