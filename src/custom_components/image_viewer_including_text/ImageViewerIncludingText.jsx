import React from 'react'
import './imageViewerIncludingTextStyle.css'
function ImageViewerIncludingText({image,text}) {
  return (
    <div className='image_viewer_including_text_main_container'>
        <div>
           <img src={image} className='image_viewer'/>
        </div>
       <div className='image_viewer_text_container'>
         <p className='image_viewer_text'>{text}</p>
       </div>
    </div>
  )
}

export default ImageViewerIncludingText