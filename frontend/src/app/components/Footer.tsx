export function Footer() {
  return (
    <footer className="bg-bg py-4 text-center">
      <div className="m-2 flex flex-col sm:flex-row gap-4 justify-center">
        <p>© {new Date().getFullYear()} SwitchMap-NG. All rights reserved.</p>
        <a href="https://docs.switchmap-ng.io/docs" className="underline">
          Docs
        </a>
        <a
          href="https://github.com/PalisadoesFoundation/switchmap-ng"
          target="_blank"
          rel="noopener noreferrer"
          className="underline"
        >
          GitHub
        </a>
      </div>
    </footer>
  );
}

export default Footer;
