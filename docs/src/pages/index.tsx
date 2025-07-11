import clsx from "clsx";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import HeroSection from "@site/src/components/HeroImage/HeroSection";

import styles from "./index.module.css";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className="buttons_AeoN">
          <a
            className={`${styles.button} button button--primary button--lg`}
            href="/docs/installation"
            aria-label="Installation"
          >
            Installation
          </a>
          <a
            className={`${styles.button} button button--secondary button--lg`}
            href="/docs/community"
            aria-label="Join the community"
          >
            Community
          </a>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="Description will go into a meta tag in <head />"
    >
      <div className={styles["home-wrapper"]}>
        <HomepageHeader />
        <main>
          <HeroSection />
        </main>
      </div>
    </Layout>
  );
}
