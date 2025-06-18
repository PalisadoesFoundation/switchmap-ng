import Image from "next/image";
import styles from "./page.module.css";
import Link from "next/link";

export default function Home() {
  return (
    <main>
      <h1>Hello</h1>
      <Link href="/device">Got to Device Details</Link>
    </main>
  );
}
