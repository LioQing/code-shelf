import React from 'react';
import ReactPlayer from 'react-player';
import styles from './styles.module.css';

interface VideoPlayerProps {
  src: string;
  children?: React.ReactNode;
}

const VideoPlayer = ({ src, children }: VideoPlayerProps) => {
  return (
    <div className={styles.div}>
      <ReactPlayer className={styles.player} url={src} width='100%' height='auto' controls loop playing muted />
      <div className={styles.text}>{children}</div>
    </div>
  );
};

export default VideoPlayer;