import "./HeroSection.css";
import React, { useEffect } from "react";

export default function HeroSection() {
  useEffect(() => {
    if (document.querySelector('script[src="/js/lottie-player.js"]')) return;

    const script = document.createElement("script");
    script.src = "/js/lottie-player.js";
    script.async = true;
    script.onerror = () =>
      console.error("Failed to load local Lottie player script");

    document.body.appendChild(script);
    return () => {
      if (document.body.contains(script)) document.body.removeChild(script);
    };
  }, []);

  return (
    <section className="hero-image-section">
      <div className="hero-image">
        {/* React.createElement is used to suppress TypeScript errors as VS code throws an error for lottie-player othe  */}
        {React.createElement("lottie-player", {
          src: "https://lottie.host/c3d8ee59-5c73-46f7-8c4e-a66763f5eba3/80bnwExY98.json",
          background: "transparent",
          speed: "1",
          loop: true,
          autoplay: true,
          style: { width: "100%", height: "auto" },
        })}
      </div>
    </section>
  );
}
