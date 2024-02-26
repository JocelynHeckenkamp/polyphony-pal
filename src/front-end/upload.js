
import React, {useState} from 'react';


function Upload() {
const [file, setFile] = useState(null);
 
function handleUpload()
{
    if( !file)
    {
        console.log("No file selected");
        return;
    }
    const fd = new FormData();
    fd.append('file',file);

    //upload file to backend
    //change fd to file if theres an error
   fetch("/upload", 
    {
        method: "PUT",
        body: fd,
    });

 
}

  return (
    <div className="Upload">
        <h1>Upload Test</h1>

        <input onChange={(e) => {setFile(e.target.files[0])}} type="file"></input>

        <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default Upload;