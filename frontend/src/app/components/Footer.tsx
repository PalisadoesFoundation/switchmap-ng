export function Footer() {
  return (
    <footer className="bg-bg py-4 text-center ml-8">
      <div className="m-4 flex flex-col sm:flex-row gap-4 justify-end text-left">
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
