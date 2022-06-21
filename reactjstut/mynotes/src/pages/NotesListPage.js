import React from 'react'
import notes from '../assets/data'
import Listitem from '../components/Listitem'

const NotesListPage = () => {
  return (
    <div>
        <div className='notes-list'>
            {notes.map((note, index) => (
                <Listitem key={index} note={note} />
            ))}
        </div>
    </div>
  )
}

export default NotesListPage