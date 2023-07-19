import React from 'react';
import ReactPlayer from 'react-player';
import styles from './styles.module.css';

interface VideoPlayerProps {
  src: string;
  text?: string;
}

const VideoPlayer = ({ src, text }: VideoPlayerProps) => {
  return (
    <div className={styles.div}>
        <ReactPlayer className={styles.player} url={src} width='100%' height='auto' controls loop playing muted/>
        <p className={styles.text}>{text}</p>
    </div>
  );
};

export default VideoPlayer;