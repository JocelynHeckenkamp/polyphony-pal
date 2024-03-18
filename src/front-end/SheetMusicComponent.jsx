import React, { useRef, useEffect } from 'react';
import { OpenSheetMusicDisplay } from 'opensheetmusicdisplay';
//recieve the MusicXML data as prop named musicXml ( make sure to check that its coming from results.js)
const SheetMusicComponent = ({ musicXml }) => {
  const sheetMusicContainer = useRef(null);

  useEffect(() => {
    if (sheetMusicContainer.current && musicXml) {
      console.log('SheetMusicComponent: TODO MAKE A LOAD THINGY Preparing to render sheet music...');
      const renderOptions = {
        autoResize: true,
        backend: "svg",
        drawingParameters: "compact",
      };
      // Initialize OpenSheetMusicDisplay with the container and render options
      const osmd = new OpenSheetMusicDisplay(sheetMusicContainer.current, renderOptions);
      osmd.load(musicXml).then(() => {
        console.log('TODO Add spinning loading bar  ...SheetMusicComponent: Sheet music rendered successfully.');
        osmd.render(); // Render the MusicXML data as sheet music in the container.
      })
      .catch(error => console.error("Error rendering sheet music:", error));
    } else {
      console.log('TODO Add loading bar ...SheetMusicComponent: Waiting for MusicXML data or the container to be ready...');
    }
  }, [musicXml]); //  runs when `musicXml` changes.


  return <div ref={sheetMusicContainer} />;
};

export default SheetMusicComponent;