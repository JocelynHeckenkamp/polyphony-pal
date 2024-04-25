import React, { useRef, useState } from 'react';
import MidiPlayer from 'midi-player-js';

const MidiPlayerComponent = ({ midiBlob }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const player = useRef(new MidiPlayer.Player());

  const loadAndPlayMidi = () => {
    const { current: midiPlayer } = player;
    midiPlayer.loadDataUri(midiBlob)
      .then(() => {
        midiPlayer.play();
        setIsPlaying(true);
      })
      .catch(error => {
        console.error('Error loading or playing MIDI file:', error);
      });
  };

  const stopMidi = () => {
    const { current: midiPlayer } = player;
    midiPlayer.stop();
    setIsPlaying(false);
  };

  const togglePlay = () => {
    if (isPlaying) {
      stopMidi();
    } else {
      loadAndPlayMidi();
    }
  };

  return (
    <div>
      <button onClick={togglePlay}>
        {isPlaying ? 'Stop' : 'Play'} MIDI
      </button>
    </div>
  );
};

export default MidiPlayerComponent;