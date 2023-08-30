import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import LogoUrl from '@site/static/img/logo.png';
import Feature1Svg from '@site/static/img/feature1.svg';
import Feature2Svg from '@site/static/img/feature2.svg';
import Feature3Svg from '@site/static/img/feature3.svg';

import styles from './index.module.css';

const HomepageHeader = () => {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.hero}>
      <div className={styles.heroContent}>
        <img src={LogoUrl} alt='logo' />
        <p>{siteConfig.tagline}</p>
      </div>
      <Link
        className="button button--outline button--secondary button--lg"
        href="/docs/Welcome%20to%20Code%20Shelf">
        Explore Topics
      </Link>
    </header>
  );
}

const HomepageIntro = () => {
  return (
    <section className={styles.intro}>
      <div className={styles.introContent}>
        <h2>About Us</h2>
        <p>
          This website is inspired from university lectures. It intends
          to guide you through programming and computer science concepts
          and theories instead of going straight into implementations like
          typical online tutorials. By incorporating interactive elements
          and visualizations, we hope to make learning abstract concepts
          more fun and engaging.
        </p>
      </div>
    </section>
  );
}

interface Feature {
  title: string;
  icon: React.ReactElement;
  description: string;
}

const features: Feature[] = [
  {
    title: 'Smooth and Simple',
    icon: <Feature1Svg />,
    description: '\
    We carefully designed the learning to be easy to navigate and read by \
    categorizing contents into different topics and chapters. The learning \
    experience is designed to flow linearly and the contents are built on \
    top of previous chapters. \
    ',
  },
  {
    title: 'Interactive and Intuitive',
    icon: <Feature2Svg />,
    description: '\
    We believe that learning should be fun and engaging. We incorporate \
    interactive elements and visual aids to make learning more fun and make \
    difficult concepts more easy to understand. \
    ',
  },
  {
    title: 'Understand then Implement',
    icon: <Feature3Svg />,
    description: '\
    We desigened the chapters in a way that you will learn the abstract \
    concepts before implementing them. This way, you can not only understand \
    the reasoning behind the implementaion, but also use it in different \
    scenarios. \
    ',
  }
]

const HomepageFeatures = () => {
  return (
    <section className={styles.features}>
      {features.map((feature, idx) => (
        <div key={idx} className={styles.feature}>
          {feature.icon}
          <h3>{feature.title}</h3>
          <p>{feature.description}</p>
        </div>
      ))}
    </section>
  );
}

const Home = (): JSX.Element => {
  const {siteConfig} = useDocusaurusContext();
  return ( 
    <Layout
      title="Homepage"
      description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        <HomepageIntro />
        <HomepageFeatures />
      </main>
    </Layout>
  );
}

export default Home;
